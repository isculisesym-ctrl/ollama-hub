import { create } from 'zustand'
import { modelsApi, type ModelInfo } from '../api/client'

interface ModelState {
  models: ModelInfo[]
  selected: string
  loading: boolean
  error: string | null
  fetch: () => Promise<void>
  select: (name: string) => void
}

export const useModelStore = create<ModelState>((set) => ({
  models: [],
  selected: '',
  loading: false,
  error: null,
  fetch: async () => {
    set({ loading: true, error: null })
    try {
      const res = await modelsApi.list()
      const models = res.data.models
      set((state) => ({
        models,
        loading: false,
        selected: state.selected || (models.length > 0 ? models[0].name : ''),
      }))
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : 'Failed to fetch models'
      set({ error: msg, loading: false })
    }
  },
  select: (name) => set({ selected: name }),
}))
