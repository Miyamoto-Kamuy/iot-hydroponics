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
            legend: { display: true, position: 'top' as const },
            tooltip: { enabled: true }
        },
        scales: { y: { beginAtZero: false } }
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
        const dataset = chartData.value.datasets.find((d: SensorDataset) => d.label === selectedTab.value)
        return { datasets: dataset ? [dataset] : [] }
    })

    return {
        chartKey, selectedTab, tabItems, chartOptions, chartData, currentChartData
    }
}