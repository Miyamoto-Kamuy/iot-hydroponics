import { useDebounceFn } from '@vueuse/core'

export const useUserList = () => {
    const userStore = useUserStore()
    const { users, total } = storeToRefs(userStore)
    const filterData = ref<{role: "admin" | "operator" | "viewer" | undefined, start: string | undefined, end: string | undefined, }>({
        role: undefined,         
        start: undefined, 
        end: undefined
    })        
    const currentPage = ref(1)
    const size = ref(20)
    
    const options=[
        { label: '全部', value: undefined },    
        { label: '管理者', value: 'admin' },
        { label: '操作者', value: 'operator' }, 
        { label: '觀看者', value: 'viewer' },
    ]
    
    const handleClearData = () => {
        filterData.value.role = undefined        
        filterData.value.start = undefined
        filterData.value.end = undefined
    }
    const fetchWithFilters = useDebounceFn(async () => {                        
        await userStore.fetchUsers({
            page: currentPage.value, 
            size: size.value,
            role: filterData.value.role,             
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
        await userStore.fetchUsers()
    })

    return {
        users, total, filterData, currentPage, size, options, handleClearData
    }
}