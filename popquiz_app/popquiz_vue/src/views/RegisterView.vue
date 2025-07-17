<template>
  <div class="main">
    <div class="register">
      <h2>微课堂 - 注册</h2>
      <el-form :model="formData" class="user_form" :rules="formRules" ref="registerFormRef">
        <el-form-item prop="identity">
          <label for="identity" class="el-form-item__label">身份</label>
          <el-select v-model="formData.identity" id="identity" placeholder="请选择身份">
            <el-option label="学生" value="student"></el-option>
            <el-option label="老师" value="teacher"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item prop="name">
          <label for="name" class="el-form-item__label">用户名</label>
          <el-input 
            v-model="formData.name" 
            id="name" 
            placeholder="请输入用户名"
            :prefix-icon="User"
          />
        </el-form-item>

      <el-form-item prop="pwd">
          <label for="pwd" class="el-form-item__label">密码</label>
            <el-input 
            v-model="formData.pwd" 
            id="pwd" 
            placeholder="请输入密码"
            :prefix-icon="Lock"
            type="pwd"
            show-password
            />
        </el-form-item>

        <el-form-item prop="real_pwd">
          <label for="real_pwd" class="el-form-item__label">确认密码</label>
          <el-input 
            v-model="formData.real_pwd" 
            id="real_pwd" 
            placeholder="请再次输入密码"
            :prefix-icon="Lock"
            type="real_pwd"
            show-password
          />
        </el-form-item>

       

        <el-form-item class="btns">
          <el-button type="primary" @click="handleRegister(registerFormRef)">注册</el-button>
          <el-button type="default" @click="handleBack">返回登录</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { Lock, User, Idcard } from '@element-plus/icons-vue';
import { useRouter } from 'vue-router';
import api from '../api/index.js';

// 表单数据
const formData = reactive({
  identity: 'student',
  name: '',
  pwd: '',
  real_pwd: ''
});

// 表单验证规则
const formRules = reactive({
  identity: [
    { required: true, message: '请选择身份', trigger: 'change' }
  ],
  name: [
    { required: true, message: '用户名不能为空', trigger: 'blur' },
    { min: 1, max: 20, message: '用户名长度在1到20个字符', trigger: 'blur' }
  ],
  real_pwd: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { min: 6, max: 18, message: '密码长度在6到18个字符', trigger: 'blur' }
  ],
  pwd: [
    { required: true, message: '密码不能为空', trigger: 'blur' },
    { min: 6, max: 18, message: '密码长度在6到18个字符', trigger: 'blur' }
  ]
});

const registerFormRef = ref(null);
const router = useRouter();

// 注册处理
const handleRegister = (formRef) => {
  formRef.validate((valid) => {
    if (valid) {
      api.getRegister(formData)
        .then(res => {
          if(res.data.status  === 200)
        {
          ElMessage({
            message: res.data.msg,
            type: 'success',
           })
          router.push('/login');
        }
        if(res.data.status === 400)
        {
          ElMessage.error(res.data.msg);
        }
        })
        // .catch((error) => {
        //   console.error('注册失败:', error);
        //   alert(error.msg || '注册失败，请检查输入信息。');
        // });
    } else {
      console.log('注册失败');
      alert('请检查信息是否完整。');
    }
  });
};

// 返回登录页
const handleBack = () => {
  router.push('/login');
};
</script>

<style scoped>
.main {       
  font-family: "Segoe UI", sans-serif;
  background: linear-gradient(to right, #ffecd2, #fcb69f);
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  margin: 0;
}

.register {
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  width: 300px;
}

h2 {
  text-align: center;
  margin-bottom: 24px;
  color: #333;
}

.user_form {
  padding: 0;
}

.btns {
  display: flex;
  justify-content: space-between;
}

.btns button {
  flex: 1;
  margin: 0 4px;
}

/* 适配Element UI组件的样式 */
.el-form-item {
  margin-bottom: 16px;
}

.el-input__inner, .el-select .el-input__inner {
  padding: 8px;
  border-radius: 6px;
}

.el-form-item__label {
  font-weight: 500;
  margin-bottom: 4px;
  display: block;
}

.el-button {
  padding: 10px;
  border-radius: 6px;
  font-weight: bold;
}

.el-button--primary {
  background-color: #4e9af1;
  border-color: #4e9af1;
}

.el-button--primary:hover {
  background-color: #387cd7;
  border-color: #387cd7;
}

.el-button--default {
  background-color: #f0f2f5;
  border-color: #f0f2f5;
}

.el-button--default:hover {
  background-color: #e5e6eb;
  border-color: #e5e6eb;
}
</style>
