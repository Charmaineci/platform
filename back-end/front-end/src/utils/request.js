import axios from 'axios'
import router from '@/router'
import { Message } from 'element-ui'

// 创建axios实例
const service = axios.create({
  baseURL: 'http://127.0.0.1:5003',
  timeout: 5000
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers['Authorization'] = 'Bearer ' + token
    }
    return config
  },
  error => {
    console.error('Request error:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  response => {
    return response
  },
  error => {
    if (error.response) {
      switch (error.response.status) {
        case 401:
          Message.error('登录已过期，请重新登录')
          localStorage.removeItem('token')
          localStorage.removeItem('user')
          router.push('/login')
          break
        default:
          Message.error(error.response.data.message || '请求失败')
      }
    } else {
      Message.error('网络错误，请稍后重试')
    }
    return Promise.reject(error)
  }
)

export default service