import { describe, it, expect } from 'vitest'
import { loginSchema, registerSchema } from '../app/composables/auth/useLoginForm'

describe('loginSchema', () => {
    it('正確的email和密碼應該要成功', () => {
        const result = loginSchema.safeParse({
            email: 'test@test.com',
            password: 'testpassword'
        })
        expect(result.success).toBe(true)
    })
    it('錯誤的email格式應該失敗', () => {        
        const result = loginSchema.safeParse({
            email: 'test@test',
            password: 'testpassword'
        })
        expect(result.success).toBe(false)   
        expect(result.error?.issues[0].message).toBe('請輸入有效的email')     
    })
    it('密碼少於6個字元應該失敗', () => {        
        const result = loginSchema.safeParse({
            email: 'test@test.com',
            password: 'err'
        })
        expect(result.success).toBe(false)
        expect(result.error?.issues[0].message).toBe('密碼至少6個字元')     
    })
})
describe('registerSchema', () => {
    it('正確的email和密碼和role應該要成功', () => {        
        const result = registerSchema.safeParse({
            email: 'test@test.com',
            password: 'testpassword',
            role: 'operator'
        })
        expect(result.success).toBe(true)
    })
    it('錯誤的role格式應該失敗', () => {        
        const result = registerSchema.safeParse({
            email: 'test@test.com',
            password: 'testpassword',
            role: 'error'
        })
        expect(result.success).toBe(false)         
    })
})