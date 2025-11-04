<template>
  <div class="min-h-screen bg-dark-purple">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      
      <!-- Header -->
      <header class="mb-8">
        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div>
            <h1 class="text-3xl sm:text-4xl font-bold text-text-light mb-2">
              {{ $t('title') }}
            </h1>
            <p class="text-text-muted">
              {{ Object.keys(grouped).length }} {{ Object.keys(grouped).length === 1 ? 'domínio encontrado' : 'domínios encontrados' }}
            </p>
          </div>

          <div class="flex flex-wrap gap-3">
            <button 
              @click="refresh" 
              :disabled="loading"
              class="btn btn-secondary flex items-center gap-2"
            >
              <svg 
                :class="{'animate-spin': loading}" 
                class="w-5 h-5" 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              <span class="hidden sm:inline">{{ loading ? 'Atualizando...' : 'Atualizar' }}</span>
            </button>

            <button 
              @click="auth.logout"
              class="btn bg-red-500/10 border border-red-500/30 text-red-400 hover:bg-red-500/20 hover:border-red-500/50 flex items-center gap-2"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              <span class="hidden sm:inline">{{ $t('logout') }}</span>
            </button>
          </div>
        </div>
      </header>

      <!-- Loading State -->
      <div v-if="loading" class="flex flex-col items-center justify-center py-20">
        <div class="relative">
          <div class="w-20 h-20 border-4 border-magenta/20 rounded-full"></div>
          <div class="absolute top-0 left-0 w-20 h-20 border-4 border-magenta border-t-transparent rounded-full animate-spin"></div>
        </div>
        <p class="mt-6 text-lg text-text-muted">Carregando seus contatos...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="card p-6 bg-red-500/5 border-red-500/20">
        <div class="flex items-start gap-4">
          <div class="flex-shrink-0">
            <svg class="w-6 h-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div class="flex-1">
            <h3 class="text-lg font-semibold text-red-400 mb-1">Erro ao carregar contatos</h3>
            <p class="text-red-300/80">{{ error }}</p>
            <button @click="refresh" class="mt-4 btn btn-secondary text-sm">
              Tentar novamente
            </button>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else-if="Object.keys(grouped).length === 0" class="card p-12 text-center">
        <div class="max-w-md mx-auto">
          <div class="w-24 h-24 mx-auto mb-6 bg-magenta/10 rounded-full flex items-center justify-center">
            <svg class="w-12 h-12 text-magenta" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
          </div>
          <h3 class="text-2xl font-bold text-text-light mb-2">{{ $t('no_contacts') }}</h3>
          <p class="text-text-muted mb-6">
            Parece que você ainda não tem contatos cadastrados na sua conta Microsoft.
          </p>
          <button @click="refresh" class="btn btn-primary">
            Verificar novamente
          </button>
        </div>
      </div>

      <!-- Contacts Grid -->
      <div v-else>
        <!-- Stats Cards -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
          <div class="card p-4 bg-magenta/5 border-magenta/20">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-text-muted text-sm">Total de Domínios</p>
                <p class="text-2xl font-bold text-text-light mt-1">{{ Object.keys(grouped).length }}</p>
              </div>
              <div class="w-12 h-12 bg-magenta/10 rounded-lg flex items-center justify-center">
                <svg class="w-6 h-6 text-magenta" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
                </svg>
              </div>
            </div>
          </div>

          <div class="card p-4 bg-purple-500/5 border-purple-500/20">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-text-muted text-sm">Total de Contatos</p>
                <p class="text-2xl font-bold text-text-light mt-1">{{ totalContacts }}</p>
              </div>
              <div class="w-12 h-12 bg-purple-500/10 rounded-lg flex items-center justify-center">
                <svg class="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
            </div>
          </div>

          <div class="card p-4 bg-blue-500/5 border-blue-500/20">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-text-muted text-sm">Maior Domínio</p>
                <p class="text-lg font-bold text-text-light mt-1 truncate">{{ largestDomain }}</p>
              </div>
              <div class="w-12 h-12 bg-blue-500/10 rounded-lg flex items-center justify-center">
                <svg class="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
                </svg>
              </div>
            </div>
          </div>
        </div>

        <!-- Domain Cards Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div 
            v-for="(emails, domain) in grouped" 
            :key="domain"
            class="card hover:scale-105 transition-transform duration-300 group"
          >
            <!-- Card Header -->
            <div class="p-5 bg-gradient-to-r from-magenta/10 to-purple-500/10 border-b border-border">
              <div class="flex items-start justify-between mb-2">
                <h2 class="font-bold text-lg text-text-light truncate flex-1 group-hover:text-magenta transition-colors">
                  {{ domain }}
                </h2>
                <span class="ml-2 px-2 py-1 bg-magenta/20 text-magenta text-xs font-semibold rounded-full">
                  {{ emails.length }}
                </span>
              </div>
              <p class="text-sm text-text-muted">
                {{ emails.length }} {{ emails.length === 1 ? 'contato' : 'contatos' }}
              </p>
            </div>

            <!-- Card Body -->
            <div class="p-4">
              <ul class="space-y-2 max-h-60 overflow-y-auto custom-scrollbar">
                <li 
                  v-for="email in emails" 
                  :key="email"
                  class="flex items-center gap-2 p-2 rounded-lg hover:bg-purple-hover/30 transition-colors group/item"
                >
                  <svg class="w-4 h-4 text-magenta flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207" />
                  </svg>
                  <span class="text-text-muted text-sm truncate flex-1 group-hover/item:text-text-light transition-colors">
                    {{ email }}
                  </span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '@/services/api'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const loading = ref(true)
const error = ref(null)
const grouped = ref({})

const totalContacts = computed(() => {
  return Object.values(grouped.value).reduce((sum, emails) => sum + emails.length, 0)
})

const largestDomain = computed(() => {
  if (Object.keys(grouped.value).length === 0) return '-'
  return Object.entries(grouped.value)
    .sort((a, b) => b[1].length - a[1].length)[0][0]
})

async function loadContacts() {
  loading.value = true
  error.value = null
  
  try {
    const res = await api.get('/contacts')
    grouped.value = res.data
  } catch (err) {
    console.error('Erro ao carregar contatos:', err)
    error.value = err.response?.data?.details || 'Falha ao carregar contatos. Verifique sua conexão.'
    
    if (err.response?.status === 401) {
      auth.logout()
    }
  } finally {
    loading.value = false
  }
}

function refresh() {
  loadContacts()
}

onMounted(() => {
  loadContacts()
})
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #3a2d56;
  border-radius: 3px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #e61e64;
}
</style>