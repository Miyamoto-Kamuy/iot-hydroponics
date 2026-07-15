<template>
    <div class="flex flex-col flex-1 overflow-hidden">
        <div class="flex flex-wrap gap-2 ml-auto mb-4 shrink-0">            
            <USelect class="min-w-40" placeholder="請選擇告警類型" v-model="filterData['sensor_type']"
                :items="sensorTypeOptions"
                value-key="value"
                label-key="label" />
            <USelect class="min-w-40" placeholder="請選擇告警狀態" v-model="filterData['status']"
            :items="statusOptions"
            value-key="value"
            label-key="label" />
            <UButton class="bg-[var(--color-accent)] hover:bg-[var(--color-accent-hover)] text-[var(--color-text-primary)]" @click="handleClearData()">清除</UButton>                               
        </div>
        <AlertsAlertDetailModal v-if="selectedAlert"
            :alert="selectedAlert" 
            v-model:open="isModalOpen" />
        <div class="flex-1 flex flex-col gap-2 overflow-auto">
            <div v-for="alert in alerts" :key="alert.id"              
             class="p-2 rounded cursor-pointer bg-[var(--color-card)] border border-[var(--color-border)]"
             @click="openModal(alert)">
                <div :class="alert.status === 'unread' ? 'text-[var(--color-error)]' : 'text-[var(--color-accent)]'">{{ alert.status }}</div>
                <div class="flex space-x-2 items-center">
                    <p class="w-24 shrink-0">{{ alert.sensor_type }}</p>
                    <p class="font-bold flex-1 truncate">{{ alert.message }}</p>                
                    <p class="text-sm shrink-0 text-right">{{ formatDate(alert.triggered_at) ?? '--' }}</p>
                </div>
            </div>
        </div>
        <div class="flex justify-center mt-4 shrink-0">
            <UPagination v-model:page="currentPage" :total="total" :items-per-page="size" />        
        </div>
    </div>
</template>

<script setup lang="ts">
    import type { AlertResponse } from '~/types/alert'        
    const isModalOpen = ref(false)
    const selectedAlert = ref<AlertResponse | null>(null)    
    const openModal = (alert: AlertResponse) => {
        selectedAlert.value = alert
        isModalOpen.value = true
    }
    const {
        alerts, total, filterData, currentPage, size, sensorTypeOptions, statusOptions, handleClearData
    } = useAlertList()    
</script>