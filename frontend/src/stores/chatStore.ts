import { create } from 'zustand'
import { chatApi, type ChatMessage, type ChatRequest, type StreamChunk } from '../api/client'

interface ChatState {
  messages: ChatMessage[]
  sending: boolean
  error: string | null
  streamController: AbortController | null
  loadHistory: (projectId: number) => Promise<void>
  sendStream: (req: ChatRequest) => void
  stopStream: () => void
  clear: () => void
}

export const useChatStore = create<ChatState>((set, get) => ({
  messages: [],
  sending: false,
  error: null,
  streamController: null,
  loadHistory: async (projectId) => {
    try {
      const res = await chatApi.history(projectId)
      set({ messages: res.data.messages })
    } catch {
      set({ messages: [] })
    }
  },
  sendStream: (req) => {
    const userMsg: ChatMessage = {
      id: Date.now(),
      project_id: req.project_id ?? null,
      role: 'user',
      content: req.message,
      model: req.model || '',
      provider: req.provider,
      created_at: new Date().toISOString(),
    }
    const assistantMsg: ChatMessage = {
      id: Date.now() + 1,
      project_id: req.project_id ?? null,
      role: 'assistant',
      content: '',
      model: '',
      provider: req.provider,
      created_at: new Date().toISOString(),
    }
    set((s) => ({
      messages: [...s.messages, userMsg, assistantMsg],
      sending: true,
      error: null,
    }))

    const assistantId = assistantMsg.id

    const controller = chatApi.stream(
      req,
      (chunk: StreamChunk) => {
        if (chunk.token) {
          set((s) => ({
            messages: s.messages.map((m) =>
              m.id === assistantId
                ? { ...m, content: m.content + chunk.token, model: chunk.model || m.model }
                : m
            ),
          }))
        }
      },
      () => {
        set({ sending: false, streamController: null })
      },
      (err: string) => {
        set({ sending: false, error: err, streamController: null })
      }
    )
    set({ streamController: controller })
  },
  stopStream: () => {
    const ctrl = get().streamController
    if (ctrl) ctrl.abort()
    set({ sending: false, streamController: null })
  },
  clear: () => set({ messages: [], error: null }),
}))
