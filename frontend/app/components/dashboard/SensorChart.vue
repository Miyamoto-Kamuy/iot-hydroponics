
<template>
    <div class="w-full h-full rounded p-4 flex flex-col background-[var(--color-card)] border border-[var(--color-border)]">
        <UTabs :items="tabItems" v-model="selectedTab"
        :ui="{ 
            list: 'bg-[var(--color-bg)]', 
            indicator: 'bg-[var(--color-accent)]', 
            trigger: 'text-[var(--color-text-secondary)] data-[state=active]:text-[var(--color-text-primary)]'
        }" calss="mb-4" />
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