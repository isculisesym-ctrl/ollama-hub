import { create } from 'zustand'
import { projectsApi, type Project } from '../api/client'

interface ProjectState {
  projects: Project[]
  current: Project | null
  loading: boolean
  error: string | null
  fetch: () => Promise<void>
  setCurrent: (p: Project | null) => void
  create: (data: { name: string; description?: string; model?: string; system_prompt?: string }) => Promise<Project>
  remove: (id: number) => Promise<void>
}

export const useProjectStore = create<ProjectState>((set, get) => ({
  projects: [],
  current: null,
  loading: false,
  error: null,
  fetch: async () => {
    set({ loading: true, error: null })
    try {
      const res = await projectsApi.list()
      set({ projects: res.data.projects, loading: false })
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : 'Failed to fetch projects'
      set({ error: msg, loading: false })
    }
  },
  setCurrent: (p) => set({ current: p }),
  create: async (data) => {
    const res = await projectsApi.create(data)
    await get().fetch()
    return res.data
  },
  remove: async (id) => {
    await projectsApi.delete(id)
    if (get().current?.id === id) set({ current: null })
    await get().fetch()
  },
}))
