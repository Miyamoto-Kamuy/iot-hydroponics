<template>
    <div class="flex flex-col flex-1 overflow-hidden">
        <div class="mb-4 shrink-0 cursor-pointer">
            <UButton class="cursor-pointer" variant="link" @click="navigateTo('/devices')">
                ← 返回設備列表
            </UButton>
        </div>
        <div class="flex-1 grid grid-cols-5 gap-2 overflow-hidden">
            <DevicesDeviceDetail class="overflow-auto" />
            <DevicesDeviceHistoryChart  class="col-span-4 overflow-hidden" />
        </div>
    </div>
</template>