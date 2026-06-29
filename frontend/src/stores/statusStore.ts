import { create } from 'zustand'
import { statusApi, type StatusResponse } from '../api/client'

interface StatusState {
  data: StatusResponse | null
  loading: boolean
  error: string | null
  fetch: () => Promise<void>
}

export const useStatusStore = create<StatusState>((set) => ({
  data: null,
  loading: false,
  error: null,
  fetch: async () => {
    set({ loading: true, error: null })
    try {
      const res = await statusApi.getStatus()
      set({ data: res.data, loading: false })
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : 'Failed to fetch status'
      set({ error: msg, loading: false })
    }
  },
}))
