<template>
  <div class="app">
    <!-- 导航栏 -->
    <el-header class="navbar">
      <div class="left">
        <el-dropdown @command="handleCommand">
          <div class="avatar-btn">
            <img src="https://cdn.jsdelivr.net/gh/placeholderuser/identicons/placeholder.png" alt="用户中心" />
          </div>
          <!-- <el-dropdown-menu slot="dropdown">
            <el-dropdown-item command="profile">个人信息</el-dropdown-item>
            <el-dropdown-item command="logout">退出登录</el-dropdown-item>
          </el-dropdown-menu> -->
        </el-dropdown>
        <h3 class="app-title">微课堂</h3>
        <h3 class="app-title2">欢迎回来,{{ teachername }}</h3>
      </div>
      <div class="right">
      <el-button @click="showUploadDialog" class="text-button" type="primary">上传课件</el-button>
      <el-button @click="showSecretDialog" class="text-button" type="primary">设置课堂码</el-button>
      <el-button class="text-button" type="primary" @click="returnlogin()">退出</el-button>
      </div>
    </el-header>

      <!-- 上传页面对话框 -->
      <el-dialog title="上传课件" v-model="uploadDialogVisible" width="30%">
      <div>
    <el-upload
  class="upload-demo"
  action=""
  :http-request="dummyRequest"
  :on-preview="handlePreview"
  :on-remove="handleRemove"
  :on-change="handleFileChange"  
  :before-remove="beforeRemove"
  :on-success="handleSuccess"
  :file-list="fileList"
  :limit="1"
  :auto-upload="false">
  <el-button size="small" type="primary">点击上传</el-button>
</el-upload>

    </div>
    <span slot="footer" class="dialog-footer">
      <el-button @click="uploadDialogVisible = false">取 消</el-button>
      <el-button  @click="handlefile">确 定</el-button>
    </span>
  </el-dialog>

    <!-- 输入暗号对话框 -->
    <el-dialog title="设置课堂码"v-model="secretDialogVisible"width="30%">
      <el-input
        v-model="classroom.classId"
        placeholder="请输入课堂码"
        show-password>
      </el-input>
      <span slot="footer" class="dialog-footer">
        <el-button @click="secretDialogVisible = false">取 消</el-button>
        <el-button @click="handleclass">确 认</el-button>
      </span>
    </el-dialog>

    <!-- 主内容区 -->
     <el-row :gutter="20" style="flex: 1;">
    <el-col :span="16">
      <el-main class="wrapper">
      <!-- 文件上传区域 -->
      <!-- <el-main class="wrapper" style="margin-left: auto; margin-right: auto; width: 500px;">
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
      </el-main> -->

      <!-- 题目内容 -->
      <el-row>
        <el-col :span="24">
          <el-card class="question-card">
            <div class="question-text">{{ questionData.question }}</div>

            <!-- 选项区域 -->
            <div class="options">
              <el-row :gutter="12">
                <el-col :span="24" v-for="(option, key) in questionData.options" :key="key">
                  <el-card :class="{'correct-option': key === questionData.answer}">
                    <div>{{ key }}: {{ option }}</div>
                  </el-card>
                </el-col>
              </el-row>
            </div>

            <!-- 正确答案 -->
            <el-row class="answer-row">
              <el-col :span="24">
                <span class="answer-label">正确答案：</span>
                <span class="correct-answer">{{ questionData.answer }}. {{ questionData.options[questionData.answer] }}</span>
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
    </el-col>
    <el-col :span="8">
    <el-main class="wrapper2">
      <el-card class="comment-card">
  <div slot="header" class="clearfix">
    <span style="font-size: 18px; font-weight: 600;">观众评论</span>
  </div>

  <div class="comment-list">
    <div class="comment-item" v-for="(comment, index) in commentList" :key="index">
      <div class="comment-user">{{ comment.username }}</div>
      <div class="comment-content">{{ comment.text}}</div>
    </div>
  </div>
</el-card>

    </el-main>
    </el-col>
    </el-row>
  </div>
</template>

<script>
import { ElMessage } from 'element-plus'
import api from '@/api/index.js'
//文件上传部分
// const uploadDialogVisible = ref(false)
// const fileList = ref([])

// // 替代默认上传行为（不触发 auto 上传）
// const dummyRequest = () => {}

// const handlefile = async () => {
//   if (fileList.value.length !== 1) {
//     ElMessage.warning('请上传且仅上传一个文件')
//     return
//   }

//   const file = fileList.value[0]
//   const filename = file.name.toLowerCase()
//   const formData = new FormData()
//   formData.append('file', file.raw)

//   try {
//     if (filename.endsWith('.pdf')) {
//       const res = await axios.post('/api/pdf_upload', formData)
//       ElMessage.success('PDF 上传成功')
//     } else if (filename.endsWith('.txt') || filename.endsWith('.text')) {
//       const res = await axios.post('/api/text_upload', formData)
//       ElMessage.success('Text 上传成功')
//     } else {
//       ElMessage.error('仅支持 PDF 或 TXT 文件上传')
//       return
//     }

