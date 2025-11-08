import { useEffect, useState } from 'react'
import { api } from '@/lib/api'
import { SectionTitle } from '@/components/SectionTitle'

export function Reports() {
  const [report, setReport] = useState<any | null>(null)
  const [year, setYear] = useState<number>(new Date().getFullYear())
  const [month, setMonth] = useState<number>(new Date().getMonth()+1)

  const load = async () => {
    const { data } = await api.get('/reports/monthly', { params: { year, month } })
    setReport(data)
  }

  useEffect(()=>{ load() }, [])

  return (
    <div className="space-y-6">
      <SectionTitle>Rapport mensuel</SectionTitle>

      <div className="flex gap-2 items-center">
        <input type="number" value={year} onChange={e=>setYear(Number(e.target.value))} className="border rounded px-3 py-2" />
        <input type="number" value={month} min={1} max={12} onChange={e=>setMonth(Number(e.target.value))} className="border rounded px-3 py-2" />
        <button onClick={load} className="bg-primary-600 hover:bg-primary-700 transition-colors text-white rounded-md px-3 py-2 shadow">Générer</button>
      </div>

      {report && (
        <div className="bg-white border rounded p-4 space-y-2">
          <div className="text-sm text-gray-600">Période {report.period.month}/{report.period.year}</div>
          <table className="text-sm">
            <tbody>
              <tr><td className="pr-4 text-gray-600">Recettes</td><td className="font-semibold">{report.income.toFixed(2)}</td></tr>
              <tr><td className="pr-4 text-gray-600">Dépenses</td><td className="font-semibold">{report.expense.toFixed(2)}</td></tr>
              <tr><td className="pr-4 text-gray-600">Net</td><td className="font-semibold">{report.net.toFixed(2)}</td></tr>
            </tbody>
          </table>
          <div className="mt-2 p-3 bg-gray-50 rounded">{report.narrative}</div>
        </div>
      )}
    </div>
  )
}
