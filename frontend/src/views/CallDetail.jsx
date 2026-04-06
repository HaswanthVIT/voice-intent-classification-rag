// src/views/CallDetail.jsx — View 2 (Section 9)
// Transcript | Signals | Evidence — 3-tab layout
import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, Clock, Zap, Brain } from 'lucide-react'
import client from '../api/client'
import IntentBadge from '../components/IntentBadge'
import Spinner from '../components/Spinner'
import TranscriptTab from '../components/TranscriptTab'
import SignalsTab from '../components/SignalsTab'
import OutcomeSubmitter from '../components/OutcomeSubmitter'

const LANG_MAP = { ta: 'Tamil', hi: 'Hindi', en: 'English' }

function fmtDuration(sec) {
  if (!sec && sec !== 0) return '--:--'
  const m = Math.floor(sec / 60)
  const s = Math.floor(sec % 60)
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
}

function MetaChip({ label, value }) {
  if (!value) return null
  return (
    <div
      className="flex flex-col px-3 py-1.5 rounded"
      style={{ background: '#1E2130', border: '1px solid #2A2D3E' }}
    >
      <span className="text-[10px] font-mono uppercase" style={{ color: '#8B90B0' }}>{label}</span>
      <span className="text-xs font-mono font-bold" style={{ color: '#E8EAF6' }}>{value}</span>
    </div>
  )
}

function ScoreBlock({ label, value, color = '#E8EAF6' }) {
  return (
    <div className="flex flex-col items-end">
      <span className="text-[10px] font-mono uppercase tracking-wider" style={{ color: '#8B90B0' }}>{label}</span>
      <span className="font-mono text-2xl font-bold" style={{ color }}>{(value ?? 0).toFixed(2)}</span>
    </div>
  )
}

