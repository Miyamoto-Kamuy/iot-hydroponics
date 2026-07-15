<template>
    <div class="flex flex-col flex-1 overflow-hidden">        
        <div class="flex flex-wrap gap-2 mb-4 shrink-0">
            <UInput class="min-w-40" placeholder="請輸入設備地點" v-model="filterData.location" />
            <USelect class="min-w-40" placeholder="請選擇設備狀態" v-model="filterData['status']"
                :items="options"
                value-key="value"
                label-key="label" />
            <UButton @click="handleClearData()">清除</UButton>                   
            <DevicesDeviceCreateModal />
        </div>
        <div class="flex-1 flex flex-col gap-2 overflow-auto">
            <div v-if="isLoading" class="flex flex-1 items-center justify-center">
                <p class="text-muted">載入中...</p>
            </div>
            <div v-else-if="isEmpty" class="flex flex-1 items-center justify-center">
                <p class="text-muted">目前沒有設備</p>
            </div>
            <template v-else>
                <div v-for="device in devices" :key="device.id"              
                 class="p-2 rounded bg-[#1da1f2] cursor-pointer"
                 @click="navigateTo(`/devices/${device.id}`)">
                    <div class="flex justify-between items-center">
                        <div class="flex flex-col gap-1">
                            <p class="font-bold">{{ device.name }}</p>
                            <p class="font-sm">{{ device.location }}</p>
                            <p class="font-sm">{{ device.status }}</p>
                        </div>
                        <p class="text-sm shrink-0 ml-2">{{ formatDate(device.last_seen_at) ?? '--' }}</p>
                    </div>
                </div>
            </template>
        </div>
        <div class="flex justify-center mt-4 shrink-0">
            <UPagination v-model:page="currentPage" :total="total" :items-per-page="size" />        
        </div>
    </div>
</template>

<script setup lang="ts">    
    const {
        devices, total, filterData, isLoading, isEmpty, currentPage, size, options, handleClearData
    } = useDeviceList()    
</script>