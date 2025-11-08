import { useEffect, useState } from 'react'
import { api } from '@/lib/api'
import { SectionTitle } from '@/components/SectionTitle'

interface Tx {
  id?: number
  account_id?: number
  date: string
  amount: number
  direction: 'income' | 'expense'
  category?: string | null
  description?: string | null
}

export function Transactions() {
  const [rows, setRows] = useState<Tx[]>([])
  const [form, setForm] = useState<Tx>({ date: new Date().toISOString().slice(0,10), amount: 0, direction: 'expense' })
  const [loading, setLoading] = useState(false)

  const load = async () => {
    const { data } = await api.get<Tx[]>('/transactions')
    setRows(data)
  }

  useEffect(() => {
    load()
  }, [])

  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    await api.post('/transactions', form)
    setForm({ date: new Date().toISOString().slice(0,10), amount: 0, direction: 'expense' })
    await load()
    setLoading(false)
  }

  const categorize = async () => {
    setLoading(true)
    await api.post('/transactions/categorize')
    await load()
    setLoading(false)
  }

  return (
    <div className="space-y-6">
      <SectionTitle>Transactions</SectionTitle>

      <form onSubmit={submit} className="bg-white border rounded p-4 grid grid-cols-1 md:grid-cols-6 gap-3">
        <input type="date" value={form.date} onChange={e=>setForm({...form, date:e.target.value})} className="border rounded px-3 py-2" />
        <input type="number" step="0.01" placeholder="Montant" value={form.amount} onChange={e=>setForm({...form, amount:Number(e.target.value)})} className="border rounded px-3 py-2" />
        <select value={form.direction} onChange={e=>setForm({...form, direction:e.target.value as Tx['direction']})} className="border rounded px-3 py-2">
          <option value="expense">Dépense</option>
          <option value="income">Recette</option>
        </select>
        <input placeholder="Catégorie (optionnel)" value={form.category ?? ''} onChange={e=>setForm({...form, category:e.target.value})} className="border rounded px-3 py-2" />
        <input placeholder="Description" value={form.description ?? ''} onChange={e=>setForm({...form, description:e.target.value})} className="border rounded px-3 py-2 md:col-span-2" />
        <button disabled={loading} className="bg-primary-600 hover:bg-primary-700 transition-colors text-white rounded-md px-3 py-2 shadow">Ajouter</button>
      </form>

      <div className="flex justify-between items-center">
        <div className="text-sm text-gray-600">{rows.length} transactions</div>
        <button onClick={categorize} disabled={loading} className="bg-primary-50 hover:bg-primary-100 text-primary-700 border border-primary-200 rounded-md px-3 py-2">Catégoriser via AI</button>
      </div>

      <div className="overflow-x-auto bg-white border rounded">
        <table className="min-w-full text-sm">
          <thead className="bg-gray-50 text-gray-600">
            <tr className="[&>th]:p-2">
              <th className="text-left">Date</th>
              <th className="text-left">Montant</th>
              <th className="text-left">Sens</th>
              <th className="text-left">Catégorie</th>
              <th className="text-left">Description</th>
              <th className="text-left">Pièces</th>
            </tr>
          </thead>
          <tbody>
            {rows.map(r => (
              <tr key={r.id} className="odd:bg-white even:bg-gray-50 border-t [&>td]:p-2">
                <td>{r.date}</td>
                <td>{r.amount.toFixed(2)}</td>
                <td>{r.direction === 'income' ? 'Recette' : 'Dépense'}</td>
                <td>{r.category ?? '—'}</td>
                <td>{r.description ?? '—'}</td>
                <td>
<label className="inline-flex items-center gap-2 px-3 py-1.5 rounded-md border border-primary-200 text-primary-700 bg-primary-50 hover:bg-primary-100 cursor-pointer">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" className="w-4 h-4">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M18.375 12.739l-7.5 7.5a4.125 4.125 0 11-5.836-5.836l9-9a3 3 0 114.243 4.243l-9 9a1.875 1.875 0 01-2.652-2.652l7.5-7.5" />
                    </svg>
                    <span>Attacher</span>
                    <input type="file" className="hidden" onChange={async (e)=>{
                      const f = e.target.files?.[0]
                      if (!f || !r.id) return
                      const form = new FormData()
                      form.append('file', f)
                      await api.post(`/documents/upload`, form, { params: { transaction_id: r.id }, headers: { 'Content-Type':'multipart/form-data' } })
                      e.currentTarget.value = ''
                    }} />
                  </label>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
