<template>
    <UModal v-model:open="open">        
        <template #content>
            <div class="p-4 space-y-4">
                <div class="flex flex-col gap-2">
                    <div class="flex gap-2" v-for="info in alertInfo.filter(i => !i.adminOnly || user?.role === 'admin')" :key="info.contentKey">
                        <p class="w-24 shring-0 text-sm text-muted">{{ info.label }}</p>
                        <p class="text-[var(--color-text-primary)]">{{ info.format ? info.format(props.alert?.[info.contentKey]) : props.alert?.[info.contentKey] }}</p>
                    </div>
                </div>     
                <div class="flex justify-center gap-2">
                    <UButton @click="open = false" 
                            class="cursor-pointer bg-[var(--color-accent)] hover:bg-[var(--color-accent-hover)] text-[var(--color-text-primary)]">返回</UButton>  
                        <UButton @click="handleUpdateAlert('read')" 
                            class="cursor-pointer bg-[var(--color-accent)] hover:bg-[var(--color-accent-hover)] text-[var(--color-text-primary)]">標誌為已讀</UButton>  
                        <UButton @click="handleUpdateAlert('resolved')" 
                            class="cursor-pointer bg-[var(--color-accent)] hover:bg-[var(--color-accent-hover)] text-[var(--color-text-primary)]">標誌為已解決</UButton>                      
                </div>       
            </div>
        </template>
    </UModal>   
</template>

<script setup lang="ts">
    import type { AlertResponse } from '~/types/alert';
    const alertStore = useAlertStore()
    const authStore = useAuthStore()
    const { user } = storeToRefs(authStore)
    const open = defineModel('open')
    const props = defineProps<{ alert: AlertResponse}>()
    const alertInfo: {
        label: string, 
        contentKey: keyof AlertResponse, 
        format?: (val: any) => string, 
        adminOnly?: boolean
    }[] = [
        { label: '類型', contentKey: 'sensor_type' }, 
        { label: '訊息', contentKey: 'message' }, 
        { label: '狀態', contentKey: 'status' }, 
        { label: '觸發時間', contentKey: 'triggered_at', format: formatDate }, 
        { label: '設備創建者', contentKey: 'device_id', adminOnly: true }, 
    ]
    const handleUpdateAlert = async (type: 'read' | 'resolved') => {
        await alertStore.updateAlertStatus(props.alert.id, type)
        open.value = false        
    }
</script>