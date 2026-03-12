import React, { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { RootState, AppDispatch } from '../../stores'
import { fetchUsers, deleteUser } from '../../stores/adminSlice'
import { UserAdmin } from '../../types/admin'
import UserFormModal from './UserFormModal'

const UserManagePage: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>()
  const { users, total, page, pageSize, loading, error } = useSelector(
    (state: RootState) => state.admin
  )
  const [showModal, setShowModal] = useState(false)
  const [editingUser, setEditingUser] = useState<UserAdmin | null>(null)

  useEffect(() => {
    dispatch(fetchUsers({ page, pageSize }))
  }, [dispatch, page, pageSize])

  const handleCreate = () => {
    setEditingUser(null)
    setShowModal(true)
  }

  const handleEdit = (user: UserAdmin) => {
    setEditingUser(user)
    setShowModal(true)
  }

  const handleDelete = async (userId: number) => {
    if (window.confirm('确定要删除这个用户吗？')) {
      dispatch(deleteUser(userId))
    }
  }

  const handleModalClose = () => {
    setShowModal(false)
    setEditingUser(null)
  }

  const handleModalSuccess = () => {
    setShowModal(false)
    setEditingUser(null)
    dispatch(fetchUsers({ page, pageSize }))
  }

  if (loading) {
    return <div>加载中...</div>
  }

  if (error) {
    return <div style={{ color: 'red' }}>错误: {error}</div>
  }

  return (
    <div>
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: 16,
        }}
      >
        <h1>用户管理</h1>
        <button
          onClick={handleCreate}
          style={{
            padding: '8px 16px',
            background: '#4a9eff',
            color: '#fff',
            border: 'none',
            borderRadius: 4,
            cursor: 'pointer',
          }}
        >
          创建用户
        </button>
      </div>

      <div style={{ background: '#fff', borderRadius: 8, overflow: 'hidden' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ background: '#f5f5f5' }}>
              <th style={{ padding: 12, textAlign: 'left' }}>ID</th>
              <th style={{ padding: 12, textAlign: 'left' }}>用户名</th>
              <th style={{ padding: 12, textAlign: 'left' }}>邮箱</th>
              <th style={{ padding: 12, textAlign: 'left' }}>状态</th>
              <th style={{ padding: 12, textAlign: 'left' }}>超级用户</th>
              <th style={{ padding: 12, textAlign: 'left' }}>创建时间</th>
              <th style={{ padding: 12, textAlign: 'left' }}>操作</th>
            </tr>
          </thead>
          <tbody>
            {users.map((user) => (
              <tr key={user.id} style={{ borderTop: '1px solid #eee' }}>
                <td style={{ padding: 12 }}>{user.id}</td>
                <td style={{ padding: 12 }}>{user.username}</td>
                <td style={{ padding: 12 }}>{user.email}</td>
                <td style={{ padding: 12 }}>
                  <span
                    style={{
                      padding: '2px 8px',
                      borderRadius: 4,
                      background: user.is_active ? '#d4edda' : '#f8d7da',
                      color: user.is_active ? '#155724' : '#721c24',
                    }}
                  >
                    {user.is_active ? '活跃' : '禁用'}
                  </span>
                </td>
                <td style={{ padding: 12 }}>{user.is_superuser ? '是' : '否'}</td>
                <td style={{ padding: 12 }}>{new Date(user.created_at).toLocaleString('zh-CN')}</td>
                <td style={{ padding: 12 }}>
                  <button
                    onClick={() => handleEdit(user)}
                    style={{ marginRight: 8, padding: '4px 8px', cursor: 'pointer' }}
                  >
                    编辑
                  </button>
                  <button
                    onClick={() => handleDelete(user.id)}
                    style={{ padding: '4px 8px', color: 'red', cursor: 'pointer' }}
                  >
                    删除
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      <div
        style={{
          marginTop: 16,
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}
      >
        <span>
          共 {total} 条记录，第 {page} / {Math.ceil(total / pageSize)} 页
        </span>
        <div>
          <button
            onClick={() => dispatch(fetchUsers({ page: page - 1, pageSize }))}
            disabled={page === 1}
            style={{ padding: '4px 12px', marginRight: 8 }}
          >
            上一页
          </button>
          <button
            onClick={() => dispatch(fetchUsers({ page: page + 1, pageSize }))}
            disabled={page * pageSize >= total}
          >
            下一页
          </button>
        </div>
      </div>

      {/* Modal */}
      {showModal && (
        <UserFormModal
          user={editingUser}
          onClose={handleModalClose}
          onSuccess={handleModalSuccess}
        />
      )}
    </div>
  )
}

export default UserManagePage
