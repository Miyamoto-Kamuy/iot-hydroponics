export default defineNuxtRouteMiddleware(async (to, from) => {
    const authStore = useAuthStore()
    if(authStore.isLoggingOut) return 
    await authStore.initAuth()
    if(authStore.isAuthenticated && to.path === '/login') return navigateTo('/dashboard')
    if(!authStore.isAuthenticated && to.path !== '/login') return navigateTo('/login')
    
    const isAdmin = authStore.user?.role === 'admin'
    const adminRoutes = ['/audit-logs', '/users']
    if(adminRoutes.includes(to.path) && !isAdmin) return navigateTo('/dashboard')
})