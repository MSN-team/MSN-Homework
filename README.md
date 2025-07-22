# MSN-Homework

> **Using AI to generate smart in‑session quizzes that keep every audience on their toes.**
> —— *“Have you really been paying attention?”*

---

## 📖 项目简介 | Overview

PopQuiz （简称 **PQ**）是一套面向 **课堂、培训与会议** 的实时互动系统。它以 AI 为核心，能够在演讲 / 授课过程中自动生成**随堂测验**（pop‑quiz），并通过网页 App 或微信小程序推送给听众，用 **10 秒钟** 即刻检验注意力与理解程度。

* **演讲者** 随时一键触发 Pop‑Quiz，获取实时反馈，调节节奏
* **听众** 手机秒收题目，答题 + 表达意见（太快 / 太慢 / 乏味…）
* **组织者** 统一查看多场活动的效果统计，量化“参与度”与“学习成果”

> <small>与传统人工出题相比，PQ 能抓取 PPT / 语音 / 视频等多模态信息，即席生成“定制化”题目，覆盖临场发挥内容。</small>

---

## ✨ 核心特性 | Key Features

| 模块        | 功能亮点                                                             |
| --------- | ---------------------------------------------------------------- |
| **输入收集**  | ‑ PPT / PDF / 纯文本<br>‑ 自动分段同步到数据库 |
| **AI 处理** | ‑ deepseek + 自研提示词链自动出题 <br>‑ 4 选 1、10 秒时限 <br>‑ 难度评估闭环，提高题目深度        |
| **输出交互**  | ‑ 网页web <br>‑ 多角色：组织者 / 演讲者 / 听众 <br>‑ 实时答题、反馈收集    |
| **数据统计**  | ‑ 个人正确率 <br>       |
| **隐私与匿名** | ‑ 可切换实名                               |

---

## 🏗️ 系统架构 | Architecture

```
┌──────────┐         ┌─────────────┐         ┌──────────┐
│  输入层   │  ───►  │   AI 处理层  │  ───►  │  交互层   │
│(PPT/音频等)│        │ Prompt Chain │        │ Web│
└──────────┘         └─────────────┘         └──────────┘
```

1. **Input Collector**：Whisper + Tesseract OCR，统一转文字 → `PostgreSQL`
2. **Quiz Generator**：FastAPI + Celery 调用 LLM，生成题库并进行质量评估闭环
3. **Delivery & UX**：

   * **Frontend**：Next.js / React
   * **Mini‑Program**：Taro / UniApp
   * **Realtime**：WebSocket + Redis Pub/Sub

---

## 🚀 快速开始 | Quick Start

```bash
# 1. 克隆仓库
$ git clone https://github.com/MSN-team/MSN-Homework.git && cd popquiz_app
# 2. 激活虚拟环境
$ .\flask_venv\Scripts\Activate
（或者根据".\MSN-Homework\popquiz_app\test\install_model.txt"中安装相应的包）
# 3. 数据库初始化
$ flask db init && flask db migrate && flask db upgrade
$ Make sure MongoDB is running locally on `mongodb://localhost:27017/`.
# 4. 启动后端（FastAPI + Flask + MongoDB）
$ $env:FLASK_APP="myapp" && python myapp.py 
$ uvicorn main:app --reload
# 5. 启动前端
$ cd popquize_vue
$ yarn serve


---

## 🖥️ 使用指南 | Usage

1. **组织者** 创建活动 → 上传 PPT / 录音 → 邀请演讲者 & 听众
2. **演讲者** 演讲中点击 **“💡 Pop Quiz”** 按钮
3. **听众** 手机收到题目 → *10 秒内答题*
4. 时间到，系统给出演讲者仪表盘 & 听众个人战报
5. 课后 **讨论区** 开放，可对题目继续深聊

---

## 🙏 鸣谢 | Acknowledgements

* [Menghan‑Xu/popquiz](https://github.com/menghan-xu/popquiz) — 早期实践样例
* OpenAI Whisper / GPT‑4o
* React • FastAPI • Taro

> *Keep your audience engaged, one quiz at a time!*
