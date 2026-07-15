import { describe, it, expect, vi, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia' 
import { useAlertStore } from '../app/stores/alert'

describe('useAlertStore', () => {
    beforeEach(() => {
        setActivePinia(createPinia())
    })

    it('updateAlertStatus 成功時應該更新本地UI狀態', async () => {

    })
    it('updateAlertStatus 失敗時應該還原本地UI狀態', async () => {
        
    })
})