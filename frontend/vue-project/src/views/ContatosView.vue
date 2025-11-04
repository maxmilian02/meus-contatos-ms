<template>
  <div class="min-h-screen bg-light-background dark:bg-dark-background">
    <!-- Header Fixo -->
    <header class="bg-light-card dark:bg-dark-card shadow-sm sticky top-0 z-20">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3 flex justify-between items-center">
        <!-- LOGO ATUALIZADO AQUI -->
        <a href="https://conectasuite.com/" target="_blank" class="flex items-center">
          <img 
            src="https://conectasuite.com/wp-content/uploads/2024/08/conecta-suite-logo.svg" 
            alt="Conecta Suite Logo" 
            class="h-9 w-auto dark:invert"
          >
        </a>
        <div class="flex items-center gap-2 sm:gap-3">
          <LanguageToggle />
          <ThemeToggle />
          <button @click="auth.logout" class="btn btn-danger !p-2" :title="$t('logout_button')">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg>
          </button>
        </div>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <transition name="slide-fade" mode="out-in">
        <!-- ############################# -->
        <!-- ## VISÃO DE LISTA DE DOMÍNIOS ## -->
        <!-- ############################# -->
        <div v-if="!selectedDomain">
          <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
            <div>
              <h2 class="font-display text-2xl font-bold text-light-text-primary dark:text-dark-text-primary">{{ $t('contacts_title') }}</h2>
              <p v-if="!loading" class="text-sm text-light-text-secondary dark:text-dark-text-secondary mt-1">{{ $t('domains_found', Object.keys(grouped).length) }}</p>
            </div>
            <div class="flex items-center gap-2" v-if="!loading && Object.keys(grouped).length > 0">
              <button @click="toggleLayout" class="btn btn-secondary !p-2" :title="$t('toggle_layout')">
                <IconGrid v-if="layout === 'list'" />
                <IconList v-else />
              </button>
              <div class="relative">
                <button @click="exportMenuOpen = !exportMenuOpen" class="btn btn-secondary !py-2 !px-3">{{ $t('export') }}</button>
                <transition name="fade">
                  <div v-if="exportMenuOpen" class="absolute right-0 mt-2 w-48 bg-light-card dark:bg-dark-card rounded-md shadow-lg border border-light-border dark:border-dark-border z-10">
                    <a @click="runExport('csv')" class="export-link">CSV</a>
                    <a @click="runExport('json')" class="export-link">JSON</a>
                    <a @click="runExport('excel')" class="export-link border-none">Excel (.xlsx)</a>
                  </div>
                </transition>
              </div>
            </div>
          </div>
          
          <div v-if="loading" class="text-center py-20 text-light-text-secondary dark:text-dark-text-secondary animate-fade-in-up">{{ $t('loading_contacts') }}</div>
          <div v-else-if="error" class="card text-center p-8 border-danger/50 animate-fade-in-up">{{ error }}</div>
          <div v-else-if="Object.keys(grouped).length === 0" class="card text-center p-12 animate-fade-in-up">{{ $t('empty_state_title') }}</div>

          <transition-group v-else :tag="layout === 'grid' ? 'div' : 'ul'" :class="layoutWrapperClass" name="layout-item">
            <li v-for="(emails, domain) in sortedDomains" :key="domain" :class="layoutItemClass">
              <!-- Layout de Lista -->
              <div v-if="layout === 'list'" class="flex w-full items-start gap-4 p-4">
                <div @click="selectDomain(domain)" class="w-1/3 cursor-pointer py-1">
                  <h3 class="font-display font-bold text-brand-secondary dark:text-brand-primary truncate">{{ domain }}</h3>
                  <p class="text-sm text-light-text-secondary dark:text-dark-text-secondary">{{ $t('contacts_found', emails.length) }}</p>
                </div>
                <div class="w-2/3 border-l border-light-border dark:border-dark-border pl-4">
                  <ul class="space-y-1">
                    <li v-for="email in emails.slice(0, expanded[domain] ? emails.length : 3)" :key="email" class="text-sm text-light-text-secondary dark:text-dark-text-secondary truncate">
                      {{ email }}
                    </li>
                  </ul>
                  <button v-if="emails.length > 3" @click.stop="expanded[domain] = !expanded[domain]" class="text-brand-accent font-semibold text-xs mt-2">
                    {{ expanded[domain] ? $t('see_less') : $t('see_more') }}
                  </button>
                </div>
              </div>
              <!-- Layout de Grid -->
              <div v-else @click="selectDomain(domain)" class="cursor-pointer p-5 flex flex-col h-full">
                <div class="flex justify-between items-baseline mb-3">
                  <h3 class="font-display font-bold text-lg text-brand-secondary dark:text-brand-primary truncate pr-2">{{ domain }}</h3>
                  <span class="text-sm font-semibold bg-light-background dark:bg-dark-background px-2 py-0.5 rounded-full">{{ emails.length }}</span>
                </div>
                <ul class="space-y-1 overflow-hidden flex-grow">
                  <li v-for="email in emails.slice(0, 3)" :key="email" class="text-sm text-light-text-secondary dark:text-dark-text-secondary truncate">
                    {{ email }}
                  </li>
                </ul>
                <div v-if="emails.length > 3" class="text-brand-accent font-semibold text-xs mt-3 pt-3 border-t border-light-border dark:border-dark-border">
                  {{ $t('and_more', { count: emails.length - 3 }) }}
                </div>
              </div>
            </li>
          </transition-group>
        </div>
        
        <!-- ############################ -->
        <!-- ## VISÃO DETALHADA DO DOMÍNIO ## -->
        <!-- ############################ -->
        <div v-else>
            <button @click="selectedDomain = null" class="btn btn-secondary mb-6">&larr; {{ $t('back_to_domains') }}</button>
            <div class="card p-5 animate-fade-in">
              <div class="flex flex-col md:flex-row gap-4 justify-between items-center mb-4 pb-4 border-b border-light-border dark:border-dark-border">
                <h3 class="font-display text-xl font-bold text-brand-secondary dark:text-brand-primary">{{ selectedDomain }}</h3>
                <div class="flex gap-2 w-full md:w-auto">
                    <input type="text" v-model="searchQuery" :placeholder="$t('search_placeholder')" class="w-full bg-light-background dark:bg-dark-background border-light-border dark:border-dark-border rounded-md px-3 py-2 text-sm focus:ring-brand-accent focus:border-brand-accent">
                </div>
              </div>
              
              <ul v-if="filteredEmails.length > 0" class="space-y-1">
                  <li v-for="email in filteredEmails" :key="email" class="flex justify-between items-center p-2.5 rounded-md hover:bg-light-background dark:hover:bg-dark-background group">
                      <span class="truncate text-light-text-secondary dark:text-dark-text-secondary group-hover:text-light-text-primary dark:group-hover:text-dark-text-primary">{{ email }}</span>
                      <div class="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                          <button @click="copyEmail(email)" class="btn btn-secondary !p-2" :title="$t('copy_email')">
                            <svg class="w-4 h-4" viewBox="0 0 20 20" fill="currentColor"><path d="M7 3a1 1 0 000 2h6a1 1 0 100-2H7zM4 7a1 1 0 011-1h10a1 1 0 110 2H5a1 1 0 01-1-1zM5 11a1 1 0 100 2h4a1 1 0 100-2H5z"></path><path fill-rule="evenodd" d="M2 5a2 2 0 012-2h12a2 2 0 012 2v10a2 2 0 01-2 2H4a2 2 0 01-2-2V5zm2-1a1 1 0 00-1 1v10a1 1 0 001 1h12a1 1 0 001-1V5a1 1 0 00-1-1H4z" clip-rule="evenodd"></path></svg>
                          </button>
                          <a :href="`mailto:${email}`" class="btn btn-secondary !p-2" :title="$t('send_email')">
                            <svg class="w-4 h-4" viewBox="0 0 20 20" fill="currentColor"><path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"></path><path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"></path></svg>
                          </a>
                      </div>
                  </li>
              </ul>
              <p v-else class="text-center py-8 text-light-text-secondary dark:text-dark-text-secondary">{{ $t('no_results') }}</p>
            </div>
            
            <div v-if="showCopyNotification" class="fixed bottom-10 left-1/2 -translate-x-1/2 bg-brand-secondary text-white px-5 py-2 rounded-full shadow-lg flex items-center gap-2 animate-fade-in-up">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
              <span>{{ $t('copied') }}</span>
            </div>
        </div>
      </transition>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { useExport } from '@/composables/useExport';
