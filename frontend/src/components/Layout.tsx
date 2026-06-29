import { NavLink, Outlet } from 'react-router-dom'

const links = [
  { to: '/', label: 'Dashboard' },
  { to: '/chat', label: 'Chat' },
  { to: '/setup', label: 'Setup' },
  { to: '/admin', label: 'Admin' },
  { to: '/demo', label: 'Demo' },
]

export default function Layout() {
  return (
    <div className="flex h-screen bg-gray-950 text-gray-100">
      <nav className="w-14 bg-gray-900 border-r border-gray-800 flex flex-col items-center py-4 gap-4">
        <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center text-xs font-bold mb-4">
          OH
        </div>
        {links.map((l) => (
          <NavLink
            key={l.to}
            to={l.to}
            end={l.to === '/'}
            className={({ isActive }) =>
              `w-10 h-10 rounded-lg flex items-center justify-center text-xs font-medium transition-colors ${
                isActive
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-500 hover:bg-gray-800 hover:text-gray-300'
              }`
            }
            title={l.label}
          >
            {l.label[0]}
          </NavLink>
        ))}
      </nav>
      <main className="flex-1 overflow-hidden">
        <Outlet />
      </main>
    </div>
  )
}
