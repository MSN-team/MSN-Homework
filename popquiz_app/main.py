# main.py
# -*- coding: utf-8 -*-

# ───── 0. 环境配置 ───────────────────────────────────────────────
import os
from http.client import HTTPException

os.environ["TRANSFORMERS_NO_TF"] = "1"        # 禁用 TensorFlow fallback

# ───── 1. 标准库 ────────────────────────────────────────────────
import io
import logging
from datetime import datetime
from pathlib import Path
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware

# ───── 2. 第三方库 ──────────────────────────────────────────────
import pdfplumber
from bson import ObjectId
from fastapi import FastAPI, UploadFile, File
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pymongo import MongoClient

# ───── 3. 本地模块 ──────────────────────────────────────────────
from models import (
    content_collection,
    quiz_collection,
    answer_collection,
    statistics_collection,
)
from services import generate_quiz_with_deepseek

# ─── 应用实例 & 日志 ────────────────────────────────────────────
app = FastAPI(title="PopQuiz API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[                # 生产环境最好精确填域名
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# ─── MongoDB 连接 ───────────────────────────────────────────────
MONGO_URI = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URI)
db = client["popquiz"]
logging.info("✅ MongoDB 连接成功：%s / %s", MONGO_URI, db.name)

# ─── 基本路由 ──────────────────────────────────────────────────
#change
@app.get("/questions")
async def questions():
    """
    取 quiz_collection 中 _id 最大（最新）的一条题目
    """
    doc = quiz_collection.find_one(sort=[("_id", -1)])   # 空集合时返回 None

    if doc is None:
        raise HTTPException(status_code=404, detail="没有题目")

    # 把 ObjectId → str，再交给 FastAPI
    payload = jsonable_encoder(
        doc,
        custom_encoder={ObjectId: str},
        by_alias=True,            # 让 _id 保持字段名不变
    )
    return JSONResponse(content=payload)

@app.get("/")
async def root():
    return {"message": "Welcome to the PopQuiz API!"}


@app.get("/test-db")
async def test_db():
    try:
        return {"status": "success", "collections": db.list_collection_names()}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ─── 启动事件：示例数据（可选）──────────────────────────────────
@app.on_event("startup")
async def initialize_database():
    if content_collection.estimated_document_count() == 0:
        content_collection.insert_one(
            {
                "title": "AI 技术的未来",
                "type": "text",
                "data": "AI 正在改变世界，包括教育、医疗等领域。",
                "metadata": {},
                "created_at": datetime.utcnow(),
            }
        )
    if quiz_collection.estimated_document_count() == 0:
        quiz_collection.insert_one(
            {
                "content_id": None,
                "question": "AI 技术正在改变哪些领域？",
                "options": ["教育", "医疗", "交通", "以上都是"],
                "answer": "以上都是",
                "created_at": datetime.utcnow(),
            }
        )
    logging.info("✅ 示例数据已初始化")

# ─── 上传 TXT ──────────────────────────────────────────────────
@app.post("/submit-text")
async def submit_text(
        file: UploadFile = File(...),
        num_questions: int = 1,          # ⬅️ 若想前端控制题量，可把它暴露出来
):
    # ① 校验类型 ------------------------------------------------
    if file.content_type not in {"text/plain", "application/octet-stream"}:
        raise HTTPException(400, "只接受纯文本文件")

    raw = await file.read()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:       # Win‑GBK 兜底
        text = raw.decode("gbk", errors="ignore")

    if not text.strip():
        raise HTTPException(400, "文件内容为空")

    # ② 落库 contents ------------------------------------------
    content_id = content_collection.insert_one(
        {
            "title": file.filename,
            "type": "text",
            "data": text,
            "metadata": {},
            "created_at": datetime.utcnow(),
        }
    ).inserted_id

    # ③ 生成 Quiz（超长文本自动切片 ⇒ 避免 1024 报错） ----------
    quizzes = generate_quiz_with_deepseek(
        text,
        num_questions=num_questions,     # 默认为 1
        collection=quiz_collection,      # 传 None 可不落库
        max_tokens=256,                  # ⬅️ 可按需再调
    )

    # ④ 返回 ----------------------------------------------------
    return JSONResponse(
        jsonable_encoder(
            {
                "status": "success",
                "content_id": str(content_id),
                "quizzes": quizzes,
            },
            custom_encoder={ObjectId: str},
        )
    )
# ─── 上传 PDF ──────────────────────────────────────────────────
@app.post("/upload-pdf")
async def upload_pdf(
        file: UploadFile = File(...),
):
    # 1) 校验类型
    if file.content_type not in {"application/pdf", "application/octet-stream"}:
        raise HTTPException(400, "只接受 PDF 文件")

    raw = await file.read()
    if not raw:
        raise HTTPException(400, "文件为空")

    # 2) 提取文字
    try:
        with pdfplumber.open(io.BytesIO(raw)) as pdf:
            text = "\n".join(
                (p.extract_text() or "") for p in pdf.pages
            ).strip()
    except Exception as e:
        raise HTTPException(400, f"无法解析 PDF：{e}") from e

    if not text:
        raise HTTPException(400, "PDF 中未检测到可提取的文本")

    # 3) 存 contents
    content_id = content_collection.insert_one(
        {
            "title": file.filename,
            "type": "pdf",
            "data": text,
            "metadata": {},
            "created_at": datetime.utcnow(),
        }
    ).inserted_id

    # 4) 生成 & 保存 1 道题
    quizzes = generate_quiz_with_deepseek(
        text,
        num_questions=1,
        collection=quiz_collection,   # 传给 services，才会真正 insert
    )

    return JSONResponse(
        jsonable_encoder(
            {
                "status": "success",
                "content_id": str(content_id),
                "quizzes": quizzes,
            },
            custom_encoder={ObjectId: str},
        )
    )

# ─── 静态文件 ──────────────────────────────────────────────────
static_dir = Path(__file__).parent / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")
