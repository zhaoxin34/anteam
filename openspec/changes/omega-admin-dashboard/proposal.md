## Why

Slack 聊天系统需要管理后台来维护用户、频道等资源。目前系统只有基础的用户认证功能，缺少统一的管理界面来管理系统核心数据。需要创建一个代号为 **Omega** 的管理后台。

## What Changes

- 新增后端 `/api/admin/*` 路由，提供用户管理 API
- 新增前端 `/admin` 页面，实现 Omega 管理后台界面
- 添加超级用户权限验证 (`is_superuser`)
- 实现用户的完整 CRUD 操作

## Capabilities

### New Capabilities
- **user-admin**: 管理后台用户管理功能，包括用户列表、创建、编辑、删除、启用/禁用

### Modified Capabilities
- (无)

## Impact

- **Backend**: 新增 `backend/src/api/admin.py`，修改 `backend/src/api/deps.py`
- **Frontend**: 新增 `frontend/src/pages/admin/` 管理页面
- **Database**: 无变更（使用现有 User 模型）
- **API**: 新增 `/api/admin/users` RESTful 端点
