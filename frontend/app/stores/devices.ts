import { type DeviceResponse } from '~/types/device'
import { type PaginateResponse } from '~/types/pagination'

export const useDeviceStore = defineStore('device', () => {
    const devices = ref<DeviceResponse[] | null>(null)
    const currentDevice = ref<DeviceResponse | null>(null)    
    const api = useApi()
    const fetchDevices = async () => {
        const response: PaginateResponse<DeviceResponse> = await api('/devices')
        devices.value = response.data
    }
    const fetchDevice = async (id: number) => {        
        const response: DeviceResponse = await api(`/devices/${id}`)
        currentDevice.value = response
    }

    return {
        devices, currentDevice, 
        fetchDevices, fetchDevice
    }
})