import api from '@/services/api';

// Component Imports
import ThemeToggle from '@/components/ThemeToggle.vue';
import LanguageToggle from '@/components/LanguageToggle.vue';
import IconGrid from '@/components/icons/IconGrid.vue';
import IconList from '@/components/icons/IconList.vue';

// Setup Stores and Utils
const auth = useAuthStore();
const { t } = useI18n();
const router = useRouter();

// Local UI and Data State
const loading = ref(true);
const error = ref(null);
const grouped = ref({});
const selectedDomain = ref(null);
const searchQuery = ref('');
const showCopyNotification = ref(false);
const expanded = reactive({});
const layout = ref('list');
const exportMenuOpen = ref(false);

const { exportToCsv, exportToJson, exportToExcel } = useExport(grouped);

// Computed Properties
const sortedDomains = computed(() => {
    return Object.entries(grouped.value)
        .sort((a, b) => b[1].length - a[1].length)
        .reduce((obj, [key, value]) => ({ ...obj, [key]: value }), {});
});

const filteredEmails = computed(() => {
  if (!selectedDomain.value) return [];
  let emails = grouped.value[selectedDomain.value] || [];
  if (searchQuery.value) {
    emails = emails.filter(email => email.toLowerCase().includes(searchQuery.value.toLowerCase()));
  }
  return emails.sort((a, b) => a.localeCompare(b));
});

