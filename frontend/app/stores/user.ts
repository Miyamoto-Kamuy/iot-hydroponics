import { type UserResponse, type UserPatch, type UserAdminPatch } from '~/types/user'
import { type PaginateResponse } from '~/types/pagination'

export const useUserStore = defineStore('user', () => {
    const users = ref<UserResponse[] | null>(null)
    const total = ref(0)
    const currentUserProfile = ref<UserResponse | null>(null)    
    const currentUser = ref<UserResponse | null>(null)    
    const api = useApi()
    const fetchUsers = async ({
        page = 1, 
        size = 20, 
        role,
        start, 
        end
    }: {
        page?: number, 
        size?: number, 
        role?: 'admin' | 'operator' | 'viewer',         
        start?: string, 
        end?: string
    } = {}) => {
        const response: PaginateResponse<UserResponse> = await api('/users', { params: { page, size, role, start, end }})
        users.value = response.data
        total.value = response.total
    }
    const fetchMe = async () => {        
        const response: UserResponse = await api(`/users/me`)
        currentUserProfile.value = response
    }    
    const fetchUser = async (id: number) => {        
        const response: UserResponse = await api(`/users/${id}`)
        currentUser.value = response
    }    
    const updateMe = async(id: number, data: UserPatch) => {        
        const response: UserResponse = await api(`/users/me`, {
            method: 'PATCH', 
            body: data
        })
        currentUserProfile.value = response
    }
    const updateUser = async(id: number, data: UserAdminPatch) => {        
        const response: UserResponse = await api(`/users/${id}`, {
            method: 'PATCH', 
            body: data
        })
        currentUser.value = response
    }

    return {
        users, currentUser, currentUserProfile, total,
        fetchUsers, fetchUser, fetchMe, updateMe, updateUser
    }
})