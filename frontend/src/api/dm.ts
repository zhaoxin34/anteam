import axios from './axios'

export interface Conversation {
  id: number
  user1_id: number
  user2_id: number
  created_at: string
  updated_at: string
}

export interface ConversationListResponse {
  items: Conversation[]
  total: number
}

export const dmApi = {
  getConversations: async (): Promise<ConversationListResponse> => {
    const response = await axios.get<ConversationListResponse>('/api/conversations')
    return response.data
  },

  getConversation: async (conversationId: number): Promise<Conversation> => {
    const response = await axios.get<Conversation>(`/api/conversations/${conversationId}`)
    return response.data
  },

  getConversationMessages: async (
    conversationId: number,
    limit: number = 50,
    offset: number = 0
  ): Promise<import('./message').MessageListResponse> => {
    const response = await axios.get<import('./message').MessageListResponse>(
      `/api/conversations/${conversationId}/messages`,
      { params: { limit, offset } }
    )
    return response.data
  },

  sendMessage: async (
    conversationId: number,
    data: { content: string }
  ): Promise<import('./message').Message> => {
    const response = await axios.post<import('./message').Message>(
      `/api/conversations/${conversationId}/messages`,
      data
    )
    return response.data
  },

  startDm: async (
    userId: number,
    data: { content: string }
  ): Promise<import('./message').Message> => {
    const response = await axios.post<import('./message').Message>(
      `/api/users/${userId}/message`,
      data
    )
    return response.data
  },
}
