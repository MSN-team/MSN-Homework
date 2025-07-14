from fastapi import FastAPI, HTTPException, UploadFile, File
from pymongo import MongoClient
from models import content_collection, quiz_collection, answer_collection, statistics_collection
from services import generate_quiz_with_deepseek
import whisper
from datetime import datetime
from bson import ObjectId
from fastapi.encoders import jsonable_encoder

# Initialize FastAPI app
app = FastAPI()

# MongoDB connection setup
client = MongoClient("mongodb://localhost:27017/")
db = client["popquiz"]

@app.get("/")
async def root():
    return {"message": "Welcome to the PopQuiz API!"}

@app.get("/test-db")
async def test_db():
    try:
        # Attempt to list collections in the database
        collections = db.list_collection_names()
        return {"status": "success", "collections": collections}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.on_event("startup")
async def initialize_database():
    """
    初始化 MongoDB 集合，插入示例数据
    """
    # 检查并插入示例内容
    if content_collection.count_documents({}) == 0:
        content_collection.insert_one({
            "title": "AI技术的未来",
            "type": "text",
            "data": "AI技术正在改变世界，包括教育、医疗等领域。",
            "metadata": {},
            "created_at": "2025-06-23T10:00:00"
        })

    # 检查并插入示例 Quiz
    if quiz_collection.count_documents({}) == 0:
        quiz_collection.insert_one({
            "content_id": None,  # 示例数据，需替换为实际内容 ID
            "question": "AI技术正在改变哪些领域？",
            "options": ["教育", "医疗", "交通", "以上都是"],
            "answer": "以上都是",
            "created_at": "2025-06-23T10:10:00"
        })

    # 检查并插入示例用户回答
    if answer_collection.count_documents({}) == 0:
        answer_collection.insert_one({
            "quiz_id": None,  # 示例数据，需替换为实际 Quiz ID
            "user_id": "user123",
            "answer": "以上都是",
            "is_correct": True,
            "submitted_at": "2025-06-23T10:15:00"
        })

    # 检查并插入示例统计数据
    if statistics_collection.count_documents({}) == 0:
        statistics_collection.insert_one({
            "content_id": None,  # 示例数据，需替换为实际内容 ID
            "total_quizzes": 5,
            "total_answers": 100,
            "correct_rate": 0.85,
            "created_at": "2025-06-23T11:00:00"
        })

@app.post("/submit-text")
async def submit_text(content: dict):
    """
    接收用户输入的文本，保存到 contents，并生成 quizzes
    """
    text = content.get("text")
    if not text:
        raise HTTPException(status_code=400, detail="Text content is required")

    # 保存到 contents 集合
    content = {
        "title": "文本内容",
        "type": "text",
        "data": text,
        "metadata": {},
        "created_at": datetime.now().isoformat()
    }
    content_id = content_collection.insert_one(content).inserted_id

    # 生成 quizzes
    quizzes = generate_quiz_with_deepseek(text)

    # 将 quizzes 中的 ObjectId 转换为字符串
    quizzes = [
        {
            "quiz_id": str(quiz["quiz_id"]),
            "quiz": quiz["quiz"]
        }
        for quiz in quizzes
    ]

    # 使用 jsonable_encoder 处理返回值
    return jsonable_encoder({"status": "success", "content_id": str(content_id), "quizzes": quizzes})

@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    """
    接收用户上传的语音文件并转换为文字，保存到 contents，并生成 quizzes
    """
    file_location = f"./{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())

    # 使用 Whisper 转换语音为文字
    model = whisper.load_model("base")
    result = model.transcribe(file_location)
    text = result["text"]

    # 保存到 contents 集合
    content = {
        "title": "语音内容",
        "type": "audio",
        "data": text,
        "metadata": {},
        "created_at": datetime.now().isoformat()
    }
    content_id = content_collection.insert_one(content).inserted_id

    # 生成 quizzes
    quizzes = generate_quiz_with_deepseek(text)

    # 将 quizzes 中的 ObjectId 转换为字符串
    quizzes = [
        {
            "quiz_id": str(quiz["quiz_id"]),
            "quiz": quiz["quiz"]
        }
        for quiz in quizzes
    ]

    # 使用 jsonable_encoder 处理返回值
    return jsonable_encoder({"status": "success", "content_id": str(content_id), "quizzes": quizzes})

from fastapi import WebSocket, WebSocketDisconnect
import aiofiles

@app.websocket("/record-audio")
async def record_audio(websocket: WebSocket):
    """
    接收实时录音数据，转换为文字，保存到 contents，并生成 quizzes
    """
    await websocket.accept()
    audio_file_path = "./recorded_audio.wav"

    try:
        async with aiofiles.open(audio_file_path, mode="wb") as audio_file:
            while True:
                data = await websocket.receive_bytes()
                await audio_file.write(data)

    except WebSocketDisconnect:
        # 使用 Whisper 转换语音为文字
        model = whisper.load_model("base")
        result = model.transcribe(audio_file_path)
        text = result["text"]

        # 保存到 contents 集合
        content = {
            "title": "实时录音内容",
            "type": "audio",
            "data": text,
            "metadata": {},
            "created_at": datetime.now().isoformat()
        }
        content_id = content_collection.insert_one(content).inserted_id

        # 生成 quizzes
        quizzes = generate_quiz_with_deepseek(text)

        # 将 quizzes 中的 ObjectId 转换为字符串
        quizzes = [
            {
                "quiz_id": str(quiz["quiz_id"]),
                "quiz": quiz["quiz"]
            }
            for quiz in quizzes
        ]

        # 返回结果
        await websocket.send_json({"status": "success", "content_id": str(content_id), "quizzes": quizzes})

@app.get("/record-audio")
async def record_audio_page():
    """
    返回录音页面或说明
    """
    return {"message": "This is a WebSocket endpoint. Please connect using WebSocket."}

from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="static"), name="static")