import Vue from 'vue'
import App from './App.vue'
import VueRouter from 'vue-router'
import axios from 'axios'
import Element from 'element-ui'
import echarts from "echarts"

Vue.prototype.$echarts = echarts
import 'element-ui/lib/theme-chalk/index.css'
import './assets/style.css'
import './theme/index.css'

Vue.use(Element)
Vue.use(VueRouter)
Vue.prototype.$http = axios

// 引入你的路由配置（改成你的实际路径）
import router from './router'

Vue.config.productionTip = false

new Vue({
  el: '#app',
  router,
  render: h => h(App)
})
