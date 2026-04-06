// src/components/OutcomeSubmitter.jsx
// Section 9.6 — unchanged from spec
import { useState } from 'react'
import { CheckCircle, AlertCircle, Loader2 } from 'lucide-react'
import client from '../api/client'

const OUTCOMES = [
  { value: 'converted',      label: 'Converted' },
  { value: 'visited',        label: 'Visited' },
  { value: 'follow_up',      label: 'Follow Up' },
  { value: 'no_response',    label: 'No Response' },
  { value: 'not_interested', label: 'Not Interested' },
]

export default function OutcomeSubmitter({ callId, currentOutcome }) {
  const [selected, setSelected] = useState(currentOutcome || '')
  const [status,   setStatus]   = useState(null)   // 'success' | 'error'
  const [loading,  setLoading]  = useState(false)

  const submit = async () => {
    if (!selected) return
    setLoading(true)
    setStatus(null)
    try {
      await client.post('/outcome', { call_id: callId, outcome: selected })
      setStatus('success')
    } catch {
      setStatus('error')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div
      className="rounded-lg p-4 mt-4"
      style={{ background: '#151820', border: '1px solid #2A2D3E' }}
    >
      <h3 className="text-sm font-medium mb-3" style={{ color: '#E8EAF6' }}>
        Submit Outcome
      </h3>

      <div className="flex items-center gap-3">
        <select
          value={selected}
          onChange={e => { setSelected(e.target.value); setStatus(null) }}
          className="flex-1 rounded px-3 py-2 text-sm font-mono outline-none transition-colors"
          style={{
            background: '#1E2130',
            border: '1px solid #2A2D3E',
            color: selected ? '#E8EAF6' : '#8B90B0',
          }}
        >
          <option value="" disabled style={{ color: '#8B90B0' }}>
            — Select Outcome —
          </option>
          {OUTCOMES.map(o => (
            <option key={o.value} value={o.value} style={{ background: '#1E2130', color: '#E8EAF6' }}>
              {o.label}
            </option>
          ))}
        </select>

        <button
          onClick={submit}
          disabled={!selected || loading}
          className="px-5 py-2 rounded text-sm font-mono font-bold uppercase tracking-wide transition-all duration-150"
          style={{
            background: selected && !loading ? '#4FC3F7' : '#2A2D3E',
            color: selected && !loading ? '#0D0F14' : '#8B90B0',
            cursor: selected && !loading ? 'pointer' : 'not-allowed',
          }}
        >
          {loading
            ? <Loader2 size={14} className="animate-spin" />
            : 'Submit'
          }
        </button>
      </div>

      {/* Feedback */}
      {status === 'success' && (
        <div className="flex items-center gap-2 mt-3">
          <CheckCircle size={14} style={{ color: '#69F0AE' }} />
          <span className="text-xs font-mono" style={{ color: '#69F0AE' }}>
            Outcome recorded. RL update triggered.
          </span>
        </div>
      )}
      {status === 'error' && (
        <div className="flex items-center gap-2 mt-3">
          <AlertCircle size={14} style={{ color: '#FF5252' }} />
          <span className="text-xs font-mono" style={{ color: '#FF5252' }}>
            Submission failed. Please retry.
          </span>
        </div>
      )}
    </div>
  )
}
