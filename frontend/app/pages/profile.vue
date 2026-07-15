<template>
    <div class="flex flex-1 items-center justify-center">
        <UCard class="w-full max-w-md bg-[var(--color-card)] border border-[var(--color-border)]">
            <div class="flex flex-col gap-3 pb-4 border-b border-gray-700">
                <h2 class="text-lg font-bold text-[var(--color-text-primary)]">個人資料</h2>
                <div class="flex gap-2">
                    <p class="w-20 text-muted shrink-0">信箱: </p>
                    <p class="text-[var(--color-text-primary)]">{{ user?.email }}</p>
                </div>
                <div class="flex gap-2">
                    <p class="w-20 text-muted shrink-0">角色: </p>
                    <p class="text-[var(--color-text-primary)]">{{ roleMap[user?.role as keyof typeof roleMap] }}</p>
                </div>
                <div class="flex gap-2">
                    <p class="w-20 text-muted shrink-0">建立時間: </p>
                    <p class="text-[var(--color-text-primary)]">{{ formatDate(user?.created_at) }}</p>
                </div>
            </div>
            <UForm :schema="schema" :state="password" @submit="handleUpdatePassword" class="space-y-4 py-4">
                <h2 class="text-lg font-bold text-[var(--color-text-primary)]">修改密碼</h2>
                <UFormField label="新密碼" name="new_password">
                    <UInput type="password" class="w-full" 
                    placeholder="請輸入新密碼..."
                    v-model="password.new_password" />
                </UFormField>
                <UFormField label="確認密碼" name="confirm_password">
                    <UInput type="password" class="w-full" 
                    placeholder="請再次輸入新密碼..."
                    v-model="password.confirm_password" />
                </UFormField>

                <UButton type="submit" 
                    class="w-full justify-center cursor-pointer bg-[var(--color-accent)] hover:bg-[var(--color-accent-hover)] text-[var(--color-text-primary)]">儲存</UButton>                        
            </UForm> 
        </UCard>
    </div>
</template>

<script setup lang="ts">
    import { z } from 'zod'
    const userStore = useUserStore()
    const authStore = useAuthStore()
    const { user } = storeToRefs(authStore)
    const schema = z.object({
        new_password: z.string().min(6, '密碼至少6個字元'), 
        confirm_password: z.string().min(6, '請確認密碼'), 
    }).refine(data => data.new_password === data.confirm_password, {
        message: '兩次密碼不一致', 
        path: ['confirm_password']
    })
    const password = ref({
        new_password: '', 
        confirm_password: ''
    })
    const roleMap: { admin: string, operator: string, viewer: string} = {
        admin: '管理者', 
        operator: '操作者', 
        viewer: '觀看者'
    } 

    const handleUpdatePassword = async () => {
        await userStore.updateMe({ password: password.value.new_password })
        password.value.new_password = ''
        password.value.confirm_password = ''
    }
</script>