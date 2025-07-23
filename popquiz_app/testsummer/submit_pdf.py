# submit_pdf.py
# -*- coding: utf-8 -*-
"""
异步上传本地 PDF 到 FastAPI /submit-pdf 端点
用法：
    python submit_pdf.py
"""

import httpx
import asyncio
import json
from pathlib import Path

# 配置 ==============================================

API_URL = "http://127.0.0.1:8000/upload-pdf"   # 根据后端实际路由修改
PDF_PATH  = Path("4-16.pdf")                   # 本地待上传文件
TIMEOUT_S = 120.0                                # 总 / 读取超时（秒）

# ===================================================


async def main() -> None:
    if not PDF_PATH.exists():
        raise FileNotFoundError(f"❌ 找不到文件: {PDF_PATH.resolve()}")

    # 创建全局超时对象
    timeout = httpx.Timeout(TIMEOUT_S, read=TIMEOUT_S)

    async with httpx.AsyncClient(timeout=timeout) as client:
        # multipart/form-data，字段名默认为 file
        with PDF_PATH.open("rb") as f:
            files = {"file": (PDF_PATH.name, f, "application/pdf")}
            response = await client.post(API_URL, files=files)

        print(f"Response Status: {response.status_code}")
        if response.status_code == 200:
            try:
                data = response.json()
                print("Response Body:\n",
                      json.dumps(data, ensure_ascii=False, indent=2))
            except Exception:
                print("⚠️ 无法解析 JSON，服务器原始响应：\n", response.text)
        else:
            print("❌ Error:\n", response.text)


if __name__ == "__main__":
    asyncio.run(main())
