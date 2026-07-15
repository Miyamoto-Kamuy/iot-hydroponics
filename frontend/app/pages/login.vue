<template>
    <div class="login-page">
        <h1 class="text-2xl font-bold text-center mb-6 text-[var(--color-text-primary)]">
            IoT Hydroponics
        </h1>        
        <p class="text-center text-[var(--color-text-secondary)] mb-6">{{ isLoginPage ? '登入您的帳號' : '建立新帳號' }}</p>

        <UForm :schema="schema" :state="data" @submit="onSubmit" class="space-y-4" aria-label="登入表單">
            <UFormField label="帳號" name="email">
                <UInput class="w-full" 
                placeholder="請輸入帳號..."
                v-model="data.email" />
            </UFormField>
            <UFormField label="密碼" name="password">
                <UInput type="password" class="w-full" 
                placeholder="請輸入密碼..."
                v-model="data.password" />
            </UFormField>
            <UFormField v-if="!isLoginPage" label="權限角色" name="role">
                <USelect class="w-full"                    
                    v-model="data['role']"
                    :items="options"
                    value-key="value"
                    label-key="label" />
            </UFormField>

            <UButton type="submit" class="w-full justify-center cursor-pointer bg-[var(--color-accent)] hover:bg-[var(--color-accent-hover)] text-[var(--color-text-primary)]">
                {{ isLoginPage ? '登入' : '註冊' }}
            </UButton>            
        </UForm>      
        <div class="flex justify-center w-full gap-8">
            <UButton variant="link" 
                class="cursor-pointer text-[var(--color-text-primary)] hover:text-[var(--color-accent)]" 
                @click="handleSwitchAuth">
                {{ isLoginPage ? '前往註冊' : '回到登入' }}
            </UButton>
            <!-- <UButton variant="link" class="cursor-pointer text-[var(--color-text-primary)] hover:text-[var(--color-accent)]" v-if="isLoginPage">忘記密碼</UButton>             -->
        </div>
    </div>
</template>
<script setup lang="ts">    
    definePageMeta({
        layout: 'auth'
    })
    const {
        isLoginPage, 
        data, 
        schema, 
        options, 
        onSubmit, 
        handleSwitchAuth
    } = useLoginForm()
</script>