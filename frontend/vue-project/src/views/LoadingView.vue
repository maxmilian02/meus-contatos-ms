<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-light-background dark:bg-dark-background">
    <svg class="animate-spin h-12 w-12 text-brand-accent" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
    </svg>
    <p class="mt-4 text-lg text-light-text-secondary dark:text-dark-text-secondary animate-pulse">
      {{ statusText }}
    </p>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useContactsStore } from '@/stores/contacts';
import { useAuthStore } from '@/stores/auth';
import { useI18n } from 'vue-i18n';

const router = useRouter();
const authStore = useAuthStore();
const contactsStore = useContactsStore();
const { t } = useI18n();

const statusText = ref(t('authenticating')); // Texto inicial

onMounted(async () => {
  // 1. Primeiro, confirma o status da autenticação com o backend
  await authStore.checkAuthStatus();

  // 2. Se a autenticação for bem-sucedida...
  if (authStore.isAuthenticated) {
    statusText.value = t('loading_contacts'); // Atualiza o texto para o usuário
    
    // 3. ...busca os contatos.
    const success = await contactsStore.fetchContacts();
    
    if (success) {
      // 4a. Se a busca for bem-sucedida, vai para a tela de contatos.
      router.push('/contatos');
    } else {
      // 4b. Se a busca falhar (API da Microsoft fora, etc.), volta para a home.
      router.push('/');
    }
  } else {
    // 5. Se a verificação de autenticação falhar, volta para a home.
    router.push('/');
  }
});
</script>