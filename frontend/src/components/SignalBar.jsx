// src/components/SignalBar.jsx
const SIGNAL_COLORS = {
  budget:     '#4FC3F7', // neon-blue
  visit:      '#4FC3F7', // neon-blue
  loan:       '#CE93D8', // neon-purple
  keyword:    '#69F0AE', // neon-green
  question:   '#FFD740', // neon-amber
  engagement: '#FFD740', // neon-amber
}

export function SignalBar({ label, value, color }) {
  const barColor = color || SIGNAL_COLORS[label?.toLowerCase()] || '#4FC3F7'
  const pct = Math.max(0, Math.min(100, (value ?? 0) * 100))

  return (
    <div className="flex flex-col gap-1">
      <div className="flex justify-between items-center">
        <span
          className="font-mono text-[10px] uppercase tracking-wider"
          style={{ color: '#8B90B0' }}
        >
          {label}
        </span>
        <span className="font-mono text-xs font-bold" style={{ color: '#E8EAF6' }}>
          {(value ?? 0).toFixed(2)}
        </span>
      </div>
      <div
        className="signal-track w-full"
        style={{ background: '#0D0F14', borderRadius: 9999, height: 6, overflow: 'hidden' }}
      >
        <div
          style={{
            width: `${pct}%`,
            height: '100%',
            background: barColor,
            borderRadius: 9999,
            transition: 'width 0.6s ease-out',
          }}
        />
      </div>
    </div>
  )
}

// SignalBreakdown — 6-bar grid from context_scores
export default function SignalBreakdown({ contextScores = {} }) {
  const signals = [
    { key: 'budget',     label: 'BUDG' },
    { key: 'visit',      label: 'VISI' },
    { key: 'loan',       label: 'LOAN' },
    { key: 'keyword',    label: 'KEYW' },
    { key: 'question',   label: 'QUES' },
    { key: 'engagement', label: 'ENGA' },
  ]

  return (
    <div className="grid grid-cols-6 gap-3">
      {signals.map(({ key, label }) => (
        <SignalBar key={key} label={label} value={contextScores[key] ?? 0} />
      ))}
    </div>
  )
}
