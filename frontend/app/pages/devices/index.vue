<template>
    <div class="flex flex-col flex-1 overflow-hidden">
        <div class="flex gap-2 ml-auto mb-4 shrink-0">
            <UInput class="min-w-40" v-model="filterData.location" />
            <USelect class="min-w-40" v-model="filterData['status']"
                :items="options"
                value-key="value"
                label-key="label" />
            <UButton @click="handleClearData()">清除</UButton>                   
            <DevicesDeviceCreateModal />
        </div>
        <div class="flex-1 flex flex-col gap-2 overflow-auto">
            <div v-for="device in devices" :key="device.id"              
             class="p-2 rounded bg-[#1da1f2] cursor-pointer"
             @click="navigateTo(`/devices/${device.id}`)">
                <div>{{ device.status }}</div>
                <div class="flex">
                    <p>{{ device.name }}</p>
                    <p>{{ device.location }}</p>
                    <p>{{ device.last_seen_at ?? '--' }}</p>
                </div>
            </div>
        </div>
        <div class="flex justify-center mt-4 shrink-0">
            <UPagination v-model:page="currentPage" :total="total" :items-per-page="size" />        
        </div>
    </div>
</template>

<script setup lang="ts">    
    const {
        devices, total, filterData, currentPage, size, options, handleClearData
    } = useDeviceList()    
</script>

<style scoped>

</style>