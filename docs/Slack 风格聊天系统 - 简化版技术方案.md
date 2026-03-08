# Slack 风格聊天系统 - 简化版技术方案

> 版本: v1.1
> 日期: 2026-03-08
> 状态: 规划中

---

## 一、需求背景

基于 `Slack 风格聊天系统 - 技术产品设计文档 (v1.0)`，针对开发初期阶段进行简化，优先实现核心功能。

### 约束条件

- 不使用 Redis、Elasticsearch、Kafka、K8s
- 接入 Bot，使用 Claude Agent SDK
- 考虑后期扩展性

---

## 二、技术架构

### 2.1 技术栈选择

| 层级 | 技术选择 | 理由 |
|------|----------|------|
| **后端 API** | Python FastAPI | 高性能异步，与 Agent SDK 同语言好集成 |
| **WebSocket** | FastAPI + WebSocket | 统一技术栈，简化部署 |
| **数据库** | SQLite (开发) / PostgreSQL (生产) | 符合偏好，SQLite 免安装适合开发 |
| **前端** | React + TypeScript | 与原版一致 |
| **Bot SDK** | Anthropic Claude Agent SDK | 用户指定 |
| **文件存储** | 本地文件系统 | 简化版不需要 S3 |

### 2.2 架构图

```mermaid
graph TB
    subgraph "Client Layer"
        Web[Web App]
    end

    subgraph "API Layer"
        Gateway[API Gateway<br/>FastAPI]
        WebSocket[WebSocket Server<br/>实时消息]
    end

    subgraph "Service Layer"
        Auth[Auth Service<br/>认证授权]
        Channel[Channel Service<br/>频道管理]
        Message[Message Service<br/>消息服务]
        User[User Service<br/>用户管理]
        Workspace[Workspace Service<br/>工作空间]
        Bot[Bot Service<br/>Bot管理 + Claude SDK]
    end

    subgraph "Data Layer"
        DB[(SQLite/PostgreSQL<br/>持久化)]
    end

    Web --> Gateway
    WebSocket --> Gateway

    Gateway --> Auth
    Gateway --> Channel
    Gateway --> Message
    Gateway --> User
    Gateway --> Workspace
    Gateway --> Bot

    Auth --> DB
    Message --> DB
    Channel --> DB
    User --> DB
    Workspace --> DB
    Bot --> DB
```

### 2.3 消息流转

```mermaid
sequenceDiagram
    participant Client as 客户端
    participant WS as WebSocket Server
    participant API as REST API
    participant DB as SQLite/PostgreSQL
    participant Bot as Bot Service

    Client->>WS: 发送消息 (WebSocket)
    WS->>DB: 持久化消息
    WS->>Client: 推送消息给订阅者

    alt 消息 @Bot
        WS->>Bot: 转发消息
        Bot->>Claude Agent: 调用 SDK
        Claude Agent-->>Bot: 生成回复
        Bot->>WS: 发布回复消息
        WS->>DB: 持久化回复
        WS->>Client: 推送 Bot 回复
    end
```

---

## 三、功能规划

### 3.1 MVP (第一阶段)

| 序号 | 功能 | 描述 |
|------|------|------|
| 1 | 用户注册/登录 | JWT 认证 |
| 2 | 工作空间 | 创建、加入、列出 |
| 3 | 频道 | 创建、列表、加入 |
| 4 | 消息收发 | REST API + WebSocket |
| 5 | 私聊 DM | 点对点消息 |

### 3.2 第二阶段

| 序号 | 功能 | 描述 |
|------|------|------|
| 1 | 消息回复/线程 | 消息嵌套回复 |
| 2 | 消息反应 | Emoji 反应 |
| 3 | Bot 接入 | Claude Agent SDK 集成 |

---

## 四、项目结构

```
anteam/
├── src/                    # 源代码
│   ├── api/               # API 路由
│   │   ├── auth.py
│   │   ├── workspace.py
│   │   ├── channel.py
│   │   ├── message.py
│   │   └── bot.py
│   ├── services/         # 业务逻辑
│   │   ├── auth.py
│   │   ├── workspace.py
│   │   ├── channel.py
│   │   ├── message.py
│   │   └── bot.py
│   ├── models/           # 数据模型 (SQLModel/Pydantic)
│   ├── db/               # 数据库
│   │   └── database.py
│   └── main.py           # 入口
├── web/                   # 前端 (React)
├── tests/                 # 测试
├── Makefile
└── requirements.txt
```

---

## 五、Bot 接入设计

### Claude Agent SDK 集成

```python
from anthropic import Anthropic

class BotService:
    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)

    async def handle_mention(self, message: str, context: dict) -> str:
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[{"role": "user", "content": message}]
        )
        return response.content[0].text
```

### Bot 事件处理流程

1. 用户在频道中 @Bot
2. WebSocket 检测到消息中的 @mention
3. 调用 Bot Service
4. Bot Service 调用 Claude Agent SDK
5. 返回回复消息到频道

---

## 六、数据库表设计

### 核心表

- `users` - 用户
- `workspaces` - 工作空间
- `workspace_members` - 工作空间成员
- `channels` - 频道
- `channel_members` - 频道成员
- `messages` - 消息 (支持 parent_id 实现线程)
- `bots` - Bot 配置

---

## 七、待讨论问题

- [ ] 开发工作流 (Git Flow / OpenSpec)
- [ ] 前端是否现在一起开发
- [ ] Bot 的具体行为定义
- [ ] 是否需要 OpenAPI 文档

---

_文档更新时间: 2026-03-08_
