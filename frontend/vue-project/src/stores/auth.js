import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  // State
  const isAuthenticated = ref(false)
  const isLoading = ref(true)
  const user = ref(null)
  const error = ref(null)

  // Getters
  const isReady = computed(() => !isLoading.value)

  // Actions
  async function checkAuthStatus() {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await api.get('/auth/status')
      isAuthenticated.value = response.data.is_authenticated
      
      if (isAuthenticated.value && response.data.user) {
        user.value = response.data.user
      }
      
      return isAuthenticated.value
    } catch (err) {
      console.error('Erro ao verificar autenticação:', err)
      isAuthenticated.value = false
      user.value = null
      error.value = err.response?.data?.message || 'Erro ao verificar autenticação'
      return false
    } finally {
      isLoading.value = false
    }
  }

  function login() {
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:5000'
    window.location.href = `${apiUrl}/auth/login`
  }

  function logout() {
    isAuthenticated.value = false
    user.value = null
    error.value = null
    
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:5000'
    window.location.href = `${apiUrl}/auth/logout`
  }

  function clearError() {
    error.value = null
  }

  return {
    // State
    isAuthenticated,
    isLoading,
    user,
    error,
    // Getters
    isReady,
    // Actions
    checkAuthStatus,
    login,
    logout,
    clearError
  }
})