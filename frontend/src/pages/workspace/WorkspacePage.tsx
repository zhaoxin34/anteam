import React, { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { RootState, AppDispatch } from '../../stores'
import { fetchWorkspaces, createWorkspace, joinWorkspace } from '../../stores/workspaceSlice'
import { CreateWorkspaceData } from '../../api/workspace'

const WorkspacePage: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>()
  const { workspaces, total, loading, error } = useSelector((state: RootState) => state.workspace)
  const [showModal, setShowModal] = useState(false)
  const [joinId, setJoinId] = useState('')

  useEffect(() => {
    dispatch(fetchWorkspaces())
  }, [dispatch])

  const handleCreate = () => {
    setShowModal(true)
  }

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const formData = new FormData(e.currentTarget)
    const data: CreateWorkspaceData = {
      name: formData.get('name') as string,
      description: (formData.get('description') as string) || undefined,
    }
    try {
      await dispatch(createWorkspace(data)).unwrap()
      setShowModal(false)
    } catch (err) {
      alert('创建失败')
    }
  }

  const handleJoin = async () => {
    if (!joinId) return
    try {
      await dispatch(joinWorkspace(parseInt(joinId))).unwrap()
      setJoinId('')
    } catch (err) {
      alert('加入失败')
    }
  }

  if (loading) {
    return <div>加载中...</div>
  }

  if (error) {
    return <div style={{ color: 'red' }}>错误: {error}</div>
  }

  return (
    <div style={{ padding: 24 }}>
      <h1>工作空间</h1>

      <div style={{ marginTop: 16, marginBottom: 24, display: 'flex', gap: 12 }}>
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
          创建工作空间
        </button>
        <div style={{ display: 'flex', gap: 8 }}>
          <input
            type="number"
            placeholder="输入工作空间ID加入"
            value={joinId}
            onChange={(e) => setJoinId(e.target.value)}
            style={{ padding: 8, border: '1px solid #ddd', borderRadius: 4 }}
          />
          <button
            onClick={handleJoin}
            style={{
              padding: '8px 16px',
              background: '#28a745',
              color: '#fff',
              border: 'none',
              borderRadius: 4,
              cursor: 'pointer',
            }}
          >
            加入
          </button>
        </div>
      </div>

      <div style={{ background: '#fff', borderRadius: 8, overflow: 'hidden' }}>
        {workspaces.length === 0 ? (
          <div style={{ padding: 24, textAlign: 'center', color: '#666' }}>
            暂无工作空间，请创建或加入
          </div>
        ) : (
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ background: '#f5f5f5' }}>
                <th style={{ padding: 12, textAlign: 'left' }}>ID</th>
                <th style={{ padding: 12, textAlign: 'left' }}>名称</th>
                <th style={{ padding: 12, textAlign: 'left' }}>描述</th>
                <th style={{ padding: 12, textAlign: 'left' }}>创建时间</th>
              </tr>
            </thead>
            <tbody>
              {workspaces.map((workspace) => (
                <tr key={workspace.id} style={{ borderTop: '1px solid #eee' }}>
                  <td style={{ padding: 12 }}>{workspace.id}</td>
                  <td style={{ padding: 12 }}>{workspace.name}</td>
                  <td style={{ padding: 12 }}>{workspace.description || '-'}</td>
                  <td style={{ padding: 12 }}>
                    {new Date(workspace.created_at).toLocaleString('zh-CN')}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      <div style={{ marginTop: 16 }}>共 {total} 个工作空间</div>

      {/* Create Modal */}
      {showModal && (
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
          onClick={() => setShowModal(false)}
        >
          <div
            style={{
              background: '#fff',
              borderRadius: 8,
              padding: 24,
              width: 400,
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <h2 style={{ marginBottom: 24 }}>创建工作空间</h2>
            <form onSubmit={handleSubmit}>
              <div style={{ marginBottom: 16 }}>
                <label style={{ display: 'block', marginBottom: 4 }}>名称 *</label>
                <input
                  name="name"
                  type="text"
                  required
                  style={{ width: '100%', padding: 8, border: '1px solid #ddd', borderRadius: 4 }}
                />
              </div>
              <div style={{ marginBottom: 16 }}>
                <label style={{ display: 'block', marginBottom: 4 }}>描述</label>
                <textarea
                  name="description"
                  style={{ width: '100%', padding: 8, border: '1px solid #ddd', borderRadius: 4 }}
                />
              </div>
              <div style={{ display: 'flex', gap: 12, justifyContent: 'flex-end' }}>
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
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
                  style={{
                    padding: '8px 16px',
                    background: '#4a9eff',
                    color: '#fff',
                    border: 'none',
                    borderRadius: 4,
                  }}
                >
                  创建
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

export default WorkspacePage
