# pdf_utils.py
import pdfplumber

def extract_text_from_pdf(path: str) -> str:
    """读取 PDF 全文并返回纯文本（去掉多余空行）"""
    text_parts = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            txt = page.extract_text() or ""
            text_parts.append(txt.strip())
    return "\n".join(text_parts).strip()
