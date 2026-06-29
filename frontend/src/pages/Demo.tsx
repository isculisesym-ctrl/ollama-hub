import { useState } from 'react'

interface ReviewChunk {
  event: string
  specialist?: string
  token?: string
  error?: string
  specialists?: Record<string, string> | number
}

const EXAMPLE_CODE = `function processData(arr) {
  for (let i = 0; i < arr.length; i++) {
    arr[i] = arr[i] * 2;
  }
  return arr;
}

const secret = "hardcoded-api-key-12345";
const result = processData([1, 2, 3]);`

export default function Demo() {
  const [code, setCode] = useState(EXAMPLE_CODE)
  const [description, setDescription] = useState('Data processor with hardcoded secrets')
  const [reviewing, setReviewing] = useState(false)
  const [reviews, setReviews] = useState<Record<string, string>>({})
  const [error, setError] = useState('')
  const [progress, setProgress] = useState('')

  const startReview = async () => {
    if (!code.trim()) return
    setReviewing(true)
    setError('')
    setReviews({})
    setProgress('')

    try {
      const res = await fetch('/api/review/code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code, description }),
      })

      if (!res.ok) {
        setError(`Review failed: HTTP ${res.status}`)
        setReviewing(false)
        return
      }

      const reader = res.body?.getReader()
      if (!reader) { setReviewing(false); return }

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
            try {
              const chunk: ReviewChunk = JSON.parse(line.slice(5).trim())

              if (chunk.event === 'started') {
                setProgress(`Starting ${chunk.specialists} parallel reviews...`)
              } else if (chunk.event === 'chunk') {
                setReviews((prev) => ({
                  ...prev,
                  [chunk.specialist || 'Unknown']:
                    (prev[chunk.specialist || 'Unknown'] || '') + (chunk.token || ''),
                }))
              } else if (chunk.event === 'reviews_done') {
                setReviews(chunk.specialists as Record<string, string>)
                setProgress('All reviews complete!')
              }
            } catch {
              /* skip malformed */
            }
          }
        }
      }
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Review failed')
    }
    setReviewing(false)
  }

  return (
    <div className="h-full overflow-y-auto p-6">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-2xl font-bold mb-2">Code Review Swarm</h1>
        <p className="text-gray-400 text-sm mb-6">
          Haiku orchestrates multiple Ollama specialists to review code in parallel.
          <br />
          <span className="text-blue-400">Security</span> + <span className="text-green-400">Performance</span> + <span className="text-yellow-400">Readability</span>
        </p>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Progress */}
          {progress && (
            <div className="lg:col-span-2 rounded-lg bg-blue-500/10 border border-blue-500/30 p-3">
              <p className="text-sm text-blue-400">{progress}</p>
            </div>
          )}

          {/* Input */}
          <div className="space-y-4">
            <div>
              <label className="text-xs text-gray-400 uppercase tracking-wide">Code</label>
              <textarea
                value={code}
                onChange={(e) => setCode(e.target.value)}
                disabled={reviewing}
                className="w-full h-64 rounded bg-gray-800 border border-gray-700 p-3 text-sm font-mono text-gray-100 focus:border-blue-500 focus:outline-none disabled:opacity-50"
                placeholder="Paste code here..."
              />
            </div>

            <div>
              <label className="text-xs text-gray-400 uppercase tracking-wide">Description</label>
              <input
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                disabled={reviewing}
                className="w-full rounded bg-gray-800 border border-gray-700 px-3 py-2 text-sm text-gray-100 focus:border-blue-500 focus:outline-none disabled:opacity-50"
                placeholder="What should reviewers focus on?"
              />
            </div>

            <button
              onClick={startReview}
              disabled={reviewing || !code.trim()}
              className="w-full rounded-lg bg-blue-600 px-4 py-2.5 text-sm font-medium text-white hover:bg-blue-500 disabled:opacity-50 transition-colors"
            >
              {reviewing ? '🔄 Reviewing...' : '▶️ Start Review'}
            </button>

            {error && (
              <div className="rounded bg-red-500/10 border border-red-500/30 p-3 text-sm text-red-400">
                {error}
              </div>
            )}
          </div>

          {/* Reviews */}
          <div className="space-y-4">

            {Object.entries(reviews).map(([specialist, review]) => (
              <div
                key={specialist}
                className={`rounded-lg border p-4 ${
                  specialist === 'Security'
                    ? 'bg-blue-500/10 border-blue-500/30'
                    : specialist === 'Performance'
                      ? 'bg-green-500/10 border-green-500/30'
                      : 'bg-yellow-500/10 border-yellow-500/30'
                }`}
              >
                <p className={`text-xs uppercase tracking-wide font-semibold mb-2 ${
                  specialist === 'Security'
                    ? 'text-blue-400'
                    : specialist === 'Performance'
                      ? 'text-green-400'
                      : 'text-yellow-400'
                }`}>
                  {specialist} Review (Ollama)
                </p>
                <p className="text-sm text-gray-200 whitespace-pre-wrap max-h-48 overflow-y-auto">
                  {review}
                </p>
              </div>
            ))}

            {reviewing && Object.keys(reviews).length === 0 && (
              <div className="rounded-lg bg-gray-800 border border-gray-700 p-4 text-center text-gray-400">
                <p className="text-sm">⏳ Waiting for specialist reviews...</p>
                <p className="text-xs mt-1 text-gray-500">Haiku orchestrates parallel reviews</p>
              </div>
            )}
          </div>
        </div>

        {/* Architecture info */}
        <div className="mt-8 rounded-lg border border-gray-800 bg-gray-900 p-4">
          <h3 className="text-sm font-semibold text-gray-300 mb-2">How it works:</h3>
          <div className="text-xs text-gray-400 space-y-1">
            <p>1. <span className="text-blue-400">Haiku</span> (Claude) reads your code + description</p>
            <p>2. Dispatches to 3 <span className="text-green-400">Ollama</span> specialists in parallel</p>
            <p>3. Each reviews with their specialty (Security, Performance, Readability)</p>
            <p>4. <span className="text-blue-400">Haiku</span> synthesizes results into executive summary</p>
            <p className="mt-2 text-gray-500">
              💰 Cost: Haiku is 50x cheaper than Opus. Ollamas are FREE. Perfect for batch code reviews!
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
