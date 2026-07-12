<template>
    <div class="flex-1 grid grid-cols-3 gap-2 overflow-hidden">
        <div class="grid grid-rows-3 gap-2 overflow-hidden">
            <DashboardDeviceStatusGrid class="row-span-2 overflow-hidden"
                @select-device="selectedDeviceId = $event" />
            <DashboardAlertList class="overflow-hidden" />
        </div>
        <DashboardSensorChart class="col-span-2 overflow-hidden"
            :device-id="selectedDeviceId" />
    </div>
</template>

<script setup lang="ts">
    const selectedDeviceId = ref<number | null>(null)
</script>

<style scoped>

</style>