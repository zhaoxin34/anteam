## Context

当前项目已有：
- **Backend**: FastAPI + SQLModel，用户认证 (JWT)
- **Frontend**: React + TypeScript + Redux Toolkit + Vite
- **现有 API**: `/api/auth/*` (register, login, me)
- **访问控制**: 基础 JWT 认证，无权限分级

Omega 管理后台需要：
- 独立的 `/api/admin` 路由
- 超级用户权限验证
- 完整用户 CRUD 界面

## Goals / Non-Goals

**Goals:**
- 实现 `/api/admin/users` RESTful API
- 实现 `/admin` 前端管理页面
- 添加超级用户权限验证
- 复用现有 User 模型

**Non-Goals:**
- 不实现频道管理（后续迭代）
- 不实现系统配置管理（后续迭代）
- 不使用第三方 Admin UI 框架

## Decisions

### 1. 同项目 vs 独立项目
- **决策**: 同项目 `/admin` 路由
- **理由**: 复用现有用户认证，减少维护成本

### 2. 权限验证方式
- **决策**: 使用 `is_superuser` 字段
- **理由**: 现有 User 模型已有此字段，无需数据库变更

### 3. 前端状态管理
- **决策**: 使用 Redux Toolkit
- **理由**: 项目已配置 Redux，复用更一致

## Risks / Trade-offs

- [风险] 前端页面开发工作量较大 → 使用简洁的表格 + 弹窗形式
- [风险] 超级用户创建需要手动修改数据库 → 提供种子脚本
