export type Role = "admin" | "operator" | "viewer"

export interface UserCreate {
    email: string
    password: string
    role: "operator" | "viewer"
}

export interface UserResponse {
    id: number
    email: string
    role: Role
    created_at: string
}

export interface LoginRequest {
    email: string
    password: string
}

export interface UserPatch {
    password?: string
}

export interface UserAdminPatch {
    role?: Role
}