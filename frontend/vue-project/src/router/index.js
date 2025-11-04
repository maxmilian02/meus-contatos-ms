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

// Guard de navegação para proteger a rota de contatos
router.beforeEach(async (to, from, next) => {
  const auth = useAuthStore()
  
  if (to.meta.requiresAuth) {
    // Sincroniza o estado de autenticação ANTES de decidir a rota
    if (auth.isAuthenticated === false && auth.isLoading === true) {
      await auth.checkAuthStatus()
    }
    
    if (auth.isAuthenticated) {
      next() // Se autenticado, prossiga para /contatos
    } else {
      next({ name: 'home' }) // Se não, volte para a tela de login
    }
  } else {
    next() // Para rotas públicas, sempre permitir
  }
})

export default router