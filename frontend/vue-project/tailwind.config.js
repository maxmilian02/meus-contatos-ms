/** @type {import('tailwindcss').Config} */
const defaultTheme = require('tailwindcss/defaultTheme')

module.exports = {
  darkMode: 'class',
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Montserrat', ...defaultTheme.fontFamily.sans],
      },
      colors: {
        'brand': {
          'primary': '#FFC153',
          'secondary': '#331D6E',
          'accent': '#613FC8',
        },
        'light': {
          'background': '#F5F5F5',
          'card': '#FFFFFF',
          'border': '#E4E4E4',
          'text-primary': '#282828',
          'text-secondary': '#6c757d',
        },
        'dark': {
          'background': '#1A1D24',
          'card': '#272A30',
          'border': '#404348',
          'text-primary': '#F8F9FA',
          'text-secondary': '#ADB5BD',
        },
        'danger': '#DC3545',
      },
      keyframes: {
        'fade-in-up': {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
      },
      animation: {
        'fade-in-up': 'fade-in-up 0.5s ease-out forwards',
      },
    },
  },
  plugins: [],
}