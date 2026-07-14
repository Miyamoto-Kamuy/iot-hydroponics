import { type AlertResponse, type AlertPatch } from '~/types/alert'
import { type PaginateResponse } from '~/types/pagination'

export const useAlertStore = defineStore('alert', () => {
    const alerts = ref<AlertResponse[] | null>(null)    
    const total = ref(0)
    const currentAlert = ref<AlertResponse | null>(null)    
    const api = useApi()
    const fetchAlerts = async ({
        page = 1,
        size = 20,
        device_id,
        sensor_type,
        status,
        start,
        end,
    }: {
        page?: number,
        size?: number,
        device_id?: number,
        sensor_type?: 'temperature' | 'humidity' | 'ph' | 'water_level',
        status?: "unread" | "read" | "resolved",
        start?: string,
        end?: string,
    } = {}) => {
        const response: PaginateResponse<AlertResponse> = await api('/alerts', { params: { page, size, device_id, sensor_type, status, start, end }})
        alerts.value = response.data
        total.value = response.total
    }
    const fetchAlert = async (id: number) => {        
        const response: AlertResponse = await api(`/alerts/${id}`)
        currentAlert.value = response
    }
    const updateAlertStatus = async (id: number, status: 'read' | 'resolved') => {
        await api(`alerts/${id}`, {
            method: 'PATCH', 
            body: { status } as AlertPatch
        })
        if(alerts.value) {
            const alert = alerts.value.find(a => a.id === id)
            if(alert) alert.status = status
        }
    }

    return {
        alerts, currentAlert, total, 
        fetchAlerts, fetchAlert, updateAlertStatus
    }
})