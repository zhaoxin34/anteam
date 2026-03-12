export interface UserAdmin {
  id: number
  email: string
  username: string
  full_name: string | null
  is_active: boolean
  is_superuser: boolean
  created_at: string
}

export interface UserListResponse {
  items: UserAdmin[]
  total: number
  page: number
  page_size: number
}

export interface CreateUserData {
  email: string
  username: string
  password: string
  full_name?: string
  is_active?: boolean
  is_superuser?: boolean
}

export interface UpdateUserData {
  email?: string
  username?: string
  full_name?: string
  is_active?: boolean
  is_superuser?: boolean
}
