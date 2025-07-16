# send_pdf.py
# -*- coding: utf-8 -*-
"""
将本地 4-16.pdf 上传到 /upload-pdf 并打印返回 JSON
"""

import httpx, json, pathlib

PDF_FILE = "4-16.pdf"
URL      = "http://127.0.0.1:8000/upload-pdf"   # 端口和路径与后端保持一致

def main():
    pdf_path = pathlib.Path(PDF_FILE)
    if not pdf_path.exists():
        print(f"❌ 找不到文件: {PDF_FILE}")
        return

    with httpx.Client(timeout=60.0) as client:
        files = {
            "file": (
                pdf_path.name,
                pdf_path.open("rb"),
                "application/pdf"
            )
        }
        resp = client.post(URL, files=files)
        try:
            data = resp.json()
        except ValueError:
            print("❌ 服务器未返回 JSON：", resp.text)
            return

        print(json.dumps(data, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
