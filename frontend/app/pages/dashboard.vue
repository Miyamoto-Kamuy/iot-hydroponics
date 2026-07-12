<template>
    <div class="flex-1 grid grid-cols-3 gap-2">
        <div class="grid grid-rows-3 gap-2">
            <DashboardDeviceStatusGrid class="row-span-2"
                @select-device="selectedDeviceId = $event" />
            <DashboardAlertList />
        </div>
        <DashboardSensorChart class="col-span-2"
            :device-id="selectedDeviceId" />
    </div>
</template>

<script setup lang="ts">
    const selectedDeviceId = ref<number | null>(null)
</script>

<style scoped>

</style>