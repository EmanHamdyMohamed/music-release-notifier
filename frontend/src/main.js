import { createApp } from 'vue'
import './style.css'
import './assets/main.css'
import App from './App.vue'
import Vue3Toastify from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

createApp(App).use(Vue3Toastify).mount('#app')
