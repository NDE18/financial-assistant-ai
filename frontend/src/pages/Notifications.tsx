import { SectionTitle } from '@/components/SectionTitle'
import { useEffect, useState } from 'react'
import { api } from '@/lib/api'

type Alert = { id:number; type:string; severity:string; message:string; created_at:string; resolved:boolean }

export function Notifications() {
  const [rows, setRows] = useState<Alert[]>([])
  const load = async ()=>{ const { data } = await api.get('/notifications'); setRows(data) }
  useEffect(()=>{ load() },[])
  const resolve = async (id:number)=>{ await api.patch(`/notifications/${id}/resolve`); await load() }
  const invoiceAlerts = rows.filter(a=>a.type==='invoice_due' && !a.resolved)
  return (
    <div className="space-y-6">
      <SectionTitle>Notifications</SectionTitle>
      <div className="bg-white border rounded divide-y">
        {invoiceAlerts.map(a => (
          <div key={a.id} className="p-3 flex items-center justify-between">
            <div>
              <div className="text-sm text-gray-500">{new Date(a.created_at).toLocaleString()}</div>
              <div className="font-medium">{a.message}</div>
            </div>
            <div className="flex items-center gap-2">
              <span className={`text-xs px-2 py-1 rounded ${a.severity==='critical'?'bg-red-100 text-red-700':a.severity==='warning'?'bg-yellow-100 text-yellow-700':'bg-gray-100 text-gray-700'}`}>{a.severity}</span>
              <button onClick={()=>resolve(a.id)} className="text-xs border rounded px-2 py-1">Marquer résolue</button>
            </div>
          </div>
        ))}
        {invoiceAlerts.length===0 && <div className="p-4 text-sm text-gray-500">Aucune alerte d'échéance</div>}
      </div>
    </div>
  )
}
