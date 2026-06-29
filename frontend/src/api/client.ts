import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

export interface StatusResponse {
  ollama: { status: string; url?: string; version?: string; detail?: string }
  claude: { status: string; model?: string; detail?: string }
  system: {
    status: string
    cpu_percent: number
    memory_total_gb: number
    memory_used_percent: number
  }
}

export interface ModelInfo {
  name: string
  size?: string
  modified_at?: string
  digest?: string
  details?: Record<string, unknown>
}

export interface Project {
  id: number
  name: string
  description: string
  model: string
  system_prompt: string
  created_at: string
  updated_at: string
}

export interface ChatMessage {
  id: number
  project_id: number | null
  role: 'user' | 'assistant' | 'system'
  content: string
  model: string
  provider: string
  created_at: string
}

export interface ChatRequest {
  message: string
  model?: string
  provider: 'ollama' | 'claude'
  project_id?: number
  system_prompt?: string
}

export interface ChatResponse {
  response: string
  model: string
  provider: string
  usage?: Record<string, unknown>
}

export const statusApi = {
  getStatus: () => api.get<StatusResponse>('/status'),
  testOllama: () => api.post('/ollama/test'),
  testClaude: () => api.post('/claude/test'),
}

export interface AdminStats {
  database: { path: string; size_bytes: number; size_mb: number }
  projects: { total: number }
  chats: {
    total: number
    by_provider: Record<string, number>
    top_models: Record<string, number>
  }
  daily_activity: Record<string, number>
}

export interface LogEntry {
  timestamp: string
  method: string
  path: string
  status_code: number
  duration_ms: number
  client_ip: string
}

export interface LogStats {
  total_requests: number
  methods: Record<string, number>
  status_codes: Record<string, number>
  avg_duration_ms: number
}

export const modelsApi = {
  list: () => api.get<{ models: ModelInfo[]; count: number }>('/models'),
  getInfo: (name: string) => api.get<ModelInfo>(`/models/${name}`),
  pull: (name: string) => {
    const controller = new AbortController()
    const promise = fetch('/api/models/pull', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name }),
      signal: controller.signal,
    })
    return { promise, controller }
  },
  delete: (name: string) => api.delete(`/models/${name}`),
}

export const adminApi = {
  stats: () => api.get<AdminStats>('/admin/stats'),
  logs: (params?: { limit?: number; method?: string; path_prefix?: string }) =>
    api.get<{ logs: LogEntry[] }>('/admin/logs', { params }),
  logStats: () => api.get<LogStats>('/admin/logs/stats'),
  authStatus: () => api.get<{ auth_enabled: boolean; api_key_set: boolean }>('/admin/auth/status'),
}

export const projectsApi = {
  list: () => api.get<{ projects: Project[]; count: number }>('/projects'),
  get: (id: number) => api.get<Project>(`/projects/${id}`),
  create: (data: { name: string; description?: string; model?: string; system_prompt?: string }) =>
    api.post<Project>('/projects', data),
  update: (id: number, data: Partial<Project>) => api.put<Project>(`/projects/${id}`, data),
  delete: (id: number) => api.delete(`/projects/${id}`),
}

export interface StreamChunk {
  token?: string
  done?: boolean
  model?: string
  provider?: string
  usage?: Record<string, unknown>
  error?: string
}

export const chatApi = {
  send: (data: ChatRequest) => api.post<ChatResponse>('/chat', data),
  history: (projectId: number) =>
    api.get<{ project_id: number; messages: ChatMessage[]; count: number }>(
      `/chat/history/${projectId}`
    ),
  stream: (data: ChatRequest, onChunk: (chunk: StreamChunk) => void, onDone: () => void, onError: (err: string) => void) => {
    const controller = new AbortController()
    fetch('/api/chat/stream', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
      signal: controller.signal,
    })
      .then(async (res) => {
        if (!res.ok) {
          const err = await res.json().catch(() => ({ detail: 'Stream failed' }))
          onError(err.detail || `HTTP ${res.status}`)
          return
        }
        const reader = res.body?.getReader()
        if (!reader) { onError('No response body'); return }
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
              const raw = line.slice(5).trim()
              if (!raw) continue
              try {
                const chunk: StreamChunk = JSON.parse(raw)
                if (chunk.error) { onError(chunk.error); return }
                onChunk(chunk)
              } catch { /* skip malformed */ }
            }
          }
        }
        onDone()
      })
      .catch((err) => {
        if (err.name !== 'AbortError') onError(err.message || 'Stream failed')
      })

    return controller
  },
}

export default api
