// src/components/MiniCallCard.jsx
import { useNavigate } from 'react-router-dom'
import { Clock } from 'lucide-react'
import IntentBadge from './IntentBadge'

function fmtDuration(sec) {
  if (!sec && sec !== 0) return '--:--'
  const m = Math.floor(sec / 60)
  const s = Math.floor(sec % 60)
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
}

export default function MiniCallCard({ call }) {
  const navigate = useNavigate()

  return (
    <div
      className="flex items-center justify-between px-4 py-3 rounded-lg cursor-pointer hover:bg-[#1E2130] transition-colors duration-150"
      style={{ borderBottom: '1px solid #2A2D3E' }}
      onClick={() => navigate(`/calls/${call.call_id}`)}
    >
      <div className="flex items-center gap-3">
        <span className="font-mono text-sm font-bold" style={{ color: '#4FC3F7' }}>
          {call.call_id}
        </span>
        <IntentBadge intent={call.intent_class} size="sm" />
        {/* Outcome chip */}
        {call.outcome && (
          <span
            className="px-2 py-0.5 rounded text-[10px] font-mono uppercase"
            style={{ color: '#8B90B0', border: '1px solid #2A2D3E' }}
          >
            {call.outcome.replace('_', ' ')}
          </span>
        )}
        {/* Customer speaker tag — shown if available */}
        {call.customer_speaker_id &&
          call.customer_speaker_id !== 'UNKNOWN' &&
          call.customer_speaker_id !== 'FALLBACK' && (
            <span className="font-mono text-[10px]" style={{ color: '#80DEEA' }}>
              {call.customer_speaker_id}
            </span>
          )}
      </div>

      <div className="flex items-center gap-4">
        <span className="font-mono text-sm font-bold" style={{ color: '#E8EAF6' }}>
          {(call.intent_score ?? 0).toFixed(2)}
        </span>
        <div className="flex items-center gap-1" style={{ color: '#8B90B0' }}>
          <Clock size={11} />
          <span className="font-mono text-xs">{fmtDuration(call.duration_sec)}</span>
        </div>
      </div>
    </div>
  )
}
