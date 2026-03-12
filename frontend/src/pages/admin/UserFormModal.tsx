import React, { useState } from 'react'
import { useDispatch } from 'react-redux'
import { AppDispatch } from '../../stores'
import { createUser, updateUser } from '../../stores/adminSlice'
import { UserAdmin, CreateUserData, UpdateUserData } from '../../types/admin'

interface UserFormModalProps {
  user: UserAdmin | null
  onClose: () => void
  onSuccess: () => void
}

const UserFormModal: React.FC<UserFormModalProps> = ({ user, onClose, onSuccess }) => {
  const dispatch = useDispatch<AppDispatch>()
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    email: user?.email || '',
    username: user?.username || '',
    password: '',
    full_name: user?.full_name || '',
    is_active: user?.is_active ?? true,
    is_superuser: user?.is_superuser ?? false,
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      if (user) {
        // Update existing user
        const updateData: UpdateUserData = {
          email: formData.email,
          username: formData.username,
          full_name: formData.full_name || undefined,
          is_active: formData.is_active,
          is_superuser: formData.is_superuser,
        }
        await dispatch(updateUser({ userId: user.id, data: updateData })).unwrap()
      } else {
        // Create new user
        const createData: CreateUserData = {
          email: formData.email,
          username: formData.username,
          password: formData.password,
          full_name: formData.full_name || undefined,
          is_active: formData.is_active,
          is_superuser: formData.is_superuser,
        }
        await dispatch(createUser(createData)).unwrap()
      }
      onSuccess()
    } catch (error) {
      alert('操作失败')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        background: 'rgba(0,0,0,0.5)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 1000,
      }}
      onClick={onClose}
    >
      <div
        style={{
          background: '#fff',
          borderRadius: 8,
          padding: 24,
          width: 480,
          maxHeight: '80vh',
          overflow: 'auto',
        }}
        onClick={(e) => e.stopPropagation()}
      >
        <h2 style={{ marginBottom: 24 }}>{user ? '编辑用户' : '创建用户'}</h2>

        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: 16 }}>
            <label style={{ display: 'block', marginBottom: 4 }}>邮箱 *</label>
            <input
              type="email"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              required
              style={{ width: '100%', padding: 8, border: '1px solid #ddd', borderRadius: 4 }}
            />
          </div>

          <div style={{ marginBottom: 16 }}>
            <label style={{ display: 'block', marginBottom: 4 }}>用户名 *</label>
            <input
              type="text"
              value={formData.username}
              onChange={(e) => setFormData({ ...formData, username: e.target.value })}
              required
              style={{ width: '100%', padding: 8, border: '1px solid #ddd', borderRadius: 4 }}
            />
          </div>

          {!user && (
            <div style={{ marginBottom: 16 }}>
              <label style={{ display: 'block', marginBottom: 4 }}>密码 *</label>
              <input
                type="password"
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                required={!user}
                style={{ width: '100%', padding: 8, border: '1px solid #ddd', borderRadius: 4 }}
              />
            </div>
          )}

          <div style={{ marginBottom: 16 }}>
            <label style={{ display: 'block', marginBottom: 4 }}>全名</label>
            <input
              type="text"
              value={formData.full_name}
              onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
              style={{ width: '100%', padding: 8, border: '1px solid #ddd', borderRadius: 4 }}
            />
          </div>

          <div style={{ marginBottom: 16, display: 'flex', gap: 24 }}>
            <label>
              <input
                type="checkbox"
                checked={formData.is_active}
                onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })}
              />
              启用用户
            </label>

            <label>
              <input
                type="checkbox"
                checked={formData.is_superuser}
                onChange={(e) => setFormData({ ...formData, is_superuser: e.target.checked })}
              />
              超级用户
            </label>
          </div>

          <div style={{ display: 'flex', gap: 12, justifyContent: 'flex-end' }}>
            <button
              type="button"
              onClick={onClose}
              style={{
                padding: '8px 16px',
                border: '1px solid #ddd',
                borderRadius: 4,
                background: '#fff',
              }}
            >
              取消
            </button>
            <button
              type="submit"
              disabled={loading}
              style={{
                padding: '8px 16px',
                background: '#4a9eff',
                color: '#fff',
                border: 'none',
                borderRadius: 4,
                cursor: loading ? 'not-allowed' : 'pointer',
              }}
            >
              {loading ? '提交中...' : '提交'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default UserFormModal
