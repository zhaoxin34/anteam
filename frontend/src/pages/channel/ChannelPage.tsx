import React, { useEffect, useState, useRef } from 'react'
import { useParams } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import { RootState, AppDispatch } from '../../stores'
import { fetchMessages, sendMessage, clearMessages } from '../../stores/messageSlice'

const ChannelPage: React.FC = () => {
  const { channelId } = useParams<{ channelId: string }>()
  const dispatch = useDispatch<AppDispatch>()
  const { messages, loading } = useSelector((state: RootState) => state.message)
  const { selectedChannel } = useSelector((state: RootState) => state.channel)
  const [messageInput, setMessageInput] = useState('')
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (channelId) {
      dispatch(fetchMessages({ channelId: parseInt(channelId) }))
    }
    return () => {
      dispatch(clearMessages())
    }
  }, [channelId, dispatch])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!messageInput.trim() || !channelId) return

    try {
      await dispatch(
        sendMessage({
          channelId: parseInt(channelId),
          data: {
            content: messageInput,
            channel_id: parseInt(channelId),
          },
        })
      ).unwrap()
      setMessageInput('')
    } catch (err) {
      alert('发送失败')
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage(e)
    }
  }

  if (loading) {
    return <div>加载中...</div>
  }

  return (
    <div style={{ display: 'flex', height: 'calc(100vh - 64px)' }}>
      {/* Messages Area */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        {/* Channel Header */}
        <div style={{ padding: '16px 24px', borderBottom: '1px solid #eee', background: '#fff' }}>
          <h2 style={{ margin: 0 }}># {selectedChannel?.name || '频道'}</h2>
          {selectedChannel?.description && (
            <p style={{ margin: '8px 0 0', color: '#666' }}>{selectedChannel.description}</p>
          )}
        </div>

        {/* Messages List */}
        <div style={{ flex: 1, overflowY: 'auto', padding: '16px 24px' }}>
          {messages.length === 0 ? (
            <div style={{ textAlign: 'center', color: '#999', marginTop: 40 }}>
              暂无消息，开始聊天吧
            </div>
          ) : (
            messages.map((message) => (
              <div
                key={message.id}
                style={{
                  display: 'flex',
                  gap: 12,
                  marginBottom: 16,
                  opacity: message.is_deleted ? 0.5 : 1,
                }}
              >
                <div
                  style={{
                    width: 36,
                    height: 36,
                    borderRadius: 4,
                    background: '#4a9eff',
                    color: '#fff',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: 14,
                  }}
                >
                  U
                </div>
                <div style={{ flex: 1 }}>
                  <div style={{ display: 'flex', alignItems: 'baseline', gap: 8 }}>
                    <span style={{ fontWeight: 600 }}>用户 {message.user_id}</span>
                    <span style={{ fontSize: 12, color: '#999' }}>
                      {new Date(message.created_at).toLocaleString('zh-CN')}
                    </span>
                    {message.updated_at && (
                      <span style={{ fontSize: 12, color: '#999' }}>(已编辑)</span>
                    )}
                  </div>
                  <div style={{ marginTop: 4, whiteSpace: 'pre-wrap' }}>
                    {message.is_deleted ? '(已删除)' : message.content}
                  </div>
                </div>
              </div>
            ))
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Message Input */}
        <div style={{ padding: '16px 24px', borderTop: '1px solid #eee', background: '#fff' }}>
          <form onSubmit={handleSendMessage} style={{ display: 'flex', gap: 8 }}>
            <textarea
              value={messageInput}
              onChange={(e) => setMessageInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder={`发送消息到 #${selectedChannel?.name || '频道'}`}
              style={{
                flex: 1,
                padding: 12,
                border: '1px solid #ddd',
                borderRadius: 4,
                resize: 'none',
                minHeight: 40,
                maxHeight: 120,
                fontFamily: 'inherit',
              }}
            />
            <button
              type="submit"
              style={{
                padding: '8px 24px',
                background: '#4a9eff',
                color: '#fff',
                border: 'none',
                borderRadius: 4,
                cursor: 'pointer',
                alignSelf: 'flex-end',
              }}
            >
              发送
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}

export default ChannelPage