const layoutWrapperClass = computed(() => ({
  'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5': layout.value === 'grid',
  'space-y-3': layout.value === 'list'
}));

const layoutItemClass = computed(() => ({
  'card rounded-lg flex flex-col transition-all duration-300': true,
  'hover:shadow-xl hover:-translate-y-1': layout.value === 'grid',
  'hover:shadow-md hover:border-brand-primary/50': layout.value === 'list',
}));

// Methods
function toggleLayout() {
  layout.value = layout.value === 'grid' ? 'list' : 'grid';
}

function runExport(format) {
  switch (format) {
    case 'csv': exportToCsv(); break;
    case 'json': exportToJson(); break;
    case 'excel': exportToExcel(); break;
  }
  exportMenuOpen.value = false;
}

function selectDomain(domain) {
  selectedDomain.value = domain;
  searchQuery.value = '';
}

function copyEmail(email) {
  navigator.clipboard.writeText(email);
  showCopyNotification.value = true;
  setTimeout(() => showCopyNotification.value = false, 2000);
}

async function loadContacts() {
    loading.value = true;
    error.value = null;
    try {
        const res = await api.get('/contacts');
        grouped.value = res.data;
    } catch (err) {
        if (err.response?.status === 401) {
            auth.logout();
        } else {
            error.value = err.response?.data?.details || t('error_loading_default');
        }
    } finally {
        loading.value = false;
    }
}

// Lifecycle Hook
onMounted(loadContacts);
</script>

<style scoped>
.export-link {
  @apply block w-full text-left px-4 py-2 text-sm text-light-text-primary dark:text-dark-text-primary hover:bg-light-background dark:hover:bg-dark-background cursor-pointer border-b border-light-border dark:border-dark-border;
}
.layout-item-move, .layout-item-enter-active, .layout-item-leave-active {
  transition: all 0.5s cubic-bezier(0.55, 0, 0.1, 1);
}
.layout-item-enter-from, .layout-item-leave-to {
  opacity: 0;
  transform: scale(0.95) translateY(20px);
}
.slide-fade-enter-active, .slide-fade-leave-active {
  transition: all 0.3s ease-out;
}
.slide-fade-enter-from, .slide-fade-leave-to {
  transform: translateY(10px);
  opacity: 0;
}
</style>```
