import { SectionTitle } from '@/components/SectionTitle'
import { useEffect, useState } from 'react'
import { api } from '@/lib/api'
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from 'recharts'
import { useToast } from '@/components/ToastProvider'

export function Treasury() {
  const [data, setData] = useState<{months:string[], values:number[], forecast:number[]}|null>(null)
  const [error, setError] = useState<string|undefined>()
  const { push } = useToast()

  const load = async ()=>{
    try {
      const { data } = await api.get('/treasury/forecast')
      setData(data)
      setError(undefined)
      if ((!data.months || data.months.length===0) && (!data.forecast || data.forecast.length===0)) {
        setError('Aucune donnée de trésorerie disponible')
      }
    } catch (e:any) {
      setError('Impossible de charger la trésorerie')
      push('Erreur lors du chargement de la trésorerie', 'error')
      setData({ months:[], values:[], forecast:[] })
    }
  }
  useEffect(()=>{ load() }, [])
  const chartData = data ? [
    ...data.months.map((m, i)=>({ name:m, net:(data.values?.[i] ?? 0) })),
    ...data.forecast.map((v, i)=>({ name:`F+${i+1}`, forecast:v }))
  ] : []
  return (
    <div className="space-y-6">
      <SectionTitle>Trésorerie</SectionTitle>
      <div className="bg-white border rounded p-4 h-80">
        {data ? (
          chartData.length>0 ? (
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="net" stroke="#10b981" dot={false} />
                <Line type="monotone" dataKey="forecast" stroke="#a7f3d0" strokeDasharray="4 4" dot={false} />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <div className="text-sm text-gray-600">{error ?? 'Aucune donnée'}</div>
          )
        ) : (
          <div>Chargement…</div>
        )}
      </div>
    </div>
  )
}
