# services.py
# -*- coding: utf-8 -*-
"""
生成 Quiz 的核心逻辑（DeepSeek + spaCy）
"""
from __future__ import annotations

import logging
import re
from datetime import datetime
from typing import Any, Dict, List, Optional

import spacy
from transformers import pipeline

# ───── 日志 ───────────────────────────────────────────────
_LOGGER = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)

# ───── 依赖加载 ───────────────────────────────────────────
_LOGGER.info("🔄  Loading spaCy model …")
_NLP = spacy.load("en_core_web_sm")

_LOGGER.info("🔄  Loading DeepSeek pipeline (cpu) …")
_PIPE = pipeline(
    task="text-generation",
    model="deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
    device=-1,                # CPU
    trust_remote_code=True,
)
_LOGGER.info("✅  DeepSeek pipeline loaded")

# ───── 正则工具 ──────────────────────────────────────────
_RE_Q   = re.compile(r"[问題]\s*[:：]\s*(.+)", re.I)
_RE_OPT = re.compile(r"^\s*([ABCD])[\.\:、\)]\s*(.+)", re.M)
_RE_ANS = re.compile(r"正确答案?\s*[:：]\s*([ABCD])", re.I)


def _parse_reply(txt: str) -> Optional[Dict[str, Any]]:
    """从 LLM 输出中抽取 {question, options[4], answer}"""
    # 去掉 DeepSeek 的 <think>
    if "</think>" in txt:
        txt = txt.split("</think>", 1)[-1]

    # ——— ① 严格正则 ———
    q    = _RE_Q.search(txt)
    opts = _RE_OPT.findall(txt)
    ans  = _RE_ANS.search(txt)
    if q and len(opts) >= 4 and ans:
        opt_dict = {k: v.strip() for k, v in opts[:4]}
        return {
            "question": q.group(1).strip(),
            "options":  [opt_dict[k] for k in "ABCD"],
            "answer":   ans.group(1).strip(),
        }

    # ——— ② fallback 粗匹配 ———
    lines      = [l.strip() for l in txt.splitlines() if l.strip()]
    cand_q     = next((l for l in lines if "?" in l or "？" in l), "")
    cand_opts  = [l for l in lines if re.match(r"^[ABCD]", l)]
    cand_ans   = next((l for l in lines if "正确" in l), "")
    if cand_q and len(cand_opts) >= 4 and cand_ans:
        return {
            "question": re.sub(r"^[^\w]*", "", cand_q),
            "options":  [re.sub(r"^[ABCD][^\w]+", "", o) for o in cand_opts[:4]],
            "answer":   re.search(r"[ABCD]", cand_ans).group(0),
        }
    return None


# ───── 外部 API ──────────────────────────────────────────
def extract_key_sentences(text: str, *, limit: int = 1) -> List[str]:
    """用 spaCy 抽取前 limit 句作为“重点句子”"""
    doc = _NLP(text)
    sent_list = [s.text.strip() for s in doc.sents if s.text.strip()]
    return sent_list[:limit]


def generate_quiz_with_deepseek(
        text: str,
        *,
        num_questions: int = 1,
        max_new_tokens: int = 256,
        collection=None,                      # 传 Mongo collection 则落库；None=不落库
        **gen_kwargs,                         # 透传给 pipeline，例如 temperature=0.7
) -> List[Dict[str, Any]]:
    """
    从文本里生成 ≤ num_questions 道选择题
    返回形如 [{"quiz_id": "...", "quiz": {...}}, …]
    """
    sentences = extract_key_sentences(text, limit=num_questions)
    quizzes: List[Dict[str, Any]] = []

    for sentence in sentences:
        # —— 保险截断，防 prompt 过长 ——
        if len(sentence) > 512:
            sentence = sentence[:509] + "…"

        prompt = f"""你是一位专业出题专家。请根据下列内容，生成一道**单项选择题**，用来考察该内容中的**关键知识点**。

要求：
1. 只考察最核心知识点。
2. 问题要能判定学生是否理解核心内容。
3. **有且仅有一个正确答案**，其他三个选项要迷惑但错误。
4. 严格使用下列格式：

内容：
{sentence}

输出格式（严格遵循）：
问题: …
选项:
A. …
B. …
C. …
D. …
正确答案: A/B/C/D
"""

        # ——— 调用 LLM（带 max_new_tokens & 额外参数） ———
        reply_raw = _PIPE(
            prompt,
            do_sample=False,
            max_new_tokens=max_new_tokens,
            **gen_kwargs,
        )[0]["generated_text"]

        parsed = _parse_reply(reply_raw)

        # 如解析失败 → 尝试一次温和采样重试
        if not parsed:
            _LOGGER.warning("⚠️  解析失败，重试一次 …")
            reply_raw = _PIPE(
                prompt,
                do_sample=True,
                temperature=0.7,
                max_new_tokens=max_new_tokens,
                **gen_kwargs,
            )[0]["generated_text"]
            parsed = _parse_reply(reply_raw)

        if not parsed:
            _LOGGER.warning("⚠️  仍解析失败，跳过本句。")
            continue

        # ——— 入库（可选） ———
        doc = {**parsed, "created_at": datetime.utcnow()}
        if collection is not None:
            _id = collection.insert_one(doc).inserted_id  # type: ignore[attr-defined]
            quiz_id = str(_id)
        else:
            quiz_id = "local-" + datetime.utcnow().isoformat(timespec="seconds")

        quizzes.append({"quiz_id": quiz_id, "quiz": parsed})

    return quizzes
