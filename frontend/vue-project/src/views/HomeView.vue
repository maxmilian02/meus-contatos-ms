<template>
  <div class="min-h-screen flex flex-col items-center justify-center p-4">
    <!-- Controles no canto superior direito -->
    <div class="absolute top-6 right-6 flex gap-2">
      <LanguageToggle />
      <ThemeToggle />
    </div>

    <div class="w-full max-w-sm text-center">
      <!-- Título e Subtítulo -->
      <div class="animate-fade-in-up">
        <h1 class="font-display text-3xl font-bold text-brand-secondary dark:text-brand-primary">
          {{ $t('title') }}
        </h1>
        <p class="text-light-text-secondary dark:text-dark-text-secondary mt-2">
          {{ $t('subtitle') }}
        </p>
      </div>
      
      <!-- Botão de Login -->
      <div class="mt-10 animate-fade-in-up" style="animation-delay: 0.2s;">
        <button 
          @click="auth.login" 
          class="w-full flex items-center justify-center px-4 py-2.5 border rounded-sm text-sm font-semibold transition-colors duration-200 
                 bg-white border-[#8C8C8C] text-[#5E5E5E] hover:bg-gray-50
                 dark:bg-[#2F2F2F] dark:border-[#2F2F2F] dark:text-white dark:hover:bg-[#444444]"
        >
          <MsLogoColor class="mr-2" />
          {{ $t('login_button') }}
        </button>
      </div>
    </div>

    <!-- Rodapé -->
    <footer class="absolute bottom-8 text-center text-sm text-light-text-secondary dark:text-dark-text-secondary animate-fade-in-up" style="animation-delay: 0.4s;">
      <p class="flex items-center gap-2">
        {{ $t('footer_project_for') }}
        <a href="https://conectasuite.com/" target="_blank">
          <img src="https://app.conectasuite.com/img/conecta_suite_full.4fd54047.png" alt="Conecta Suite Logo" class="h-5 w-auto opacity-70 dark:invert">
        </a>
      </p>
    </footer>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import MsLogoColor from '@/components/icons/MsLogoColor.vue'
import ThemeToggle from '@/components/ThemeToggle.vue'
import LanguageToggle from '@/components/LanguageToggle.vue'

const auth = useAuthStore()
</script>