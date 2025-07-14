# services.py  (单文件即可运行)
# -*- coding: utf-8 -*-

import logging, os, re, time, uuid
from datetime import datetime
from typing import List, Dict, Optional

import torch
from transformers import pipeline, AutoTokenizer, Pipeline
from models import quiz_collection        # 若无 Mongo，请用假集合降级

# ───────────────────────────────────
# 日志
# ───────────────────────────────────
logging.basicConfig(
    level=os.getenv("QUIZ_LOG_LEVEL", "INFO").upper(),
    format="%(levelname)s | %(message)s",
)
log = logging.getLogger(__name__)

# ───────────────────────────────────
# spaCy 分句（无 spaCy 则用正则）
# ───────────────────────────────────
try:
    import spacy
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        nlp = spacy.load("zh_core_web_sm")
    log.info("spaCy model loaded")
except ImportError:
    nlp = None
    log.warning("spaCy not installed，回退正则分句")

def extract_key_sentences(text: str, n: int = 2) -> List[str]:
    """抽取前 n 句长度 20-300 字的句子"""
    if nlp:
        doc = nlp(text)
        sents = [s.text.strip() for s in doc.sents
                 if 20 <= len(s.text.strip()) <= 300]
    else:
        sents = re.findall(r".{20,300}(?:[。！？.!?]|$)", text)
    log.debug("Key sentences: %s", sents[:n])
    return sents[:n]

# ───────────────────────────────────
# DeepSeek pipeline（懒加载）
# ───────────────────────────────────
_MODEL_ID = os.getenv("DEEPSEEK_MODEL",
                      "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B")
_TOKENIZER = AutoTokenizer.from_pretrained(_MODEL_ID)
_MAX_CTX = 900          # 预留给 prompt 的最大 token

_PIPE: Optional[Pipeline] = None
def _get_pipe() -> Pipeline:
    global _PIPE
    if _PIPE: return _PIPE

    if torch.cuda.is_available():
        kwargs = dict(device=0, torch_dtype=torch.float16)
        log.info("DeepSeek → GPU:0")
    else:
        kwargs = dict(device=-1)
        log.info("DeepSeek → CPU")

    _PIPE = pipeline(
        "text-generation",
        model=_MODEL_ID,
        trust_remote_code=True,
        max_new_tokens=256,       # 仅限制新增 token
        do_sample=False,
        **kwargs,
    )
    log.info("Pipeline ready: %s", _MODEL_ID)
    return _PIPE

def _safe_prompt(text: str) -> str:
    """截断过长 prompt，保证总 token 不超过模型上限"""
    ids = _TOKENIZER(text).input_ids
    if len(ids) > _MAX_CTX:
        text = _TOKENIZER.decode(ids[-_MAX_CTX:], skip_special_tokens=True)
    return text

# ───────────────────────────────────
# 解析 LLM 输出
# ───────────────────────────────────
_Q_RE   = re.compile(r"问题[:：]\s*(.+)")
_OPT_RE = re.compile(r"[A-D]\.\s*(.+)")
_ANS_RE = re.compile(r"正确答案[:：]\s*([A-D])")

def _parse_out(raw: str) -> Dict:
    if "</think>" in raw:
        raw = raw.split("</think>")[-1]

    q   = _Q_RE.search(raw)
    ops = _OPT_RE.findall(raw)          # 只捕获选项内容
    an  = _ANS_RE.search(raw)

    if not (q and an and len(ops) == 4):
        raise ValueError("无法解析输出:\n" + raw)

    # 重新拼接前缀 A./B./C./D.
    labeled_ops = [f"{chr(65+i)}. {txt.strip()}" for i, txt in enumerate(ops)]

    return {
        "question": q.group(1).strip(),
        "options": labeled_ops,          # ← 现在带 A./B./C./D.
        "answer" : an.group(1).strip(),
        "created_at": datetime.now().isoformat()
    }

# ───────────────────────────────────
# 生成 Quiz 主函数
# ───────────────────────────────────
def generate_quiz_with_deepseek(text: str,
                                num_questions: int = 2,
                                retry: int = 2) -> List[Dict]:
    pipe = _get_pipe()
    quizzes: List[Dict] = []

    for sent in extract_key_sentences(text, num_questions):
        prompt = f"""
你是一位专业出题专家。请根据下列内容，生成一道**单项选择题**，用来考察该内容中的**关键知识点**。

要求：
1. 只考察最核心知识点，切勿枝节。
2. 选项以 "A." "B." "C." "D." 开头，且仅一个正确。
3. 输出严格使用以下格式，无空行：

问题: ...
选项:
A. ...
B. ...
C. ...
D. ...
正确答案: A/B/C/D

内容：
{sent}
"""
        for k in range(retry + 1):
            try:
                raw = pipe(_safe_prompt(prompt))[0]["generated_text"]
                quiz = _parse_out(raw)
                break
            except Exception as e:
                log.warning("解析失败(%d/%d): %s", k+1, retry, e)
                if k == retry: raise
                time.sleep(1)

        # 存库（若仅离线测试可去掉）
        res = quiz_collection.insert_one(quiz)
        quizzes.append({"quiz_id": str(res.inserted_id), "quiz": quiz})
    return quizzes

# ───────────────────────────────────
# CLI 自测
# ───────────────────────────────────
if __name__ == "__main__":
    from pathlib import Path
    sample = Path("sample.txt").read_text(encoding="utf-8")
    for q in generate_quiz_with_deepseek(sample, 3):
        print(q)
