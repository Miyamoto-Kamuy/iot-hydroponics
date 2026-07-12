<template>
    <div class="bg-inverted w-full h-full rounded flex flex-col">        
        <div class="p-2 border-b border-gray-700 text-sm text-[#000]">
            未讀告警：{{ unreadAlerts.length }}
        </div>
        <div class="flex flex-col gap-2 p-2 overflow-y-auto">
            <div v-for="alert in unreadAlerts" :key="alert.id" 
                 @click="alertStore.markAsRead(alert.id)"
                 class="p-2 bg-[#1da1f2] rounded cursor-pointer">
                <p>{{ alert.status }}</p>
                <div class="flex">
                    <p>{{ alert.sensor_type }}</p>
                    <p>{{ alert.message }}</p>                
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

<style scoped>

</style>