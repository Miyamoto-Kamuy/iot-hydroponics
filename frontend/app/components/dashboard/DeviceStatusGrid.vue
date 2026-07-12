<template>
    <div class="bg-inverted w-full h-full rounded px-4 py-2">
        <div v-for="device in devices" :key="device.id" 
             @click="selectDevice(device.id)">
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
    const emit = defineEmits(['select-device'])
    const selectDevice = (id: number) => {
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