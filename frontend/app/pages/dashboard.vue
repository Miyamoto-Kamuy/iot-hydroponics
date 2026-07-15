<template>
    <div class="flex-1 flex flex-col lg:grid lg:grid-cols-3 gap-2 overflow-hidden">
        <div class="flex flex-col lg:grid lg:grid-rows-3 gap-2 h-64 lg:h-auto lg:overflow-hidden">
            <LazyDashboardDeviceStatusGrid class="h-40 lg:h-auto lg:row-span-2 overflow-y-auto lg:overflow-hidden"
                @select-device="selectedDeviceId = $event" />
            <LazyDashboardAlertList class="h-24 lg:h-auto overflow-y-auto lg:overflow-hidden" />
        </div>
        <LazyDashboardSensorChart class="lg:col-span-2 overflow-hidden"
            :device-id="selectedDeviceId" />
    </div>
</template>

<script setup lang="ts">
    const selectedDeviceId = ref<number | null>(null)
</script>