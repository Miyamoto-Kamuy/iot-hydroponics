import { type AlertResponse, type AlertPatch } from '~/types/alert'
import { type PaginateResponse } from '~/types/pagination'

export const useAlertStore = defineStore('alert', () => {
    const alerts = ref<AlertResponse[] | null>(null)    
    const currentAlert = ref<AlertResponse | null>(null)    
    const api = useApi()
    const fetchAlerts = async () => {
        const response: PaginateResponse<AlertResponse> = await api('/alerts')
        alerts.value = response.data
    }
    const fetchAlert = async (id: number) => {        
        const response: AlertResponse = await api(`/alerts/${id}`)
        currentAlert.value = response
    }
    const markAsRead = async (id: number) => {
        await api(`alerts/${id}`, {
            method: 'PATCH', 
            body: { status: 'read' } as AlertPatch
        })
        if(alerts.value) {
            const alert = alerts.value.find(a => a.id === id)
            if(alert) alert.status = 'read'
        }
    }

    return {
        alerts, currentAlert, 
        fetchAlerts, fetchAlert, markAsRead
    }
})