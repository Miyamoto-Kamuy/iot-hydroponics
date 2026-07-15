import { Chart as ChartJS, LineElement, PointElement, LinearScale, CategoryScale, Title, Tooltip, Legend } from 'chart.js'

export type SensorDataset = {
    label: string
    data: { x: string, y: number }[]
    borderColor: string
}

export const useChartBase = () => {
    ChartJS.register(LineElement, PointElement, LinearScale, CategoryScale, Title, Tooltip, Legend)

    const chartKey = ref(0)
    const selectedTab = ref('temperature')

    const tabItems = [
        { label: '溫度', value: 'temperature' },
        { label: '濕度', value: 'humidity' },
        { label: 'pH', value: 'ph' },
        { label: '水位', value: 'water_level' },
    ]

    const chartOptions = ref({
        responsive: true,
        maintainAspectRatio: false,
        parsing: { xAxisKey: 'x', yAxisKey: 'y' },
        plugins: {
            legend: { display: false },
            tooltip: { enabled: true }
        },
        scales: { 
            x: {
                grid: { color: 'rgba(254, 250, 224, 0.1)'}, 
                ticks: { color: '#FEFAE0'}
            },
            y: { 
                beginAtZero: false, 
                grid: { color: 'rgba(254, 250, 224, 0.1)'}, 
                ticks: { color: '#FEFAE0'}
            } 
        }
    })
    const chartData = shallowRef<any>({
        datasets: [
            { label: 'temperature', data: [], borderColor: '#FF6B6B' },
            { label: 'humidity', data: [], borderColor: '#4ECDC4' },
            { label: 'ph', data: [], borderColor: '#FFE66D' },
            { label: 'water_level', data: [], borderColor: '#6BB5FF' },
        ]
    })

    const currentChartData = computed(() => {
        chartKey.value
        const dataset = chartData.value.datasets.find((d: SensorDataset) => d.label === selectedTab.value)
        return { datasets: dataset ? [dataset] : [] }
    })

    return {
        chartKey, selectedTab, tabItems, chartOptions, chartData, currentChartData
    }
}