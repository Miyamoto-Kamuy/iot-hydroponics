<template>
    <UModal v-model:open="open">        
        <template #content>
            <div class="p-4 space-y-4">
                <div class="flex flex-col gap-2">
                    <div class="flex gap-2" v-for="info in auditLogInfo.filter(i => i && (!i.adminOnly || user?.role === 'admin'))" :key="info.contentKey">
                        <p class="w-24 shring-0 text-sm text-muted">{{ info.label }}</p>

                        <pre v-if="info.contentKey === 'detail'" class="text-xs overflow-auto text-[var(--color-text-primary)]">
                            {{ info.format ? info.format(props.log?.[info.contentKey]) : props.log?.[info.contentKey] ?? '--' }}
                        </pre>
                        <p v-else class="text-[var(--color-text-primary)]">
                            {{ info.format ? info.format(props.log?.[info.contentKey]) : props.log?.[info.contentKey] ?? '--' }}
                        </p>
                    </div>
                </div>     
                <div class="flex justify-center gap-2">
                    <UButton @click="open = false" 
                            class="cursor-pointer bg-[var(--color-accent)] hover:bg-[var(--color-accent-hover)] text-[var(--color-text-primary)]">返回</UButton>                     
                </div>       
            </div>
        </template>
    </UModal>   
</template>

<script setup lang="ts">
    import type { AuditLogResponse } from '~/types/audit-log';
    const auditLogStore = useAuditLogStore()
    const authStore = useAuthStore()
    const { user } = storeToRefs(authStore)
    const open = defineModel('open')
    const props = defineProps<{ log: AuditLogResponse}>()
    const auditLogInfo: {
        label: string, 
        contentKey: keyof AuditLogResponse, 
        format?: (val: any) => string, 
        adminOnly?: boolean
    }[] = [
        { label: '動作', contentKey: 'action' }, 
        { label: '資源', contentKey: 'resource' }, 
        { label: '資源ID', contentKey: 'resource_id' }, 
        { label: '紀錄', contentKey: 'detail', format: (val) => val ? JSON.stringify(val, null, 2) : '--' }, 
        { label: '狀態碼', contentKey: 'status_code' }, 
        { label: '錯誤紀錄', contentKey: 'error_detail' }, 
        { label: '執行時間', contentKey: 'performed_at', format: formatDate }, 
        { label: '執行者', contentKey: 'performed_by', adminOnly: true }, 
    ]
</script>