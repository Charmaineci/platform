<template>
    <div class="login-container">
      <el-card class="login-card">
        <div slot="header" class="clearfix">
          <span>用户登录</span>
        </div>
        <el-form :model="loginForm" :rules="rules" ref="loginForm" label-width="80px">
          <el-form-item label="用户名" prop="username">
            <el-input v-model="loginForm.username" placeholder="请输入用户名"></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input type="password" v-model="loginForm.password" placeholder="请输入密码"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleLogin" :loading="loading">登录</el-button>
            <el-button @click="$router.push('/register')">注册账号</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    name: 'Login',
    data() {
      return {
        loginForm: {
          username: '',
          password: ''
        },
        loading: false,
        rules: {
          username: [
            { required: true, message: '请输入用户名', trigger: 'blur' }
          ],
          password: [
            { required: true, message: '请输入密码', trigger: 'blur' }
          ]
        }
      }
    },
    methods: {
      handleLogin() {
        this.$refs.loginForm.validate(async (valid) => {
          if (valid) {
            this.loading = true
            try {
              const response = await axios.post('http://127.0.0.1:5003/api/login', this.loginForm)
              if (response.data.status === 1) {
                // 保存token和用户信息
                localStorage.setItem('token', response.data.token)
                localStorage.setItem('user', JSON.stringify(response.data.user))
                this.$message.success('登录成功')
                
                // 获取重定向地址或默认跳转到主页
                const redirectPath = this.$route.query.redirect || '/home'
                this.$router.replace(redirectPath)
              } else {
                this.$message.error(response.data.message)
              }
            } catch (error) {
              this.$message.error('登录失败，请重试')
              console.error('Login error:', error)
            } finally {
              this.loading = false
            }
          }
        })
      }
    }
  }
  </script>
  
  <style scoped>
  .login-container {
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #f5f7fa;
  }
  
  .login-card {
    width: 400px;
  }
  
  .el-button {
    margin-right: 15px;
  }
  </style>