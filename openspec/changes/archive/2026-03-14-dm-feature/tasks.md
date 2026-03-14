# DM Feature Implementation Tasks

## 1. Backend - Database Models

- [x] 1.1 Create Conversation model (`backend/src/models/conversation.py`)
- [x] 1.2 Update Message model - add conversation_id field
- [x] 1.3 Export models in `backend/src/models/__init__.py`

## 2. Backend - Pydantic Schemas

- [x] 2.1 Create Conversation schemas (`backend/src/schemas/conversation.py`)
  - ConversationResponse, ConversationListResponse

## 3. Backend - Repository Layer

- [x] 3.1 Create Conversation repository (`backend/src/repository/conversation_repository.py`)
  - get_or_create_conversation, get_user_conversations
  - get_conversation, update_conversation_timestamp

## 4. Backend - API Layer

- [x] 4.1 Create DM API (`backend/src/api/dm.py`)
  - GET /api/conversations - list conversations
  - GET /api/conversations/{id} - get conversation
  - GET /api/conversations/{id}/messages - get DM messages
  - POST /api/conversations/{id}/messages - send DM message
  - POST /api/users/{user_id}/message - start/new DM with user

## 5. Backend - WebSocket Integration

- [ ] 5.1 Extend WebSocket to support DM rooms
- [ ] 5.2 Add DM message broadcast

## 6. Frontend - API Client

- [x] 6.1 Create DM API client (`frontend/src/api/dm.ts`)

## 7. Frontend - Redux Store

- [x] 7.1 Create Conversation slice (`frontend/src/stores/conversationSlice.ts`)

## 8. Frontend - Pages

- [x] 8.1 Create DMListPage (`frontend/src/pages/dm/DMListPage.tsx`)
- [x] 8.2 Create DMPage (`frontend/src/pages/dm/DMPage.tsx`)
- [x] 8.3 Add routes in `frontend/src/App.tsx`
- [x] 8.4 Add DM navigation in header

## 9. Verification

- [x] 9.1 Run backend tests
- [ ] 9.2 Test DM via API
- [ ] 9.3 Test WebSocket DM messaging
