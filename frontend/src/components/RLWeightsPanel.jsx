// src/components/RLWeightsPanel.jsx — NEW (Section 9.5)
// Per-call bespoke W_t bar chart from Contextual Bandit

const SIGNAL_KEYS = ['visit', 'budget', 'keyword', 'question', 'loan', 'engagement']

export default function RLWeightsPanel({ rl_weights_used }) {
  // Graceful degradation — render nothing if absent
  if (!rl_weights_used || Object.keys(rl_weights_used).length === 0) {
    return (
      <div
        className="rounded-lg p-4"
        style={{ background: '#151820', border: '1px solid #2A2D3E' }}
      >
        <h3 className="text-sm font-medium mb-2" style={{ color: '#E8EAF6' }}>
          RL Weights Applied to This Call
        </h3>
        <p className="text-xs" style={{ color: '#8B90B0' }}>
          RL weights not available for this call.
        </p>
      </div>
    )
  }

  // Sort by weight descending — matching spec layout
  const entries = SIGNAL_KEYS
    .map(k => ({ signal: k, weight: rl_weights_used[k] || 0 }))
    .sort((a, b) => b.weight - a.weight)

  // Max weight for bar scaling (cap at 0.4 per spec)
  const MAX_W = 0.4

  return (
    <div
      className="rounded-lg p-4"
      style={{ background: '#151820', border: '1px solid #2A2D3E' }}
    >
      <h3 className="text-sm font-medium mb-1" style={{ color: '#E8EAF6' }}>
        RL Weights Applied to This Call
      </h3>
      <p className="text-xs mb-4" style={{ color: '#8B90B0' }}>
        Contextual Bandit W_t — bespoke to this caller's 15-dimensional state
      </p>

      <div className="flex flex-col gap-2">
        {entries.map(({ signal, weight }, i) => {
          const pct = Math.min((weight / MAX_W) * 100, 100)
          const isTop = i === 0
          return (
            <div key={signal} className="flex items-center gap-3">
              <span
                className="w-24 text-xs font-mono text-right capitalize"
                style={{ color: isTop ? '#E8EAF6' : '#8B90B0' }}
              >
                {signal}
              </span>
              <div
                className="flex-1 rounded-full overflow-hidden"
                style={{ background: '#0D0F14', height: 8 }}
              >
                <div
                  style={{
                    width: `${pct}%`,
                    height: '100%',
                    background: isTop ? '#69F0AE' : '#4FC3F7',
                    borderRadius: 9999,
                    transition: 'width 0.6s ease-out',
                  }}
                />
              </div>
              <span
                className="w-14 text-xs font-mono"
                style={{ color: isTop ? '#E8EAF6' : '#8B90B0' }}
              >
                {weight.toFixed(3)}
                {isTop && (
                  <span className="ml-1 text-[10px]" style={{ color: '#69F0AE' }}>
                    ↑
                  </span>
                )}
              </span>
            </div>
          )
        })}
      </div>

      {/* Fixed weights note */}
      <div
        className="mt-4 pt-3 flex gap-6"
        style={{ borderTop: '1px solid #2A2D3E' }}
      >
        <div className="flex items-center gap-2">
          <span className="text-xs font-mono" style={{ color: '#8B90B0' }}>tone</span>
          <span className="text-xs font-mono font-bold" style={{ color: '#8B90B0' }}>
            {(rl_weights_used.tone ?? 0.03).toFixed(3)}
          </span>
          <span className="text-[10px]" style={{ color: '#4A4F6A' }}>(fixed)</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs font-mono" style={{ color: '#8B90B0' }}>sentiment</span>
          <span className="text-xs font-mono font-bold" style={{ color: '#8B90B0' }}>
            {(rl_weights_used.sentiment ?? 0.02).toFixed(3)}
          </span>
          <span className="text-[10px]" style={{ color: '#4A4F6A' }}>(fixed)</span>
        </div>
      </div>
    </div>
  )
}
