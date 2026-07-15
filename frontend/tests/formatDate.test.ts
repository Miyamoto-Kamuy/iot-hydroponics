import { describe, it, expect } from 'vitest'
import { formatDate } from '../app/utils/formatDate'

describe('formatDate', () => {
    it('應該把ISO字串轉成可讀的日期格式', () => {
        const time = '2026-07-15T14:24:08.000Z'
        const result = formatDate(time)
        expect(result).not.toBe('--')
        expect(result).toContain('2026')
        expect(result).toContain('07')
        expect(result).toContain('15')        
    })
    it('當傳入 undefined 時應該回傳 --', () => {
        const errorTime = undefined
        const result = formatDate(errorTime)
        expect(result).toBe('--')
    })
})