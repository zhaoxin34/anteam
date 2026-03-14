import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit'
import { messageApi, Message, CreateMessageData, UpdateMessageData } from '../api/message'

interface MessageState {
  messages: Message[]
  total: number
  loading: boolean
  error: string | null
}

const initialState: MessageState = {
  messages: [],
  total: 0,
  loading: false,
  error: null,
}

export const fetchMessages = createAsyncThunk(
  'message/fetchMessages',
  async ({ channelId, limit = 50, offset = 0 }: { channelId: number; limit?: number; offset?: number }) => {
    const response = await messageApi.getChannelMessages(channelId, limit, offset)
    return response
  }
)

export const sendMessage = createAsyncThunk(
  'message/sendMessage',
  async ({ channelId, data }: { channelId: number; data: CreateMessageData }) => {
    const response = await messageApi.createMessage(channelId, data)
    return response
  }
)

export const editMessage = createAsyncThunk(
  'message/editMessage',
  async ({ messageId, data }: { messageId: number; data: UpdateMessageData }) => {
    const response = await messageApi.updateMessage(messageId, data)
    return response
  }
)

export const deleteMessage = createAsyncThunk(
  'message/deleteMessage',
  async (messageId: number) => {
    await messageApi.deleteMessage(messageId)
    return messageId
  }
)

export const fetchReplies = createAsyncThunk(
  'message/fetchReplies',
  async (messageId: number) => {
    const response = await messageApi.getReplies(messageId)
    return { parentId: messageId, ...response }
  }
)

const messageSlice = createSlice({
  name: 'message',
  initialState,
  reducers: {
    addMessage: (state, action: PayloadAction<Message>) => {
      // Add message to the top (newest first)
      state.messages.unshift(action.payload)
      state.total += 1
    },
    clearMessages: (state) => {
      state.messages = []
      state.total = 0
    },
    clearError: (state) => {
      state.error = null
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch messages
      .addCase(fetchMessages.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(fetchMessages.fulfilled, (state, action) => {
        state.loading = false
        state.messages = action.payload.items
        state.total = action.payload.total
      })
      .addCase(fetchMessages.rejected, (state, action) => {
        state.loading = false
        state.error = action.error.message || 'Failed to fetch messages'
      })
      // Send message
      .addCase(sendMessage.fulfilled, (state, action) => {
        state.messages.unshift(action.payload)
        state.total += 1
      })
      // Edit message
      .addCase(editMessage.fulfilled, (state, action) => {
        const index = state.messages.findIndex((m) => m.id === action.payload.id)
        if (index !== -1) {
          state.messages[index] = action.payload
        }
      })
      // Delete message
      .addCase(deleteMessage.fulfilled, (state, action) => {
        const index = state.messages.findIndex((m) => m.id === action.payload)
        if (index !== -1) {
          state.messages[index].is_deleted = true
        }
      })
  },
})

export const { addMessage, clearMessages, clearError } = messageSlice.actions
export default messageSlice.reducer
