interface Props {
  title: string
  status: string
  details?: Record<string, string | number>
  color: 'green' | 'red' | 'yellow' | 'blue'
}

const colorMap = {
  green: 'border-green-500 bg-green-500/10',
  red: 'border-red-500 bg-red-500/10',
  yellow: 'border-yellow-500 bg-yellow-500/10',
  blue: 'border-blue-500 bg-blue-500/10',
}

const dotMap = {
  green: 'bg-green-400',
  red: 'bg-red-400',
  yellow: 'bg-yellow-400',
  blue: 'bg-blue-400',
}

export default function StatusCard({ title, status, details, color }: Props) {
  return (
    <div className={`rounded-lg border p-4 ${colorMap[color]}`}>
      <div className="flex items-center gap-2 mb-2">
        <span className={`h-2.5 w-2.5 rounded-full ${dotMap[color]}`} />
        <h3 className="font-semibold text-sm uppercase tracking-wide text-gray-300">
          {title}
        </h3>
      </div>
      <p className="text-lg font-bold capitalize">{status}</p>
      {details && (
        <div className="mt-2 space-y-1">
          {Object.entries(details).map(([k, v]) => (
            <div key={k} className="flex justify-between text-xs text-gray-400">
              <span>{k}</span>
              <span className="text-gray-200">{v}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
