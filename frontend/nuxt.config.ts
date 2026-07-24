// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  modules: [
    '@nuxt/eslint',
    '@nuxt/ui', 
    '@pinia/nuxt'
  ],

  devtools: {
    enabled: true
  },
  ssr: false,

  css: ['~/assets/css/main.css'],

  compatibilityDate: '2026-06-30',

  eslint: {
    config: {
      stylistic: {
        commaDangle: 'never',
        braceStyle: '1tbs'
      }
    }
  }, 

  runtimeConfig: {
    public: {
      apiBase: process.env.API_BASE || 'http://localhost:8000'
    }
  },

  imports: {
    dirs: ['composables', 'composables/**']
  }, 

  vite: {
    optimizeDeps: {
      include: [
        '@vueuse/core', 
        'zod'
      ]
    }
  }, 

  colorMode: {
    preference: 'dark', 
    fallback: 'dark'
  }
})
