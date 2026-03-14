import axios from './axios'

export interface Message {
  id: number
  channel_id: number | null
  conversation_id: number | null
  user_id: number
  content: string
  parent_id: number | null
  is_deleted: boolean
  created_at: string
  updated_at: string | null
}

export interface CreateMessageData {
  content: string
  channel_id: number
  parent_id?: number
}

export interface UpdateMessageData {
  content: string
}

export interface MessageListResponse {
  items: Message[]
  total: number
}

export const messageApi = {
  getChannelMessages: async (
    channelId: number,
    limit: number = 50,
    offset: number = 0
  ): Promise<MessageListResponse> => {
    const response = await axios.get<MessageListResponse>(
      `/api/channels/${channelId}/messages`,
      { params: { limit, offset } }
    )
    return response.data
  },

  createMessage: async (channelId: number, data: CreateMessageData): Promise<Message> => {
    const response = await axios.post<Message>(
      `/api/channels/${channelId}/messages`,
      data
    )
    return response.data
  },

  updateMessage: async (messageId: number, data: UpdateMessageData): Promise<Message> => {
    const response = await axios.put<Message>(`/api/messages/${messageId}`, data)
    return response.data
  },

  deleteMessage: async (messageId: number): Promise<void> => {
    await axios.delete(`/api/messages/${messageId}`)
  },

  getReplies: async (messageId: number): Promise<MessageListResponse> => {
    const response = await axios.get<MessageListResponse>(
      `/api/messages/${messageId}/replies`
    )
    return response.data
  },
}
