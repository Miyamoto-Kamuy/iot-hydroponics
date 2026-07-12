
<template>
    <div class="bg-inverted w-full h-full rounded p-4 flex flex-col">
        <UTabs :items="tabItems" v-model="selectedTab" calss="mb-4" />
        <div class="flex-1">
            <Line :key="chartKey" :data="currentChartData" :options="chartOptions" />
        </div>
    </div>
</template>

<script setup lang="ts">
    import { Line } from 'vue-chartjs'    
    const props = defineProps<{
        deviceId: number | null
    }>()
    const { 
        chartKey, 
        selectedTab, 
        tabItems, 
        chartOptions, 
        currentChartData } = useSensorChart(toRef(props, 'deviceId'))
</script>

<style scoped>

</style>