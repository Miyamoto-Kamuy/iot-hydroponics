<template>
    <div class="flex flex-col flex-1 overflow-hidden">
        <div class="flex gap-2 ml-auto mb-4 shrink-0">            
            <USelect class="min-w-40" placeholder="請選擇使用者角色" v-model="filterData['role']"
                :items="options"
                value-key="value"
                label-key="label" />
            <UButton @click="handleClearData()">清除</UButton>                               
        </div>
        <UsersUserDetailModal v-if="selectedUser"
            :user="selectedUser" 
            v-model:open="isModalOpen" />
        <div class="flex-1 grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2 overflow-auto content-start">
            <div v-for="user in users" :key="user.id"              
             class="p-2 rounded bg-[#1da1f2] cursor-pointer"
             @click="openModal(user)">
                <div :class="roleMap[user.role as keyof typeof roleMap]">{{ user.role }}</div>
                <div class="flex space-x-2 items-center">
                    <p class="w-40 shrink-0">{{ user.email }}</p>
                </div>
            </div>        
        </div>
        <div class="flex justify-center mt-4 shrink-0">
            <UPagination v-model:page="currentPage" :total="total" :items-per-page="size" />        
        </div>
    </div>
</template>

<script setup lang="ts">
    import type { UserResponse } from '~/types/user'        
    const isModalOpen = ref(false)
    const selectedUser = ref<UserResponse | null>(null)    
    const openModal = (user: UserResponse) => {
        selectedUser.value = user
        isModalOpen.value = true
    }
    const {
        users, total, filterData, currentPage, size, options, handleClearData
    } = useUserList()    
    const roleMap: { admin: string, operator: string, viewer: string} = {
        admin: 'text-red-400', 
        operator: 'text-yellow-400', 
        viewer: 'text-green-400'
    } 
</script>