<script setup>
useHead({
  meta: [
    { name: 'viewport', content: 'width=device-width, initial-scale=1' }
  ],
  link: [
    { rel: 'icon', href: '/favicon.ico' }
  ],
  htmlAttrs: {
    lang: 'zh-TW'
  }
})

useSeoMeta({
  title: "IoT Hydroponics Monitor",
  description: '水耕系統即時監控平台',  
})
</script>

<template>
  <UApp>    
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </UApp>
</template>
