export interface AuditLogResponse {
    id: number
    action: string
    resource: string
    resource_id?: number
    detail?: Record<string, unknown>
    status_code: number
    error_detail?: string
    performed_at: string
    performed_by?: number
}