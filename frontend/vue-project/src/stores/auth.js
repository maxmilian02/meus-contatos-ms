import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/services/api'
import router from '@/router'

export const useAuthStore = defineStore('auth', () => {
  const isAuthenticated = ref(false)
  const isLoading = ref(true) // Inicia como true para a verificação inicial
  const isLoggingOut = ref(false)
  const error = ref(null)

  async function checkAuthStatus() {
    isLoading.value = true
    try {
      const response = await api.get('/auth/status')
      isAuthenticated.value = response.data.is_authenticated
    } catch (err) {
      isAuthenticated.value = false
    } finally {
      isLoading.value = false
    }
  }

  function login() {
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:5000'
    window.location.href = `${apiUrl}/auth/login`
  }

  async function logout() {
    isLoggingOut.value = true
    try {
      await api.get('/auth/logout')
    } catch (err) {
      console.error('Erro no logout do backend:', err)
    } finally {
      isAuthenticated.value = false
      router.push('/')
      // Um pequeno delay para a transição ser percebida
      setTimeout(() => { isLoggingOut.value = false }, 300);
    }
  }
  
  return { isAuthenticated, isLoading, isLoggingOut, error, checkAuthStatus, login, logout }
})