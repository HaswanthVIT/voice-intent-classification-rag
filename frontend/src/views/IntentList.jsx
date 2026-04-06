// src/views/IntentList.jsx — View 3 (Section 10)
// Categorical grouping: High / Medium / Low Intent — collapsible
import { useState, useEffect } from 'react'
import { ChevronUp, ChevronDown } from 'lucide-react'
import client from '../api/client'
import MiniCallCard from '../components/MiniCallCard'
import Spinner from '../components/Spinner'

const SECTIONS = [
  {
    key:      'high',
    label:    'High Intent',
    classes:  ['Very Strong', 'Strong'],
    color:    '#69F0AE',
  },
  {
    key:      'medium',
    label:    'Medium Intent',
    classes:  ['Mild'],
    color:    '#FFD740',
  },
  {
    key:      'low',
    label:    'Low Intent',
    classes:  ['Very Mild', 'No Chance'],
    color:    '#FF5252',
  },
]

function CollapsibleSection({ section, calls }) {
  const [open, setOpen] = useState(true)
  const filtered = calls.filter(c => section.classes.includes(c.intent_class))

  return (
    <div
      className="rounded-xl overflow-hidden mb-4"
      style={{ border: `1px solid #2A2D3E` }}
    >
      {/* Section header */}
      <button
        onClick={() => setOpen(o => !o)}
        className="w-full flex items-center justify-between px-5 py-4 transition-colors duration-150 hover:bg-[#1E2130]"
        style={{ background: '#151820' }}
      >
        <div className="flex items-center gap-3">
          <span
            className="w-2.5 h-2.5 rounded-full"
            style={{ background: section.color }}
          />
          <span
            className="font-mono text-sm font-bold uppercase tracking-wide"
            style={{ color: section.color }}
          >
            {section.label}
          </span>
          <span
            className="font-mono text-xs px-2 py-0.5 rounded-full"
            style={{ background: `${section.color}22`, color: section.color }}
          >
            {filtered.length}
          </span>
        </div>
        {open
          ? <ChevronUp size={16} style={{ color: '#8B90B0' }} />
          : <ChevronDown size={16} style={{ color: '#8B90B0' }} />
        }
      </button>

      {/* Call list */}
      {open && (
        <div style={{ background: '#0D0F14' }}>
          {filtered.length === 0
            ? (
              <p className="px-5 py-4 text-xs font-mono" style={{ color: '#8B90B0' }}>
                No calls in this category.
              </p>
            )
            : filtered.map(c => <MiniCallCard key={c.call_id} call={c} />)
          }
        </div>
      )}
    </div>
  )
}

export default function IntentList() {
  const [calls,   setCalls]   = useState([])
  const [loading, setLoading] = useState(true)
  const [error,   setError]   = useState(null)

  useEffect(() => {
    const load = async () => {
      try {
        const res = await client.get('/calls')
        setCalls(res.data)
      } catch (e) {
        setError(e.message || 'Failed to load calls.')
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  return (
    <div className="max-w-4xl mx-auto px-6 py-8 animate-fade-in">
      <div className="mb-6">
        <h1
          className="font-mono text-2xl font-bold uppercase tracking-tight"
          style={{ color: '#E8EAF6' }}
        >
          Intent List
        </h1>
        <p className="text-xs font-mono mt-1" style={{ color: '#8B90B0' }}>
          Categorical View — Collapsible Sections
        </p>
      </div>

      {loading && <Spinner label="Loading intent list…" />}

      {!loading && error && (
        <div className="rounded-lg p-4 text-sm font-mono"
          style={{ background: '#FF525215', border: '1px solid #FF5252', color: '#FF5252' }}>
          {error}
        </div>
      )}

      {!loading && !error && SECTIONS.map(section => (
        <CollapsibleSection key={section.key} section={section} calls={calls} />
      ))}
    </div>
  )
}
