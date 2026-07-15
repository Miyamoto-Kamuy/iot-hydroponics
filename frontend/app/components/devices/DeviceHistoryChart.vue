<template>
    <div class="bg-inverted w-full min-h-64 lg:h-full rounded p-4 flex flex-col">
        <UTabs :items="tabItems" v-model="selectedTab" calss="mb-4" />
        <div class="flex-1 h-64 lg:h-full">
            <Line :key="chartKey" :data="currentChartData" :options="chartOptions" />
        </div>
    </div>
</template>

<script setup lang="ts">
    import { Line } from 'vue-chartjs'  
    import type { MeasurementResponse } from '~/types/measurement'
    import type { PaginateResponse } from '~/types/pagination'
    const api = useApi()
    const route = useRoute()
    const { chartKey, selectedTab, tabItems, chartOptions, chartData, currentChartData } = useChartBase()


    onMounted(async () => {
        const response: PaginateResponse<MeasurementResponse> = await api(`/devices/${Number(route.params.id)}/measurements`, { 
            params: { size: 100 }
        }) 
        response.data.forEach(res => {
            const dataset = chartData.value.datasets.find((d: SensorDataset) => d.label === res.sensor_type)

            if(dataset) dataset.data.push({
                x: new Date(res.recorded_at).toLocaleTimeString(), 
                y: res.value
            })
        })
        triggerRef(chartData)
        chartKey.value++
    })
</script>