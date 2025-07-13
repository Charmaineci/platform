<template>
  <div id="app">
    <app-header></app-header>
    <router-view />  <!-- 通过路由展示 Login/Home/Register/Profile 等页面 -->
    <app-footer></app-footer>
  </div>
</template>

<script>
import Header from "./components/Header.vue"
import Footer from "./components/Footer.vue"

export default {
  name: "App",
  components: {
    "app-header": Header,
    "app-footer": Footer,
  },
}
</script>

<style scope="this api replaced by slot-scope in 2.5.0+">
</style>
