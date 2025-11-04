// frontend/vue-project/vite.config.js

import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
// import tailwindcss from '@tailwindcss/vite' // <-- 1. REMOVA ou comente esta linha

export default defineConfig({
  plugins: [
    vue(),
    // tailwindcss(), // <-- 2. REMOVA ou comente esta linha
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
})