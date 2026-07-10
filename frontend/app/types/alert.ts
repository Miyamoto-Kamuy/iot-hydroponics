export type AlertStatus = "unread" | "read" | "resolved"

export interface AlertResponse {
    id: number
    sensor_type: string
    message: string
    status: AlertStatus
    triggered_at: string
    device_id: number
}           

export interface AlertPatch {
    status?: AlertStatus
}