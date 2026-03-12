import React from 'react'
import { Link, Outlet, useLocation } from 'react-router-dom'

const AdminLayout: React.FC = () => {
  const location = useLocation()

  const navItems = [
    { path: '/admin/users', label: '用户管理' },
    { path: '/admin/channels', label: '频道管理' },
  ]

  return (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      {/* Sidebar */}
      <aside style={{ width: 240, background: '#1a1a1a', padding: '16px' }}>
        <h2 style={{ color: '#fff', marginBottom: 24 }}>Omega</h2>
        <nav>
          {navItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              style={{
                display: 'block',
                padding: '12px 16px',
                color: location.pathname === item.path ? '#4a9eff' : '#999',
                textDecoration: 'none',
                borderRadius: 4,
                background:
                  location.pathname === item.path ? 'rgba(74, 158, 255, 0.1)' : 'transparent',
              }}
            >
              {item.label}
            </Link>
          ))}
        </nav>
      </aside>

      {/* Main content */}
      <main style={{ flex: 1, padding: 24, background: '#f5f5f5' }}>
        <Outlet />
      </main>
    </div>
  )
}

export default AdminLayout
