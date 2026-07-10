export const useApi = () => {
    const authStore = useAuthStore()
    const config = useRuntimeConfig()

    return $fetch.create({
        baseURL: config.public.apiBase, 
        onRequest({options}) {
            if(authStore.token) {
                options.headers = new Headers(options.headers as HeadersInit);
                options.headers.set('Authorization',  `Bearer ${authStore.token}`)                
            }
        }, 
        onResponseError({response}) {
            if(response.status === 401) {
                authStore.logout()
                navigateTo('/login')
            }
        }
    })
}