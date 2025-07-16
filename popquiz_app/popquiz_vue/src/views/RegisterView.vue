<template>
  <div class="register-container">
    <div class="register-form">
      <h2>微课堂 - 注册</h2>
      <div class="form-group">
        <label for="identity">身份</label>
        <select v-model="formData.identity" id="identity">
          <option value="student">学生</option>
          <option value="teacher">老师</option>
        </select>
      </div>

      <div class="form-group">
        <label for="userId">ID号</label>
        <input 
          type="text" 
          v-model="formData.userId" 
          id="userId" 
          placeholder="请输入ID号"
        >
      </div>

      <div class="form-group">
        <label for="nickname">昵称</label>
        <input 
          type="text" 
          v-model="formData.nickname" 
          id="nickname" 
          placeholder="请输入昵称"
        >
      </div>

      <div class="form-group">
        <label for="password">密码</label>
        <input 
          type="password" 
          v-model="formData.password" 
          id="password" 
          placeholder="请输入密码"
          show-password
        >
      </div>

      <button @click="handleRegister" class="register-btn">注册</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RegisterView',
  data() {
    return {
      formData: {
        identity: 'student',
        userId: '',
        nickname: '',
        password: ''
      }
    }
  },
  methods: {
    async handleRegister() {
      try {
        const response = await fetch('/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(this.formData)
        });
        
        if (response.ok) {
          alert("注册成功，请登录！");
          this.$router.push('/login');
        } else {
          const errorData = await response.json();
          alert(errorData.message || "注册失败，请检查填写信息。");
        }
      } catch (error) {
        console.error('注册请求出错:', error);
        alert("网络错误，请稍后再试。");
      }
    }
  }
}
</script>

<style scoped>
.register-container {       
  font-family: "Segoe UI", sans-serif;
  background: linear-gradient(to right, #ffecd2, #fcb69f);
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  margin: 0;
}

.register-form {
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

.form-group {
  margin-bottom: 16px;
}

label {
  display: block;
  margin-bottom: 4px;
  font-weight: 500;
}

input, select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 6px;
  box-sizing: border-box;
}

button {
  width: 100%;
  padding: 10px;
  border: none;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
  margin-top: 8px;
}

.register-btn {
  background-color: #f68084;
  color: white;
}

.register-btn:hover {
  background-color: #e45b5f;
}
</style>
    