export const useApi = (option?: { silent?: boolean }) => {
    const authStore = useAuthStore()
    const config = useRuntimeConfig()
    const toast = useToast()
    const isLoading = useState('globalLoading', () => false)

    return $fetch.create({
        baseURL: config.public.apiBase, 
        credentials: 'include',
        onRequest() {
            if(!option?.silent) isLoading.value = true
        }, 
        onResponse(){
            if(!option?.silent) isLoading.value = false
        },
        onResponseError({ request, response }) {
            if(!option?.silent) isLoading.value = false
            if(response.status === 401) {
                if(request.toString().includes('/auth/login')) return
                authStore.logout()
                navigateTo('/login')
                return
            }
            if(request.toString().includes('/auth')) return
            const detail = response._data?.detail || '發生未知錯誤'
            toast.add({
                title: `錯誤 ${response.status}`, 
                description: detail, 
                color: 'error'
            })
        }
    })
}