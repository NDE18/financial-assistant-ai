import { NavLink, Outlet, Route, Routes, useLocation, useNavigate } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { api } from '@/lib/api'
import { Dashboard } from './pages/Dashboard'
import { Transactions } from './pages/Transactions'
import { Budgets } from './pages/Budgets'
import { Reports } from './pages/Reports'
import { Analysis } from './pages/Analysis'
import { Reconciliation } from './pages/Reconciliation'
import { Documents } from './pages/Documents'
import { Treasury } from './pages/Treasury'
import { Notifications } from './pages/Notifications'
import { Audit } from './pages/Audit'
import { Rates } from './pages/Rates'
import { Login } from './pages/Login'
import { UsersAdmin } from './pages/UsersAdmin'

function Layout() {
  const [me, setMe] = useState<{email:string; role:string} | null>(null)
  const [authChecked, setAuthChecked] = useState(false)
  const location = useLocation()
  const navigate = useNavigate()

  useEffect(() => {
    const token = localStorage.getItem('token')
    const onLoginPage = location.pathname.startsWith('/login')
    if (!token) {
      if (!onLoginPage) navigate('/login')
      setMe(null)
      setAuthChecked(true)
      return
    }
    // fetch current user
    ;(async ()=>{
      try {
        const { data } = await api.get('/auth/me')
        setMe(data)
      } catch {
        localStorage.removeItem('token')
        if (!onLoginPage) navigate('/login')
      } finally {
        setAuthChecked(true)
      }
    })()
  }, [location.pathname, navigate])

  const logout = () => {
    localStorage.removeItem('token')
    setMe(null)
    navigate('/login')
  }

  const isLoggedIn = !!me
  if (!authChecked && localStorage.getItem('token')) {
    return (
      <div className="min-h-screen grid place-items-center text-gray-500">Chargement…</div>
    )
  }

  return (
    <div className={`min-h-screen ${isLoggedIn ? 'grid grid-cols-[260px_1fr]' : ''}`}>
      {isLoggedIn && (
        <aside className="bg-white border-r border-gray-200 p-4">
        <div className="mb-4 flex items-center justify-between">
          <h1 className="text-xl font-semibold text-primary-700">Finance AI</h1>
          {me?.role==='admin' && (<span className="text-xs bg-primary-100 text-primary-700 px-2 py-0.5 rounded">admin</span>)}
        </div>
        <nav className="space-y-1">
          {[
            /* Admin */
            { to: '/', label: 'Tableau de bord', roles: ['admin','finance_manager','accountant','user'] },
            { to: '/transactions', label: 'Transactions', roles: ['admin','finance_manager','accountant'] },
            { to: '/budgets', label: 'Budgets', roles: ['admin','finance_manager'] },
            { to: '/reports', label: 'Rapports', roles: ['admin','finance_manager','accountant','user'] },
            { to: '/analysis', label: 'Analyses', roles: ['admin','finance_manager','accountant','user'] },
            { to: '/reconciliation', label: 'Rapprochement', roles: ['admin','finance_manager','accountant'] },
            { to: '/documents', label: 'Documents', roles: ['admin','finance_manager','accountant'] },
            { to: '/treasury', label: 'Trésorerie', roles: ['admin','finance_manager'] },
            { to: '/notifications', label: 'Notifications', roles: ['admin','finance_manager','accountant','user'] },
            { to: '/rates', label: 'Taux de change', roles: ['admin'] },
            { to: '/users', label: 'Utilisateurs', roles: ['admin'] },
            { to: '/login', label: 'Connexion', hideWhenAuth: true },
            { to: '/audit', label: 'Audit', roles: ['admin','finance_manager'] },
          ]
            .filter(item => (item as any).hideWhenAuth ? !me : true)
            .filter(item => (item as any).roles ? (me && (item as any).roles.includes(me.role)) : true)
            .map(({ to, label }) => (
              <NavLink
                key={to}
                to={to}
                className={({ isActive }) =>
                  `block rounded-md px-3 py-2 text-sm transition-colors ${
                    isActive
                      ? 'bg-primary-50 text-primary-700 shadow-sm'
                      : 'text-gray-700 hover:bg-gray-50 hover:text-primary-700'
                  }`
                }
                end
              >
                {label}
              </NavLink>
            ))}
        </nav>
        <div className="mt-6">
<button onClick={logout} className="inline-flex items-center gap-2 text-sm text-gray-700 border border-gray-300 rounded-md px-3 py-1.5 bg-white hover:bg-gray-50">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" className="w-4 h-4">
              <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6A2.25 2.25 0 005.25 5.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15M12 9l-3 3m0 0l3 3m-3-3h12" />
            </svg>
            <span>Déconnexion</span>
          </button>
        </div>
        </aside>
      )}
      <main className="p-0">
        {isLoggedIn && (
          <div className="sticky top-0 z-10 bg-white/90 backdrop-blur border-b">
            <div className="p-3 flex items-center gap-2">
              <input placeholder="Rechercher..." className="border rounded-md px-3 py-2 w-full max-w-md focus:outline-none focus:ring-2 focus:ring-primary-200" onKeyDown={(e)=>{ if (e.key==='Enter') { const v=(e.target as HTMLInputElement).value; navigate(`/analysis?q=${encodeURIComponent(v)}`) } }} />
              <button className="bg-primary-600 hover:bg-primary-700 text-white rounded-md px-3 py-2" onClick={()=>{
                const el = document.querySelector('input[placeholder=\"Rechercher...\"]') as HTMLInputElement|null; if (el) navigate(`/analysis?q=${encodeURIComponent(el.value)}`)
              }}>Rechercher</button>
            </div>
          </div>
        )}
        <div className="p-6">
          <Outlet />
        </div>
      </main>
    </div>
  )
}

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<Dashboard />} />
        <Route path="/transactions" element={<Transactions />} />
        <Route path="/budgets" element={<Budgets />} />
        <Route path="/reports" element={<Reports />} />
        <Route path="/analysis" element={<Analysis />} />
        <Route path="/reconciliation" element={<Reconciliation />} />
        <Route path="/documents" element={<Documents />} />
        <Route path="/treasury" element={<Treasury />} />
        <Route path="/notifications" element={<Notifications />} />
        <Route path="/rates" element={<Rates />} />
        <Route path="/login" element={<Login />} />
        <Route path="/audit" element={<Audit />} />
        <Route path="/users" element={<UsersAdmin />} />
      </Route>
    </Routes>
  )
}
