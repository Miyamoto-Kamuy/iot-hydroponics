<template>
    <aside :class="['fixed left-0 top-0 h-full z-50 transition-all duration-300 overflow-hidden flex flex-col bg-[var(--color-sidebar)] border-right border-[var(--color-border)]', isOpen ? 'w-48' : 'w-14']"
        aria-label="主要導覽"
        @mouseenter="isOpen = true"
        @mouseleave="isOpen = false">
        <div class="flex items-center gap-4 px-4 py-5 mb-4 border-b border-gray-700 whitespace-nowrap" 
            @click="toggleSidebar">
            <UIcon :name="'i-lucide-leaf'" class="w-6 h-6 shrink-0 text-[var(--color-text-primary)]" />
            <span class="text-default font-extrabold font-xl text-[var(--color-text-primary)]">IoT Hydroponics</span>
        </div>
        <nav class="flex flex-col flex-1" aria-label="頁面導覽">
            <NuxtLink v-for="item in navItems" :key="item.to"
                :to="item.to"
                class="flex items-center gap-4 px-4 py-3
                    text-[var(--color-text-primary)] hover:bg-[var(--color-border)]
                    transition-colors duration-200 whitespace-nowrap"            
                :class="route.path === item.to ? 'bg-[var(--color-border)]' : ''">
                <UIcon :name="item.icon" class="w-6 h-6 shrink-0" />
                <span class="font-semibold">{{ item.label }}</span>
            </NuxtLink>
        </nav>
        <div class="border-t border-gray-700 p-2">
            <button @click="handleLogout" class="flex items-center gap-4 py-3 px-2 w-full
                text-[var(--color-text-secondary)] hover:text-white hover:bg-[var(--color-border)]
                transition-colors duration-200 whitespace-nowrap rounded-lg cursor-pointer" aria-label="登出系統">
                <UIcon name="i-lucide-log-out" class="w-6 h-6 shrink-0" />
                <span class="font-semibold">登出</span>
            </button>
        </div>
    </aside>
    <main class="h-screen flex flex-col overflow-hidden p-6 ml-14 bg-[var(--color-bg)]">
        <div v-if="isLoading" class="fixed inset-0 z-[100] bg-black/30 flex items-center justify-center">
            <div class="w-12 h-12 border-4 border-green-400 border-t-transparent rounded-full animate-spin"></div>
        </div>
        <header class="flex items-end w-full gap-8 mb-6">
            <UIcon class="w-10 h-10 text-[var(--color-text-primary)]" :name="currentNavItem?.icon" />
            <h1 class="text-4xl font-bold text-[var(--color-text-primary)]">
                {{ currentNavItem?.label }}
            </h1>
        </header>
        <slot />
    </main>    
</template>

<script setup lang="ts">
    const authStore = useAuthStore()
    const route = useRoute()
    const isLoading = useState('globalLoading')
    const isOpen = ref(false)    
    const toggleSidebar = () => isOpen.value = !isOpen.value
    const navItems = computed(() => [
        { icon: 'i-lucide-layout-dashboard', label: '即時監控', to: '/dashboard' },
        { icon: 'i-lucide-cpu', label: '設備管理', to: '/devices' },
        { icon: 'i-lucide-bell', label: '告警列表', to: '/alerts' },
        ...(authStore.user?.role === 'admin' ? [
            { icon: 'i-lucide-scroll-text', label: '操作紀錄', to: '/audit-logs' },
            { icon: 'i-lucide-users', label: '使用者管理', to: '/users' },                
        ] : []), 
        { icon: 'i-lucide-user', label: '個人資料', to: '/profile' },        
    ])
    const currentNavItem = computed(() => navItems.value.find(item => item.to === route.path))
    const handleLogout = () => {
        authStore.logout()
        navigateTo('/login')
    }
    
</script>