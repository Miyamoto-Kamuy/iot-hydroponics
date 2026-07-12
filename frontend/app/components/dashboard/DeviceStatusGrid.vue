<template>
    <div class="bg-inverted w-full h-full rounded px-4 py-2 flex flex-col gap-2 overflow-auto">
        <div v-for="device in devices" :key="device.id" 
             @click="selectDevice(device.id)"
             class="p-2 rounded bg-[#1da1f2] cursor-pointer"
             :class="selectedDeviceId === device.id ? 'bg-[#1da1f2]' : 'bg-blue-200'">
            <div>狀態</div>
            <div class="flex">
                <p>{{ device.name }}</p>
                <p>{{ device.location }}</p>
                <p>{{ device.last_seen_at ?? '--' }}</p>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { useIntervalFn } from '@vueuse/core'
    const deviceStore = useDeviceStore()
    const { devices } = storeToRefs(deviceStore)
    const selectedDeviceId = ref<number | null>(null) 
    const emit = defineEmits(['select-device'])
    const selectDevice = (id: number) => {        
        selectedDeviceId.value = id
        emit('select-device', id)
    }

    onMounted(async () => {
        await deviceStore.fetchDevices()
        const firstDevice = devices.value?.[0]        
        if(firstDevice) {
            emit('select-device', firstDevice.id)
        }
    })

    useIntervalFn(async () => {
        await deviceStore.fetchDevices()
    }, 30000)
</script>

<style scoped>

</style>