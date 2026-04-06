// src/components/PolicyModeBadge.jsx — NEW (Section 11)
import { Cpu, Zap } from 'lucide-react'

export default function PolicyModeBadge({ policyMode }) {
  const isRL = policyMode === 'rl_contextual_bandit'

  return (
    <span
      className="inline-flex items-center gap-1.5 px-3 py-1 rounded text-xs font-mono font-bold uppercase tracking-wide"
      style={{
        background: isRL ? '#69F0AE' : '#FFD740',
        color: '#0D0F14',
      }}
    >
      {isRL ? <Cpu size={11} /> : <Zap size={11} />}
      {isRL ? 'RL Contextual Bandit' : 'Initial Weights'}
    </span>
  )
}
