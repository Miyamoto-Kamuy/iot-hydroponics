import { useDebounceFn } from '@vueuse/core'

export const useAuditLogList = () => {
    const auditLogStore = useAuditLogStore()
    const { auditLogs, total } = storeToRefs(auditLogStore)
    const filterData = ref<{action: "CREATE" | "UPDATE" | "DELETE" | undefined, resource: string | undefined, resource_id: number | undefined, status_code: number | undefined, performed_by: number | undefined, start: string | undefined, end: string | undefined, }>({
        action: undefined, 
        resource: undefined,
        resource_id: undefined,
        status_code: undefined,
        performed_by: undefined,
        start: undefined, 
        end: undefined
    })        
    const currentPage = ref(1)
    const size = ref(20)
    
    const actionOptions=[
        { label: '全部', value: undefined },    
        { label: '建立', value: 'CREATE' },
        { label: '更新', value: 'UPDATE' }, 
        { label: '刪除', value: 'DELETE' },
    ]
    
    const handleClearData = () => {
        filterData.value.action = undefined
        filterData.value.resource = undefined
        filterData.value.resource_id = undefined
        filterData.value.status_code = undefined
        filterData.value.performed_by = undefined
        filterData.value.start = undefined
        filterData.value.end = undefined
    }
    const fetchWithFilters = useDebounceFn(async () => {                        
        await auditLogStore.fetchAuditLogs({
            page: currentPage.value, 
            size: size.value,
            action: filterData.value.action, 
            resource: filterData.value.resource, 
            resource_id: filterData.value.resource_id || undefined, 
            status_code: filterData.value.status_code || undefined, 
            performed_by: filterData.value.performed_by || undefined, 
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
        await auditLogStore.fetchAuditLogs()
    })

    return {
        auditLogs, total, filterData, currentPage, size, actionOptions, handleClearData
    }
}