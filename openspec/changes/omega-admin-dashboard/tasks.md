## 1. Backend - Admin API

- [x] 1.1 Add `get_current_superuser` dependency in `backend/src/api/deps.py`
- [x] 1.2 Create `backend/src/schemas/user_admin.py` (UserAdminResponse, UserAdminCreate, UserAdminUpdate)
- [x] 1.3 Create `backend/src/api/admin.py` with CRUD endpoints
- [x] 1.4 Register admin router in `backend/src/main.py`
- [x] 1.5 Add tests for admin endpoints in `backend/tests/test_admin.py`

## 2. Frontend - Admin API Client

- [x] 2.1 Create `frontend/src/api/admin.ts` with API calls for user CRUD
- [x] 2.2 Create `frontend/src/types/admin.ts` for TypeScript types

## 3. Frontend - Redux State

- [x] 3.1 Create `frontend/src/stores/adminSlice.ts` for admin state management

## 4. Frontend - Admin Pages

- [x] 4.1 Create `frontend/src/pages/admin/AdminLayout.tsx` - Admin layout with navigation
- [x] 4.2 Create `frontend/src/pages/admin/UserManagePage.tsx` - User management page
- [x] 4.3 Create `frontend/src/pages/admin/UserFormModal.tsx` - Create/Edit user modal

## 5. Frontend - Routing

- [x] 5.1 Add `/admin` routes in `frontend/src/App.tsx`
- [x] 5.2 Add admin route protection (check is_superuser)

## 6. Verification

- [x] 6.1 Run `make ci` to verify code quality
- [x] 6.2 Test admin API endpoints with Swagger
- [x] 6.3 Test frontend admin pages
