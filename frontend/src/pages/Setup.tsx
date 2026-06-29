import { useState } from 'react'
import { statusApi } from '../api/client'

type Step = 'ollama' | 'claude' | 'done'

interface TestResult {
  ok: boolean
  message: string
}

export default function Setup() {
  const [step, setStep] = useState<Step>('ollama')
  const [ollamaResult, setOllamaResult] = useState<TestResult | null>(null)
  const [claudeResult, setClaudeResult] = useState<TestResult | null>(null)
  const [testing, setTesting] = useState(false)

  const testOllama = async () => {
    setTesting(true)
    setOllamaResult(null)
    try {
      await statusApi.testOllama()
      setOllamaResult({ ok: true, message: 'Ollama is running and reachable.' })
    } catch (e: unknown) {
      const msg =
        e && typeof e === 'object' && 'response' in e
          ? String((e as { response: { data: { detail: string } } }).response.data?.detail)
          : 'Cannot connect to Ollama. Make sure it is running on localhost:11434.'
      setOllamaResult({ ok: false, message: msg })
    }
    setTesting(false)
  }

  const testClaude = async () => {
    setTesting(true)
    setClaudeResult(null)
    try {
      await statusApi.testClaude()
      setClaudeResult({ ok: true, message: 'Claude API connected successfully.' })
    } catch (e: unknown) {
      const msg =
        e && typeof e === 'object' && 'response' in e
          ? String((e as { response: { data: { detail: string } } }).response.data?.detail)
          : 'Claude API connection failed. Check your CLAUDE_API_KEY in .env.'
      setClaudeResult({ ok: false, message: msg })
    }
    setTesting(false)
  }

  return (
    <div className="h-full overflow-y-auto flex items-center justify-center p-6">
      <div className="w-full max-w-lg">
        <h1 className="text-2xl font-bold mb-2">Setup Wizard</h1>
        <p className="text-gray-400 text-sm mb-8">
          Test your connections to Ollama and Claude before getting started.
        </p>

        <div className="flex gap-2 mb-8">
          {(['ollama', 'claude', 'done'] as Step[]).map((s, i) => (
            <div key={s} className="flex items-center gap-2">
              <button
                onClick={() => setStep(s)}
                className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium transition-colors ${
                  step === s
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-800 text-gray-500'
                }`}
              >
                {i + 1}
              </button>
              {i < 2 && <div className="w-12 h-px bg-gray-800" />}
            </div>
          ))}
        </div>

        {step === 'ollama' && (
          <div className="rounded-lg border border-gray-800 bg-gray-900 p-6">
            <h2 className="text-lg font-semibold mb-2">Ollama Connection</h2>
            <p className="text-sm text-gray-400 mb-4">
              OllamaHub connects to your local Ollama instance at{' '}
              <code className="text-gray-300 bg-gray-800 px-1 rounded">localhost:11434</code>.
            </p>
            <ol className="text-sm text-gray-400 space-y-1 mb-5 list-decimal list-inside">
              <li>Install Ollama from ollama.com</li>
              <li>Run <code className="text-gray-300 bg-gray-800 px-1 rounded">ollama serve</code></li>
              <li>Pull a model: <code className="text-gray-300 bg-gray-800 px-1 rounded">ollama pull llama3.2</code></li>
            </ol>
            <button
              onClick={testOllama}
              disabled={testing}
              className="w-full rounded-lg bg-green-600 px-4 py-2.5 text-sm font-medium text-white hover:bg-green-500 disabled:opacity-50 transition-colors"
            >
              {testing ? 'Testing...' : 'Test Connection'}
            </button>
            {ollamaResult && (
              <div
                className={`mt-3 rounded p-3 text-sm ${
                  ollamaResult.ok
                    ? 'bg-green-500/10 text-green-400 border border-green-500/30'
                    : 'bg-red-500/10 text-red-400 border border-red-500/30'
                }`}
              >
                {ollamaResult.message}
              </div>
            )}
            <button
              onClick={() => setStep('claude')}
              className="mt-4 text-sm text-blue-400 hover:text-blue-300"
            >
              Next: Claude Setup →
            </button>
          </div>
        )}

        {step === 'claude' && (
          <div className="rounded-lg border border-gray-800 bg-gray-900 p-6">
            <h2 className="text-lg font-semibold mb-2">Claude API (Optional)</h2>
            <p className="text-sm text-gray-400 mb-4">
              To use Claude as an AI provider, add your API key to the{' '}
              <code className="text-gray-300 bg-gray-800 px-1 rounded">.env</code> file.
            </p>
            <div className="bg-gray-800 rounded p-3 text-sm text-gray-300 font-mono mb-5">
              CLAUDE_API_KEY=sk-ant-api03-...
            </div>
            <button
              onClick={testClaude}
              disabled={testing}
              className="w-full rounded-lg bg-purple-600 px-4 py-2.5 text-sm font-medium text-white hover:bg-purple-500 disabled:opacity-50 transition-colors"
            >
              {testing ? 'Testing...' : 'Test Claude Connection'}
            </button>
            {claudeResult && (
              <div
                className={`mt-3 rounded p-3 text-sm ${
                  claudeResult.ok
                    ? 'bg-green-500/10 text-green-400 border border-green-500/30'
                    : 'bg-yellow-500/10 text-yellow-400 border border-yellow-500/30'
                }`}
              >
                {claudeResult.message}
              </div>
            )}
            <div className="flex justify-between mt-4">
              <button
                onClick={() => setStep('ollama')}
                className="text-sm text-gray-400 hover:text-gray-300"
              >
                ← Back
              </button>
              <button
                onClick={() => setStep('done')}
                className="text-sm text-blue-400 hover:text-blue-300"
              >
                Finish →
              </button>
            </div>
          </div>
        )}

        {step === 'done' && (
          <div className="rounded-lg border border-gray-800 bg-gray-900 p-6 text-center">
            <div className="text-4xl mb-3">✓</div>
            <h2 className="text-lg font-semibold mb-2">Setup Complete</h2>
            <p className="text-sm text-gray-400 mb-5">
              You're ready to start using OllamaHub. Head to the Dashboard or Chat page.
            </p>
            <div className="flex gap-3 justify-center">
              <a
                href="/"
                className="rounded-lg bg-blue-600 px-5 py-2.5 text-sm font-medium text-white hover:bg-blue-500 transition-colors"
              >
                Go to Dashboard
              </a>
              <a
                href="/chat"
                className="rounded-lg bg-gray-800 px-5 py-2.5 text-sm font-medium text-gray-300 hover:bg-gray-700 transition-colors"
              >
                Start Chatting
              </a>
            </div>
            <button
              onClick={() => setStep('ollama')}
              className="mt-4 text-sm text-gray-500 hover:text-gray-400"
            >
              ← Run setup again
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
