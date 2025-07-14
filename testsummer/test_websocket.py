# -*- coding: utf-8 -*-
"""
向 /record-audio 端点发送本地音频文件并打印返回结果
pip install websockets
"""

import asyncio, json
from pathlib import Path
import websockets

WS_URI     = "ws://127.0.0.1:8000/record-audio"  # 与后端保持一致
AUDIO_FILE = "sample.webm"                       # 准备一段音频

async def main():
    audio = Path(AUDIO_FILE).read_bytes()

    async with websockets.connect(WS_URI, max_size=None) as ws:
        print("✅ WebSocket connected")
        await ws.send(audio)
        await ws.send("DONE")                    # 关键：告诉服务器音频结束
        print(f"▶ Sent {len(audio)/1024:.1f} KB")

        resp = await ws.recv()
        print("📩 Response:")
        print(json.dumps(json.loads(resp), ensure_ascii=False, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
