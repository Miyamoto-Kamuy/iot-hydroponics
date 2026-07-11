export const useApi = () => {
    const authStore = useAuthStore()
    const config = useRuntimeConfig()
    const toast = useToast()

    return $fetch.create({
        baseURL: config.public.apiBase, 
        onRequest({ options }) {
            if(authStore.token) {
                options.headers = new Headers(options.headers as HeadersInit);
                options.headers.set('Authorization',  `Bearer ${authStore.token}`)                
            }
        }, 
        onResponseError({ request, response }) {
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