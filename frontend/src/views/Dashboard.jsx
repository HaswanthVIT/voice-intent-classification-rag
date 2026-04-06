// src/views/Dashboard.jsx — View 1 (Section 8)
import { useState, useEffect } from 'react'
import { RefreshCw } from 'lucide-react'
import client from '../api/client'
import CallCard from '../components/CallCard'
import Spinner from '../components/Spinner'

const FILTERS = ['All', 'Very Strong', 'Strong', 'Mild', 'Very Mild', 'No Chance']

export default function Dashboard() {
  const [calls,   setCalls]   = useState([])
  const [loading, setLoading] = useState(true)
  const [error,   setError]   = useState(null)
  const [filter,  setFilter]  = useState('All')

  const fetchCalls = async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await client.get('/calls')
      setCalls(res.data)
    } catch (e) {
      setError(e.message || 'Failed to load calls.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { fetchCalls() }, [])

  // Apply filter
  const displayed = filter === 'All'
    ? calls
    : calls.filter(c => c.intent_class === filter)

  return (
    <div className="max-w-5xl mx-auto px-6 py-8 animate-fade-in">

      {/* Page header */}
      <div className="flex items-start justify-between mb-6">
        <div>
          <h1
            className="font-mono text-2xl font-bold tracking-tight uppercase"
            style={{ color: '#E8EAF6', letterSpacing: '-0.01em' }}
          >
            Call Dashboard
          </h1>
          <p className="text-xs font-mono mt-1" style={{ color: '#8B90B0' }}>
            {displayed.length} call{displayed.length !== 1 ? 's' : ''} — sorted by intent score desc
          </p>
        </div>

        <button
          onClick={fetchCalls}
          className="flex items-center gap-2 px-3 py-1.5 rounded text-xs font-mono transition-colors duration-150"
          style={{ background: '#1E2130', color: '#8B90B0', border: '1px solid #2A2D3E' }}
        >
          <RefreshCw size={12} className={loading ? 'animate-spin' : ''} />
          Refresh
        </button>
      </div>

      {/* Filter bar */}
      <div className="flex flex-wrap gap-2 mb-6">
        {FILTERS.map(f => {
          const active = filter === f
          return (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className="px-4 py-1.5 rounded text-xs font-mono uppercase tracking-wide transition-all duration-150"
              style={{
                background: active ? '#1E2130' : 'transparent',
                color:      active ? '#E8EAF6'  : '#8B90B0',
                border:     `1px solid ${active ? '#4FC3F7' : '#2A2D3E'}`,
              }}
            >
              {f}
            </button>
          )
        })}
      </div>

      {/* State rendering */}
      {loading && <Spinner label="Loading calls…" />}

      {!loading && error && (
        <div
          className="rounded-lg p-4 text-sm font-mono"
          style={{ background: '#FF525215', border: '1px solid #FF5252', color: '#FF5252' }}
        >
          {error}
        </div>
      )}

      {!loading && !error && displayed.length === 0 && (
        <div
          className="rounded-lg p-8 text-center"
          style={{ background: '#151820', border: '1px solid #2A2D3E' }}
        >
          <p className="font-mono text-sm" style={{ color: '#8B90B0' }}>
            No calls match the selected filter.
          </p>
        </div>
      )}

      {/* Call cards — rank re-computed on filter change */}
      {!loading && !error && (
        <div className="flex flex-col gap-4">
          {displayed.map((call, idx) => (
            <CallCard key={call.call_id} call={call} rank={idx + 1} />
          ))}
        </div>
      )}
    </div>
  )
}
