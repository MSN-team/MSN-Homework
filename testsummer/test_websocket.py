# -*- coding: utf-8 -*-
"""
向 /upload-text 端点发送本地文本文件并打印返回结果
pip install httpx
"""

import asyncio, json
from pathlib import Path
import httpx

# 设置 API 地址，处理上传文本文件
UPLOAD_URL = "http://127.0.0.1:8000/submit-text"  # 与后端保持一致
TEXT_FILE = "test.txt"  # 文本文件路径

async def main():
    # 读取文本文件内容
    text_file = Path(TEXT_FILE)

    # 使用 httpx 的 AsyncClient 来处理异步请求
    async with httpx.AsyncClient() as client:
        # 打开文本文件并准备文件上传
        with open(text_file, "rb") as f:
            files = {"file": (text_file.name, f, "text/plain")}

            # 发送请求到后端的上传文本接口
            response = await client.post(UPLOAD_URL, files=files)

            # 打印响应状态码和响应体
            print(f"Response Status: {response.status_code}")
            print(f"Response Body: {response.text}")  # 打印原始响应体

            # 检查响应是否为有效的 JSON 数据
            try:
                response_json = response.json()
                print(f"Parsed Response: {json.dumps(response_json, ensure_ascii=False, indent=2)}")
            except json.JSONDecodeError:
                print("Failed to parse JSON response.")

if __name__ == "__main__":
    asyncio.run(main())
