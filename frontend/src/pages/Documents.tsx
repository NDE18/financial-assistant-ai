import { SectionTitle } from '@/components/SectionTitle'
import { useState } from 'react'
import { api } from '@/lib/api'

export function Documents() {
  const [invId, setInvId] = useState<number|undefined>()
  const [busy, setBusy] = useState(false)
  const upload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0]
    if (!f) return
    const form = new FormData()
    form.append('file', f)
    setBusy(true)
    const { data } = await api.post('/invoices/ocr', form, { headers: { 'Content-Type':'multipart/form-data' } })
    if (data?.id) setInvId(data.id)
    setBusy(false)
  }
  return (
    <div className="space-y-6">
      <SectionTitle>Documents</SectionTitle>
      <div className="bg-white border rounded p-4 space-y-3">
        <input type="file" accept="application/pdf" onChange={upload} className="block text-sm" />
        {busy && <div className="text-sm text-gray-600">OCR en cours…</div>}
        {invId && <div className="text-sm text-green-700">Facture créée: ID {invId}</div>}
      </div>
    </div>
  )
}
