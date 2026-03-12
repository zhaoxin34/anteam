# Anteam - Slack 风格聊天系统

Anteam 是一个 Slack 风格的企业级聊天系统，采用前后端分离架构。

## 技术栈

### 后端
- Python 3.12+ / FastAPI
- SQLModel (SQLite)
- JWT 认证
- Pydantic v2

### 前端
- React 18 + TypeScript
- Redux Toolkit
- Vite

## 功能特性

### 用户认证
- 用户注册/登录
- JWT Token 认证
- 权限控制（普通用户 / 超级用户）

### 管理后台 (Omega)
- 用户管理（CRUD）
- 超级用户专属访问

## 快速开始

### 1. 启动后端

```bash
cd backend
make dev
```

后端服务将在 http://localhost:8000 运行

### 2. 启动前端

```bash
cd frontend
npm run dev
```

前端服务将在 http://localhost:3000 运行

## 登录信息

首次启动后，使用以下凭据登录：

| 账号 | 密码 | 权限 |
|------|------|------|
| admin | admin123 | 超级用户 |

## API 文档

后端启动后，访问以下地址查看 OpenAPI 文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 项目结构

```
anteam/
├── backend/           # Python FastAPI 后端
│   ├── src/
│   │   ├── api/      # API 路由
│   │   ├── service/  # 业务逻辑
│   │   ├── repository/ # 数据访问
│   │   ├── models/   # 数据模型
│   │   └── schemas/  # Pydantic schemas
│   └── tests/        # 测试代码
│
└── frontend/         # React TypeScript 前端
    ├── src/
    │   ├── api/     # API 调用
    │   ├── pages/   # 页面组件
    │   ├── stores/  # Redux 状态管理
    │   └── types/   # TypeScript 类型
    └── tests/       # 测试代码
```

## 开发命令

### 后端

```bash
make dev        # 启动开发服务器
make lint       # 代码检查
make format     # 代码格式化
make type-check # 类型检查
make test       # 运行测试
make ci         # CI 检查
```

### 前端

```bash
npm run dev       # 启动开发服务器
npm run lint      # 代码检查
npm run format    # 代码格式化
npm run type-check # 类型检查
npm run test      # 运行测试
```

## 许可证

MIT
