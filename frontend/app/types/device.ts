export type DeviceStatus = "offline" | "online"

export interface DeviceResponse {
    id: number
    name: string
    location: string
    status: DeviceStatus
    last_seen_at?: string
    created_at: string
    created_by: number
}

export interface DeviceCreate {
    name: string
    location: string
    status?: DeviceStatus
}

export interface DevicePatch {
    name?: string
    location?: string
    status?: DeviceStatus
}