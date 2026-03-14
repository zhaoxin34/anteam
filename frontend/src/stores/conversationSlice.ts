import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit'
import { dmApi, Conversation } from '../api/dm'

interface ConversationState {
  conversations: Conversation[]
  total: number
  loading: boolean
  error: string | null
  selectedConversation: Conversation | null
}

const initialState: ConversationState = {
  conversations: [],
  total: 0,
  loading: false,
  error: null,
  selectedConversation: null,
}

export const fetchConversations = createAsyncThunk('conversation/fetchConversations', async () => {
  const response = await dmApi.getConversations()
  return response
})

const conversationSlice = createSlice({
  name: 'conversation',
  initialState,
  reducers: {
    setSelectedConversation: (state, action: PayloadAction<Conversation | null>) => {
      state.selectedConversation = action.payload
    },
    clearError: (state) => {
      state.error = null
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchConversations.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(fetchConversations.fulfilled, (state, action) => {
        state.loading = false
        state.conversations = action.payload.items
        state.total = action.payload.total
      })
      .addCase(fetchConversations.rejected, (state, action) => {
        state.loading = false
        state.error = action.error.message || 'Failed to fetch conversations'
      })
  },
})

export const { setSelectedConversation, clearError } = conversationSlice.actions
export default conversationSlice.reducer
