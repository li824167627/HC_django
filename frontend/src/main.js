import Vue from 'vue'
import App from './App'
import router from './router'
import ElementUI from 'element-ui'
import VueResource from 'vue-resource'
import 'element-ui/lib/theme-chalk/index.css'
import axios from 'axios'


// 将API方法绑定到全局
Vue.prototype.$axios = axios

// 配置全局域名
axios.defaults.baseURL = "http://10.100.19.228:8000";

Vue.use(ElementUI)
Vue.use(VueResource)

Vue.config.productionTip = false

/* eslint-disable no-new */

new Vue({
  el: '#app',
  router,
  render: h => h(App)
})
