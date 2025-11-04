import { defineStore } from 'pinia';
import { ref, reactive } from 'vue';
import api from '@/services/api';
import { useAuthStore } from './auth';

export const useContactsStore = defineStore('contacts', () => {
  const grouped = ref({});
  const loading = ref(true);
  const error = ref(null);
  const expanded = reactive({}); // Para controlar o "Ver mais"

  async function fetchContacts() {
    loading.value = true;
    error.value = null;
    try {
      const res = await api.get('/contacts');
      grouped.value = res.data;
      return true; // Sucesso
    } catch (err) {
      if (err.response?.status === 401) {
        const authStore = useAuthStore();
        authStore.logout(); // Se o token for inválido, desloga
      } else {
        error.value = err.response?.data?.details || 'Falha ao carregar contatos.';
      }
      return false; // Falha
    } finally {
      loading.value = false;
    }
  }

  function clearContacts() {
    grouped.value = {};
  }

  return { grouped, loading, error, expanded, fetchContacts, clearContacts };
});