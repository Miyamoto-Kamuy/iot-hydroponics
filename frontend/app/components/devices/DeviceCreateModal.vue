<template>
    <UModal v-model:open="isOpen">
        <template #default>
            <UButton>新增設備</UButton>
        </template>
        <template #content>
            <UForm :schema="schema" :state="addData" @submit="handleCreate" class="space-y-4 p-4">
                <UFormField label="設備名稱" name="name">
                    <UInput class="w-full" 
                    placeholder="請輸入設備名稱..."
                    v-model="addData.name" />
                </UFormField>
                <UFormField label="設備地點" name="location">
                    <UInput class="w-full" 
                    placeholder="請輸入設備地點..."
                    v-model="addData.location" />
                </UFormField>
                <UFormField label="設備狀態" name="status">
                    <USelect class="w-full"                    
                        v-model="addData.status"
                        :items="options"
                        value-key="value"
                        label-key="label" />
                </UFormField>

                <div class="flex justify-center gap-2">
                    <UButton @click="isOpen = false" 
                        class="cursor-pointer">取消</UButton>   
                    <UButton type="submit" 
                        class="cursor-pointer">新增</UButton>        
                </div>
            </UForm> 
        </template>
    </UModal>   
</template>

<script setup lang="ts">
    import { z } from 'zod'
    const deviceStore = useDeviceStore()
    const isOpen = ref(false)
    const schema = z.object({
        name: z.string().min(1, '請輸入設備名稱'), 
        location: z.string().min(1, '請輸入設備地點'),         
    })
    const addData = ref<{name: string, location: string, status: 'online' | 'offline' | undefined }>({
        name: '', 
        location: '', 
        status: undefined,         
    })
    const options=[   
        { label: '在線', value: 'online' },
        { label: '離線', value: 'offline' }
    ]
    const handleCreate = async () => {
        await deviceStore.createDevice({
            name: addData.value.name, 
            location: addData.value.location, 
            status: addData.value.status ?? 'offline', 
        })
        isOpen.value = false
        addData.value = { name: '', location: '', status: undefined}
    }
</script>