<template>
  <div class="main">
    <div class="login">
      <h2>微课堂 - 登录</h2>
      <el-form :model="user" class="user_form" :rules="formRules" ref="userFormRef">
        <el-form-item prop="identity">
          <label for="identity" class="el-form-item__label">身份</label>
          <el-select v-model="user.identity" id="identity" placeholder="请选择身份">
            <el-option label="学生" value="student"></el-option>
            <el-option label="老师" value="teacher"></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item prop="name">
          <label for="name" class="el-form-item__label">用户名</label>
          <el-input v-model="user.name" id="name" placeholder="请输入用户名" :prefix-icon="User" />
        </el-form-item>
        
        <el-form-item prop="password">
          <label for="password" class="el-form-item__label">密码</label>
          <el-input 
            v-model="user.password" id="password" placeholder="请输入密码" :prefix-icon="Lock"/>
        </el-form-item>
        
        <el-form-item class="btns">
          <el-button type="primary" @click="handleLogin">登录</el-button>
          <el-button type="success" @click="handleRegister">注册</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { Lock, User } from '@element-plus/icons-vue';
import { useRouter } from 'vue-router';
import api from '../api/index.js';

// 表单数据
const user = reactive({
  identity: 'student',
  name: '',
  password: ''
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
  password: [
    { required: true, message: '密码不能为空', trigger: 'blur' },
    { min: 6, max: 18, message: '密码长度在6到18个字符', trigger: 'blur' }
  ]
});

const userFormRef = ref(null);

// 路由实例
const router = useRouter();

// 登录处理
const handleLogin = () => {
  userFormRef.value.validate((valid) => {
    if (valid) {
      api.getLogin(user)
        .then(() => {
          router.push('/');
        })
        .catch((error) => {
          console.error('登录失败:', error);
          // 可以在这里添加更多的错误处理逻辑，例如显示错误信息给用户
          alert('登录失败，请检查用户名和密码是否正确。');
        });
    } else {
      console.log('表单验证失败');
      alert('表单验证失败，请检查输入信息。');
    }
  });
};

// 注册处理
const handleRegister = () => {
  router.push('/register');
};
</script>

<style scoped>
.main {
  font-family: "Segoe UI", sans-serif;
  background: linear-gradient(to right, #74ebd5, #ACB6E5);
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  margin: 0;
}

.login {
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

.el-button--success {
  background-color: #aaa;
  border-color: #aaa;
}

.el-button--success:hover {
  background-color: #888;
  border-color: #888;
}
</style>
