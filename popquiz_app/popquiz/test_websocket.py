# -*- coding: utf-8 -*-
"""
向 /upload-pdf 端点发送本地 PDF 文件并打印返回结果
pip install websockets httpx
"""

import asyncio, json
from pathlib import Path
import httpx

# 设置 WebSocket 服务器地址，改为上传 PDF 路径
UPLOAD_URL = "http://127.0.0.1:8000/upload-pdf"  # 与后端保持一致
PDF_FILE = "4-16.pdf"  # PDF 文件路径

async def main():
    # 读取 PDF 文件内容
    pdf_file = Path(PDF_FILE)

    async with httpx.Client() as client:
        # 打开 PDF 文件并准备文件上传
        with open(pdf_file, "rb") as f:
            files = {"file": (pdf_file.name, f, "application/pdf")}

            # 发送请求到后端的上传 PDF 接口
            response = await client.post(UPLOAD_URL, files=files)

            # 打印响应
            print(f"Response Status: {response.status_code}")
            print(f"Response Body: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")

if __name__ == "__main__":
    asyncio.run(main())