//     uploadDialogVisible.value = false
//     fileList.value = []  // 清空文件列表
//   } catch (err) {
//     console.error('上传失败:', err)
//     ElMessage.error('上传失败')
//   }
// }
//文件上传部分
export default {
  data() {
    return {
      commentList: [

],

      // 题目数据
      teachername: localStorage.getItem('teachername') || '', 
      questionData: { question: '', options: { A: '', B: '', C: '', D: '' }, answer: '' },
      selectedOption: '',
      isSubmitted: false,
      isCorrect: false,
      commentContent: '',
      classroom: {
        name: localStorage.getItem('teachername') || '',
        classId: ''
      },
      fileList: [],
      // 统计数据
      answerCount: 219,
      correctRate: 79,
      errorRate: 21,

      // 存储用户选择的文件
      selectedFile: null,

      // 弹窗状态
      uploadDialogVisible: false,
      secretDialogVisible: false,
    };
  },
  computed: {
    correctAnswerText() {
      return this.questionData.options[this.questionData.answer] || ''
    }
  },
  //   mounted() {
  //   this.refreshQuestion();
  //   this.fetchComments();
  // },

  methods: {
    fetchComments() {
       api.getshowcomment(this.classroom)  // 调用后端接口
       .then(res=>{
        if(res.data.status==200){
         this.commentList = res.data.data;  // 获取到评论列表
        } else {
          console.error('评论加载失败');
        }
       })
        
    },

    //文件上传部分
    handleFileChange(file, fileList) {
  // 只保留最后一个
  this.fileList = [fileList[fileList.length - 1]];
},


  // 删除文件时触发
  handleRemove(file, fileList) {
    this.fileList = fileList
  },


  handlefile() {
  if (!this.fileList || this.fileList.length !== 1) {
    ElMessage.warning('请上传且仅上传一个文件');
    return;
  }

  const file = this.fileList[0];
  const filename = file.name.toLowerCase();
  const formData = new FormData();
  formData.append('file', file.raw);

  try {
    if (filename.endsWith('.pdf')) {
      api.uploadPDF(formData).then(() => {
        ElMessage.success('PDF 上传成功');
        this.uploadDialogVisible = false;
        this.fileList = [];
      });
    } else if (filename.endsWith('.txt') || filename.endsWith('.text')) {
      api.uploadText(formData).then(() => {
        ElMessage.success('文本上传成功');
        this.uploadDialogVisible = false;
        this.fileList = [];
      });
    } else {
      ElMessage.error('仅支持 PDF 或 TXT 文件上传');
    }
  } catch (err) {
    console.error('上传失败', err);
    ElMessage.error('上传失败');
  }
},


//文件上传部分
    //课堂码
    handleclass() {
    if (!this.classroom.classId.trim()) {
      ElMessage.warning('请输入课堂码')
      return
    }
    // 输入正确，弹窗关闭并提示成功
    api.getSetclass(this.classroom)
    .then(res => {
      if(res.data.status===200)
    {
        this.refreshQuestion();
      this.fetchComments();
      this.secretDialogVisible = false
      ElMessage.success(`课堂码已设置：${this.classroom.classId}`)
    }
    // else if(res.data.status===400)
    // ElMessage.success(`课堂码已存在，请重新设置`)
    // 
    }
    )
    
  },


    returnlogin() {
      this.$router.push('/login')  // 使用 this.$router 来跳转
    },

    // 显示上传文件对话框
    showUploadDialog() {
      this.uploadDialogVisible = true;
    },
    // 显示输入暗号对话框
    showSecretDialog() {
      this.secretDialogVisible = true;
    },
    
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
    },



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
.app-title {
  margin-left: 20px;
  font-size: 36px;
  font-weight: 500;
  color: #000;
}
.app-title2 {
  margin-left: 20px;
  font-size: 18px;
  font-weight: 500;
  color: #ffffff;
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
  padding: 40px;
  height: 100%;
  overflow-y: auto;
  overflow-x: hidden;
}
.wrapper2 {
  padding: 40px;
   height: 80%;
  overflow-y: auto;
  overflow-x: hidden;
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
  width: 100%;
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
.text-button {
  background: transparent !important;   /* 无背景 */
  border: none !important;              /* 无边框 */
  color: #fff !important;               /* 字体颜色（你导航栏是深色背景） */
  font-size: 16px;
  padding: 6px 12px;
  box-shadow: none !important;
  font-weight: 500;
  cursor: pointer;
}

/* ✅ 禁用悬浮变化 */
.text-button:hover,
.text-button:focus {
  background: transparent !important;
  color: #fff !important;
  box-shadow: none !important;
  border: none !important;
}
.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}
* {
  box-sizing: border-box;
  max-width: 100%;
}
.comment-card {
  height: 100%;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.comment-list {
  flex: 1;
  overflow-y: auto;
  max-height: 600px;
  padding-right: 5px;
}

.comment-item {
  background-color: #f4f6f9;
  border-radius: 8px;
  padding: 10px;
  margin-bottom: 10px;
  word-break: break-word;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.comment-user {
  font-weight: 600;
  font-size: 14px;
  color: #409EFF;
  margin-bottom: 5px;
}

.comment-content {
  font-size: 14px;
  color: #333;
}

</style>