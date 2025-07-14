from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection
client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("MONGO_DB")]

# Define collections
content_collection = db["contents"]  # 存储演讲内容
quiz_collection = db["quizzes"]      # 存储生成的 Quiz
answer_collection = db["answers"]    # 存储用户回答
statistics_collection = db["statistics"]  # 存储统计数据