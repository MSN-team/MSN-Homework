<template>
  <div class="app">
    <!-- 导航栏 -->
    <el-header class="navbar">
      <div class="left">
        <el-dropdown @command="handleCommand">
          <div class="avatar-btn">
            <img src="https://cdn.jsdelivr.net/gh/placeholderuser/identicons/placeholder.png" alt="用户中心" />
          </div>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item command="profile">个人信息</el-dropdown-item>
            <el-dropdown-item command="logout">退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
        <h3>微课堂</h3>
      </div>
      <div class="right">
        <span>演讲者界面</span>
      </div>
    </el-header>

    <!-- 主内容区 -->
    <el-main class="wrapper">
      <el-card class="box-card">
        <div slot="header" class="clearfix">
          <span>当前题目</span>
        </div>
        
        <!-- 题目内容 -->
        <el-row>
          <el-col :span="24">
            <el-card class="question-card">
              <div class="question-text">{{ questionText }}</div>
              
              <!-- 选项区域 -->
              <div class="options">
                <el-row :gutter="12">
                  <el-col :span="24" v-for="(option, key) in options" :key="key">
                    <el-card :class="{'correct-option': key === correctAnswer}">
                      <div>{{ key }}: {{ option }}</div>
                    </el-card>
                  </el-col>
                </el-row>
              </div>
              
              <!-- 正确答案 -->
              <el-row class="answer-row">
                <el-col :span="24">
                  <span class="answer-label">正确答案：</span>
                  <span class="correct-answer">{{ correctAnswerText }}</span>
                </el-col>
              </el-row>
            </el-card>
          </el-col>
        </el-row>
        
        <!-- 统计数据 -->
        <el-row class="statistics" :gutter="12">
          <el-col :span="8">
            <el-card class="stat-card">
              <div class="stat-title">答题人数</div>
              <div class="stat-value">{{ answerCount }}</div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card class="stat-card">
              <div class="stat-title">正确率</div>
              <div class="stat-value">{{ correctRate }}%</div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card class="stat-card">
              <div class="stat-title">错误率</div>
              <div class="stat-value">{{ errorRate }}%</div>
            </el-card>
          </el-col>
        </el-row>
      </el-card>
    </el-main>
  </div>
</template>

<script>
export default {
  data() {
    return {
      // 题目数据
      questionText: "猫有几种颜色？",
      options: {
        A: "黑色",
        B: "粉色",
        C: "黄色",
        D: "蓝色"
      },
      correctAnswer: "C",
      
      // 统计数据
      answerCount: 219,
      correctRate: 79,
      errorRate: 21
    };
  },
  computed: {
    // 根据正确答案选项计算显示文本
    correctAnswerText() {
      switch(this.correctAnswer) {
        case 'A': return '黑色';
        case 'B': return '粉色';
        case 'C': return '黄色';
        case 'D': return '蓝色';
        default: return '';
      }
    }
  },
  methods: {
    // 处理下拉菜单命令
    handleCommand(command) {
      if (command === 'logout') {
        // 处理退出登录逻辑
        console.log('退出登录');
      } else if (command === 'profile') {
        // 处理个人信息逻辑
        console.log('查看个人信息');
      }
    }
  }
};
</script>

<style>
/* 基础样式 */
.app {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.navbar {
  background: linear-gradient(135deg, #6A82FB 0%, #FC5C7D 100%);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.left, .right {
  display: flex;
  align-items: center;
}

.avatar-btn {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: rgba(255,255,255,0.25);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  margin-right: 20px;
}

.avatar-btn img {
  width: 24px;
  height: 24px;
}

h3 {
  font-size: 20px;
  font-weight: 500;
}

.right span {
  font-size: 16px;
  font-weight: 500;
}

.wrapper {
  padding: 20px;
}

/* 题目卡片样式 */
.question-card {
  margin-bottom: 20px;
}

.question-text {
  font-size: 18px;
  font-weight: 500;
  margin-bottom: 15px;
}

.options {
  margin-bottom: 15px;
}

.answer-row {
  margin-top: 15px;
}

.answer-label {
  font-weight: 500;
  margin-right: 10px;
}

.correct-answer {
  color: #67C23A;
  font-weight: 500;
}

/* 统计卡片样式 */
.statistics {
  margin-top: 20px;
}

.stat-card {
  text-align: center;
}

.stat-title {
  font-size: 16px;
  color: #606266;
  margin-bottom: 10px;
}

.stat-value {
  font-size: 24px;
  font-weight: 500;
  color: #303133;
}

/* 正确选项样式 */
.correct-option {
  border-color: #67C23A;
  background-color: #F0F9EB;
}
</style>