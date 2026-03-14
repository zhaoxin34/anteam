import { configureStore } from '@reduxjs/toolkit'
import adminReducer from './adminSlice'
import channelReducer from './channelSlice'
import conversationReducer from './conversationSlice'
import messageReducer from './messageSlice'
import workspaceReducer from './workspaceSlice'

export const store = configureStore({
  reducer: {
    admin: adminReducer,
    workspace: workspaceReducer,
    channel: channelReducer,
    conversation: conversationReducer,
    message: messageReducer,
  },
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch
