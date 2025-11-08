import { useEffect, useState } from 'react'
import { api } from '@/lib/api'
import { SectionTitle } from '@/components/SectionTitle'

interface Budget {
  id?: number
  name: string
  period: string
  start_date: string
  end_date: string
  total_amount: number
}

export function Budgets() {
  const [rows, setRows] = useState<Budget[]>([])
  const [form, setForm] = useState<Budget>({ name: '', period: 'monthly', start_date: new Date().toISOString().slice(0,10), end_date: new Date().toISOString().slice(0,10), total_amount: 0 })

  const load = async () => {
    const { data } = await api.get<Budget[]>('/budgets')
    setRows(data)
  }
  useEffect(()=>{ load() },[])

  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    await api.post('/budgets', form)
    setForm({ name: '', period: 'monthly', start_date: new Date().toISOString().slice(0,10), end_date: new Date().toISOString().slice(0,10), total_amount: 0 })
    await load()
  }

  return (
    <div className="space-y-6">
      <SectionTitle>Budgets</SectionTitle>

      <form onSubmit={submit} className="bg-white border rounded p-4 grid grid-cols-1 md:grid-cols-6 gap-3">
        <input placeholder="Nom" value={form.name} onChange={e=>setForm({...form, name:e.target.value})} className="border rounded px-3 py-2" />
        <select value={form.period} onChange={e=>setForm({...form, period:e.target.value})} className="border rounded px-3 py-2">
          <option value="monthly">Mensuel</option>
          <option value="quarterly">Trimestriel</option>
          <option value="yearly">Annuel</option>
        </select>
        <input type="date" value={form.start_date} onChange={e=>setForm({...form, start_date:e.target.value})} className="border rounded px-3 py-2" />
        <input type="date" value={form.end_date} onChange={e=>setForm({...form, end_date:e.target.value})} className="border rounded px-3 py-2" />
        <input type="number" step="0.01" value={form.total_amount} onChange={e=>setForm({...form, total_amount:Number(e.target.value)})} className="border rounded px-3 py-2" />
        <button className="bg-primary-600 hover:bg-primary-700 transition-colors text-white rounded-md px-3 py-2 shadow">Créer</button>
      </form>

      <div className="overflow-x-auto bg-white border rounded">
        <table className="min-w-full text-sm">
          <thead className="bg-gray-50 text-gray-600">
            <tr className="[&>th]:p-2">
              <th className="text-left">Nom</th>
              <th className="text-left">Période</th>
              <th className="text-left">Début</th>
              <th className="text-left">Fin</th>
              <th className="text-left">Montant</th>
            </tr>
          </thead>
          <tbody>
            {rows.map(r => (
              <tr key={r.id} className="odd:bg-white even:bg-gray-50 border-t [&>td]:p-2">
                <td>{r.name}</td>
                <td>{r.period}</td>
                <td>{r.start_date}</td>
                <td>{r.end_date}</td>
                <td>{r.total_amount.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
