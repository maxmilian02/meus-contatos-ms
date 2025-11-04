<template>
  <button @click="toggleLng" class="btn btn-secondary !p-2">
    <span class="font-bold text-xs">{{ locale === 'pt' ? 'EN' : 'PT' }}</span>
  </button>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
const { locale } = useI18n()

const toggleLng = () => {
  const newLocale = locale.value === 'pt' ? 'en' : 'pt'
  locale.value = newLocale
  localStorage.setItem('locale', newLocale)
}
</script>