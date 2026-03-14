# DM Feature Proposal

## Why

实现私聊（DM）功能是 MVP 第一阶段的核心需求之一。与频道的群组聊天不同，DM 支持用户之间一对一的私密消息交流，是 Slack 风格聊天系统的必备功能。

## What Changes

### Backend Changes
- 创建 `conversations` 表（存储用户之间的对话关系）
- 实现 DM API（创建对话、获取对话列表、获取对话消息）
- 支持通过 WebSocket 发送和接收 DM
- 复用消息持久化机制

### Frontend Changes
- 创建 DM 列表页面
- 创建 DM 聊天页面
- 支持实时消息推送

## Capabilities

### New Capabilities

- `direct-messaging`: 私聊功能 - 用户之间点对点消息
- `conversation-management`: 对话管理 - 创建、列出对话

### Modified Capabilities

- `real-time-messaging`: 扩展支持 DM 实时推送

## Impact

### 涉及的代码模块

- Backend: `src/models/conversation.py`, `src/schemas/conversation.py`, `src/repository/conversation_repository.py`, `src/api/dm.py`
- Frontend: `src/api/dm.ts`, `src/pages/dm/`, `src/stores/dmSlice.ts`

### 数据库变更

- 新增 `conversations` 表（记录用户对话关系）
- 消息复用 `messages` 表，通过 `conversation_id` 关联

### API 变更

- 新增 REST API: `/api/dm`, `/api/conversations`
