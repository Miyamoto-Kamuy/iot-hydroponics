import { type LoginRequest, type UserResponse, type UserCreate } from "~/types/user"

export const useAuthStore = defineStore('auth', () => {
    const api = useApi()
    const user = ref<UserResponse | null>(null)
    const login = async(credentials: LoginRequest) => {
        await api<{ message: string }>('/auth/login', {
            method: "POST", 
            body: credentials
        })        
        user.value = await api<UserResponse>('/users/me')    
    }
    const logout = () => {        
        user.value = null
        api('/auth/logout', { method: 'POST' })
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
        user, 
        login, logout, initAuth, register,
        isAuthenticated
    }
})