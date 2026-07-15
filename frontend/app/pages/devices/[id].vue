<template>
    <div class="flex flex-col flex-1 overflow-hidden">
        <div class="mb-4 shrink-0 cursor-pointer">
            <UButton class="cursor-pointer text-[var(--color-text-primary)]" variant="link" @click="navigateTo('/devices')">
                ← 返回設備列表
            </UButton>
        </div>
        <div class="flex-1 flex flex-col lg:grid lg:grid-cols-5 gap-2 overflow-hidden">
            <LazyDevicesDeviceDetail class="overflow-auto lg:col-span-1" />
            <LazyDevicesDeviceHistoryChart  class="flex-1 lg:col-span-4 overflow-hidden" />
        </div>
    </div>
</template>