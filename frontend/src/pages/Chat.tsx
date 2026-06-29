import { useEffect } from 'react'
import { useProjectStore } from '../stores/projectStore'
import { useModelStore } from '../stores/modelStore'
import ProjectList from '../components/ProjectList'
import ChatPanel from '../components/ChatPanel'
import ModelSelector from '../components/ModelSelector'

export default function Chat() {
  const { fetch: fetchProjects } = useProjectStore()
  const { fetch: fetchModels } = useModelStore()

  useEffect(() => {
    fetchProjects()
    fetchModels()
  }, [fetchProjects, fetchModels])

  return (
    <div className="flex h-full">
      <aside className="w-60 border-r border-gray-800 bg-gray-900 flex flex-col">
        <ProjectList />
        <div className="border-t border-gray-800 p-3">
          <label className="text-xs text-gray-500 uppercase tracking-wide block mb-1.5">
            Model
          </label>
          <ModelSelector />
        </div>
      </aside>
      <div className="flex-1">
        <ChatPanel />
      </div>
    </div>
  )
}
