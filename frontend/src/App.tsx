import React, { useEffect, useState } from 'react'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import { Provider } from 'react-redux'
import { store } from './stores'
import AdminLayout from './pages/admin/AdminLayout'
import UserManagePage from './pages/admin/UserManagePage'

const LoginPage: React.FC = () => {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    const formData = new FormData()
    formData.append('username', username)
    formData.append('password', password)

    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        body: formData,
      })

      if (response.ok) {
        const data = await response.json()
        localStorage.setItem('access_token', data.access_token)
        window.location.href = '/'
      } else {
        alert('登录失败')
      }
    } catch (error) {
      alert('登录失败')
    }
  }

  return (
    <div
      style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}
    >
      <form
        onSubmit={handleLogin}
        style={{ width: 320, padding: 24, border: '1px solid #ddd', borderRadius: 8 }}
      >
        <h2 style={{ marginBottom: 24 }}>登录</h2>
        <div style={{ marginBottom: 16 }}>
          <input
            type="text"
            placeholder="用户名"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            style={{ width: '100%', padding: 8, border: '1px solid #ddd', borderRadius: 4 }}
          />
        </div>
        <div style={{ marginBottom: 24 }}>
          <input
            type="password"
            placeholder="密码"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={{ width: '100%', padding: 8, border: '1px solid #ddd', borderRadius: 4 }}
          />
        </div>
        <button
          type="submit"
          style={{
            width: '100%',
            padding: 8,
            background: '#4a9eff',
            color: '#fff',
            border: 'none',
            borderRadius: 4,
          }}
        >
          登录
        </button>
      </form>
    </div>
  )
}

const HomePage: React.FC = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false)

  useEffect(() => {
    const token = localStorage.getItem('access_token')
    setIsLoggedIn(!!token)
  }, [])

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    setIsLoggedIn(false)
  }

  return (
    <div style={{ padding: 24 }}>
      <h1>Anteam - Slack-style Chat</h1>
      {isLoggedIn ? (
        <>
          <p>欢迎！</p>
          <button onClick={handleLogout} style={{ padding: '8px 16px', marginRight: 8 }}>
            退出
          </button>
          <Link to="/admin/users" style={{ padding: '8px 16px', marginRight: 8 }}>
            管理后台
          </Link>
        </>
      ) : (
        <Link
          to="/login"
          style={{
            padding: '8px 16px',
            background: '#4a9eff',
            color: '#fff',
            textDecoration: 'none',
            borderRadius: 4,
          }}
        >
          登录
        </Link>
      )}
    </div>
  )
}

const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isAuthorized, setIsAuthorized] = useState<boolean | null>(null)

  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('access_token')
      if (!token) {
        setIsAuthorized(false)
        return
      }

      try {
        const response = await fetch('/api/auth/me', {
          headers: { Authorization: `Bearer ${token}` },
        })

        if (response.ok) {
          const user = await response.json()
          setIsAuthorized(user.is_superuser)
        } else {
          setIsAuthorized(false)
        }
      } catch {
        setIsAuthorized(false)
      }
    }

    checkAuth()
  }, [])

  if (isAuthorized === null) {
    return <div>检查权限...</div>
  }

  if (!isAuthorized) {
    return (
      <div style={{ padding: 24 }}>
        <h2>权限不足</h2>
        <p>只有超级用户才能访问此页面。</p>
      </div>
    )
  }

  return <>{children}</>
}

function App() {
  return (
    <Provider store={store}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route
            path="/admin"
            element={
              <ProtectedRoute>
                <AdminLayout />
              </ProtectedRoute>
            }
          >
            <Route path="users" element={<UserManagePage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </Provider>
  )
}

export default App
