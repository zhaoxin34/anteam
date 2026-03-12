import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit'
import { adminApi, UserAdmin, UserListResponse, CreateUserData, UpdateUserData } from '../api/admin'

interface AdminState {
  users: UserAdmin[]
  total: number
  page: number
  pageSize: number
  loading: boolean
  error: string | null
  selectedUser: UserAdmin | null
}

const initialState: AdminState = {
  users: [],
  total: 0,
  page: 1,
  pageSize: 20,
  loading: false,
  error: null,
  selectedUser: null,
}

export const fetchUsers = createAsyncThunk(
  'admin/fetchUsers',
  async ({ page, pageSize }: { page: number; pageSize: number }) => {
    const response = await adminApi.getUsers(page, pageSize)
    return response
  }
)

export const createUser = createAsyncThunk('admin/createUser', async (data: CreateUserData) => {
  const response = await adminApi.createUser(data)
  return response
})

export const updateUser = createAsyncThunk(
  'admin/updateUser',
  async ({ userId, data }: { userId: number; data: UpdateUserData }) => {
    const response = await adminApi.updateUser(userId, data)
    return response
  }
)

export const deleteUser = createAsyncThunk('admin/deleteUser', async (userId: number) => {
  await adminApi.deleteUser(userId)
  return userId
})

const adminSlice = createSlice({
  name: 'admin',
  initialState,
  reducers: {
    setSelectedUser: (state, action: PayloadAction<UserAdmin | null>) => {
      state.selectedUser = action.payload
    },
    clearError: (state) => {
      state.error = null
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch users
      .addCase(fetchUsers.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(fetchUsers.fulfilled, (state, action: PayloadAction<UserListResponse>) => {
        state.loading = false
        state.users = action.payload.items
        state.total = action.payload.total
        state.page = action.payload.page
        state.pageSize = action.payload.page_size
      })
      .addCase(fetchUsers.rejected, (state, action) => {
        state.loading = false
        state.error = action.error.message || 'Failed to fetch users'
      })
      // Create user
      .addCase(createUser.fulfilled, (state, action: PayloadAction<UserAdmin>) => {
        state.users.push(action.payload)
        state.total += 1
      })
      // Update user
      .addCase(updateUser.fulfilled, (state, action: PayloadAction<UserAdmin>) => {
        const index = state.users.findIndex((u) => u.id === action.payload.id)
        if (index !== -1) {
          state.users[index] = action.payload
        }
      })
      // Delete user
      .addCase(deleteUser.fulfilled, (state, action: PayloadAction<number>) => {
        state.users = state.users.filter((u) => u.id !== action.payload)
        state.total -= 1
      })
  },
})

export const { setSelectedUser, clearError } = adminSlice.actions
export default adminSlice.reducer
