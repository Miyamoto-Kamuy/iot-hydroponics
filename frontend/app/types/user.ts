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

export interface LoginResponse {
    access_token: string
    token_type: string
    expires_in: number
}

export interface UserPatch {
    password?: string
}

export interface UserAdminPatch {
    role?: Role
}