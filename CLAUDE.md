# Slack 聊天系统 - Claude Code 项目配置

## 项目概述

这是一个 Slack 风格的聊天系统，采用前后端分离架构，后端使用 Python FastAPI，前端使用 React TypeScript。

## 技术栈

### 后端
- Python 3.11+
- FastAPI (Web 框架)
- SQLModel (数据库 ORM)
- Pydantic v2 (数据验证)
- Alembic (数据库迁移)
- pytest + pytest-asyncio (测试)

### 前端
- React 18+
- TypeScript (strict mode)
- Redux Toolkit (状态管理)
- Vite (构建工具)
- ESLint + Prettier (代码规范)

### 开发工具
- Black (代码格式化)
- isort (导入排序)
- mypy (类型检查)
- ruff (代码检查)

## 项目结构

```
anteam/
├── backend/                 # Python FastAPI 后端
│   ├── src/
│   │   ├── api/            # 路由层 - API 端点定义
│   │   ├── service/        # 业务逻辑层
│   │   ├── repository/     # 数据访问层
│   │   ├── models/         # 数据模型 (SQLModel)
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── core/           # 核心配置
│   │   ├── db/             # 数据库配置
│   │   └── main.py         # 应用入口
│   ├── tests/              # 测试代码
│   ├── Makefile           # 后端命令
│   └── requirements.txt    # 依赖
│
├── frontend/               # React TypeScript 前端
│   ├── src/
│   │   ├── components/    # 组件
│   │   ├── pages/         # 页面
│   │   ├── api/           # API 调用
│   │   ├── hooks/         # 自定义 Hooks
│   │   ├── stores/        # 状态管理
│   │   └── types/         # 类型定义
│   ├── tests/             # 测试代码
│   ├── package.json
│   └── Makefile          # 前端命令
│
└── CLAUDE.md              # Claude Code 项目配置
```

## 代码规范摘要

### 后端规范

1. **代码风格**
   - 使用 Black 格式化 (行长度 100)
   - 使用 isort 排序导入
   - 使用 mypy strict 模式类型检查
   - 使用 ruff 代码检查

2. **API 设计**
   - RESTful 风格
   - 使用 Pydantic v2 定义 Request/Response
   - 统一错误响应格式

3. **分层架构**
   - API Layer: 路由、请求验证
   - Service Layer: 业务逻辑
   - Repository Layer: 数据访问
   - Model Layer: 数据模型

### 前端规范

1. **代码风格**
   - 使用 Prettier 格式化
   - 使用 ESLint (Airbnb config) 检查
   - TypeScript strict 模式

2. **组件规范**
   - 函数组件 + Hooks
   - 使用 TypeScript 泛型
   - 组件 Props 类型定义

3. **状态管理**
   - Redux Toolkit (客户端状态)

## 常用命令

### 后端命令 (在 backend/ 目录执行)

```bash
# 开发
make dev          # 启动开发服务器

# 代码质量
make lint         # 代码检查 (ruff)
make format       # 代码格式化 (black + isort)
make type-check   # 类型检查 (mypy)

# 测试
make test         # 运行测试 (pytest)

# CI
make ci           # 运行所有检查
```

### 前端命令 (在 frontend/ 目录执行)

```bash
# 开发
npm run dev       # 启动开发服务器

# 代码质量
npm run lint      # 代码检查 (ESLint)
npm run format   # 代码格式化 (Prettier)

# 测试
npm run test     # 运行测试 (Vitest)

# 构建
npm run build    # 生产构建
```

## 注意事项

1. **Bot 接入**: 系统预留 Bot 接入接口，可通过继承 `BaseBot` 抽象类接入多种 AI Agent
2. **数据库**: 使用 SQLite 作为默认数据库，配置位于 `backend/src/core/config.py`
3. **Git 工作流**: 使用 Trunk-Based 开发模式，提交遵循 Conventional Commits 规范

## Git Hooks

项目已配置 pre-commit hooks，在提交前会自动检查：
- 代码格式化 (Black, isort)
- 类型检查 (mypy)
- 代码检查 (ruff)
