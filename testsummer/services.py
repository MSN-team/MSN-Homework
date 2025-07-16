from transformers import pipeline
import re
from datetime import datetime
from models import quiz_collection

# Load DeepSeek model
pipe = pipeline(
    "text-generation", 
    model="deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B", 
    trust_remote_code=True, 
    max_new_tokens=512,  # 使用 max_new_tokens 替代 max_length
    do_sample=False,
)

def split_document(text: str, chunk_size: int = 1024) -> list:
    """将长文本分割成多个小段，避免超出模型的 token 限制"""
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

def generate_quiz_with_deepseek(text: str):
    """
    使用 DeepSeek 模型根据文本内容生成 Quiz
    """
    quizzes = []
    segments = split_document(text)

    for segment in segments:
        # 使用 DeepSeek 生成问题和选项
        messages = [
            {
                "role": "user",
                "content": f"""你是一位专业出题专家。请根据下列内容，生成一道**单项选择题**，用来考察该内容中的**关键知识点**。

要求：
1. 请判断文本中最重要、最值得掌握的知识点，并据此出题。不要为出题而出题，也不要考察一些细枝末节，只需要考察最核心的知识点。
2. 问题要有明确教学价值，能反映学生是否理解了核心内容。
3. 四个选项中**有且仅有一个是正确答案**，其余三个可以不出现在原文，但必须具有合理性和迷惑性，不能明显错误或胡编乱造， 但是其余三个选项必须要是错误的。
4. 输出必须严格遵循以下格式。

内容：
{segment}

输出格式（严格遵循）：
问题: ...
选项:
A. ...
B. ...
C. ...
D. ...
正确答案: A/B/C/D
"""
            }
        ]
        result = pipe(messages)
        generated_text = result[0]['generated_text'][1]['content']

        # 解析 DeepSeek 的输出
        if "</think>" in generated_text:
            generated_text = generated_text.split("</think>")[-1].strip()

        lines = re.split(r'\n+', generated_text)
        question = lines[0].replace("问题:", "").strip()
        options = [line.strip() for line in lines[2:6]]
        answer = lines[6].replace("正确答案:", "").strip()

        # 构造 Quiz 数据
        quiz = {
            "question": question,
            "options": options,
            "answer": answer,
            "created_at": datetime.now().isoformat()
        }

        # 存储到数据库
        quiz_id = quiz_collection.insert_one(quiz).inserted_id
        quiz.pop("_id", None)
        quizzes.append({"quiz_id": str(quiz_id), "quiz": quiz})

    return quizzes
