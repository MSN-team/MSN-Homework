<template>
  <div class="app-container">
    <!-- 导航栏 -->
    <el-row class="navbar">
      <el-container>
        <el-header height="72px" class="header-content">
          <div class="left-section">
            <el-dropdown trigger="click" @command="handleDropdownCommand">
              <div class="avatar-btn">
                <el-avatar icon="el-icon-user" :size="44"></el-avatar>
              </div>
            </el-dropdown>
            <h3 class="app-title">微课堂</h3>
          </div>
          <div class="right-section">
            <el-button class="class-button" type="primary" @click="joinClass">
              加入课堂
            </el-button>
            <!-- <span class="page-title">听众界面</span> -->
          </div>
        </el-header>
      </el-container>
    </el-row>
    <!-- 答题和评论区域 -->
    <div class="main-content">
      <!-- 答题区域 -->
      <div class="question-area">
        <el-card class="main-card">
          <template #header>
            <span class="question-text">{{ `题目：${questionData.question}` }}</span>
          </template>
          <!-- 选项区域 -->
          <el-radio-group v-model="selectedOption" @change="handleOptionChange" :disabled="isSubmitted">
            <el-row :gutter="12">
              <el-col :span="24" v-for="(option, key) in questionData.options" :key="key">
                <el-radio :label="key" border class="radio-option">
                  <span class="option-label">{{ key }}. {{ option }}</span>
                </el-radio>
              </el-col>
            </el-row>
          </el-radio-group>
          <br>
          <!-- 提交按钮 -->
          <el-button
            class="submit-btn"
            type="primary"
            @click="submitAnswer"
            :disabled="!selectedOption || isSubmitted"
          >
            提交答案
          </el-button>
          <br>
          <!-- 刷新按钮 -->
          <el-button
            class="submit-btn"
            type="primary"
            @click="refreshQuestion"
            :disabled="!selectedOption || isSubmitted"
          >
            刷新
          </el-button>
          <!-- 答案结果 -->
          <div v-if="isSubmitted" class="answer-result">
            <el-descriptions column="1" border>
              <el-descriptions-item label="答案结果">
                <span v-if="isCorrect" class="correct-answer">
                  <i class="el-icon-success"></i> 回答正确！正确答案是 {{ questionData.answer }}. {{ questionData.options[questionData.answer] }}
                </span>
                <span v-else class="wrong-answer">
                  <i class="el-icon-error"></i> 回答错误！正确答案是 {{ questionData.answer }}. {{ questionData.options[questionData.answer] }}
                </span>
              </el-descriptions-item>
            </el-descriptions>
          </div>
        </el-card>
      </div>
      <!-- 评论区域 -->
      <div class="comment-area">
        <el-card class="comment-card">
          <template #header>
            <span class="question-text">评论区</span>
          </template>
          <el-input
            type="textarea"
            :rows="4"
            placeholder="请输入评论内容..."
            v-model="commentContent"
          >
          </el-input>
          <el-button
            class="comment-btn"
            type="primary"
            @click="submitComment"
            :disabled="!commentContent.trim()"
          >
            提交评论
          </el-button>
        </el-card>
      </div>
    </div>

    <!-- 加入课堂表单对话框 -->
    <el-dialog title="加入课堂" v-model="dialogVisible" width="30%">
      <el-form :model="form" label-width="80px">
        <el-form-item label="课堂名称">
          <el-input v-model="form.name" placeholder="请输入老师用户名"></el-input>
        </el-form-item>
        <el-form-item label="课堂密码">
          <el-input v-model="form.classid" type="classId" placeholder="请输入课堂暗号"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="submitJoinClass">确 定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ElMessage } from 'element-plus'
import api from '@/api/index.js'

