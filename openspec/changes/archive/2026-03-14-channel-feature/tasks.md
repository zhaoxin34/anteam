# Channel Feature Implementation Tasks

## 1. Backend - Database Models

- [x] 1.1 Create Channel model (`backend/src/models/channel.py`)
- [x] 1.2 Create ChannelMember model (`backend/src/models/channel.py`)
- [x] 1.3 Update Message model - add channel_id, parent_id, is_deleted fields
- [x] 1.4 Export models in `backend/src/models/__init__.py`

## 2. Backend - Pydantic Schemas

- [x] 2.1 Create Channel schemas (`backend/src/schemas/channel.py`)
  - ChannelCreate, ChannelUpdate, ChannelResponse
  - ChannelMemberResponse
  - ChannelListResponse
- [x] 2.2 Create Message schemas (`backend/src/schemas/message.py`)
  - MessageCreate, MessageUpdate, MessageResponse
  - MessageListResponse

## 3. Backend - Repository Layer

- [x] 3.1 Create Channel repository (`backend/src/repository/channel_repository.py`)
  - get_channel, get_user_channels, create_channel
  - update_channel, delete_channel
  - add_member, remove_member, get_members, is_member
- [x] 3.2 Create Message repository (`backend/src/repository/message_repository.py`)
  - create_message, get_message, get_channel_messages
  - update_message, delete_message
  - get_thread_replies, get_reply_count

## 4. Backend - API Layer

- [x] 4.1 Create Channel API (`backend/src/api/channel.py`)
  - GET /api/channels - list channels
  - POST /api/channels - create channel
  - GET /api/channels/{id} - get channel
  - PUT /api/channels/{id} - update channel
  - DELETE /api/channels/{id} - delete channel
  - POST /api/channels/{id}/join - join channel
  - POST /api/channels/{id}/leave - leave channel
  - GET /api/channels/{id}/members - list members
  - DELETE /api/channels/{id}/members/{user_id} - remove member
- [x] 4.2 Create Message API (`backend/src/api/message.py`)
  - GET /api/channels/{channel_id}/messages - get messages
  - POST /api/channels/{channel_id}/messages - send message
  - PUT /api/messages/{id} - edit message
  - DELETE /api/messages/{id} - delete message
  - GET /api/messages/{message_id}/replies - get thread replies

## 5. Backend - WebSocket

- [x] 5.1 Create WebSocket endpoint (`backend/src/api/websocket.py`)
  - WebSocket /ws/{workspace_id}
  - Connection management (join/leave rooms)
  - Message broadcast to channel
- [x] 5.2 Register WebSocket router in main.py

## 6. Frontend - API Client

- [x] 6.1 Create Channel API client (`frontend/src/api/channel.ts`)
- [x] 6.2 Create Message API client (`frontend/src/api/message.ts`)

## 7. Frontend - Redux Store

- [x] 7.1 Create Channel slice (`frontend/src/stores/channelSlice.ts`)
  - fetchChannels, createChannel, joinChannel, leaveChannel
  - setSelectedChannel
- [x] 7.2 Create Message slice (`frontend/src/stores/messageSlice.ts`)
  - fetchMessages, sendMessage, editMessage, deleteMessage
  - fetchReplies
- [x] 7.3 Register slices in `frontend/src/stores/index.ts`

## 8. Frontend - Pages

- [x] 8.1 Create ChannelListPage (`frontend/src/pages/channel/ChannelListPage.tsx`)
- [x] 8.2 Create ChannelPage with messages (`frontend/src/pages/channel/ChannelPage.tsx`)
- [x] 8.3 Add routes in `frontend/src/App.tsx`
- [x] 8.4 Add navigation link in header

## 9. Integration

- [x] 9.1 Connect WebSocket client in frontend
- [x] 9.2 Display real-time messages
- [x] 9.3 Implement thread/reply UI

## 10. Verification

- [x] 10.1 Run backend tests
- [x] 10.2 Run frontend type-check
- [ ] 10.3 Test channel CRUD via API
- [ ] 10.4 Test WebSocket connection and messaging
- [ ] 10.5 Test message threads
