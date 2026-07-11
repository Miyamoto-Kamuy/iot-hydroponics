<template>
    <div class="flex-1 grid grid-cols-3 gap-2">
        <DashboardDeviceStatusGrid class="col-span-2" />
        <div class="grid grid-rows-3 gap-2">
            <DashboardSensorChart class="row-span-2" />
            <DashboardAlertList />
        </div>
    </div>
</template>

<script setup lang="ts">

</script>

<style scoped>

</style>