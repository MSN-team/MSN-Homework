# popquiz/models.py
import os
import uuid
import types
import logging
from dotenv import load_dotenv, find_dotenv

# 1) 加载环境变量（可选）
load_dotenv(find_dotenv())

# 2) 配置 MongoDB URI 和 DB 名
mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
db_name   = os.getenv("MONGODB_DB",  "popquiz")

try:
    # 3) 尝试连接 MongoDB
    from pymongo import MongoClient
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=3000)
    client.server_info()                # 触发一次网络请求，确保可连通
    db = client[db_name]
    # 这里可以根据你的需要增加更多 collection
    content_collection = db["contents"]
    quiz_collection    = db["quizzes"]
    answer_collection  = db["answers"]
    statistics_collection = db["statistics"]
    logging.info("✅ MongoDB 连接成功：%s / %s", mongo_uri, db_name)

except Exception as e:
    # 4) Fallback 内存集合（只支持 insert_one）
    logging.warning("⚠️ MongoDB 不可用 (%s)，转为内存模式", e)

    def _mem_insert_one(doc: dict):
        """给 doc 造一个假的 inserted_id"""
        return types.SimpleNamespace(inserted_id=uuid.uuid4().hex)

    # 仅保留 insert_one，其它方法遇到就报错
    mem_ns = types.SimpleNamespace(
        insert_one=_mem_insert_one,
        count_documents=lambda *_, **__: 0
    )

    content_collection    = mem_ns
    quiz_collection       = mem_ns
    answer_collection     = mem_ns
    statistics_collection = mem_ns
