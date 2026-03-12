import axios from './axios'

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

export const adminApi = {
  getUsers: async (page = 1, pageSize = 20): Promise<UserListResponse> => {
    const response = await axios.get<UserListResponse>('/api/admin/users', {
      params: { page, page_size: pageSize },
    })
    return response.data
  },

  getUser: async (userId: number): Promise<UserAdmin> => {
    const response = await axios.get<UserAdmin>(`/api/admin/users/${userId}`)
    return response.data
  },

  createUser: async (data: CreateUserData): Promise<UserAdmin> => {
    const response = await axios.post<UserAdmin>('/api/admin/users', data)
    return response.data
  },

  updateUser: async (userId: number, data: UpdateUserData): Promise<UserAdmin> => {
    const response = await axios.put<UserAdmin>(`/api/admin/users/${userId}`, data)
    return response.data
  },

  deleteUser: async (userId: number): Promise<void> => {
    await axios.delete(`/api/admin/users/${userId}`)
  },
}
