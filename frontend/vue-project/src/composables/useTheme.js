import { ref, onMounted, watch } from 'vue'

export function useTheme() {
  // Inicializa com um valor padrão para evitar FOUC (Flash of Unstyled Content)
  const theme = ref('light') 

  // Função centralizada para aplicar o tema
  const applyTheme = (newTheme) => {
    theme.value = newTheme
    localStorage.setItem('theme', newTheme)
    if (newTheme === 'dark') {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }

  const toggleTheme = () => {
    applyTheme(theme.value === 'light' ? 'dark' : 'light')
  }

  onMounted(() => {
    // Determina o tema inicial com base no localStorage ou preferência do sistema
    const initialTheme = localStorage.getItem('theme') || 
      (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')
    applyTheme(initialTheme)
  })

  // A watch não é mais estritamente necessária com esta lógica, mas mantemos para reatividade
  watch(theme, (newTheme) => {
    if (newTheme !== (document.documentElement.classList.contains('dark') ? 'dark' : 'light')) {
      applyTheme(newTheme)
    }
  })

  return { theme, toggleTheme }
}