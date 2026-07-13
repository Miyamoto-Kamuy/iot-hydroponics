
import { useWebSocket } from '@vueuse/core'

export const useSensorChart = (deviceId: Ref<number | null>) => {    
    const { chartKey, selectedTab, tabItems, chartOptions, chartData, currentChartData } = useChartBase()
    const authStore = useAuthStore()    
    const { token } = storeToRefs(authStore)    

    const wsUrl = computed(() => {
        if(!deviceId.value) return undefined        

        return `ws://localhost:8000/ws/devices/${deviceId.value}?token=${token.value}`
    })
    const { data } = useWebSocket(wsUrl, {
        autoReconnect: true, 
        immediate: false
    })
    watch(data, (newData) => {
        if(!newData || newData === 'undefined') return
        try {
            const parsed = JSON.parse(newData)            

            const dataset = chartData.value.datasets.find((data: SensorDataset) => data.label === parsed.sensor_type)
            if(dataset) {
                dataset.data.push({
                    x: new Date(parsed.recorded_at).toLocaleTimeString(), 
                    y: parsed.value
                })
                if(dataset.data.length > 15) dataset.data.shift()
            }       
            triggerRef(chartData)    
            chartKey.value++ 
        } catch(e) {
            console.error('JSON parse error:', e)
        }     
    })
    watch(deviceId, () => {
        chartData.value.datasets.forEach((d: SensorDataset) => {
            d.data = []
        })
        triggerRef(chartData)
        chartKey.value++
    })

    return {
        chartKey, 
        selectedTab, 
        tabItems, 
        chartOptions, 
        currentChartData
    }
}