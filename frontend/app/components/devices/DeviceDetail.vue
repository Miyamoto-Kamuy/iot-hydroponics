<template>
    <div>
        <div class="flex flex-col">
            <div class="flex flex-col gap-2 md:gap-5 p-4" v-if="!isEdit">                
                <div class="flex flex-col gap-1">
                    <p class="text-sm">設備名稱</p>
                    <p class="font-bold">{{ currentDevice?.name }}</p>
                </div>
                <div class="flex flex-col gap-1">
                    <p class="text-sm">設備地點</p>
                    <p class="font-bold">{{ currentDevice?.location }}</p>
                </div>
                <div class="flex flex-col gap-1">
                    <p class="text-sm">設備狀態</p>
                    <p class="font-bold">{{ currentDevice?.status }}</p>                    
                </div>
                <div class="flex flex-col gap-1">
                    <p class="text-sm">上次查看時間</p>
                    <p class="font-bold">{{ formatDate(currentDevice?.last_seen_at) }}</p>                    
                </div>
                <div class="flex flex-col gap-1">
                    <p class="text-sm">設備建立時間</p>
                    <p class="font-bold">{{ formatDate(currentDevice?.created_at) }}</p>                    
                </div>
                <div class="flex flex-col gap-1" v-if="user?.role === 'admin'">
                    <p class="text-sm">建立者</p>
                    <p class="font-bold">{{ currentDevice?.created_by }}</p>                    
                </div>
                <div class="flex gap-2">
                    <UButton class="cursor-pointer" @click="startEdit">編輯</UButton>
                    <UPopover class="cursor-pointer" v-model:open="isDeleteConfirm">                    
                        <UButton color="error" @click="isDeleteConfirm = true">刪除</UButton>
    
                        <template #content>
                            <div class="p-4 flex flex-col gap-2">
                                <p>確定要刪除這台設備嗎？</p>
                                <div class="flex gap-2">
                                    <UButton @click="isDeleteConfirm = false">取消</UButton>
                                    <UButton color="error" @click="confirmDelete">確認刪除</UButton>
                                </div>                            
                            </div>
                        </template>
                    </UPopover>                    
                </div>
            </div>
            <UForm v-else :schema="schema" :state="editData" @submit="handleUpdate" class="space-y-4 p-4">                
                <UFormField label="設備名稱" name="name">
                    <UInput v-if="isEdit" class="w-full" 
                    placeholder="請輸入設備名稱..."
                    v-model="editData.name" />
                </UFormField>
                <UFormField label="設備地點" name="location">
                    <UInput v-if="isEdit" class="w-full" 
                    placeholder="請輸入設備地點..."
                    v-model="editData.location" />
                </UFormField>
                <UFormField label="設備狀態" name="status">
                    <USelect class="w-full"                    
                        v-model="editData.status"
                        :items="options"
                        value-key="value"
                        label-key="label" />
                </UFormField>
                <div class="flex flex-col gap-1">
                    <p>上次查看時間</p>
                    <p>{{ formatDate(currentDevice?.last_seen_at) }}</p>                    
                </div>
                <div class="flex flex-col gap-1">
                    <p>設備建立時間</p>
                    <p>{{ formatDate(currentDevice?.created_at) }}</p>                    
                </div>
                <div class="flex flex-col gap-1 mb-6" v-if="user?.role === 'admin'">
                    <p>建立者</p>
                    <p>{{ currentDevice?.created_by }}</p>                    
                </div>
                <div class="flex gap-2">
                    <UButton class="cursor-pointer" type="button" @click="cancelEdit">取消</UButton>
                    <UButton class="cursor-pointer" type="submit">儲存</UButton>
                </div>
            </UForm>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { z } from 'zod'     
    const schema = z.object({
        name: z.string().min(1, '請輸入設備名稱'), 
        location: z.string().min(1, '請輸入設備地點'),         
    })
    const route = useRoute()
    const toast = useToast()
    const authStore = useAuthStore()
    const deviceStore = useDeviceStore()
    const { currentDevice } = storeToRefs(deviceStore)
    const { user } = storeToRefs(authStore)
    const isEdit = ref(false)
    const isDeleteConfirm = ref(false)
    const editData = ref<{name: string, location: string, status: 'online' | 'offline' | undefined}>({
        name: '', 
        location: '', 
        status: undefined
    })
    const options=[   
        { label: '在線', value: 'online' },
        { label: '離線', value: 'offline' }
    ]
    const startEdit = () => {
        editData.value = {
            name: currentDevice.value?.name ?? '',
            location: currentDevice.value?.location ?? '',
            status: currentDevice.value?.status
        } 
        isEdit.value = true
    }
    const cancelEdit = () => {
        editData.value = {
            name: '',
            location: '',
            status: undefined
        } 
        isEdit.value = false
    }
    const handleUpdate = async() => {
        await deviceStore.updateDevice(Number(route.params.id), {
            name: editData.value.name, 
            location: editData.value.location, 
            status: editData.value.status, 
        })
        isEdit.value = false
        toast.add({
            title: '更新成功', 
            color: 'success'
        })
    }
    const confirmDelete = async() => {
        await deviceStore.deleteDevice(Number(route.params.id))
        isDeleteConfirm.value = false
        navigateTo('/devices')
    }

    onMounted(async () => {
        await deviceStore.fetchDevice(Number(route.params.id))
    })
</script>