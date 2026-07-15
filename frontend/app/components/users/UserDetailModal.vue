<template>
    <UModal v-model:open="open">        
        <template #content>
            <div class="p-4 space-y-4">
                <div class="flex flex-col gap-2">
                    <div class="flex gap-2" v-for="info in userInfo" :key="info.contentKey">
                        <p class="w-24 shring-0 text-sm text-muted">{{ info.label }}</p>
                        <p class="text-[var(--color-text-primary)]">{{ info.format ? info.format(props.user?.[info.contentKey]) : props.user?.[info.contentKey] }}</p>
                    </div>
                    <div class="flex gap-2">
                        <p class="w-24 shring-0 text-sm text-muted">角色</p>
                        <p class="text-[var(--color-text-primary)]" v-if="!isEdit">{{ roleMap[props.user?.role] }}</p>
                        <USelect v-else 
                            v-model="editRole"
                            :items="roleOptions"
                            value-key="value"
                            label-key="label"
                            class="flex-1" />
                    </div>
                </div>     
                <div class="flex justify-center gap-2">
                    <UButton @click="open = false" 
                            class="cursor-pointer bg-[var(--color-text-secondary)] hover:bg-[var(--color-text-secondary-hover)] text-[var(--color-text-primary)]">返回</UButton>  
                    <template v-if="!isEdit">
                        <UButton @click="startEdit" 
                            class="cursor-pointer bg-[var(--color-accent)] hover:bg-[var(--color-accent-hover)] text-[var(--color-text-primary)]">編輯角色</UButton>                                           
                    </template>
                    <template v-else>
                        <UButton @click="cancelEdit" 
                            class="cursor-pointer bg-[var(--color-text-secondary)] hover:bg-[var(--color-text-secondary-hover)] text-[var(--color-text-primary)]">取消</UButton>                                           
                        <UButton @click="handleUpdateUser" 
                            class="cursor-pointer bg-[var(--color-accent)] hover:bg-[var(--color-accent-hover)] text-[var(--color-text-primary)]">儲存</UButton>                                           
                    </template>
                </div>       
            </div>
        </template>
    </UModal>   
</template>

<script setup lang="ts">
    import type { UserResponse } from '~/types/user';
    const userStore = useUserStore()
    const authStore = useAuthStore()
    const { user } = storeToRefs(authStore)
    const open = defineModel('open')
    const props = defineProps<{ user: UserResponse}>()
    const isEdit = ref(false)
    const editRole = ref<'admin' | 'operator' | 'viewer'>(props.user?.role)
    const roleOptions = [  
        { label: '管理者', value: 'admin' },
        { label: '操作者', value: 'operator' }, 
        { label: '觀看者', value: 'viewer' },
    ]
    const roleMap = {
        admin: '管理者', 
        operator: '操作者',
        viewer: '觀看者',
    }
    const userInfo: {
        label: string, 
        contentKey: keyof UserResponse, 
        format?: (val: any) => string, 
        adminOnly?: boolean
    }[] = [
        { label: '信箱', contentKey: 'email' }, 
        // { label: '角色', contentKey: 'role' },
        { label: '建立時間', contentKey: 'created_at', format: formatDate }, 
    ]
    const startEdit = () => isEdit.value = true
    const cancelEdit = () => {
        isEdit.value = false
        editRole.value = props.user?.role
    }
    const handleUpdateUser = async () => {
        await userStore.updateUser(props.user.id, { role: editRole.value })
        open.value = false        
    }
    watch(open, (newVal) => {
        if(!newVal) {
            cancelEdit()
        }
    })
</script>