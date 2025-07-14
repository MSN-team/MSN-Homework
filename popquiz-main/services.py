from transformers import pipeline
import spacy
from models import quiz_collection
import re
from datetime import datetime
# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Load DeepSeek model
# pipe = pipeline("text-generation", model="deepseek-ai/DeepSeek-R1-0528", trust_remote_code=True, device=-1)
pipe = pipeline("text-generation", model="deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B", trust_remote_code=True, max_length=1024)
def extract_key_sentences(text: str):
    """
    使用 spaCy 提取文本中的重点句子
    """
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    print("重点内容", sentences)
    # 简单提取：返回前两句作为重点内容（可优化）
    return sentences[:2]

def generate_quiz_with_deepseek(text: str):
    """
    使用 DeepSeek 模型根据文本内容生成 Quiz
    """
    key_sentences = extract_key_sentences(text)
    quizzes = []

    for sentence in key_sentences:
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
{sentence}

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
        # print(result)  # 输出 DeepSeek 的结果，便于调试
        # 解析 DeepSeek 的输出

        generated_text = result[0]['generated_text'][1]['content']
        # print(result[0]['generated_text'][1]['content'])
        # print(result)
        if "</think>" in generated_text:
            generated_text = generated_text.split("</think>")[-1].strip()
        lines = re.split(r'\n+', generated_text)
        print("生成的文本:", lines)
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