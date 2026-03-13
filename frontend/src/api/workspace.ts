import axios from './axios'

export interface Workspace {
  id: number
  name: string
  description: string | null
  owner_id: number
  created_at: string
}

export interface WorkspaceMember {
  id: number
  workspace_id: number
  user_id: number
  role: string
  joined_at: string
}

export interface CreateWorkspaceData {
  name: string
  description?: string
}

export interface UpdateWorkspaceData {
  name?: string
  description?: string
}

export interface WorkspaceListResponse {
  items: Workspace[]
  total: number
}

export const workspaceApi = {
  getWorkspaces: async (): Promise<WorkspaceListResponse> => {
    const response = await axios.get<WorkspaceListResponse>('/api/workspaces')
    return response.data
  },

  getWorkspace: async (workspaceId: number): Promise<Workspace> => {
    const response = await axios.get<Workspace>(`/api/workspaces/${workspaceId}`)
    return response.data
  },

  createWorkspace: async (data: CreateWorkspaceData): Promise<Workspace> => {
    const response = await axios.post<Workspace>('/api/workspaces', data)
    return response.data
  },

  updateWorkspace: async (workspaceId: number, data: UpdateWorkspaceData): Promise<Workspace> => {
    const response = await axios.put<Workspace>(`/api/workspaces/${workspaceId}`, data)
    return response.data
  },

  deleteWorkspace: async (workspaceId: number): Promise<void> => {
    await axios.delete(`/api/workspaces/${workspaceId}`)
  },

  joinWorkspace: async (workspaceId: number): Promise<Workspace> => {
    const response = await axios.post<Workspace>(`/api/workspaces/${workspaceId}/join`)
    return response.data
  },

  leaveWorkspace: async (workspaceId: number): Promise<void> => {
    await axios.post(`/api/workspaces/${workspaceId}/leave`)
  },

  removeMember: async (workspaceId: number, userId: number): Promise<void> => {
    await axios.delete(`/api/workspaces/${workspaceId}/members/${userId}`)
  },

  getMembers: async (workspaceId: number): Promise<WorkspaceMember[]> => {
    const response = await axios.get<WorkspaceMember[]>(`/api/workspaces/${workspaceId}/members`)
    return response.data
  },
}
