# test_submit_text.py
# -*- coding: utf-8 -*-
"""
异步上传本地 TXT 到后端 /submit-text
用法:
    python test_submit_text.py
"""

import asyncio, httpx, json
from pathlib import Path

API_URL   = "http://127.0.0.1:8000/submit-text"
TXT_PATH  = Path("test.txt")          # 待上传的文本
TIMEOUT   = httpx.Timeout(60.0, read=60.0)

async def main() -> None:
    if not TXT_PATH.exists():
        raise FileNotFoundError(f"❌ 找不到文件: {TXT_PATH.resolve()}")

    # 先读取文件并保持句柄打开, 再发请求
    with TXT_PATH.open("rb") as fh:
        files = {"file": (TXT_PATH.name, fh, "text/plain")}

        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            resp = await client.post(API_URL, files=files)

    print("Status:", resp.status_code)
    try:
        print("Response:\n", json.dumps(resp.json(), ensure_ascii=False, indent=2))
    except Exception:
        print("⚠️  非 JSON 响应:\n", resp.text)

if __name__ == "__main__":
    asyncio.run(main())
