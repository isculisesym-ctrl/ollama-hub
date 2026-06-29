import { create } from 'zustand'
import { chatApi, type ChatMessage, type ChatRequest, type ChatResponse } from '../api/client'

interface ChatState {
  messages: ChatMessage[]
  sending: boolean
  error: string | null
  loadHistory: (projectId: number) => Promise<void>
  send: (req: ChatRequest) => Promise<ChatResponse>
  clear: () => void
}

export const useChatStore = create<ChatState>((set, get) => ({
  messages: [],
  sending: false,
  error: null,
  loadHistory: async (projectId) => {
    try {
      const res = await chatApi.history(projectId)
      set({ messages: res.data.messages })
    } catch {
      set({ messages: [] })
    }
  },
  send: async (req) => {
    const userMsg: ChatMessage = {
      id: Date.now(),
      project_id: req.project_id ?? null,
      role: 'user',
      content: req.message,
      model: req.model || '',
      provider: req.provider,
      created_at: new Date().toISOString(),
    }
    set((s) => ({ messages: [...s.messages, userMsg], sending: true, error: null }))

    try {
      const res = await chatApi.send(req)
      const assistantMsg: ChatMessage = {
        id: Date.now() + 1,
        project_id: req.project_id ?? null,
        role: 'assistant',
        content: res.data.response,
        model: res.data.model,
        provider: res.data.provider,
        created_at: new Date().toISOString(),
      }
      set((s) => ({ messages: [...s.messages, assistantMsg], sending: false }))
      return res.data
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : 'Chat request failed'
      set({ sending: false, error: msg })
      throw e
    }
  },
  clear: () => set({ messages: [], error: null }),
}))
