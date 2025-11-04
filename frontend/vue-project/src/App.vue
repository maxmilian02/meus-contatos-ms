<template>
  <div id="app" class="min-h-screen">
    <!-- Loading state -->
    <div v-if="auth.isLoading" class="flex items-center justify-center min-h-screen bg-dark-purple">
      <div class="text-center">
        <div class="inline-block">
          <svg class="animate-spin h-12 w-12 text-magenta" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </div>
        <p class="mt-4 text-text-muted text-lg">Carregando...</p>
      </div>
    </div>

    <!-- Main content -->
    <router-view v-else v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>

    <!-- Error toast (se necessário) -->
    <transition name="slide-down">
      <div v-if="auth.error" class="fixed top-4 right-4 z-50 max-w-md">
        <div class="bg-red-500/90 backdrop-blur-sm text-white px-6 py-4 rounded-lg shadow-lg flex items-center gap-3">
          <svg class="w-6 h-6 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <p class="flex-1">{{ auth.error }}</p>
          <button @click="auth.clearError" class="text-white/80 hover:text-white">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { onMounted, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

// Verifica autenticação ao montar
onMounted(async () => {
  await auth.checkAuthStatus()
})

// Auto-hide error after 5 seconds
watch(() => auth.error, (newError) => {
  if (newError) {
    setTimeout(() => {
      auth.clearError()
    }, 5000)
  }
})
</script>

<style scoped>
/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s ease;
}

.slide-down-enter-from {
  transform: translateY(-100%);
  opacity: 0;
}

.slide-down-leave-to {
  opacity: 0;
}
</style>