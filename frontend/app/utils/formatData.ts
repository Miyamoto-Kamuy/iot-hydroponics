export const formatDate = (dateString: string | undefined) => {
    if(!dateString) return '--'

    return new Date(dateString).toLocaleString('zh-TW', {
        year: 'numeric', 
        month: '2-digit', 
        day: '2-digit', 
        hour: '2-digit', 
        minute: '2-digit', 
        second: '2-digit', 
    })
}