
import { useWebSocket } from '@vueuse/core'
import { Chart as ChartJS, LineElement, PointElement, LinearScale, CategoryScale, Title, Tooltip, Legend } from 'chart.js'
export const useSensorChart = (deviceId: Ref<number | null>) => {
    ChartJS.register(LineElement, PointElement, LinearScale, CategoryScale, Title, Tooltip, Legend)    
    type SensorDataset = {
        label: string
        data: { x: string, y: number }[]
        borderColor: string
    }
    const authStore = useAuthStore()    
    const { token } = storeToRefs(authStore)
    const chartKey = ref(0)
    const selectedTab = ref('temperature')
    const tabItems = [
        { label: '溫度', value: 'temperature'}, 
        { label: '濕度', value: 'humidity'}, 
        { label: 'pH', value: 'ph'}, 
        { label: '水位', value: 'water_level'}, 
    ]
    const chartOptions = ref({
        responsive: true, 
        maintainAspectRatio: false, 
        parsing: {
            xAxisKey: 'x', 
            yAxisKey: 'y'
        },
        plugins: {
            legend: {
                display: true, 
                position: 'top' as const,
            }, 
            tooltip: {
                enabled: true
            }
        }, 
        scales: {
            y: {
                beginAtZero: false
            }
        }
    })
    const chartData = shallowRef<any>({
        datasets: [
            { label: 'temperature', data: [], borderColor: 'red' },
            { label: 'humidity', data: [], borderColor: 'blue' },
            { label: 'ph', data: [], borderColor: 'green' },
            { label: 'water_level', data: [], borderColor: 'purple' },
        ]
    })
    const currentChartData = computed(() => {
        chartKey.value
        const currentSensor = selectedTab.value
        const dataset = chartData.value.datasets.find((d: SensorDataset) => d.label === currentSensor)
        return {
            datasets: dataset ? [dataset] : []
        }
    })

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