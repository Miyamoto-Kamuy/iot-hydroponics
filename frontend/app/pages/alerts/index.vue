<template>
    <div class="flex flex-col flex-1 overflow-hidden">
        <div class="flex gap-2 ml-auto mb-4 shrink-0">            
            <USelect class="min-w-40" v-model="filterData['sensor_type']"
                :items="sensorTypeOptions"
                value-key="value"
                label-key="label" />
            <USelect class="min-w-40" v-model="filterData['status']"
            :items="statusOptions"
            value-key="value"
            label-key="label" />
            <!-- <UInput class="min-w-40" v-model="filterData.device_id" /> -->
            <UButton @click="handleClearData()">清除</UButton>                               
        </div>
        <div class="flex-1 flex flex-col gap-2 overflow-auto">
            <div v-for="alert in alerts" :key="alert.id"              
             class="p-2 rounded bg-[#1da1f2] cursor-pointer"
             @click="console.log('open detail modal')">
                <div>{{ alert.status }}</div>
                <div class="flex">
                    <p>{{ alert.sensor_type }}</p>
                    <p>{{ alert.message }}</p>
                    <p v-if="user?.role === 'admin'">{{ alert.device_id }}</p>
                    <p>{{ formatDate(alert.triggered_at) ?? '--' }}</p>
                </div>
            </div>
        </div>
        <div class="flex justify-center mt-4 shrink-0">
            <UPagination v-model:page="currentPage" :total="total" :items-per-page="size" />        
        </div>
    </div>
</template>

<script setup lang="ts">    
    const authStore = useAuthStore()
    const { user } = storeToRefs(authStore)
    const {
        alerts, total, filterData, currentPage, size, sensorTypeOptions, statusOptions, handleClearData
    } = useAlertList()    
</script>