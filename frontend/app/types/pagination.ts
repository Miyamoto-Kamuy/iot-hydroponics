export interface PaginateResponse<T> {
    data: T[]
    total: number
    page: number
    size: number
}