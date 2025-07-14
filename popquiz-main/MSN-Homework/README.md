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
| **输入收集**  | ‑ PPT / PDF / 纯文本 / 音频 / 视频 <br>‑ OCR & ASR 转文字 <br>‑ 自动分段同步到数据库 |
| **AI 处理** | ‑ GPT + 自研提示词链自动出题 <br>‑ 4 选 1、10 秒时限 <br>‑ 难度评估闭环，提高题目深度        |
| **输出交互**  | ‑ 网页 App + 微信小程序 <br>‑ 多角色：组织者 / 演讲者 / 听众 <br>‑ 实时答题、排行榜、反馈收集    |
| **数据统计**  | ‑ 个人正确率 & 全场排名 <br>‑ 题目‑级、演讲‑级与活动‑级报表 <br>‑ UX‑友好的可视化仪表盘         |
| **隐私与匿名** | ‑ 可切换实名 / 匿名模式 <br>‑ 只记录统计，不暴露个人身份                               |

---

## 🏗️ 系统架构 | Architecture

```
┌──────────┐         ┌─────────────┐         ┌──────────┐
│  输入层   │  ───►  │   AI 处理层  │  ───►  │  交互层   │
│(PPT/音频等)│        │ Prompt Chain │        │ Web / 小程序│
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
$ git clone https://github.com/your-org/popquiz.git && cd popquiz

# 2. 启动后端（FastAPI + Postgres + Redis）
$ docker compose up backend db redis

# 3. 启动前端
$ cd packages/webapp && npm i && npm run dev

# 4. 可选：小程序预览
$ cd packages/miniprogram && npm i && npm run dev:weapp
```

> ✨ 默认使用 OpenAI API，可在 `.env` 中改为 Azure / Minimax 等。

---

## 🖥️ 使用指南 | Usage

1. **组织者** 创建活动 → 上传 PPT / 录音 → 邀请演讲者 & 听众
2. **演讲者** 演讲中点击 **“💡 Pop Quiz”** 按钮
3. **听众** 手机收到题目 → *10 秒内答题*
4. 时间到，系统给出演讲者仪表盘 & 听众个人战报
5. 课后 **讨论区** 开放，可对题目继续深聊

---

## 🔒 数据隐私 | Privacy

* 默认开启 **匿名模式**，仅统计正确率与排名
* 用户可自选实名，并下载个人学习档案
* 所有原始素材加密存储，可一键删除

---

## 🗺️ 路线图 | Roadmap

* [x] MVP：单场活动、选择题、排行榜
* [ ] 多模态输入（视频 OCR 字幕）
* [ ] 题目难度自适应 & 动态加权评分
* [ ] 徽章系统 / 成就收集（游戏化）
* [ ] 插件化 LLM 选择（OpenAI / Claude / Gemini）
* [ ] 企业/校园 SSO 登录集成

---

## 🤝 贡献指南 | Contributing

1. Fork ➜ 新建分支 ➜ 提交 PR
2. Commit Message 遵循 `feat|fix|docs: 描述`
3. 通过 `npm run test` 确保单元测试通过

欢迎提交 **功能提案 / Bug 报告 / 文档改进**！

---

## 📜 许可证 | License

MIT © 2025 PopQuiz Team

---

## 🙏 鸣谢 | Acknowledgements

* [Menghan‑Xu/popquiz](https://github.com/menghan-xu/popquiz) — 早期实践样例
* OpenAI Whisper / GPT‑4o
* React • FastAPI • Taro

> *Keep your audience engaged, one quiz at a time!*
