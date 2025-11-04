import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ContatosView from '../views/ContatosView.vue'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/contatos',
      name: 'contatos',
      component: ContatosView,
      meta: { requiresAuth: true }
    }
  ]
})

// Guard de navegação
router.beforeEach(async (to, from, next) => {
  const auth = useAuthStore()
  
  if (to.meta.requiresAuth) {
    // Se ainda não verificou o status, verifica
    if (auth.isLoading) {
      await auth.checkAuthStatus()
    }
    
    if (auth.isAuthenticated) {
      next()
    } else {
      // Redireciona para login do backend
      window.location.href = `${import.meta.env.VITE_API_URL || 'http://localhost:5000'}/auth/login`
    }
  } else {
    next()
  }
})

export default router