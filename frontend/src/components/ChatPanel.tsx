import { useState, useRef, useEffect } from 'react'
import { useChatStore } from '../stores/chatStore'
import { useModelStore } from '../stores/modelStore'
import { useProjectStore } from '../stores/projectStore'

export default function ChatPanel() {
  const { messages, sending, error, sendStream, stopStream } = useChatStore()
  const { selected: model } = useModelStore()
  const { current: project } = useProjectStore()
  const [input, setInput] = useState('')
  const [provider, setProvider] = useState<'ollama' | 'claude'>('ollama')
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, messages[messages.length - 1]?.content])

  const handleSend = (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || sending) return
    const msg = input.trim()
    setInput('')
    sendStream({
      message: msg,
      model: provider === 'ollama' ? model : undefined,
      provider,
      project_id: project?.id,
      system_prompt: project?.system_prompt || undefined,
    })
  }

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="flex items-center justify-center h-full text-gray-500">
            <div className="text-center">
              <p className="text-lg mb-1">Start a conversation</p>
              <p className="text-sm">
                {project ? `Project: ${project.name}` : 'Select a project or chat freely'}
              </p>
            </div>
          </div>
        )}
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[75%] rounded-lg px-4 py-2.5 text-sm leading-relaxed ${
                msg.role === 'user'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-800 text-gray-100 border border-gray-700'
              }`}
            >
              <p className="whitespace-pre-wrap">{msg.content}</p>
              {msg.role === 'assistant' && msg.model && (
                <p className="text-xs text-gray-500 mt-1.5">{msg.model}</p>
              )}
            </div>
          </div>
        ))}
        {sending && messages[messages.length - 1]?.content === '' && (
          <div className="flex justify-start">
            <div className="bg-gray-800 border border-gray-700 rounded-lg px-4 py-2.5 text-sm text-gray-400">
              <span className="animate-pulse">Thinking...</span>
            </div>
          </div>
        )}
        {error && (
          <div className="flex justify-center">
            <p className="text-red-400 text-sm bg-red-500/10 px-3 py-1.5 rounded">{error}</p>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <form onSubmit={handleSend} className="border-t border-gray-800 p-4">
        <div className="flex gap-2 mb-2">
          <button
            type="button"
            onClick={() => setProvider('ollama')}
            className={`px-3 py-1 rounded text-xs font-medium transition-colors ${
              provider === 'ollama'
                ? 'bg-green-600 text-white'
                : 'bg-gray-800 text-gray-400 hover:text-gray-200'
            }`}
          >
            Ollama
          </button>
          <button
            type="button"
            onClick={() => setProvider('claude')}
            className={`px-3 py-1 rounded text-xs font-medium transition-colors ${
              provider === 'claude'
                ? 'bg-purple-600 text-white'
                : 'bg-gray-800 text-gray-400 hover:text-gray-200'
            }`}
          >
            Claude
          </button>
        </div>
        <div className="flex gap-2">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={sending ? 'Streaming response...' : 'Type a message...'}
            disabled={sending}
            className="flex-1 rounded-lg bg-gray-800 border border-gray-700 px-4 py-2.5 text-sm text-gray-100 placeholder-gray-500 focus:border-blue-500 focus:outline-none disabled:opacity-50"
          />
          {sending ? (
            <button
              type="button"
              onClick={stopStream}
              className="rounded-lg bg-red-600 px-5 py-2.5 text-sm font-medium text-white hover:bg-red-500 transition-colors"
            >
              Stop
            </button>
          ) : (
            <button
              type="submit"
              disabled={!input.trim()}
              className="rounded-lg bg-blue-600 px-5 py-2.5 text-sm font-medium text-white hover:bg-blue-500 disabled:opacity-50 disabled:hover:bg-blue-600 transition-colors"
            >
              Send
            </button>
          )}
        </div>
      </form>
    </div>
  )
}