export default {
  name: 'MicroClassroom',

  data() {
    return {
      questionData: { question: '', options: { A: '', B: '', C: '', D: '' }, answer: '' },
      selectedOption: '',
      isSubmitted: false,
      isCorrect: false,
      commentContent: '',
      dialogVisible: false, // 对话框显示控制变量
      form: {
        className: '',
        classPassword: ''
      }
    }
  },

  computed: {
    correctAnswerText() {
      return this.questionData.options[this.questionData.answer] || ''
    }
  },

  mounted() {
    this.refreshQuestion()
  },

  methods: {
    joinClass() {
      this.dialogVisible = true; // 打开对话框
    },

    submitJoinClass() {
      // 提交加入课堂的逻辑
      if (!this.form.className || !this.form.classPassword) {
        ElMessage.warning('请填写课堂名称和密码')
        return
      }
      // 这里可以调用后端API来验证课堂名称和密码
      // 例如：api.joinClass(this.form.className, this.form.classPassword)
      this.dialogVisible = false; // 关闭对话框
      ElMessage.success('加入课堂成功！')
    },

    /* 下拉头像菜单示例 */
    handleDropdownCommand(cmd) {
      if (cmd === 'logout') ElMessage.info('已退出')
      else if (cmd === 'profile') ElMessage.info('个人信息 ~')
    },

    /* 选项切换 */
    handleOptionChange(val) {
      this.selectedOption = val
    },

    /* 交卷 */
    submitAnswer() {
      if (!this.selectedOption) return ElMessage.warning('请先选择一个答案')
      this.isSubmitted = true
      this.isCorrect = this.selectedOption === this.questionData.answer
      ElMessage[this.isCorrect ? 'success' : 'error'](
        this.isCorrect
          ? '回答正确！'
          : `回答错误，正确答案：${this.questionData.answer}`
      )
    },

    /* 拉取最新题目 */
    async refreshQuestion() {
      this.selectedOption = ''
      this.isSubmitted = false
      this.isCorrect = false

      try {
        const dat = await api.getquestion() // 已在 api/index.js 处理 data
        console.log(dat)
        if (!dat || !Array.isArray(dat.data.options) || dat.data.options.length < 4) {
          throw new Error('题目字段格式不对')
        }

        /* 后端给的是数组 [A,B,C,D]，这里组装成对象方便模板 v-for */
        this.questionData = {
          question: dat.data.question,
          options: {
            A: dat.data.options[0] ?? '', // 使用 ?? 防御 undefined
            B: dat.data.options[1] ?? '',
            C: dat.data.options[2] ?? '',
            D: dat.data.options[3] ?? ''
          },
          answer: dat.data.answer,
          _id: dat.data._id
        }
      } catch (err) {
        console.error('[refreshQuestion] ', err)
        ElMessage.error('获取题目失败，请稍后重试')
      }
    }
  }
}
</script>

<style scoped>
/* 导航栏样式 */
.navbar {
  background: linear-gradient(135deg, #6A82FB 0%, #FC5C7D 100%);
  color: #fff;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 28px;
}

.left-section {
  display: flex;
  align-items: center;
}

.avatar-btn {
  cursor: pointer;
}

.app-title {
  margin-left: 20px;
  font-size: 18px;
  font-weight: 500;
}

.right-section {
  display: flex;
  align-items: center;
}

.page-title {
  font-size: 15px;
  font-weight: 500;
}

.class-button {
  font-size: 15px;
  font-weight: 500;
  background-color: transparent; /* 设置背景颜色为透明 */
  border: none; /* 可选：如果不需要边框，可以设置边框为透明或移除 */
  padding: 5px;
}

/* 主内容区样式 */
.main-content {
  display: flex;
  height: 80vh; /* 占据页面高度的80% */
  padding: 20px;
}

.question-area {
  flex: 2;
  padding-right: 20px;
  height: 100%;
}

.comment-area {
  flex: 1;
  height: 100%;
}

.main-card,
.comment-card {
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  height: 100%; /* 卡片高度占满父容器 */
}

.card-header {
  padding: 20px 24px;
  border-bottom: 1px solid #e0e4ef;
}

.question-text {
  font-size: 25px;
  font-weight: 500;
}

/* 选项样式 */
.option-item {
  margin-bottom: 12px;
}

.radio-option {
  width: 100%;
  border-radius: 8px;
  padding: 12px 16px;
  transition: all 0.15s;
  margin-bottom: 18px; /* 增加垂直边距 */
}

.radio-option:hover {
  background-color: #f5f7ff;
}

.option-label {
  margin-left: 8px;
}

/* 按钮样式 */
.submit-btn,
.comment-btn {
  margin-top: 24px;
  padding: 10px 20px;
}

/* 答案结果样式 */
.answer-result {
  margin-top: 24px;
  padding: 16px;
  border-radius: 8px;
  background-color: #f5f7ff;
}

.correct-answer {
  color: #67c23a;
  font-weight: 500;
}

.wrong-answer {
  color: #f56c6c;
  font-weight: 500;
}

/* 评论区域样式 */
.comment-section {
  margin-top: 32px;
}
</style>
