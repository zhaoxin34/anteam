import { configureStore } from '@reduxjs/toolkit'
import adminReducer from './adminSlice'
import workspaceReducer from './workspaceSlice'

export const store = configureStore({
  reducer: {
    admin: adminReducer,
    workspace: workspaceReducer,
  },
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch
