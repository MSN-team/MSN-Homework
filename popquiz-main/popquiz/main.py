# main.py
# -*- coding: utf-8 -*-
"""
PopQuiz FastAPI
- /submit-text      上传纯文本 → Whisper ↓
- /upload-audio     上传整段音频文件
- /record-audio     WebSocket 实时录音
可在无 MongoDB 环境下自动降级为内存集合，或设 USE_DB=0 强制内存模式。
"""

import os, uuid, logging, asyncio, aiofiles
from datetime import datetime
from pathlib import Path
from typing import Any, List

from fastapi import FastAPI, HTTPException, UploadFile, File, WebSocket, WebSocketDisconnect
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from pymongo import MongoClient, errors as mongoerr
import whisper

# ───────────────────────────────
# 日志
# ───────────────────────────────
logging.basicConfig(
    level=os.getenv("QUIZ_LOG_LEVEL", "INFO").upper(),
    format="%(levelname)s | %(message)s",
)
log = logging.getLogger(__name__)

# ───────────────────────────────
# MongoDB or In-Memory fallback
# ───────────────────────────────
def _mem_collection() -> Any:
    """简单内存集合，支持 insert_one / count_documents"""
    store: List[dict] = []

    class _Mem:
        def insert_one(self, doc: dict):
            doc["_id"] = uuid.uuid4().hex
            store.append(doc)
            return type("R", (), {"inserted_id": doc["_id"]})()

        def count_documents(self, _filter):
            return len(store)

    return _Mem()

def _init_collections():
    if os.getenv("USE_DB", "1") == "0":
        log.warning("USE_DB=0 → 使用内存集合")
        return _mem_collection(), _mem_collection()

    try:
        uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        client = MongoClient(uri, serverSelectionTimeoutMS=3000)
        client.server_info()                          # 立即触发连接
        db = client["popquiz"]
        log.info("MongoDB 连接成功")
        return db["contents"], db["quizzes"]
    except mongoerr.PyMongoError as e:
        log.warning("MongoDB 不可用 (%s)，降级为内存集合", e)
        return _mem_collection(), _mem_collection()

content_collection, quiz_collection = _init_collections()

# ───────────────────────────────
# Whisper — 单例
# ───────────────────────────────
import functools
@functools.lru_cache()
def get_whisper():
    return whisper.load_model("base")

# ───────────────────────────────
# 业务依赖：生成题目
# ───────────────────────────────
from services import generate_quiz_with_deepseek   # 本地 services.py

# ───────────────────────────────
# FastAPI 应用
# ───────────────────────────────
app = FastAPI(title="PopQuiz API")

@app.get("/")
async def home():
    return {"message": "PopQuiz ready ✨"}

# ────────── 插入种子数据（仅首次 / 有 DB 功能时） ──────────
@app.on_event("startup")
async def seed():
    if hasattr(content_collection, "count_documents") and content_collection.count_documents({}) == 0:
        content_collection.insert_one({
            "title": "AI 技术的未来",
            "type": "text",
            "data": "AI 技术正在改变世界，包括教育、医疗等领域。",
            "created_at": datetime.utcnow().isoformat()
        })
        log.info("Seed content inserted")

# ────────── 工具函数 ──────────
async def _run_quiz(text: str):
    try:
        quizzes_raw = await asyncio.to_thread(generate_quiz_with_deepseek, text)
        if not quizzes_raw:
            log.error("LLM 返回空列表")
            return None
        return [{"quiz_id": q["quiz_id"], "quiz": q["quiz"]} for q in quizzes_raw]
    except Exception as exc:
        log.exception("出题失败: %s", exc)
        return None

def _json_ok(cid, quizzes):
    return {"status": "success", "content_id": str(cid), "quizzes": quizzes}

def _json_err(detail):
    return {"status": "error", "detail": detail}

# ────────── 上传纯文本 ──────────
@app.post("/submit-text")
async def submit_text(payload: dict):
    text = payload.get("text", "").strip()
    if not text:
        raise HTTPException(400, "text 字段不能为空")

    cid = content_collection.insert_one({
        "title": "文本内容",
        "type": "text",
        "data": text,
        "created_at": datetime.utcnow().isoformat()
    }).inserted_id

    quizzes = await _run_quiz(text)
    return _json_ok(cid, quizzes) if quizzes else _json_err("题目生成失败")

# ────────── 上传整段音频文件 ──────────
@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    tmp = Path(f"upload_{uuid.uuid4().hex}.wav")
    tmp.write_bytes(await file.read())

    text = (await asyncio.to_thread(get_whisper().transcribe, str(tmp)))["text"]
    tmp.unlink(missing_ok=True)

    cid = content_collection.insert_one({
        "title": "语音内容",
        "type": "audio",
        "data": text,
        "created_at": datetime.utcnow().isoformat()
    }).inserted_id

    quizzes = await _run_quiz(text)
    return _json_ok(cid, quizzes) if quizzes else _json_err("题目生成失败")

# ────────── WebSocket 实时录音 ──────────
@app.websocket("/record-audio")
async def record_audio(ws: WebSocket):
    await ws.accept()
    tmp_path = Path(f"rec_{uuid.uuid4().hex}.wav")

    # 1 收流
    try:
        async with aiofiles.open(tmp_path, "wb") as f:
            while True:
                try:
                    msg = await ws.receive()
                except WebSocketDisconnect:
                    return
                if msg["type"] == "websocket.receive":
                    if "bytes" in msg:
                        await f.write(msg["bytes"])
                    elif msg.get("text") == "DONE":
                        break
                elif msg["type"] == "websocket.disconnect":
                    return
    except Exception as e:
        await ws.send_json(_json_err(f"录音写入失败: {e}"))
        await ws.close()
        return

    # 2 Whisper
    try:
        text = (await asyncio.to_thread(get_whisper().transcribe, str(tmp_path)))["text"]
    finally:
        tmp_path.unlink(missing_ok=True)

    # 3 出题
    quizzes = await _run_quiz(text)
    if not quizzes:
        await ws.send_json(_json_err("题目生成失败"))
        await ws.close()
        return

    cid = content_collection.insert_one({
        "title": "实时录音",
        "type": "audio",
        "data": text,
        "created_at": datetime.utcnow().isoformat()
    }).inserted_id

    await ws.send_json(_json_ok(cid, quizzes))
    await ws.close()

@app.get("/record-audio")
async def record_info():
    return {"message": "WebSocket endpoint at /record-audio"}

# ────────── 静态文件（可选） ──────────
if os.path.isdir("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")
