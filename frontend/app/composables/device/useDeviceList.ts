import { useDebounceFn } from '@vueuse/core'

export const useDeviceList = () => {
    const deviceStore = useDeviceStore()
    const { devices, total } = storeToRefs(deviceStore)
    const filterData = ref<{location: string, status: 'online' | 'offline' | undefined}>({
        location: '', 
        status: undefined,
    })        
    const currentPage = ref(1)
    const size = ref(20)
    const isLoading = ref(false)
    const isEmpty = computed(() => !devices.value || devices.value.length === 0)
    
    const options=[
        { label: '全部', value: undefined },    
        { label: '在線', value: 'online' },
        { label: '離線', value: 'offline' }
    ]
    
    const handleClearData = () => {
        filterData.value.location = ''
        filterData.value.status = undefined
    }
    const fetchWithFilters = useDebounceFn(async () => {   
        isLoading.value = true
        try{
            await deviceStore.fetchDevices({
                page: currentPage.value, 
                size: size.value,
                location: filterData.value.location || undefined, 
                status: filterData.value.status
            })
        } finally {
            isLoading.value = false
        }        
    }, 500)
    
    watch(filterData, async () => {
        currentPage.value = 1
        await fetchWithFilters()
    }, { deep: true })   
    watch(currentPage, fetchWithFilters) 
    
    onMounted(async () => {
        isLoading.value = true
        try {
            await deviceStore.fetchDevices()
        } finally {
            isLoading.value = false
        }
    })

    return {
        devices, total, isLoading, isEmpty,filterData, currentPage, size, options, handleClearData
    }
}