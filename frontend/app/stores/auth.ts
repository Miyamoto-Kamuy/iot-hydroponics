import { type LoginResponse, type LoginRequest, type UserResponse, type UserCreate } from "~/types/user"

export const useAuthStore = defineStore('auth', () => {
    const api = useApi()
    const token = useCookie<string | null>('token', {
        maxAge: 60 * 60,
        sameSite: 'strict'
    })
    const user = ref<UserResponse | null>(null)
    const login = async(credentials: LoginRequest) => {
        const response = await api<LoginResponse>('/auth/login', {
            method: "POST", 
            body: credentials
        })
        token.value = response.access_token    
        user.value = await api<UserResponse>('/users/me')    
    }
    const logout = () => {
        token.value = null
        user.value = null
    }
    const initAuth = async() => {
        if(token.value && !user.value) {
            try {
                user.value = await api<UserResponse>('/users/me')
            } catch {
                token.value = null
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
    const isAuthenticated = computed(() => !!token.value)

    return {
        token, user, 
        login, logout, initAuth, register,
        isAuthenticated
    }
})