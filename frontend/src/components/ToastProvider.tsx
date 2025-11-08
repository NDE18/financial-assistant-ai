import React, { createContext, useCallback, useContext, useMemo, useState } from 'react'

export type ToastType = 'success' | 'info' | 'error'

type Toast = { id: number; message: string; type: ToastType; until: number }

type ToastCtx = {
  push: (message: string, type?: ToastType, durationMs?: number) => void
}

const Ctx = createContext<ToastCtx | null>(null)

export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [toasts, setToasts] = useState<Toast[]>([])
  const push = useCallback((message: string, type: ToastType = 'success', durationMs: number = 3500) => {
    const id = Date.now() + Math.random()
    const until = Date.now() + durationMs
    setToasts((prev) => [...prev, { id, message, type, until }])
    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id))
    }, durationMs)
  }, [])

  const value = useMemo(() => ({ push }), [push])

  return (
    <Ctx.Provider value={value}>
      {children}
      <div className="fixed left-4 bottom-4 space-y-2 z-[1000] pointer-events-none">
        {toasts.map((t) => (
          <div
            key={t.id}
            className={
              'pointer-events-auto rounded-md px-4 py-2 shadow border text-sm flex items-center gap-2 ' +
              (t.type === 'success'
                ? 'bg-green-50 border-green-200 text-green-800'
                : t.type === 'info'
                ? 'bg-blue-50 border-blue-200 text-blue-800'
                : 'bg-red-50 border-red-200 text-red-800')
            }
            onClick={() => setToasts((prev) => prev.filter((x) => x.id !== t.id))}
          >
            <span>
              {t.type === 'success' ? '✓' : t.type === 'info' ? 'ℹ' : '⚠'}
            </span>
            <span>{t.message}</span>
          </div>
        ))}
      </div>
    </Ctx.Provider>
  )
}

export function useToast() {
  const ctx = useContext(Ctx)
  if (!ctx) throw new Error('useToast must be used within ToastProvider')
  return ctx
}
