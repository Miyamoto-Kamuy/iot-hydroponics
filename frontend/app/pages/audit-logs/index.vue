<template>
    <div class="flex flex-col flex-1 overflow-hidden">
        <div class="flex gap-2 ml-auto mb-4 shrink-0">            
            <USelect class="min-w-40" v-model="filterData['action']"
                :items="actionOptions"
                value-key="value"
                label-key="label" />
            <UInput v-model="filterData['resource']" />
            <UButton @click="handleClearData()">清除</UButton>                               
        </div>
        <AudigLogsAuditLogDetailModal v-if="selectedAuditLog"
            :log="selectedAuditLog" 
            v-model:open="isModalOpen" />
        <div class="flex-1 flex flex-col gap-2 overflow-auto">
            <div v-for="log in auditLogs" :key="log.id"              
             class="p-2 rounded bg-[#1da1f2] cursor-pointer"
             @click="openModal(log)">
                <div :class="actionMap[log.action as keyof typeof actionMap]">{{ log.action }}</div>
                <div class="flex space-x-2 items-center">
                    <p class="w-24 shrink-0">{{ log.resource }}</p>                    
                    <p class="w-50 shrink-0 text-right">{{ formatDate(log.performed_at) ?? '--' }}</p>
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
        CREATE: 'text-green-400', 
        UPDATE: 'text-yellow-400', 
        DELETE: 'text-red-400'
    } 
</script>