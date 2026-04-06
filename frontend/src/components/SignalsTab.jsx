// src/components/SignalsTab.jsx — EXTENDED (Section 9.3)
// Acoustic + NLP + Context Scores + Speaker Comparison + RL Weights + Scoring Breakdown

import { SignalBar } from './SignalBar'
import SpeakerComparison from './SpeakerComparison'
import RLWeightsPanel from './RLWeightsPanel'

function SectionLabel({ children }) {
  return (
    <p className="text-[10px] font-mono uppercase tracking-widest mb-3" style={{ color: '#8B90B0' }}>
      {children}
    </p>
  )
}

function InfoRow({ label, value }) {
  return (
    <div className="flex justify-between items-center py-1.5" style={{ borderBottom: '1px solid #1E2130' }}>
      <span className="text-xs" style={{ color: '#8B90B0' }}>{label}</span>
      <span className="text-xs font-mono font-bold" style={{ color: '#E8EAF6' }}>{value ?? '—'}</span>
    </div>
  )
}

export default function SignalsTab({ call }) {
  const ctx = call.context_scores || {}

  // Context score bars list
  const CTX_BARS = [
    { key: 'budget',     label: 'Budget',     color: '#4FC3F7' },
    { key: 'visit',      label: 'Visit',      color: '#4FC3F7' },
    { key: 'loan',       label: 'Loan',       color: '#CE93D8' },
    { key: 'keyword',    label: 'Keyword',    color: '#69F0AE' },
    { key: 'question',   label: 'Question',   color: '#FFD740' },
    { key: 'engagement', label: 'Engagement', color: '#FFD740' },
  ]

  // Scoring breakdown math
  const sig  = call.signal_score      ?? 0
  const llm  = call.llm_holistic_score ?? 0
  const final = call.intent_score      ?? 0

  return (
    <div className="flex flex-col gap-5">

      {/* ── Row 1: Acoustic + NLP ──────────────────────────────── */}
      <div className="grid grid-cols-2 gap-4">
        {/* Acoustic Signals */}
        <div
          className="rounded-lg p-4"
          style={{ background: '#151820', border: '1px solid #2A2D3E' }}
        >
          <SectionLabel>Acoustic Signals</SectionLabel>
          <InfoRow label="Pitch Mean"    value={call.pitch_mean ? `${call.pitch_mean.toFixed(0)} Hz` : null} />
          <InfoRow label="Speech Rate"   value={call.speech_rate ? `${call.speech_rate.toFixed(0)} wpm` : null} />
          <InfoRow label="Energy Delta"  value={call.energy_delta != null ? `${call.energy_delta > 0 ? '+' : ''}${call.energy_delta.toFixed(1)}%` : null} />
          <InfoRow label="Tone"          value={call.tone} />
          <InfoRow label="Language"      value={{ ta: 'Tamil', hi: 'Hindi', en: 'English' }[call.language] || call.language} />
        </div>

        {/* NLP Signals — full-call */}
        <div
          className="rounded-lg p-4"
          style={{ background: '#151820', border: '1px solid #2A2D3E' }}
        >
          <SectionLabel>NLP Signals (Full-Call)</SectionLabel>
          <InfoRow label="Has Budget"     value={call.has_budget ? 'Yes' : 'No'} />
          <InfoRow label="Has Loan"       value={call.has_loan ? 'Yes' : 'No'} />
          <InfoRow label="Has Visit"      value={call.has_visit ? 'Yes' : 'No'} />
          <InfoRow label="Sentiment"      value={call.sentiment} />
          <InfoRow label="Engagement"     value={call.engagement_score?.toFixed(2)} />
          <InfoRow label="Keyword Norm"   value={call.keyword_norm?.toFixed(2)} />
          <InfoRow label="Question Norm"  value={call.question_norm?.toFixed(2)} />
          <InfoRow label="Duration Norm"  value={call.duration_norm?.toFixed(2)} />
        </div>
      </div>

      {/* ── Row 2: Context Scores (LLM-validated) ─────────────── */}
      <div
        className="rounded-lg p-4"
        style={{ background: '#151820', border: '1px solid #2A2D3E' }}
      >
        <SectionLabel>Context Scores — LLM-validated, customer signals only</SectionLabel>
        <div className="grid grid-cols-2 gap-x-8 gap-y-3">
          {CTX_BARS.map(({ key, label, color }) => (
            <SignalBar key={key} label={label} value={ctx[key] ?? 0} color={color} />
          ))}
        </div>
      </div>

      {/* ── Row 3: Per-Speaker Signal Comparison (NEW) ────────── */}
      <SpeakerComparison call={call} />

      {/* ── Row 4: RL Weights Panel (NEW) ─────────────────────── */}
      <RLWeightsPanel rl_weights_used={call.rl_weights_used} />

      {/* ── Row 5: Scoring Breakdown ──────────────────────────── */}
      <div
        className="rounded-lg p-4"
        style={{ background: '#151820', border: '1px solid #2A2D3E' }}
      >
        <SectionLabel>Scoring Breakdown</SectionLabel>
        <div className="font-mono text-sm flex flex-col gap-2">
          <div className="flex justify-between items-center">
            <span style={{ color: '#8B90B0' }}>Signal Score (35%)</span>
            <span style={{ color: '#E8EAF6' }}>
              {sig.toFixed(2)} × 0.35 ={' '}
              <span style={{ color: '#4FC3F7' }}>{(sig * 0.35).toFixed(3)}</span>
            </span>
          </div>
          <div className="flex justify-between items-center">
            <span style={{ color: '#8B90B0' }}>LLM Holistic (65%)</span>
            <span style={{ color: '#E8EAF6' }}>
              {llm.toFixed(2)} × 0.65 ={' '}
              <span style={{ color: '#CE93D8' }}>{(llm * 0.65).toFixed(3)}</span>
            </span>
          </div>
          <div
            className="flex justify-between items-center pt-2 mt-1"
            style={{ borderTop: '1px solid #2A2D3E' }}
          >
            <span className="font-bold" style={{ color: '#E8EAF6' }}>Final Intent Score</span>
            <span className="text-lg font-bold" style={{ color: '#69F0AE' }}>
              {final.toFixed(2)}
            </span>
          </div>
        </div>
      </div>

    </div>
  )
}
