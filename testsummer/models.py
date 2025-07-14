import os, uuid, types, logging
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())  # 读取 .env，但如果没有也不会报错

mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
db_name   = os.getenv("MONGODB_DB",  "popquiz")   # ✅ 给默认名

try:
    from pymongo import MongoClient
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=3000)
    client.server_info()                # 测试连接
    db = client[db_name]
    quiz_collection = db["quizzes"]
except Exception as e:
    logging.warning("MongoDB 不可用 (%s)，转为内存模式", e)
    def _insert_one(doc):
        return types.SimpleNamespace(inserted_id=uuid.uuid4().hex)
    quiz_collection = types.SimpleNamespace(insert_one=_insert_one)
