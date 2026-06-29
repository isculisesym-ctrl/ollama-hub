import { useState } from 'react'
import { useProjectStore } from '../stores/projectStore'
import { useChatStore } from '../stores/chatStore'
import type { Project } from '../api/client'

export default function ProjectList() {
  const { projects, current, setCurrent, create, remove, loading } = useProjectStore()
  const { loadHistory, clear } = useChatStore()
  const [showForm, setShowForm] = useState(false)
  const [name, setName] = useState('')

  const handleSelect = async (p: Project) => {
    setCurrent(p)
    await loadHistory(p.id)
  }

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!name.trim()) return
    const p = await create({ name: name.trim() })
    setCurrent(p)
    clear()
    setName('')
    setShowForm(false)
  }

  const handleDelete = async (id: number, e: React.MouseEvent) => {
    e.stopPropagation()
    if (current?.id === id) clear()
    await remove(id)
  }

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center justify-between px-4 py-3 border-b border-gray-800">
        <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wide">Projects</h2>
        <button
          onClick={() => setShowForm(!showForm)}
          className="text-blue-400 hover:text-blue-300 text-lg leading-none"
          title="New project"
        >
          +
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleCreate} className="px-4 py-2 border-b border-gray-800">
          <input
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Project name"
            autoFocus
            className="w-full rounded bg-gray-800 border border-gray-700 px-2 py-1.5 text-sm text-gray-100 focus:border-blue-500 focus:outline-none"
          />
        </form>
      )}

      <div className="flex-1 overflow-y-auto">
        {loading && <p className="px-4 py-3 text-sm text-gray-500">Loading...</p>}
        {!loading && projects.length === 0 && (
          <p className="px-4 py-3 text-sm text-gray-500">No projects yet</p>
        )}
        {projects.map((p) => (
          <button
            key={p.id}
            onClick={() => handleSelect(p)}
            className={`w-full text-left px-4 py-3 border-b border-gray-800/50 hover:bg-gray-800/50 transition-colors ${
              current?.id === p.id ? 'bg-gray-800 border-l-2 border-l-blue-500' : ''
            }`}
          >
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium truncate">{p.name}</span>
              <button
                onClick={(e) => handleDelete(p.id, e)}
                className="text-gray-600 hover:text-red-400 text-xs ml-2"
                title="Delete"
              >
                ×
              </button>
            </div>
            {p.description && (
              <p className="text-xs text-gray-500 mt-0.5 truncate">{p.description}</p>
            )}
          </button>
        ))}
      </div>
    </div>
  )
}
