import { createApp } from 'vue'
import App from './App.vue'
import { createPinia } from 'pinia'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

import router from './router'

const app = createApp(App)

const pinia = createPinia()   // ✅ 创建 Pinia 实例
app.use(pinia)                // ✅ 注册 Pinia 到 app

app.use(ElementPlus)
app.use(router)

app.mount('#app')