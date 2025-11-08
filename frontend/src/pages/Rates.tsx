import { useEffect, useState } from 'react'
import { api } from '@/lib/api'
import { SectionTitle } from '@/components/SectionTitle'

interface Rate { id:number; currency:string; date:string; rate_to_base:number }

export function Rates() {
  const [rows, setRows] = useState<Rate[]>([])
  const [currency, setCurrency] = useState('USD')
  const [rate, setRate] = useState<number>(1)
  const [date, setDate] = useState<string>('')

  const load = async ()=>{
    const { data } = await api.get('/fx/rates')
    setRows(data)
  }
  useEffect(()=>{ load() },[])

  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    await api.post('/fx/rates', null, { params: { currency, rate_to_base: rate, on_date: date || undefined } })
    setDate('')
    await load()
  }

  return (
    <div className="space-y-6">
      <SectionTitle>Taux de change</SectionTitle>
      <form onSubmit={submit} className="bg-white border rounded p-4 grid grid-cols-1 md:grid-cols-5 gap-3">
        <input value={currency} onChange={e=>setCurrency(e.target.value.toUpperCase())} className="border rounded px-3 py-2" />
        <input type="number" step="0.0001" value={rate} onChange={e=>setRate(Number(e.target.value))} className="border rounded px-3 py-2" />
        <input type="date" value={date} onChange={e=>setDate(e.target.value)} className="border rounded px-3 py-2" />
        <div className="md:col-span-2"><button className="bg-primary-600 text-white rounded px-3 py-2">Enregistrer</button></div>
      </form>
      <div className="overflow-x-auto bg-white border rounded">
        <table className="min-w-full text-sm">
          <thead className="bg-gray-50 text-gray-600">
            <tr>
              <th className="text-left p-2">Devise</th>
              <th className="text-left p-2">Date</th>
              <th className="text-left p-2">Taux → EUR</th>
            </tr>
          </thead>
          <tbody>
            {rows.map(r => (
              <tr key={r.id} className="border-t">
                <td className="p-2">{r.currency}</td>
                <td className="p-2">{r.date}</td>
                <td className="p-2">{r.rate_to_base}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
