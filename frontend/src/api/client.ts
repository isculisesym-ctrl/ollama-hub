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

export const modelsApi = {
  list: () => api.get<{ models: ModelInfo[]; count: number }>('/models'),
  getInfo: (name: string) => api.get<ModelInfo>(`/models/${name}`),
}

export const projectsApi = {
  list: () => api.get<{ projects: Project[]; count: number }>('/projects'),
  get: (id: number) => api.get<Project>(`/projects/${id}`),
  create: (data: { name: string; description?: string; model?: string; system_prompt?: string }) =>
    api.post<Project>('/projects', data),
  update: (id: number, data: Partial<Project>) => api.put<Project>(`/projects/${id}`, data),
  delete: (id: number) => api.delete(`/projects/${id}`),
}

export const chatApi = {
  send: (data: ChatRequest) => api.post<ChatResponse>('/chat', data),
  history: (projectId: number) =>
    api.get<{ project_id: number; messages: ChatMessage[]; count: number }>(
      `/chat/history/${projectId}`
    ),
}

export default api
