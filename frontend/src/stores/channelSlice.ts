import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit'
import { channelApi, Channel, CreateChannelData, UpdateChannelData } from '../api/channel'

interface ChannelState {
  channels: Channel[]
  total: number
  loading: boolean
  error: string | null
  selectedChannel: Channel | null
}

const initialState: ChannelState = {
  channels: [],
  total: 0,
  loading: false,
  error: null,
  selectedChannel: null,
}

export const fetchChannels = createAsyncThunk(
  'channel/fetchChannels',
  async (workspaceId?: number) => {
    const response = await channelApi.getChannels(workspaceId)
    return response
  }
)

export const createChannel = createAsyncThunk(
  'channel/createChannel',
  async (data: CreateChannelData) => {
    const response = await channelApi.createChannel(data)
    return response
  }
)

export const updateChannel = createAsyncThunk(
  'channel/updateChannel',
  async ({ channelId, data }: { channelId: number; data: UpdateChannelData }) => {
    const response = await channelApi.updateChannel(channelId, data)
    return response
  }
)

export const deleteChannel = createAsyncThunk(
  'channel/deleteChannel',
  async (channelId: number) => {
    await channelApi.deleteChannel(channelId)
    return channelId
  }
)

export const joinChannel = createAsyncThunk(
  'channel/joinChannel',
  async (channelId: number) => {
    const response = await channelApi.joinChannel(channelId)
    return response
  }
)

export const leaveChannel = createAsyncThunk(
  'channel/leaveChannel',
  async (channelId: number) => {
    await channelApi.leaveChannel(channelId)
    return channelId
  }
)

const channelSlice = createSlice({
  name: 'channel',
  initialState,
  reducers: {
    setSelectedChannel: (state, action: PayloadAction<Channel | null>) => {
      state.selectedChannel = action.payload
    },
    clearError: (state) => {
      state.error = null
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch channels
      .addCase(fetchChannels.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(fetchChannels.fulfilled, (state, action) => {
        state.loading = false
        state.channels = action.payload.items
        state.total = action.payload.total
      })
      .addCase(fetchChannels.rejected, (state, action) => {
        state.loading = false
        state.error = action.error.message || 'Failed to fetch channels'
      })
      // Create channel
      .addCase(createChannel.fulfilled, (state, action) => {
        state.channels.push(action.payload)
        state.total += 1
      })
      // Update channel
      .addCase(updateChannel.fulfilled, (state, action) => {
        const index = state.channels.findIndex((c) => c.id === action.payload.id)
        if (index !== -1) {
          state.channels[index] = action.payload
        }
      })
      // Delete channel
      .addCase(deleteChannel.fulfilled, (state, action) => {
        state.channels = state.channels.filter((c) => c.id !== action.payload)
        state.total -= 1
      })
      // Join channel
      .addCase(joinChannel.fulfilled, (state, action) => {
        const exists = state.channels.find((c) => c.id === action.payload.id)
        if (!exists) {
          state.channels.push(action.payload)
          state.total += 1
        }
      })
      // Leave channel
      .addCase(leaveChannel.fulfilled, (state, action) => {
        state.channels = state.channels.filter((c) => c.id !== action.payload)
        state.total -= 1
      })
  },
})

export const { setSelectedChannel, clearError } = channelSlice.actions
export default channelSlice.reducer
