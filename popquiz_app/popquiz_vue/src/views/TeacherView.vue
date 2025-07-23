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
      <!-- 文件上传区域 -->
      <el-main class="wrapper" style="margin-left: auto; margin-right: auto; width: 500px;">
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span style="font-size: 18px; font-weight: 600;">演讲者文件上传</span>
          </div>
          <el-row>
            <el-col :span="24">
              <input type="file" ref="fileInput" @change="handleFileChange" accept=".txt,.pdf" />
              <el-button type="primary" @click="submitFile" style="margin-top: 10px;">提交</el-button>
            </el-col>
          </el-row>
        </el-card>
      </el-main>

      <!-- 题目内容 -->
      <el-row>
        <el-col :span="24">
          <el-card class="question-card">
            <div class="question-text"><span>题目:</span>{{ questionText }}</div>

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
      errorRate: 21,

      // 存储用户选择的文件
      selectedFile: null
    };
  },
  computed: {
    // 根据正确答案选项计算显示文本
    correctAnswerText() {
      switch (this.correctAnswer) {
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
        console.log('退出登录');
      } else if (command === 'profile') {
        console.log('查看个人信息');
      }
    },
    // 新增：处理文件选取事件
    handleFileChange(event) {
      this.selectedFile = event.target.files[0];
    },
    // 新增：模拟文件上传
    submitFile() {
      if (!this.selectedFile) {
        alert("请选择一个文件");
        return;
      }
      // 模拟文件上传过程（实际上这里应该是向后端API发起请求）
      setTimeout(() => {
        console.log(`文件"${this.selectedFile.name}"已成功上传`);
        // 清除已选文件
        this.$refs.fileInput.value = '';
        this.selectedFile = null;
      }, 1000); // 延迟1秒以模拟网络延迟
    }
  }
};
</script>

<style>
/* 全局字体和基础样式 */
.app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f5f7fa;
}

/* 导航栏样式 */
.navbar {
  background: linear-gradient(135deg, #6A82FB 0%, #FC5C7D 100%);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  z-index: 999;
}

.left, .right {
  display: flex;
  align-items: center;
}

.avatar-btn {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.25);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  margin-right: 20px;
  transition: background 0.3s ease;
}

.avatar-btn img {
  width: 24px;
  height: 24px;
}

.avatar-btn:hover {
  background: rgba(255, 255, 255, 0.4);
}

h3 {
  font-size: 20px;
  font-weight: 600;
  margin: 0;
}

.right span {
  font-size: 16px;
  font-weight: 500;
  color: #fff;
}

/* 主内容区域 */
.wrapper {
  padding: 5px;
  flex: 1;
  overflow-y: auto;
}

/* 卡片基础样式 */
.box-card {
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  margin-bottom: 20px;
  background-color: #ffffff;
  transition: box-shadow 0.3s ease;
}

.box-card:hover {
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

/* 文件上传区域标题 */
.box-card .el-card__header {
  background-color: #f9f9f9;
  font-size: 18px;
  font-weight: 600;
  color: #333;
  border-bottom: 1px solid #ebeef5;
}

/* 文件输入区域 */
input[type="file"] {
  border: 1px solid #dcdfe6;
  border-radius: 6px;
  padding: 10px;
  width: 100%;
  font-size: 14px;
  margin-bottom: 10px;
  transition: border-color 0.3s ease;
}

input[type="file"]:focus {
  border-color: #6A82FB;
  outline: none;
}

/* 题目卡片样式 */
.question-card {
  margin-bottom: 20px;
}

.question-text {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 15px;
  color: #333;
}

.options {
  margin-bottom: 15px;
}

/* 选项卡片样式 */
.options .el-card {
  border-radius: 8px;
  border: 1px solid #e4e7ed;
  margin-bottom: 10px;
  padding: 12px;
  background-color: #fafafa;
  transition: all 0.3s ease;
}

.options .el-card:hover {
  background-color: #f0f0f0;
  transform: translateX(2px);
}

/* 正确答案样式 */
.correct-option {
  border-color: #67C23A !important;
  background-color: #F0F9EB !important;
}

/* 正确答案显示区域 */
.answer-row {
  margin-top: 15px;
  padding: 10px;
  background-color: #ecf5ff;
  border-radius: 8px;
}

.answer-label {
  font-weight: 600;
  margin-right: 10px;
  color: #1a73e8;
}

.correct-answer {
  color: #1a73e8;
  font-weight: 600;
}

/* 统计信息卡片 */
.statistics {
  margin-top: 20px;
}

.stat-card {
  border-radius: 10px;
  text-align: center;
  background-color: #ffffff;
  border: 1px solid #ebeef5;
  padding: 15px;
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
}

.stat-title {
  font-size: 16px;
  color: #606266;
  margin-bottom: 10px;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}
</style>