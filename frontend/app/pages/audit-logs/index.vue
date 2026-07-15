<template>
    <div class="flex flex-col flex-1 overflow-hidden">
        <div class="flex flex-wrap gap-2 ml-auto mb-4 shrink-0">            
            <USelect class="min-w-40" placeholder="請選擇紀錄動作" v-model="filterData['action']"
                :items="actionOptions"
                value-key="value"
                label-key="label" />
            <UInput class="min-w-40" placeholder="請輸入紀錄資源" v-model="filterData['resource']" />
            <UButton class="bg-[var(--color-accent)] hover:bg-[var(--color-accent-hover)] text-[var(--color-text-primary)]" @click="handleClearData()">清除</UButton>                               
        </div>
        <AudigLogsAuditLogDetailModal v-if="selectedAuditLog"
            :log="selectedAuditLog" 
            v-model:open="isModalOpen" />
        <div class="flex-1 flex flex-col gap-2 overflow-auto">
            <div v-for="log in auditLogs" :key="log.id"              
             class="p-2 rounded cursor-pointer bg-[var(--color-card)] border border-[var(--color-border)]"
             @click="openModal(log)">
                <div :class="actionMap[log.action as keyof typeof actionMap]">{{ log.action }}</div>
                <div class="flex space-x-2 items-center">
                    <p class="w-24 flex-1 shrink-0 text-[var(--color-text-primary)]">{{ log.resource }}</p>                    
                    <p class="text-sm shrink-0 text-right">{{ formatDate(log.performed_at) ?? '--' }}</p>
                </div>
            </div>
        </div>
        <div class="flex justify-center mt-4 shrink-0">
            <UPagination v-model:page="currentPage" :total="total" :items-per-page="size" />        
        </div>
    </div>
</template>

<script setup lang="ts">    
    import type { AuditLogResponse } from '~/types/audit-log'        
    const isModalOpen = ref(false)
    const selectedAuditLog = ref<AuditLogResponse | null>(null)    
    const openModal = (auditLog: AuditLogResponse) => {
        selectedAuditLog.value = auditLog
        isModalOpen.value = true
    }
    const {
        auditLogs, total, filterData, currentPage, size, actionOptions, handleClearData
    } = useAuditLogList()   
    const actionMap: { CREATE: string, UPDATE: string, DELETE: string} = {
        CREATE: 'text-[var(--color-success)]', 
        UPDATE: 'text-[#D4A853]', 
        DELETE: 'text-[var(--color-error)]'
    } 
</script>