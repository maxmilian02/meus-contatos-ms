<template>
  <div class="min-h-screen flex flex-col items-center justify-center p-4 relative overflow-hidden">
    <!-- Background gradient effect -->
    <div class="absolute inset-0 bg-gradient-to-br from-dark-purple via-purple-900/20 to-dark-purple"></div>
    <div class="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(230,30,100,0.1),transparent_50%)]"></div>
    
    <div class="relative z-10 w-full max-w-md">
      <!-- Logo/Header -->
      <div class="text-center mb-8 fade-in">
        <div class="inline-flex items-center justify-center w-20 h-20 bg-magenta/10 rounded-2xl mb-4 border border-magenta/20">
          <svg class="w-10 h-10 text-magenta" fill="currentColor" viewBox="0 0 24 24">
            <path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>
          </svg>
        </div>
        <h1 class="text-4xl font-bold text-text-light mb-2">
          {{ $t('title') }}
        </h1>
        <p class="text-text-muted text-lg">
          Organize seus contatos Microsoft por domínio
        </p>
      </div>

      <!-- Main Card -->
      <div class="card p-8 backdrop-blur-sm bg-card-bg/80 fade-in" style="animation-delay: 0.1s">
        <div class="space-y-6">
          <!-- Feature list -->
          <div class="space-y-4">
            <div class="flex items-start gap-3">
              <div class="flex-shrink-0 w-8 h-8 bg-magenta/10 rounded-lg flex items-center justify-center mt-0.5">
                <svg class="w-5 h-5 text-magenta" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <div>
                <h3 class="text-text-light font-semibold">Login Seguro</h3>
                <p class="text-text-muted text-sm">Autenticação via Microsoft OAuth2</p>
              </div>
            </div>

            <div class="flex items-start gap-3">
              <div class="flex-shrink-0 w-8 h-8 bg-magenta/10 rounded-lg flex items-center justify-center mt-0.5">
                <svg class="w-5 h-5 text-magenta" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
              </div>
              <div>
                <h3 class="text-text-light font-semibold">Organização Inteligente</h3>
                <p class="text-text-muted text-sm">Contatos agrupados automaticamente por domínio</p>
              </div>
            </div>

            <div class="flex items-start gap-3">
              <div class="flex-shrink-0 w-8 h-8 bg-magenta/10 rounded-lg flex items-center justify-center mt-0.5">
                <svg class="w-5 h-5 text-magenta" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <div>
                <h3 class="text-text-light font-semibold">Rápido e Eficiente</h3>
                <p class="text-text-muted text-sm">Interface moderna e responsiva</p>
              </div>
            </div>
          </div>

          <!-- Divider -->
          <div class="border-t border-border"></div>

          <!-- Action buttons -->
          <div class="space-y-3">
            <button 
              @click="auth.login" 
              class="btn btn-primary w-full group relative overflow-hidden"
            >
              <span class="relative z-10 flex items-center justify-center gap-2">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M11.5 22.5h-9V13h9v9.5zm-11-11h9V2h-9v9.5zm11 11h9V13h-9v9.5zm0-21v9.5h9V2h-9z"/>
                </svg>
                {{ $t('login') }}
              </span>
              <div class="absolute inset-0 bg-gradient-to-r from-pink-600 to-magenta opacity-0 group-hover:opacity-100 transition-opacity"></div>
            </button>

            <button 
              @click="toggleLng" 
              class="btn btn-secondary w-full flex items-center justify-center gap-2"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129" />
              </svg>
              {{ locale === 'pt' ? 'Português' : 'English' }}
            </button>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <footer class="mt-8 text-center fade-in" style="animation-delay: 0.2s">
        <p class="text-sm text-text-muted">
          Um projeto para <span class="text-magenta font-semibold">Conecta Suite</span>
        </p>
        <p class="text-xs text-text-muted mt-2">
          Desenvolvido com Vue 3, Flask e Microsoft Graph API
        </p>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'

const { locale } = useI18n()
const auth = useAuthStore()

const toggleLng = () => {
  const newLocale = locale.value === 'pt' ? 'en' : 'pt'
  locale.value = newLocale
  localStorage.setItem('locale', newLocale)
}
</script>

<style scoped>
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.fade-in {
  animation: fadeIn 0.6s ease-out forwards;
}
</style>