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
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item command="profile">个人信息</el-dropdown-item>
                <el-dropdown-item command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
            <h3 class="app-title">微课堂</h3>
          </div>
          <div class="right-section">
            <span class="page-title">听众界面</span>
          </div>
        </el-header>
      </el-container>
    </el-row>

    <!-- 主内容区 -->
    <el-container class="main-container">
      <el-row :gutter="20">
        <el-col :xs="24" :sm="24" :md="18" :lg="16" :xl="14" :offset="(24-14)/2">
          <el-card class="main-card">
            <div slot="header" class="card-header">
              <span class="question-text">{{ `题目：${questionData.question}` }}</span>
            </div>
            
            <!-- 选项区域 -->
            <el-radio-group v-model="selectedOption" @change="handleOptionChange" :disabled="isSubmitted">
              <div v-for="(option, key) in questionData.options" :key="key" class="option-item">
                <el-radio :label="key" border class="radio-option">
                  <span class="option-label">{{ key }}. {{ option }}</span>
                </el-radio>
              </div>
            </el-radio-group>
            
            <!-- 提交按钮 -->
            <el-button 
              class="submit-btn" 
              type="primary" 
              @click="submitAnswer"
              :disabled="!selectedOption || isSubmitted"
            >
              提交答案
            </el-button>
            
            <!-- 答案结果 -->
            <div v-if="isSubmitted" class="answer-result">
              <el-descriptions column="1" border>
                <el-descriptions-item label="答案结果">
                  <span v-if="isCorrect" class="correct-answer">
                    <i class="el-icon-success"></i> 回答正确！正确答案是 {{ questionData.correct }}. {{ questionData.options[questionData.correct] }}
                  </span>
                  <span v-else class="wrong-answer">
                    <i class="el-icon-error"></i> 回答错误！正确答案是 {{ questionData.correct }}. {{ questionData.options[questionData.correct] }}
                  </span>
                </el-descriptions-item>
              </el-descriptions>
            </div>
            
            <!-- 评论区域 -->
            <div class="comment-section">
              <el-input
                type="textarea"
                :rows="3"
                placeholder="请输入您的评论..."
                v-model="commentContent"
              ></el-input>
              <el-button 
                class="comment-btn" 
                type="primary" 
                @click="submitComment"
                :disabled="!commentContent.trim()"
              >
                提交评论
              </el-button>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'MicroClassroom',
  data() {
    return {
      // 题目数据
      questionData: {
        question: "猫有几种颜色？",
        options: {
          A: "黑色",
          B: "粉色",
          C: "黄色",
          D: "蓝色"
        },
        correct: "C"
      },
      // 选中的选项
      selectedOption: '',
      // 是否已提交
      isSubmitted: false,
      // 是否回答正确
      isCorrect: false,
      // 评论内容
      commentContent: ''
    };
  },
  methods: {
    // 处理选项变更
    handleOptionChange(value) {
      this.selectedOption = value;
    },
    
    // 提交答案
    submitAnswer() {
      if (!this.selectedOption) {
        this.$message.warning('请先选择一个答案');
        return;
      }
      
      this.isSubmitted = true;
      this.isCorrect = this.selectedOption === this.questionData.correct;
      
      // 显示结果提示
      if (this.isCorrect) {
        this.$message.success('回答正确！');
      } else {
        this.$message.error('回答错误，请查看正确答案');
      }
    },
    
    // 提交评论
    submitComment() {
      if (!this.commentContent.trim()) {
        this.$message.warning('请输入评论内容');
        return;
      }
      
      // 实际项目中这里会调用API提交评论
      this.$message.success('评论提交成功！');
      this.commentContent = '';
    },
    
    // 处理下拉菜单命令
    handleDropdownCommand(command) {
      switch (command) {
        case 'profile':
          this.$message.info('跳转到个人信息页面');
          break;
        case 'logout':
          this.$message.confirm('确定要退出登录吗？', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            this.$message.success('退出登录成功');
          }).catch(() => {
            this.$message.info('已取消退出');
          });
          break;
      }
    }
  }
};
</script>

<style scoped>
/* 导航栏样式 */
.navbar {
  background: linear-gradient(135deg, #6A82FB 0%, #FC5C7D 100%);
  color: #fff;
  box-shadow: 0 4px 16px rgba(0,0,0,.08);
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

/* 主内容区样式 */
.main-container {
  padding: 40px 24px;
  max-width: 960px;
  margin: 0 auto;
  width: 100%;
}

.main-card {
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0,0,0,.08);
  overflow: hidden;
}

.card-header {
  padding: 20px 24px;
  border-bottom: 1px solid #e0e4ef;
}

.question-text {
  font-size: 18px;
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
}

.radio-option:hover {
  background-color: #f5f7ff;
}

.option-label {
  margin-left: 8px;
}

/* 按钮样式 */
.submit-btn {
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

.comment-btn {
  margin-top: 12px;
  padding: 10px 20px;
}
</style>