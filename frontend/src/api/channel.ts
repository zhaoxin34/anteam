import axios from './axios'

export interface Channel {
  id: number
  name: string
  description: string | null
  workspace_id: number
  owner_id: number
  created_at: string
}

export interface ChannelMember {
  id: number
  channel_id: number
  user_id: number
  role: string
  joined_at: string
}

export interface CreateChannelData {
  name: string
  description?: string
  workspace_id: number
}

export interface UpdateChannelData {
  name?: string
  description?: string
}

export interface ChannelListResponse {
  items: Channel[]
  total: number
}

export const channelApi = {
  getChannels: async (workspaceId?: number): Promise<ChannelListResponse> => {
    const params = workspaceId ? { workspace_id: workspaceId } : {}
    const response = await axios.get<ChannelListResponse>('/api/channels', { params })
    return response.data
  },

  getChannel: async (channelId: number): Promise<Channel> => {
    const response = await axios.get<Channel>(`/api/channels/${channelId}`)
    return response.data
  },

  createChannel: async (data: CreateChannelData): Promise<Channel> => {
    const response = await axios.post<Channel>('/api/channels', data)
    return response.data
  },

  updateChannel: async (channelId: number, data: UpdateChannelData): Promise<Channel> => {
    const response = await axios.put<Channel>(`/api/channels/${channelId}`, data)
    return response.data
  },

  deleteChannel: async (channelId: number): Promise<void> => {
    await axios.delete(`/api/channels/${channelId}`)
  },

  joinChannel: async (channelId: number): Promise<Channel> => {
    const response = await axios.post<Channel>(`/api/channels/${channelId}/join`)
    return response.data
  },

  leaveChannel: async (channelId: number): Promise<void> => {
    await axios.post(`/api/channels/${channelId}/leave`)
  },

  getMembers: async (channelId: number): Promise<ChannelMember[]> => {
    const response = await axios.get<ChannelMember[]>(`/api/channels/${channelId}/members`)
    return response.data
  },

  removeMember: async (channelId: number, userId: number): Promise<void> => {
    await axios.delete(`/api/channels/${channelId}/members/${userId}`)
  },
}