export default function CallDetail() {
  const { id }      = useParams()
  const navigate    = useNavigate()
  const [call,    setCall]    = useState(null)
  const [loading, setLoading] = useState(true)
  const [error,   setError]   = useState(null)
  const [tab,     setTab]     = useState('transcript') // 'transcript' | 'signals' | 'evidence'

  useEffect(() => {
    const load = async () => {
      setLoading(true)
      setError(null)
      try {
        const res = await client.get(`/calls/${id}`)
        // Parse JSON fields if they arrive as strings
        const data = res.data
        const parse = f => {
          if (typeof data[f] === 'string') {
            try { data[f] = JSON.parse(data[f]) } catch {}
          }
        }
        ;['context_scores','reasoning','evidence_refs','learning_insight',
          'rl_weights_used','transcript_segments','speakers','speakers_nlp'].forEach(parse)
        setCall(data)
      } catch (e) {
        setError(e.message || 'Failed to load call.')
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [id])

  if (loading) return <div className="py-16"><Spinner label="Loading call data…" /></div>

  if (error) return (
    <div className="max-w-5xl mx-auto px-6 py-8">
      <div className="rounded-lg p-4 font-mono text-sm"
        style={{ background: '#FF525215', border: '1px solid #FF5252', color: '#FF5252' }}>
        {error}
      </div>
    </div>
  )

  if (!call) return null

  const TABS = [
    { key: 'transcript', label: 'Transcript' },
    { key: 'signals',    label: 'Signals' },
    { key: 'evidence',   label: 'Evidence' },
  ]

  const { INTENT_COLORS } = IntentBadge

  return (
    <div className="max-w-5xl mx-auto px-6 py-8 animate-slide-up">

      {/* Back button */}
      <button
        onClick={() => navigate('/dashboard')}
        className="flex items-center gap-1.5 text-xs font-mono mb-5 transition-colors"
        style={{ color: '#8B90B0' }}
      >
        <ArrowLeft size={13} />
        Back to Dashboard
      </button>

      {/* ── Header Card ── */}
      <div
        className="rounded-xl mb-6 overflow-hidden"
        style={{ background: '#151820', border: '1px solid #2A2D3E' }}
      >
        {/* Intent top-border stripe */}
        <div style={{
          height: 3,
          background: (() => {
            const MAP = { 'Very Strong': '#69F0AE', 'Strong': '#CE93D8', 'Mild': '#FFD740', 'Very Mild': '#4FC3F7', 'No Chance': '#FF5252' }
            return MAP[call.intent_class] || '#2A2D3E'
          })()
        }} />

        <div className="p-6">
          {/* Title row */}
          <div className="flex items-start justify-between mb-4">
            <div className="flex items-center gap-3 flex-wrap">
              <span className="font-mono text-xl font-bold" style={{ color: '#4FC3F7' }}>
                {call.call_id}
              </span>
              <IntentBadge intent={call.intent_class} showMsg />
              {/* Customer speaker identification — NEW */}
              {call.customer_speaker_id &&
                call.customer_speaker_id !== 'UNKNOWN' &&
                call.customer_speaker_id !== 'FALLBACK' && (
                  <span
                    className="px-2 py-0.5 rounded text-xs font-mono"
                    style={{ background: '#80DEEA15', color: '#80DEEA', border: '1px solid #80DEEA44' }}
                  >
                    Customer: {call.customer_speaker_id}
                  </span>
                )}
            </div>

            {/* Score blocks */}
            <div className="flex items-start gap-6">
              <ScoreBlock label="Intent Score"  value={call.intent_score}       color="#E8EAF6" />
              <ScoreBlock label="Signal Score"  value={call.signal_score}       color="#4FC3F7" />
              <ScoreBlock label="LLM Score"     value={call.llm_holistic_score} color="#CE93D8" />
              <ScoreBlock label="Confidence"    value={call.confidence}         color="#69F0AE" />
            </div>
          </div>

          {/* Meta chips */}
          <div className="flex flex-wrap gap-2">
            <MetaChip label="Lang"      value={LANG_MAP[call.language] || call.language} />
            <MetaChip label="Sentiment" value={call.sentiment} />
            <MetaChip label="Tone"      value={call.tone} />
            <MetaChip label="Duration"  value={fmtDuration(call.duration_sec)} />
            {call.speech_rate && (
              <MetaChip label="Rate" value={`${call.speech_rate.toFixed(0)} w/s`} />
            )}
          </div>
        </div>

        {/* Tab bar */}
        <div className="flex" style={{ borderTop: '1px solid #2A2D3E' }}>
          {TABS.map(t => (
            <button
              key={t.key}
              onClick={() => setTab(t.key)}
              className="px-6 py-3 text-xs font-mono uppercase tracking-wider transition-colors duration-150"
              style={{
                color:       tab === t.key ? '#E8EAF6' : '#8B90B0',
                borderBottom: tab === t.key ? '2px solid #4FC3F7' : '2px solid transparent',
                background:  'transparent',
              }}
            >
              {t.label}
            </button>
          ))}
        </div>
      </div>

      {/* ── Tab Content ── */}
      <div className="animate-fade-in">
        {tab === 'transcript' && <TranscriptTab call={call} />}
        {tab === 'signals'    && <SignalsTab    call={call} />}
        {tab === 'evidence'   && <EvidenceTab   call={call} />}
      </div>
    </div>
  )
}

// ── Evidence Tab ─────────────────────────────────────────────
function EvidenceTab({ call }) {
  const reasoning       = Array.isArray(call.reasoning)      ? call.reasoning      : []
  const evidenceRefs    = Array.isArray(call.evidence_refs)  ? call.evidence_refs  : []
  const learningInsight = Array.isArray(call.learning_insight)? call.learning_insight : []

  return (
    <div className="flex flex-col gap-4">
      {/* Reasoning chain */}
      <div
        className="rounded-lg p-5"
        style={{ background: '#151820', border: '1px solid #2A2D3E' }}
      >
        <p className="text-[10px] font-mono uppercase tracking-widest mb-3" style={{ color: '#8B90B0' }}>
          Reasoning Chain
        </p>
        {reasoning.length === 0
          ? <p className="text-xs" style={{ color: '#8B90B0' }}>No reasoning available.</p>
          : (
            <ol className="flex flex-col gap-2">
              {reasoning.map((r, i) => (
                <li key={i} className="flex gap-3 text-sm" style={{ color: '#E8EAF6' }}>
                  <span className="font-mono shrink-0" style={{ color: '#8B90B0' }}>{i + 1}.</span>
                  <span>{r}</span>
                </li>
              ))}
            </ol>
          )
        }
      </div>

      {/* Evidence references */}
      {evidenceRefs.length > 0 && (
        <div
          className="rounded-lg p-5"
          style={{ background: '#151820', border: '1px solid #2A2D3E' }}
        >
          <p className="text-[10px] font-mono uppercase tracking-widest mb-3" style={{ color: '#8B90B0' }}>
            Evidence References
          </p>
          <div className="flex flex-col gap-2">
            {evidenceRefs.map((ref, i) => (
              <div
                key={i}
                className="flex items-center gap-2 px-3 py-2 rounded"
                style={{ background: '#4FC3F715', border: '1px solid #4FC3F744' }}
              >
                <span className="text-xs font-mono" style={{ color: '#8B90B0' }}>Ref:</span>
                <span className="text-xs font-mono font-bold" style={{ color: '#4FC3F7' }}>{ref}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Learning insights */}
      {learningInsight.length > 0 && (
        <div
          className="rounded-lg p-5"
          style={{ background: '#151820', border: '1px solid #2A2D3E' }}
        >
          <p className="text-[10px] font-mono uppercase tracking-widest mb-3" style={{ color: '#CE93D8' }}>
            Learning Insights
          </p>
          <ul className="flex flex-col gap-1.5">
            {learningInsight.map((ins, i) => (
              <li key={i} className="flex gap-2 text-xs" style={{ color: '#CE93D8' }}>
                <span>→</span>
                <span>{ins}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Outcome submitter */}
      <OutcomeSubmitter callId={call.call_id} currentOutcome={call.outcome} />
    </div>
  )
}
