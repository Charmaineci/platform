<template>
    <div class="register-container">
      <el-card class="register-card">
        <div slot="header" class="clearfix">
          <span>用户注册</span>
        </div>
        <el-form :model="registerForm" :rules="rules" ref="registerForm" label-width="80px">
          <el-form-item label="用户名" prop="username">
            <el-input v-model="registerForm.username" placeholder="请输入用户名"></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input type="password" v-model="registerForm.password" placeholder="请输入密码"></el-input>
          </el-form-item>
          <el-form-item label="确认密码" prop="confirmPassword">
            <el-input type="password" v-model="registerForm.confirmPassword" placeholder="请确认密码"></el-input>
          </el-form-item>
          <el-form-item label="邮箱" prop="email">
            <el-input v-model="registerForm.email" placeholder="请输入邮箱"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleRegister" :loading="loading">注册</el-button>
            <el-button @click="$router.push('/login')">返回登录</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    name: 'Register',
    data() {
      // 自定义验证规则
      const validatePass2 = (rule, value, callback) => {
        if (value !== this.registerForm.password) {
          callback(new Error('两次输入密码不一致!'))
        } else {
          callback()
        }
      }
      return {
        registerForm: {
          username: '',
          password: '',
          confirmPassword: '',
          email: ''
        },
        loading: false,
        rules: {
          username: [
            { required: true, message: '请输入用户名', trigger: 'blur' },
            { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
          ],
          password: [
            { required: true, message: '请输入密码', trigger: 'blur' },
            { min: 6, message: '密码长度不能小于6位', trigger: 'blur' }
          ],
          confirmPassword: [
            { required: true, message: '请再次输入密码', trigger: 'blur' },
            { validator: validatePass2, trigger: 'blur' }
          ],
          email: [
            { required: true, message: '请输入邮箱地址', trigger: 'blur' },
            { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
          ]
        }
      }
    },
    methods: {
      handleRegister() {
        this.$refs.registerForm.validate(async (valid) => {
          if (valid) {
            this.loading = true
            try {
              const { confirmPassword, ...registerData } = this.registerForm
              const response = await axios.post('http://127.0.0.1:5003/api/register', registerData)
              if (response.data.status === 1) {
                this.$message.success('注册成功')
                this.$router.push('/login')
              } else {
                this.$message.error(response.data.message)
              }
            } catch (error) {
              this.$message.error('注册失败，请重试')
              console.error('Register error:', error)
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
  .register-container {
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #f5f7fa;
  }
  
  .register-card {
    width: 400px;
  }
  
  .el-button {
    margin-right: 15px;
  }
  </style>