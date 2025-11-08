export function SectionTitle({ children }: { children: React.ReactNode }) {
  return (
    <div className="mb-4">
      <h2 className="text-xl font-semibold text-gray-900">{children}</h2>
      <div className="h-1 w-12 bg-primary-200 rounded mt-1" />
    </div>
  )
}
