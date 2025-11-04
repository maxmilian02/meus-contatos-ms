import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createI18n } from 'vue-i18n'

import App from './App.vue'
import router from './router'
import messages from './i18n/messages'
import './assets/main.css'


// Configuração do i18n
const i18n = createI18n({
  legacy: false,
  locale: localStorage.getItem('locale') || 'pt',
  fallbackLocale: 'en',
  messages,
  globalInjection: true,
  missingWarn: false,
  fallbackWarn: false
})

// Criar aplicação
const app = createApp(App)

// Criar e configurar Pinia
const pinia = createPinia()

// Usar plugins na ordem correta
app.use(pinia)
app.use(router)
app.use(i18n)

// Error handler global
app.config.errorHandler = (err, instance, info) => {
  console.error('Global error:', err)
  console.error('Error info:', info)
}

// Warning handler
app.config.warnHandler = (msg, instance, trace) => {
  console.warn('Warning:', msg)
  console.warn('Trace:', trace)
}

// Montar aplicação
app.mount('#app')

console.log('🚀 Aplicação iniciada com sucesso!')