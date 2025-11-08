import { useEffect, useState } from 'react'
import { api } from '@/lib/api'
import { SectionTitle } from '@/components/SectionTitle'

type User = { id:number; email:string; role:string; is_active:boolean }

export function UsersAdmin() {
  const [rows, setRows] = useState<User[]>([])
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [role, setRole] = useState<'user'|'admin'>('user')

  const load = async ()=>{ const { data } = await api.get('/users'); setRows(data) }
  useEffect(()=>{ load() }, [])

  const add = async (e: React.FormEvent)=>{
    e.preventDefault()
    await api.post('/users', null, { params: { email, password, role } })
    setEmail(''); setPassword(''); setRole('user')
    await load()
  }
  const del = async (id:number)=>{ await api.delete(`/users/${id}`); await load() }
  const setActive = async (id:number, is_active:boolean)=>{ await api.patch(`/users/${id}/activate`, null, { params: { is_active } }); await load() }

  return (
    <div className="space-y-6">
      <SectionTitle>Utilisateurs</SectionTitle>
      <form onSubmit={add} className="bg-white border rounded p-4 grid grid-cols-1 md:grid-cols-5 gap-3">
        <input value={email} onChange={e=>setEmail(e.target.value)} placeholder="Email" className="border rounded-md px-3 py-2" />
        <input type="password" value={password} onChange={e=>setPassword(e.target.value)} placeholder="Mot de passe" className="border rounded-md px-3 py-2" />
        <select value={role} onChange={e=>setRole(e.target.value as any)} className="border rounded-md px-3 py-2">
          <option value="user">Utilisateur</option>
          <option value="admin">Admin</option>
        </select>
        <div className="md:col-span-2">
          <button className="bg-primary-600 hover:bg-primary-700 text-white rounded-md px-3 py-2 shadow">Ajouter</button>
        </div>
      </form>

      <div className="overflow-x-auto bg-white border rounded">
        <table className="min-w-full text-sm">
          <thead className="bg-gray-50 text-gray-600">
            <tr className="[&>th]:p-2">
              <th className="text-left">Email</th>
              <th className="text-left">Rôle</th>
              <th className="text-left">Statut</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {rows.map(u => (
              <tr key={u.id} className="odd:bg-white even:bg-gray-50 border-t [&>td]:p-2">
                <td>{u.email}</td>
                <td><span className={`text-xs px-2 py-1 rounded ${u.role==='admin'?'bg-primary-100 text-primary-700':'bg-gray-100 text-gray-700'}`}>{u.role}</span></td>
                <td>{u.is_active ? 'Actif' : 'Bloqué'}</td>
                <td className="text-right space-x-2">
                  <button onClick={()=>setActive(u.id, !u.is_active)} className="text-xs border rounded px-2 py-1">{u.is_active ? 'Bloquer' : 'Activer'}</button>
                  <button onClick={()=>del(u.id)} className="text-xs border rounded px-2 py-1 text-red-700">Supprimer</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}