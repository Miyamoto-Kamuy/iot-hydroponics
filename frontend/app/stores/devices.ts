import { type DeviceResponse, type DeviceCreate, type DevicePatch } from '~/types/device'
import { type PaginateResponse } from '~/types/pagination'

export const useDeviceStore = defineStore('device', () => {
    const devices = ref<DeviceResponse[] | null>(null)
    const total = ref(0)
    const currentDevice = ref<DeviceResponse | null>(null)    
    const api = useApi()
    const fetchDevices = async ({
        page = 1, 
        size = 20, 
        location, 
        status, 
        created_by, 
        start, 
        end
    }: {
        page?: number, 
        size?: number, 
        location?: string, 
        status?: 'online' | 'offline', 
        created_by?: number, 
        start?: string, 
        end?: string
    } = {}) => {
        const response: PaginateResponse<DeviceResponse> = await api('/devices', { params: { page, size, location, status, created_by, start, end }})
        devices.value = response.data
        total.value = response.total
    }
    const fetchDevice = async (id: number) => {        
        const response: DeviceResponse = await api(`/devices/${id}`)
        currentDevice.value = response
    }
    const createDevice = async(data: DeviceCreate) => {        
        const response: DeviceResponse = await api(`/devices`, {
            method: 'POST', 
            body: data
        })
        if(devices.value) devices.value.push(response)
    }
    const updateDevice = async(id: number, data: DevicePatch) => {        
        const response: DeviceResponse = await api(`/devices/${id}`, {
            method: 'PATCH', 
            body: data
        })
        currentDevice.value = response
    }
    const deleteDevice = async(id: number) => {        
        await api(`/devices/${id}`, { method: 'DELETE' })
        currentDevice.value = null
    }

    return {
        devices, currentDevice, total,
        fetchDevices, fetchDevice, createDevice, updateDevice, deleteDevice
    }
})