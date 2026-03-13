import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit'
import { workspaceApi, Workspace, CreateWorkspaceData, UpdateWorkspaceData } from '../api/workspace'

interface WorkspaceState {
  workspaces: Workspace[]
  total: number
  loading: boolean
  error: string | null
  selectedWorkspace: Workspace | null
}

const initialState: WorkspaceState = {
  workspaces: [],
  total: 0,
  loading: false,
  error: null,
  selectedWorkspace: null,
}

export const fetchWorkspaces = createAsyncThunk('workspace/fetchWorkspaces', async () => {
  const response = await workspaceApi.getWorkspaces()
  return response
})

export const createWorkspace = createAsyncThunk(
  'workspace/createWorkspace',
  async (data: CreateWorkspaceData) => {
    const response = await workspaceApi.createWorkspace(data)
    return response
  }
)

export const updateWorkspace = createAsyncThunk(
  'workspace/updateWorkspace',
  async ({ workspaceId, data }: { workspaceId: number; data: UpdateWorkspaceData }) => {
    const response = await workspaceApi.updateWorkspace(workspaceId, data)
    return response
  }
)

export const deleteWorkspace = createAsyncThunk(
  'workspace/deleteWorkspace',
  async (workspaceId: number) => {
    await workspaceApi.deleteWorkspace(workspaceId)
    return workspaceId
  }
)

export const joinWorkspace = createAsyncThunk(
  'workspace/joinWorkspace',
  async (workspaceId: number) => {
    const response = await workspaceApi.joinWorkspace(workspaceId)
    return response
  }
)

export const leaveWorkspace = createAsyncThunk(
  'workspace/leaveWorkspace',
  async (workspaceId: number) => {
    await workspaceApi.leaveWorkspace(workspaceId)
    return workspaceId
  }
)

const workspaceSlice = createSlice({
  name: 'workspace',
  initialState,
  reducers: {
    setSelectedWorkspace: (state, action: PayloadAction<Workspace | null>) => {
      state.selectedWorkspace = action.payload
    },
    clearError: (state) => {
      state.error = null
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch workspaces
      .addCase(fetchWorkspaces.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(fetchWorkspaces.fulfilled, (state, action) => {
        state.loading = false
        state.workspaces = action.payload.items
        state.total = action.payload.total
      })
      .addCase(fetchWorkspaces.rejected, (state, action) => {
        state.loading = false
        state.error = action.error.message || 'Failed to fetch workspaces'
      })
      // Create workspace
      .addCase(createWorkspace.fulfilled, (state, action) => {
        state.workspaces.push(action.payload)
        state.total += 1
      })
      // Update workspace
      .addCase(updateWorkspace.fulfilled, (state, action) => {
        const index = state.workspaces.findIndex((w) => w.id === action.payload.id)
        if (index !== -1) {
          state.workspaces[index] = action.payload
        }
      })
      // Delete workspace
      .addCase(deleteWorkspace.fulfilled, (state, action) => {
        state.workspaces = state.workspaces.filter((w) => w.id !== action.payload)
        state.total -= 1
      })
      // Join workspace
      .addCase(joinWorkspace.fulfilled, (state, action) => {
        const exists = state.workspaces.find((w) => w.id === action.payload.id)
        if (!exists) {
          state.workspaces.push(action.payload)
          state.total += 1
        }
      })
      // Leave workspace
      .addCase(leaveWorkspace.fulfilled, (state, action) => {
        state.workspaces = state.workspaces.filter((w) => w.id !== action.payload)
        state.total -= 1
      })
  },
})

export const { setSelectedWorkspace, clearError } = workspaceSlice.actions
export default workspaceSlice.reducer
