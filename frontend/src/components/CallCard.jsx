// src/components/CallCard.jsx
// Implements Section 8.1 — extended with customer_speaker_id tag
import { useNavigate } from 'react-router-dom'
import { ChevronRight, Clock } from 'lucide-react'
import IntentBadge, { INTENT_COLORS } from './IntentBadge'
import SignalBreakdown from './SignalBar'

const LANG_MAP = { ta: 'Tamil', hi: 'Hindi', en: 'English' }

function fmtDuration(sec) {
  if (!sec && sec !== 0) return '--:--'
  const m = Math.floor(sec / 60)
  const s = Math.floor(sec % 60)
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
}

function intentBorderStyle(intent) {
  const c = INTENT_COLORS[intent]
  return c ? { borderTop: `2px solid ${c.bg}` } : {}
}

export default function CallCard({ call, rank }) {
  const navigate = useNavigate()
  const ctx = call.context_scores || {}

  // Truncate call_id at 12 chars for display
  const displayId = call.call_id?.length > 12
    ? call.call_id.slice(0, 12) + '…'
    : call.call_id

  // First reasoning string, truncated at 80 chars
  const reasoning = Array.isArray(call.reasoning) ? call.reasoning[0] : call.reasoning
  const shortReason = reasoning?.length > 80
    ? reasoning.slice(0, 80) + '…'
    : reasoning

  return (
    <div
      className="card animate-slide-up cursor-pointer group hover:border-[#3D4260] transition-colors duration-200"
      style={{ ...intentBorderStyle(call.intent_class) }}
      onClick={() => navigate(`/calls/${call.call_id}`)}
    >
      <div className="p-5">
        {/* Header row */}
        <div className="flex items-start justify-between mb-3">
          <div className="flex items-center gap-3">
            {/* Rank number */}
            <span
              className="font-mono text-xs w-6 text-right shrink-0"
              style={{ color: '#8B90B0' }}
            >
              #{rank}
            </span>

            {/* Call ID + speaker tag */}
            <div className="flex flex-col gap-0.5">
              <span className="font-mono text-sm font-bold" style={{ color: '#4FC3F7' }}>
                {displayId}
              </span>
              {/* Customer tag — NEW: shown when not NULL/UNKNOWN */}
              {call.customer_speaker_id &&
                call.customer_speaker_id !== 'UNKNOWN' &&
                call.customer_speaker_id !== 'FALLBACK' && (
                  <span
                    className="font-mono text-[10px]"
                    style={{ color: '#80DEEA' }}
                  >
                    Customer: {call.customer_speaker_id}
                  </span>
                )}
            </div>

            <IntentBadge intent={call.intent_class} />

            {/* Outcome chip if present */}
            {call.outcome && (
              <span
                className="px-2 py-0.5 rounded text-[10px] font-mono uppercase tracking-wide border"
                style={{ color: '#8B90B0', borderColor: '#2A2D3E' }}
              >
                {call.outcome.replace('_', ' ')}
              </span>
            )}
          </div>

          {/* Right side: scores + duration + chevron */}
          <div className="flex items-center gap-6 shrink-0">
            <div className="text-right">
              <div className="font-mono text-[10px] uppercase tracking-wider" style={{ color: '#8B90B0' }}>
                Score
              </div>
              <div className="font-mono text-lg font-bold" style={{ color: '#E8EAF6' }}>
                {(call.intent_score ?? 0).toFixed(2)}
              </div>
            </div>
            <div className="text-right">
              <div className="font-mono text-[10px] uppercase tracking-wider" style={{ color: '#8B90B0' }}>
                Conf
              </div>
              <div className="font-mono text-lg font-bold" style={{ color: '#E8EAF6' }}>
                {(call.confidence ?? 0).toFixed(2)}
              </div>
            </div>
            <div className="flex items-center gap-1" style={{ color: '#8B90B0' }}>
              <Clock size={12} />
              <span className="font-mono text-xs">{fmtDuration(call.duration_sec)}</span>
            </div>
            <ChevronRight
              size={16}
              style={{ color: '#8B90B0' }}
              className="group-hover:text-[#4FC3F7] transition-colors"
            />
          </div>
        </div>

        {/* Meta row: language, tone */}
        <div className="flex items-center gap-4 mb-3 pl-9">
          {call.language && (
            <span className="text-xs" style={{ color: '#8B90B0' }}>
              {LANG_MAP[call.language] || call.language}
            </span>
          )}
          {call.tone && (
            <span className="text-xs" style={{ color: '#8B90B0' }}>
              Tone: {call.tone}
            </span>
          )}
        </div>

        {/* Reasoning preview */}
        {shortReason && (
          <p className="text-xs mb-4 pl-9" style={{ color: '#8B90B0', lineHeight: 1.6 }}>
            {shortReason}
          </p>
        )}

        {/* Signal breakdown bars — sourced from context_scores */}
        <div className="pl-9">
          <SignalBreakdown contextScores={ctx} />
        </div>
      </div>
    </div>
  )
}
