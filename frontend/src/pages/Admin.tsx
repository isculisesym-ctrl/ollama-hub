import { useEffect, useState } from 'react'
import { adminApi, modelsApi, type AdminStats, type LogEntry, type LogStats, type ModelInfo } from '../api/client'

export default function Admin() {
  const [stats, setStats] = useState<AdminStats | null>(null)
  const [logStats, setLogStats] = useState<LogStats | null>(null)
  const [logs, setLogs] = useState<LogEntry[]>([])
  const [models, setModels] = useState<ModelInfo[]>([])
  const [pullName, setPullName] = useState('')
  const [pulling, setPulling] = useState(false)
  const [pullStatus, setPullStatus] = useState('')
  const [error, setError] = useState('')

  const refresh = async () => {
    try {
      const [s, ls, l, m] = await Promise.all([
        adminApi.stats(),
        adminApi.logStats(),
        adminApi.logs({ limit: 20 }),
        modelsApi.list(),
      ])
      setStats(s.data)
      setLogStats(ls.data)
      setLogs(l.data.logs)
      setModels(m.data.models)
    } catch {
      setError('Failed to load admin data. Is the backend running?')
    }
  }

  useEffect(() => { refresh() }, [])

  const handlePull = async () => {
    if (!pullName.trim() || pulling) return
    setPulling(true)
    setPullStatus('Starting pull...')
    setError('')
    const { promise } = modelsApi.pull(pullName.trim())
    try {
      const res = await promise
      if (!res.ok) {
        setPullStatus('')
        setError(`Pull failed: HTTP ${res.status}`)
        setPulling(false)
        return
      }
      const reader = res.body?.getReader()
      if (!reader) { setPulling(false); return }
      const decoder = new TextDecoder()
      let buffer = ''
      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() || ''
        for (const line of lines) {
          if (line.startsWith('data:')) {
            try {
              const data = JSON.parse(line.slice(5).trim())
              const status = data.status || ''
              const pct = data.total ? ` (${Math.round((data.completed / data.total) * 100)}%)` : ''
              setPullStatus(`${status}${pct}`)
            } catch { /* skip */ }
          }
        }
      }
      setPullStatus('Pull complete!')
      setPullName('')
      await refresh()
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Pull failed')
    }
    setPulling(false)
  }

  const handleDelete = async (name: string) => {
    if (!confirm(`Delete model "${name}"?`)) return
    try {
      await modelsApi.delete(name)
      await refresh()
    } catch {
      setError(`Failed to delete ${name}`)
    }
  }

  return (
    <div className="h-full overflow-y-auto p-6">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">Admin</h1>
        <button
          onClick={refresh}
          className="rounded bg-gray-800 px-3 py-1.5 text-sm text-gray-300 hover:bg-gray-700 transition-colors"
        >
          Refresh
        </button>
      </div>

      {error && (
        <div className="mb-4 rounded bg-red-500/10 border border-red-500/30 p-3 text-sm text-red-400">
          {error}
        </div>
      )}

      {/* Stats Cards */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <StatBox label="Projects" value={stats.projects.total} />
          <StatBox label="Total Chats" value={stats.chats.total} />
          <StatBox label="DB Size" value={`${stats.database.size_mb} MB`} />
          <StatBox
            label="Avg Response"
            value={logStats ? `${logStats.avg_duration_ms} ms` : '—'}
          />
        </div>
      )}

      {/* Model Manager */}
      <div className="rounded-lg border border-gray-800 bg-gray-900 p-5 mb-6">
        <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wide mb-3">
          Model Manager
        </h2>
        <div className="flex gap-2 mb-4">
          <input
            value={pullName}
            onChange={(e) => setPullName(e.target.value)}
            placeholder="Model name (e.g. llama3.2)"
            disabled={pulling}
            className="flex-1 rounded bg-gray-800 border border-gray-700 px-3 py-2 text-sm text-gray-100 focus:border-blue-500 focus:outline-none disabled:opacity-50"
            onKeyDown={(e) => e.key === 'Enter' && handlePull()}
          />
          <button
            onClick={handlePull}
            disabled={pulling || !pullName.trim()}
            className="rounded bg-green-600 px-4 py-2 text-sm font-medium text-white hover:bg-green-500 disabled:opacity-50 transition-colors"
          >
            {pulling ? 'Pulling...' : 'Pull'}
          </button>
        </div>
        {pullStatus && (
          <p className="text-sm text-blue-400 mb-3">{pullStatus}</p>
        )}
        {models.length === 0 ? (
          <p className="text-sm text-gray-500">No models installed</p>
        ) : (
          <div className="space-y-2">
            {models.map((m) => (
              <div
                key={m.name}
                className="flex items-center justify-between bg-gray-800 rounded px-3 py-2"
              >
                <div>
                  <span className="text-sm text-gray-200">{m.name}</span>
                  {m.size && (
                    <span className="text-xs text-gray-500 ml-2">{m.size}</span>
                  )}
                </div>
                <button
                  onClick={() => handleDelete(m.name)}
                  className="text-xs text-gray-500 hover:text-red-400 transition-colors"
                >
                  Delete
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        {/* Provider Stats */}
        {stats && (
          <div className="rounded-lg border border-gray-800 bg-gray-900 p-5">
            <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wide mb-3">
              Usage by Provider
            </h2>
            {Object.keys(stats.chats.by_provider).length === 0 ? (
              <p className="text-sm text-gray-500">No chats yet</p>
            ) : (
              <div className="space-y-2">
                {Object.entries(stats.chats.by_provider).map(([provider, count]) => (
                  <div key={provider} className="flex justify-between text-sm">
                    <span className="text-gray-300 capitalize">{provider}</span>
                    <span className="text-gray-400">{count} messages</span>
                  </div>
                ))}
              </div>
            )}
            {Object.keys(stats.chats.top_models).length > 0 && (
              <>
                <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wide mt-4 mb-2">
                  Top Models
                </h3>
                <div className="space-y-1">
                  {Object.entries(stats.chats.top_models).map(([model, count]) => (
                    <div key={model} className="flex justify-between text-xs">
                      <span className="text-gray-300">{model}</span>
                      <span className="text-gray-500">{count}</span>
                    </div>
                  ))}
                </div>
              </>
            )}
          </div>
        )}

        {/* Request Log Stats */}
        {logStats && (
          <div className="rounded-lg border border-gray-800 bg-gray-900 p-5">
            <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wide mb-3">
              API Request Stats
            </h2>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-400">Total Requests</span>
                <span className="text-gray-200">{logStats.total_requests}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Avg Duration</span>
                <span className="text-gray-200">{logStats.avg_duration_ms} ms</span>
              </div>
            </div>
            {Object.keys(logStats.status_codes).length > 0 && (
              <>
                <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wide mt-4 mb-2">
                  Status Codes
                </h3>
                <div className="space-y-1">
                  {Object.entries(logStats.status_codes).map(([code, count]) => (
                    <div key={code} className="flex justify-between text-xs">
                      <span className={`${code.startsWith('2') ? 'text-green-400' : code.startsWith('4') ? 'text-yellow-400' : 'text-red-400'}`}>
                        {code}
                      </span>
                      <span className="text-gray-500">{count}</span>
                    </div>
                  ))}
                </div>
              </>
            )}
          </div>
        )}
      </div>

      {/* Recent Logs */}
      <div className="rounded-lg border border-gray-800 bg-gray-900 p-5">
        <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wide mb-3">
          Recent API Logs
        </h2>
        {logs.length === 0 ? (
          <p className="text-sm text-gray-500">No logs yet</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-xs">
              <thead>
                <tr className="text-gray-500 border-b border-gray-800">
                  <th className="text-left py-2 pr-4">Time</th>
                  <th className="text-left py-2 pr-4">Method</th>
                  <th className="text-left py-2 pr-4">Path</th>
                  <th className="text-right py-2 pr-4">Status</th>
                  <th className="text-right py-2">Duration</th>
                </tr>
              </thead>
              <tbody>
                {logs.map((log, i) => (
                  <tr key={i} className="border-b border-gray-800/50">
                    <td className="py-1.5 pr-4 text-gray-500">
                      {new Date(log.timestamp).toLocaleTimeString()}
                    </td>
                    <td className="py-1.5 pr-4">
                      <span className={`font-medium ${
                        log.method === 'GET' ? 'text-blue-400' :
                        log.method === 'POST' ? 'text-green-400' :
                        log.method === 'DELETE' ? 'text-red-400' :
                        'text-yellow-400'
                      }`}>
                        {log.method}
                      </span>
                    </td>
                    <td className="py-1.5 pr-4 text-gray-300">{log.path}</td>
                    <td className={`py-1.5 pr-4 text-right ${
                      log.status_code < 300 ? 'text-green-400' :
                      log.status_code < 400 ? 'text-yellow-400' : 'text-red-400'
                    }`}>
                      {log.status_code}
                    </td>
                    <td className="py-1.5 text-right text-gray-400">
                      {log.duration_ms} ms
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}

function StatBox({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="rounded-lg border border-gray-800 bg-gray-900 p-4">
      <p className="text-xs text-gray-500 uppercase tracking-wide">{label}</p>
      <p className="text-2xl font-bold mt-1">{value}</p>
    </div>
  )
}
