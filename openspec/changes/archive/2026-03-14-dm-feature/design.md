# DM Feature Design

## Context

当前项目已实现用户认证、工作空间和频道功能。DM（私聊）是 MVP 第一阶段的最后一个核心功能，实现用户之间的一对一私密消息交流。

**现状：**
- 已完成用户注册/登录（JWT 认证）
- 已完成工作空间管理
- 已完成频道功能（包括 WebSocket 实时消息）
- 数据库使用 SQLite

**约束：**
- 复用现有 WebSocket 机制
- 消息持久化复用现有 messages 表

## Goals / Non-Goals

**Goals:**
- 实现用户之间一对一私聊
- 实现对话列表（显示所有 DM 会话）
- 实现 DM 实时消息推送
- 消息持久化存储

**Non-Goals:**
- 群组聊天（后续实现）
- 消息已读未读状态
- 消息提醒设置
- 文件传输

## Decisions

### D1: 对话关系存储

**决策：** 创建 `conversations` 表存储用户对话关系

```python
class Conversation(SQLModel, table=True):
    id: int
    user1_id: int  # 较小的用户 ID
    user2_id: int  # 较大的用户 ID
    created_at: datetime
    updated_at: datetime  # 最后一条消息时间
```

**理由：**
- 确保两个用户之间只有一条对话记录
- 通过 user1_id < user2_id 保证唯一性
- 方便查询用户的对话列表

**备选方案：** 只用 messages 表通过 sender_id + receiver_id 查询
- 查询效率低，代码复杂

### D2: 消息关联

**决策：** 消息表增加 `conversation_id` 外键

```python
class Message(SQLModel, table=True):
    # ... existing fields
    channel_id: int | None = None
    conversation_id: int | None = None
    # channel_id 和 conversation_id 只能有一个有值
```

**理由：**
- 明确区分频道消息和私聊消息
- 查询效率高
- 便于消息历史管理

### D3: WebSocket 房间管理

**决策：** DM 使用用户 ID 作为 room 标识

**理由：**
- 简化实现，消息直接推送给目标用户
- 不需要额外的对话房间管理

**备选方案：** 使用 conversation_id 作为 room
- 需要维护更多连接映射

## Risks / Trade-offs

### R1: 消息查询

**风险：** DM 消息查询需要额外关联 conversations 表

**缓解措施：**
- 添加适当索引
- 考虑使用视图简化查询

### R2: 重复对话

**风险：** 可能创建重复的对话记录

**缓解措施：**
- 创建对话前先查询是否已存在
- 使用数据库唯一约束

## Migration Plan

1. **数据库迁移**
   - 新建 conversations 表
   - 修改 messages 表添加 conversation_id

2. **后端部署**
   - 依次部署：models → schemas → repository → API

3. **前端部署**
   - 上线 DM 列表和聊天页面

## Open Questions

- [ ] 是否需要支持群组 DM（3人以上）？
- [ ] DM 消息是否需要显示"已读"状态？
