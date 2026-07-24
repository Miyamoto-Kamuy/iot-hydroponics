import { type LoginRequest, type UserResponse, type UserCreate } from "~/types/user"

export const useAuthStore = defineStore('auth', () => {
    const api = useApi()
    const user = ref<UserResponse | null>(null)
    const isLoggingOut = ref(false)
    const login = async(credentials: LoginRequest) => {
        await api<{ message: string }>('/auth/login', {
            method: "POST", 
            body: credentials
        })        
        user.value = await api<UserResponse>('/users/me')    
    }
    const logout = async () => {        
        isLoggingOut.value = true
        await api('/auth/logout', { method: 'POST' })
        user.value = null
        isLoggingOut.value = false
    }
    const initAuth = async() => {
        if(!user.value) {
            try {
                user.value = await api<UserResponse>('/users/me')
            } catch {
                console.log('token expired')
            }
        }
    }
    const register = async(credentials: UserCreate) => {
        await api<UserResponse>('/auth/register', {
            method: 'POST', 
            body: credentials
        })
        await login({ email: credentials.email, password: credentials.password})
    }
    const isAuthenticated = computed(() => !!user.value)

    return {
        user, isLoggingOut,
        login, logout, initAuth, register,
        isAuthenticated
    }
})