import { createApp } from 'vue'
import App from './App.vue'

import Axios from 'axios'

// 解决跨域问题
Axios.defaults.baseURL = '/api'

var app = createApp(App);
app.mount('#app')
app.config.globalProperties.$axios = Axios  // 页面中直接用this.$axios即可使用

