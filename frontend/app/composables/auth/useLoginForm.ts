import { z } from 'zod';    
export const useLoginForm = () => {
    const authStore = useAuthStore()    
    const toast = useToast()
    const isLoginPage = ref(true)    
    const data = ref({
        email: '', 
        password: '',
        role: 'viewer' as 'operator' | 'viewer'
    })
    const loginSchema = z.object({
        email: z.email('請輸入有效的email'), 
        password: z.string().min(6, '密碼至少6個字元')
    })
    const registerSchema = z.object({
        email: z.email('請輸入有效的email'), 
        password: z.string().min(6, '密碼至少6個字元'), 
        role: z.enum(['operator', 'viewer'])
    })
    const schema = computed(() => isLoginPage.value ? loginSchema : registerSchema)    
    const options=[
        { label: '操作者', value: 'operator' },
        { label: '檢視者', value: 'viewer' }
    ]
    const onSubmit = async () => {
        try {
            if(isLoginPage.value) {
                await authStore.login({
                    email: data.value.email, 
                    password: data.value.password
                })                
            } else {
                await authStore.register(data.value)
            } 
            await navigateTo('/dashboard')
        } catch (error: any) {
            console.error(`錯誤： ${error.data.detail}`)
            toast.add({
                title: isLoginPage.value ? '登入失敗' : '註冊失敗',
                description: error?.data?.detail || '帳號或密碼錯誤',
                color: 'error'
            })
        }
    }
    const defaultData = () => {
        data.value.email = ''
        data.value.password = ''
        data.value.role = 'viewer'
    }
    const handleSwitchAuth = () => {
        defaultData()
        isLoginPage.value = !isLoginPage.value
    }
    return {
        isLoginPage, 
        data, 
        schema, 
        options, 
        onSubmit, 
        handleSwitchAuth
    }
}