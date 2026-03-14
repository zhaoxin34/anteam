# Channel Feature Design

## Context

当前项目已实现用户认证和工作空间功能。MVP 第一阶段需要实现频道（Channel）功能，频道是工作空间内的组织单元，用户在频道内发送消息。

**现状：**
- 已完成用户注册/登录（JWT 认证）
- 已完成工作空间管理（创建、加入、列表）
- 数据库使用 SQLite
- 后端使用 FastAPI，前端使用 React + TypeScript

**约束：**
- 不使用 Redis、Elasticsearch、Kafka
- 消息需要持久化到数据库
- Bot 接入是第二阶段
- 使用 FastAPI 内置 WebSocket

## Goals / Non-Goals

**Goals:**
- 实现频道 CRUD（创建、列表、获取、更新、删除）
- 实现频道成员管理（加入、离开、成员列表）
- 实现 WebSocket 实时消息推送
- 实现消息持久化存储
- 实现消息回复/线程功能

**Non-Goals:**
- Bot 接入（第二阶段）
- 消息 reactions（第二阶段）
- 私聊 DM（后续实现）
- 文件/图片上传
- 消息搜索

## Decisions

### D1: 消息存储方式

**决策：** 消息同时存储到数据库并通过 WebSocket 推送

**理由：**
- 数据库存储保证消息历史可查询
- WebSocket 推送保证实时性
- 简单可靠，无需额外消息队列

### D2: WebSocket 连接管理

**决策：** 使用 FastAPI 内置 WebSocket，以 workspace_id 为连接 room

**理由：**
- FastAPI WebSocket 与 REST API 统一技术栈
- 以 workspace 维度管理连接，用户加入频道时加入对应 room
- 简化连接管理，无需独立 WebSocket 服务

**备选方案：** 使用独立 WebSocket 服务或 Socket.IO
- 复杂度高，需要额外服务部署

### D3: 频道成员权限

**决策：** 频道成员分为 owner、admin、member 三种角色

**理由：**
- owner: 创建者，拥有全部权限
- admin: 管理员，可以管理频道和成员
- member: 普通成员，只能收发消息

### D4: 消息线程实现

**决策：** 使用 parent_id 自引用实现消息树

```python
class Message(SQLModel, table=True):
    id: int
    channel_id: int
    user_id: int
    content: str
    parent_id: int | None = None  # null 表示顶级消息
    created_at: datetime
```

**理由：**
- 简单直观，查询效率可接受
- 支持无限层级嵌套
- 配合索引优化查询性能

## Risks / Trade-offs

### R1: WebSocket 连接数

**风险：** 高并发下 WebSocket 连接数可能成为瓶颈

**缓解措施：**
- 限制单个 workspace 最大在线用户数
- 考虑后续使用独立 WebSocket 服务

### R2: 消息查询效率

**风险：** 大量消息时查询线程评论可能慢

**缓解措施：**
- 在 channel_id + parent_id 上添加复合索引
- 分页加载消息历史

### R3: 前端状态管理

**风险：** WebSocket 消息与 Redux 状态同步复杂

**缓解措施：**
- WebSocket 消息直接更新 Redux store
- 考虑使用 React Query 管理消息状态

## Migration Plan

1. **数据库迁移**
   - 新建 channels 表
   - 新建 channel_members 表
   - 修改 messages 表添加 channel_id、parent_id

2. **后端部署**
   - 依次部署：models → schemas → repository → API
   - WebSocket 端点最后上线

3. **前端部署**
   - 先上线频道列表页面
   - 再上线消息页面和 WebSocket

## Open Questions

- [ ] 频道是否需要私密/公开属性？
- [ ] 消息是否需要支持编辑/删除？
- [ ] WebSocket 重连策略如何设计？
