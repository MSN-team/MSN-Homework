# pdf_utils.py
# -*- coding: utf-8 -*-
"""
PDF → 纯文本小工具
pip install pdfplumber
"""

import pdfplumber

def extract_text_from_pdf(path: str) -> str:
    """读取整份 PDF，返回去掉多余空行的纯文本"""
    parts = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            txt = page.extract_text() or ""
            parts.append(txt.strip())
    return "\n".join(parts).strip()

def split_document(text: str, chunk: int = 3000) -> list[str]:
    """把超长文本按字符数切块，方便分段调用 LLM"""
    return [text[i:i + chunk] for i in range(0, len(text), chunk)]
