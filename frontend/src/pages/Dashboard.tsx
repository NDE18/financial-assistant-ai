import { SectionTitle } from '@/components/SectionTitle'
import { useEffect, useState } from 'react'
import { api } from '@/lib/api'

export function Dashboard() {
  const [year, setYear] = useState<number>(new Date().getFullYear())
  const [month, setMonth] = useState<number>(new Date().getMonth() + 1)
  const [income, setIncome] = useState<number>(0)
  const [expense, setExpense] = useState<number>(0)
  const [net, setNet] = useState<number>(0)
  const [qtr, setQtr] = useState<{income:number; expense:number; net:number}>({income:0,expense:0,net:0})
  const [ann, setAnn] = useState<{income:number; expense:number; net:number; budget_total:number; budget_consumed:number; budget_remaining:number}>({income:0,expense:0,net:0,budget_total:0,budget_consumed:0,budget_remaining:0})
  const [loading, setLoading] = useState<boolean>(false)

  const load = async () => {
    setLoading(true)
    try {
      const { data } = await api.get('/reports/monthly', { params: { year, month } })
      setIncome(Number(data.income || 0))
      setExpense(Number(data.expense || 0))
      setNet(Number(data.net || 0))
      // quarterly
      const quarter = Math.floor((month - 1) / 3) + 1
      const qRes = await api.get('/reports/quarterly', { params: { year, quarter } })
      setQtr({ income: Number(qRes.data.income||0), expense: Number(qRes.data.expense||0), net: Number(qRes.data.net||0) })
      const annRes = await api.get('/reports/annual', { params: { year } })
      setAnn(annRes.data)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  return (
    <div className="space-y-6">
      <SectionTitle>Tableau de bord</SectionTitle>

      <div className="flex items-center gap-2">
        <input type="number" value={year} onChange={e=>setYear(Number(e.target.value))} className="border rounded px-3 py-2 w-28" />
        <input type="number" min={1} max={12} value={month} onChange={e=>setMonth(Number(e.target.value))} className="border rounded px-3 py-2 w-24" />
        <button onClick={load} className="bg-primary-600 hover:bg-primary-700 text-white rounded-md px-3 py-2">Actualiser</button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {[{label:'Recettes', value:income},{label:'Dépenses', value:expense},{label:'Net', value:net}].map((c)=> (
          <div key={c.label} className="rounded-lg border bg-white p-4">
            <div className="text-sm text-gray-500">{c.label} (mois)</div>
            <div className="text-2xl font-semibold mt-1">{loading ? '...' : c.value.toFixed(2)}</div>
          </div>
        ))}
      </div>

      <SectionTitle>Trimestriel</SectionTitle>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {[{label:'Recettes T', value:qtr.income},{label:'Dépenses T', value:qtr.expense},{label:'Net T', value:qtr.net}].map((c)=> (
          <div key={c.label} className="rounded-lg border bg-white p-4">
            <div className="text-sm text-gray-500">{c.label}</div>
            <div className="text-2xl font-semibold mt-1">{loading ? '...' : Number(c.value||0).toFixed(2)}</div>
          </div>
        ))}
      </div>

      <SectionTitle>Annuel</SectionTitle>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {[{label:'Recettes YTD', value:ann.income},{label:'Dépenses YTD', value:ann.expense},{label:'Net YTD', value:ann.net},{label:'Budget annuel', value:ann.budget_total}].map((c)=> (
          <div key={c.label} className="rounded-lg border bg-white p-4">
            <div className="text-sm text-gray-500">{c.label}</div>
            <div className="text-2xl font-semibold mt-1">{loading ? '...' : Number(c.value||0).toFixed(2)}</div>
          </div>
        ))}
      </div>

      <div className="bg-white border rounded p-4">
        <div className="text-sm text-gray-600 mb-2">Consommation budget annuel</div>
        <div className="w-full bg-gray-100 rounded h-3 overflow-hidden">
          <div className="bg-primary-500 h-3" style={{ width: `${ann.budget_total>0 ? Math.min(100, Math.round((ann.budget_consumed/ann.budget_total)*100)) : 0}%` }} />
        </div>
        <div className="mt-1 text-xs text-gray-600">{Number(ann.budget_consumed||0).toFixed(2)} / {Number(ann.budget_total||0).toFixed(2)} ({ann.budget_total>0 ? Math.min(100, Math.round((ann.budget_consumed/ann.budget_total)*100)) : 0}%)</div>
      </div>
    </div>
  )
}
