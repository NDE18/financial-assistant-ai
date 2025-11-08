import { useState } from 'react'
import { api } from '@/lib/api'

export function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string|undefined>()

  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(undefined)
    try {
      const params = new URLSearchParams()
      params.append('username', email)
      params.append('password', password)
      const { data } = await api.post('/auth/login', params, { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } })
      localStorage.setItem('token', data.access_token)
      window.location.href = '/'
    } catch (err: any) {
      setError('Identifiants invalides')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-[calc(100vh-0px)] grid place-items-center bg-gradient-to-br from-primary-50 to-white">
      <div className="w-full max-w-sm bg-white border rounded-xl shadow-lg p-6">
        <div className="mb-4 text-center">
          <div className="text-2xl font-semibold text-primary-700">Finance AI</div>
          <div className="text-sm text-gray-500">Connectez-vous pour continuer</div>
        </div>
        <form onSubmit={submit} className="space-y-3">
          <input value={email} onChange={e=>setEmail(e.target.value)} placeholder="Email" className="border rounded-md px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-primary-200" />
          <input type="password" value={password} onChange={e=>setPassword(e.target.value)} placeholder="Mot de passe" className="border rounded-md px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-primary-200" />
          {error && <div className="text-sm text-red-600">{error}</div>}
          <button disabled={loading} className="bg-primary-600 hover:bg-primary-700 transition-colors text-white rounded-md px-3 py-2 w-full shadow">
            {loading ? 'Connexion…' : 'Se connecter'}
          </button>
        </form>
      </div>
    </div>
  )
}
