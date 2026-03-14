import React, { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { useNavigate } from 'react-router-dom'
import { RootState, AppDispatch } from '../../stores'
import { fetchConversations } from '../../stores/conversationSlice'

const DMListPage: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>()
  const navigate = useNavigate()
  const { conversations, total, loading, error } = useSelector((state: RootState) => state.conversation)
  const [newDmUserId, setNewDmUserId] = useState('')

  useEffect(() => {
    dispatch(fetchConversations())
  }, [dispatch])

  const handleConversationClick = (conversationId: number) => {
    navigate(`/dm/${conversationId}`)
  }

  if (loading) {
    return <div>加载中...</div>
  }

  if (error) {
    return <div style={{ color: 'red' }}>错误: {error}</div>
  }

  return (
    <div style={{ padding: 24 }}>
      <h1>私信</h1>

      <div style={{ marginTop: 16, marginBottom: 24, display: 'flex', gap: 12 }}>
        <input
          type="number"
          placeholder="输入用户ID开始私信"
          value={newDmUserId}
          onChange={(e) => setNewDmUserId(e.target.value)}
          style={{ padding: 8, border: '1px solid #ddd', borderRadius: 4 }}
        />
        <button
          onClick={() => {
            if (newDmUserId) {
              navigate(`/dm/new?userId=${newDmUserId}`)
            }
          }}
          style={{
            padding: '8px 16px',
            background: '#4a9eff',
            color: '#fff',
            border: 'none',
            borderRadius: 4,
            cursor: 'pointer',
          }}
        >
          开始私信
        </button>
      </div>

      <div style={{ background: '#fff', borderRadius: 8, overflow: 'hidden' }}>
        {conversations.length === 0 ? (
          <div style={{ padding: 24, textAlign: 'center', color: '#666' }}>
            暂无私信对话
          </div>
        ) : (
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ background: '#f5f5f5' }}>
                <th style={{ padding: 12, textAlign: 'left' }}>ID</th>
                <th style={{ padding: 12, textAlign: 'left' }}>用户1</th>
                <th style={{ padding: 12, textAlign: 'left' }}>用户2</th>
                <th style={{ padding: 12, textAlign: 'left' }}>更新时间</th>
              </tr>
            </thead>
            <tbody>
              {conversations.map((conv) => (
                <tr
                  key={conv.id}
                  style={{ borderTop: '1px solid #eee', cursor: 'pointer' }}
                  onClick={() => handleConversationClick(conv.id)}
                >
                  <td style={{ padding: 12 }}>{conv.id}</td>
                  <td style={{ padding: 12 }}>用户 {conv.user1_id}</td>
                  <td style={{ padding: 12 }}>用户 {conv.user2_id}</td>
                  <td style={{ padding: 12 }}>
                    {new Date(conv.updated_at).toLocaleString('zh-CN')}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      <div style={{ marginTop: 16 }}>共 {total} 个对话</div>
    </div>
  )
}

export default DMListPage
