import { SectionTitle } from '@/components/SectionTitle'
import { useState } from 'react'
import { api } from '@/lib/api'

export function Reconciliation() {
  const [res, setRes] = useState<{matched:number; total:number}|null>(null)
  const [busy, setBusy] = useState(false)
  const upload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0]
    if (!f) return
    const form = new FormData()
    form.append('file', f)
    setBusy(true)
    const { data } = await api.post('/reconciliation/upload', form, { headers: { 'Content-Type':'multipart/form-data' } })
    setRes(data)
    setBusy(false)
  }
  return (
    <div className="space-y-6">
      <SectionTitle>Rapprochement bancaire</SectionTitle>
      <div className="bg-white border rounded p-4 space-y-3">
        <input type="file" accept=".csv,.json" onChange={upload} />
        {busy && <div>Traitement…</div>}
        {res && <div className="text-sm">Correspondances: <b>{res.matched}</b> / {res.total}</div>}
      </div>
    </div>
  )
}
