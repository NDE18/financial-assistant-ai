import { SectionTitle } from '@/components/SectionTitle'
import { useEffect, useState } from 'react'
import { useLocation } from 'react-router-dom'
import { api } from '@/lib/api'

export function Analysis() {
  const location = useLocation()
  const params = new URLSearchParams(location.search)
  const q = params.get('q') || ''
  const [data, setData] = useState<{transactions:any[]; invoices:any[]; budgets:any[]; documents:any[]} | null>(null)

  useEffect(()=>{
    (async ()=>{
      if (!q) { setData(null); return }
      const { data } = await api.get('/search', { params: { q } })
      setData(data)
    })()
  }, [q])

  return (
    <div className="space-y-6">
      <SectionTitle>Analyses</SectionTitle>

      <div className="text-sm text-gray-600">Résultats pour: <b>{q || '—'}</b></div>

      {data && (
        <div className="grid md:grid-cols-2 gap-4">
          <div className="bg-white border rounded p-4">
            <div className="font-semibold mb-2">Transactions</div>
            <div className="overflow-x-auto">
              <table className="min-w-full text-sm">
                <thead className="bg-gray-50 text-gray-600">
                  <tr className="[&>th]:p-2"><th className="text-left">Date</th><th className="text-left">Montant</th><th className="text-left">Catégorie</th><th className="text-left">Description</th></tr>
                </thead>
                <tbody>
                  {data.transactions.map((t)=> (
                    <tr key={t.id} className="odd:bg-white even:bg-gray-50 border-t [&>td]:p-2">
                      <td>{t.date}</td>
                      <td>{t.amount?.toFixed ? t.amount.toFixed(2) : t.amount}</td>
                      <td>{t.category ?? '—'}</td>
                      <td>{t.description ?? '—'}</td>
                    </tr>
                  ))}
                  {data.transactions.length===0 && <tr><td className="p-2 text-gray-500" colSpan={4}>Aucune transaction</td></tr>}
                </tbody>
              </table>
            </div>
          </div>

          <div className="bg-white border rounded p-4">
            <div className="font-semibold mb-2">Factures</div>
            <div className="overflow-x-auto">
              <table className="min-w-full text-sm">
                <thead className="bg-gray-50 text-gray-600">
                  <tr className="[&>th]:p-2"><th className="text-left">Contrepartie</th><th className="text-left">Montant</th><th className="text-left">Échéance</th><th className="text-left">Devise</th></tr>
                </thead>
                <tbody>
                  {data.invoices.map((i)=> (
                    <tr key={i.id} className="odd:bg-white even:bg-gray-50 border-t [&>td]:p-2">
                      <td>{i.counterparty ?? '—'}</td>
                      <td>{i.amount?.toFixed ? i.amount.toFixed(2) : i.amount}</td>
                      <td>{i.due_date}</td>
                      <td>{i.currency}</td>
                    </tr>
                  ))}
                  {data.invoices.length===0 && <tr><td className="p-2 text-gray-500" colSpan={4}>Aucune facture</td></tr>}
                </tbody>
              </table>
            </div>
          </div>

          <div className="bg-white border rounded p-4">
            <div className="font-semibold mb-2">Budgets</div>
            <div className="overflow-x-auto">
              <table className="min-w-full text-sm">
                <thead className="bg-gray-50 text-gray-600">
                  <tr className="[&>th]:p-2"><th className="text-left">Nom</th><th className="text-left">Période</th><th className="text-left">Début</th><th className="text-left">Fin</th></tr>
                </thead>
                <tbody>
                  {data.budgets.map((b)=> (
                    <tr key={b.id} className="odd:bg-white even:bg-gray-50 border-t [&>td]:p-2">
                      <td>{b.name}</td>
                      <td>{b.period}</td>
                      <td>{b.start_date}</td>
                      <td>{b.end_date}</td>
                    </tr>
                  ))}
                  {data.budgets.length===0 && <tr><td className="p-2 text-gray-500" colSpan={4}>Aucun budget</td></tr>}
                </tbody>
              </table>
            </div>
          </div>

          <div className="bg-white border rounded p-4">
            <div className="font-semibold mb-2">Documents</div>
            <div className="overflow-x-auto">
              <table className="min-w-full text-sm">
                <thead className="bg-gray-50 text-gray-600">
                  <tr className="[&>th]:p-2"><th className="text-left">Fichier</th><th className="text-left">Type</th><th className="text-left">Date</th></tr>
                </thead>
                <tbody>
                  {data.documents.map((d)=> (
                    <tr key={d.id} className="odd:bg-white even:bg-gray-50 border-t [&>td]:p-2">
                      <td>{d.original_filename}</td>
                      <td>{d.type ?? '—'}</td>
                      <td>{new Date(d.uploaded_at).toLocaleString()}</td>
                    </tr>
                  ))}
                  {data.documents.length===0 && <tr><td className="p-2 text-gray-500" colSpan={3}>Aucun document</td></tr>}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
