import { type AuditLogResponse } from '~/types/audit-log'
import { type PaginateResponse } from '~/types/pagination'

export const useAuditLogStore = defineStore('audit-log', () => {
    const auditLogs = ref<AuditLogResponse[] | null>(null)    
    const total = ref(0)
    const currentAuditLog = ref<AuditLogResponse | null>(null)    
    const api = useApi()
    const fetchAuditLogs = async ({
        page = 1,
        size = 20,
        action, 
        resource, 
        resource_id, 
        status_code, 
        performed_by, 
        start, 
        end,
    }: {
        page?: number,
        size?: number,
        action?: string, 
        resource?: string, 
        resource_id?: number, 
        status_code?: number, 
        performed_by?: number, 
        start?: string, 
        end?: string,
    } = {}) => {
        const response: PaginateResponse<AuditLogResponse> = await api('/audit-logs', { params: { page, size, action, resource, resource_id, status_code, performed_by, start, end }})
        auditLogs.value = response.data
        total.value = response.total
    }
    const fetchAuditLog = async (id: number) => {        
        const response: AuditLogResponse = await api(`/audit-logs/${id}`)
        currentAuditLog.value = response
    }

    return {
        auditLogs, currentAuditLog, total, 
        fetchAuditLogs, fetchAuditLog
    }
})