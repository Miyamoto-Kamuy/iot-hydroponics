<template>
    <div class="w-full h-full rounded flex flex-col bg-[var(--color-card)] border border-[var(--color-border)]">        
        <div class="p-2 border-b font-bold border-gray-700 text-sm text-[var(--color-text-primary)]">
            未讀告警：{{ unreadAlerts.length }}
        </div>
        <div class="flex flex-col gap-2 p-2 overflow-y-auto">
            <div v-for="alert in unreadAlerts" :key="alert.id" 
                 @click="alertStore.updateAlertStatus(alert.id, 'read')"
                 class="p-2 rounded cursor-pointer bg-[var(--color-warning)]">
                <p class="text-[var(--color-text-primary)]">{{ alert.sensor_type }}</p>
                <div class="flex">
                    <p class="text-[var(--color-text-primary)]">{{ alert.message }}</p>                
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { useIntervalFn } from '@vueuse/core'
    const alertStore = useAlertStore()
    const { alerts } = storeToRefs(alertStore)
    const unreadAlerts = computed(() => {
        return alerts.value?.filter(a => a.status === 'unread') ?? []
    })

    onMounted(async () => {
        await alertStore.fetchAlerts()
    })

    useIntervalFn(async () => {
        await alertStore.fetchAlerts()
    }, 30000)
</script>