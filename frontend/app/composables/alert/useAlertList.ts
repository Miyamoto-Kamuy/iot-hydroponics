import { useDebounceFn } from '@vueuse/core'

export const useAlertList = () => {
    const alertStore = useAlertStore()
    const { alerts, total } = storeToRefs(alertStore)
    const filterData = ref<{sensor_type: 'temperature' | 'humidity' | 'ph' | 'water_level' | undefined, status: 'unread' | 'read' | 'resolved' | undefined, device_id: number | undefined, start: string | undefined, end: string | undefined, }>({
        sensor_type: undefined, 
        status: undefined,
        device_id: undefined,
        start: undefined, 
        end: undefined
    })        
    const currentPage = ref(1)
    const size = ref(20)
    
    const sensorTypeOptions=[
        { label: '全部', value: undefined },    
        { label: '溫度', value: 'temperature' },
        { label: '濕度', value: 'humidity' }, 
        { label: 'pH值', value: 'ph' },
        { label: '水位', value: 'water_level' }, 
    ]
    const statusOptions=[
        { label: '全部', value: undefined },    
        { label: '未讀', value: 'unread' },
        { label: '已讀', value: 'read' }, 
        { label: '已解決', value: 'resolved' }, 
    ]
    
    const handleClearData = () => {
        filterData.value.sensor_type = undefined
        filterData.value.status = undefined
        filterData.value.device_id = undefined
        filterData.value.start = undefined
        filterData.value.end = undefined
    }
    const fetchWithFilters = useDebounceFn(async () => {                        
        await alertStore.fetchAlerts({
            page: currentPage.value, 
            size: size.value,
            sensor_type: filterData.value.sensor_type, 
            status: filterData.value.status, 
            device_id: filterData.value.device_id || undefined, 
            start: filterData.value.start || undefined, 
            end: filterData.value.end || undefined, 
        })
    }, 500)
    
    watch(filterData, async () => {
        currentPage.value = 1
        await fetchWithFilters()
    }, { deep: true })   
    watch(currentPage, fetchWithFilters) 
    
    onMounted(async () => {
        await alertStore.fetchAlerts()
    })

    return {
        alerts, total, filterData, currentPage, size, sensorTypeOptions, statusOptions, handleClearData
    }
}