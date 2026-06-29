import { useModelStore } from '../stores/modelStore'

export default function ModelSelector() {
  const { models, selected, select, loading } = useModelStore()

  if (loading) {
    return (
      <select disabled className="w-full rounded bg-gray-800 border border-gray-700 px-3 py-2 text-sm text-gray-400">
        <option>Loading models...</option>
      </select>
    )
  }

  if (models.length === 0) {
    return (
      <select disabled className="w-full rounded bg-gray-800 border border-gray-700 px-3 py-2 text-sm text-gray-400">
        <option>No models available</option>
      </select>
    )
  }

  return (
    <select
      value={selected}
      onChange={(e) => select(e.target.value)}
      className="w-full rounded bg-gray-800 border border-gray-700 px-3 py-2 text-sm text-gray-100 focus:border-blue-500 focus:outline-none"
    >
      {models.map((m) => (
        <option key={m.name} value={m.name}>
          {m.name} {m.size ? `(${m.size})` : ''}
        </option>
      ))}
    </select>
  )
}
