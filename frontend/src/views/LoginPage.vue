<template>
  <div class="login-wrapper">
    <el-card class="login-card">
      <h2 class="login-title">登录</h2>

      <el-form :model="loginForm" @submit.prevent="handleLogin">
        <el-form-item label="用户名">
          <el-input v-model="loginForm.username" placeholder="请输入用户名" />
        </el-form-item>

        <el-form-item label="密码">
          <el-input v-model="loginForm.password" placeholder="请输入密码" show-password />
        </el-form-item>

        <el-button type="primary" @click="handleLogin" style="width: 100%">登录</el-button>
      </el-form>

    </el-card>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const loginForm = reactive({
  username: '',
  password: ''
})

const router = useRouter()

async function handleLogin() {
  try {
    const res = await axios.post('http://localhost:8000/login', new URLSearchParams({
      username: loginForm.username,
      password: loginForm.password
    }))

    const token = res.data.access_token
    localStorage.setItem('token', token)

    // 可选：你也可以记录用户名和角色
    const userInfo = await axios.get('http://localhost:8000/me', {
      headers: { Authorization: `Bearer ${token}` }
    })
    
    localStorage.setItem('username', userInfo.data.username)
    localStorage.setItem('role', userInfo.data.role)
    localStorage.setItem('family_id', userInfo.data.family_id)

    // 跳转到主页面
    router.push('/tasks')
  } catch (err) {
    console.error('登录失败:', err)
    ElMessage.error('用户名或密码错误')
  }
}
</script>

<style scoped>
.login-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: #ecf5ff;
}

.login-card {
  width: 400px;
  padding: 30px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.login-title {
  text-align: center;
  margin-bottom: 20px;
  font-weight: bold;
  color: #409EFF;
}

.hint {
  margin-top: 12px;
  font-size: 12px;
  color: #999;
  text-align: center;
}
</style>