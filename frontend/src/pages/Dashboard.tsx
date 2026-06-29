import { useEffect } from 'react'
import { useStatusStore } from '../stores/statusStore'
import { useModelStore } from '../stores/modelStore'
import { useProjectStore } from '../stores/projectStore'
import StatusCard from '../components/StatusCard'
import ModelSelector from '../components/ModelSelector'

function statusColor(status: string): 'green' | 'red' | 'yellow' {
  if (status === 'running' || status === 'connected' || status === 'ok') return 'green'
  if (status === 'not_configured') return 'yellow'
  return 'red'
}

export default function Dashboard() {
  const { data, loading, fetch: fetchStatus } = useStatusStore()
  const { models, fetch: fetchModels } = useModelStore()
  const { projects, fetch: fetchProjects } = useProjectStore()

  useEffect(() => {
    fetchStatus()
    fetchModels()
    fetchProjects()
  }, [fetchStatus, fetchModels, fetchProjects])

  return (
    <div className="h-full overflow-y-auto p-6">
      <h1 className="text-2xl font-bold mb-6">Dashboard</h1>

      {loading && <p className="text-gray-500 mb-4">Loading status...</p>}

      {data && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <StatusCard
            title="Ollama"
            status={data.ollama.status}
            color={statusColor(data.ollama.status)}
            details={{
              URL: data.ollama.url || '—',
              ...(data.ollama.version ? { Version: data.ollama.version } : {}),
            }}
          />
          <StatusCard
            title="Claude"
            status={data.claude.status}
            color={statusColor(data.claude.status)}
            details={{
              ...(data.claude.model ? { Model: data.claude.model } : {}),
              ...(data.claude.detail ? { Detail: data.claude.detail } : {}),
            }}
          />
          <StatusCard
            title="System"
            status={data.system.status}
            color={statusColor(data.system.status)}
            details={{
              CPU: `${data.system.cpu_percent}%`,
              RAM: `${data.system.memory_used_percent}% of ${data.system.memory_total_gb} GB`,
            }}
          />
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="rounded-lg border border-gray-800 bg-gray-900 p-5">
          <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wide mb-3">
            Models ({models.length})
          </h2>
          <ModelSelector />
          {models.length > 0 && (
            <ul className="mt-3 space-y-1.5">
              {models.map((m) => (
                <li key={m.name} className="flex justify-between text-sm text-gray-400">
                  <span className="text-gray-200">{m.name}</span>
                  {m.size && <span>{m.size}</span>}
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className="rounded-lg border border-gray-800 bg-gray-900 p-5">
          <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wide mb-3">
            Projects ({projects.length})
          </h2>
          {projects.length === 0 ? (
            <p className="text-sm text-gray-500">No projects yet. Create one from the Chat page.</p>
          ) : (
            <ul className="space-y-2">
              {projects.slice(0, 5).map((p) => (
                <li key={p.id} className="flex justify-between text-sm">
                  <span className="text-gray-200 truncate">{p.name}</span>
                  <span className="text-gray-500 text-xs">
                    {new Date(p.updated_at).toLocaleDateString()}
                  </span>
                </li>
              ))}
              {projects.length > 5 && (
                <li className="text-xs text-gray-500">+{projects.length - 5} more</li>
              )}
            </ul>
          )}
        </div>
      </div>
    </div>
  )
}
