// src/views/InsightsPanel.jsx — View 4 (Section 11)
// Extended: PolicyModeBadge + rolling 500-call avg note + RL weight chart
import { useEffect, useState } from 'react'
import {
  ResponsiveContainer, BarChart, Bar, XAxis, YAxis,
  Tooltip, Cell
} from 'recharts'
import client from '../api/client'
import Spinner from '../components/Spinner'
import PolicyModeBadge from '../components/PolicyModeBadge'

// Recharts custom tooltip
function CustomTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null
  return (
    <div className="px-3 py-2 rounded text-xs font-mono"
      style={{ background: '#1E2130', border: '1px solid #3D4260', color: '#E8EAF6' }}>
      <p style={{ color: '#8B90B0' }}>{label}</p>
      <p>{payload[0]?.value?.toFixed(3)}</p>
    </div>
  )
}

// Horizontal bar for conversion rates / class performance
function HBar({ label, value, color, suffix = '%', extra }) {
  return (
    <div className="flex items-center gap-3 mb-3">
      <div className="w-28 shrink-0">
        {typeof label === 'string'
          ? <span className="text-xs font-mono" style={{ color: '#8B90B0' }}>{label}</span>
          : label
        }
      </div>
      <div className="flex-1 rounded-full overflow-hidden" style={{ background: '#0D0F14', height: 8 }}>
        <div
          style={{
            width: `${Math.min(value * 100, 100)}%`,
            height: '100%',
            background: color,
            borderRadius: 9999,
            transition: 'width 0.8s ease-out',
          }}
        />
      </div>
      <span className="text-xs font-mono font-bold w-16 text-right" style={{ color: '#E8EAF6' }}>
        {(value * 100).toFixed(0)}{suffix}
      </span>
      {extra && <span className="text-xs font-mono" style={{ color: '#8B90B0' }}>{extra}</span>}
    </div>
  )
}

// Intent badge pill inline
function IntentPill({ intent }) {
  const MAP = {
    'Very Strong': '#69F0AE',
    'Strong':      '#CE93D8',
    'Mild':        '#FFD740',
    'Very Mild':   '#4FC3F7',
    'No Chance':   '#FF5252',
  }
  const c = MAP[intent] || '#2A2D3E'
  return (
    <span
      className="px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase w-28 text-center inline-block"
      style={{ background: `${c}33`, color: c, border: `1px solid ${c}55` }}
    >
      {intent}
    </span>
  )
}

export default function InsightsPanel() {
  const [summary, setSummary] = useState(null)
  const [perf,    setPerf]    = useState(null)
  const [loading, setLoading] = useState(true)
  const [error,   setError]   = useState(null)

  useEffect(() => {
    const load = async () => {
      try {
        const [s, p] = await Promise.all([
          client.get('/learning_summary'),
          client.get('/performance'),
        ])
        setSummary(s.data)
        setPerf(p.data)
      } catch (e) {
        setError(e.message || 'Failed to load insights.')
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  if (loading) return <div className="py-16"><Spinner label="Loading insights…" /></div>

  if (error) return (
    <div className="max-w-5xl mx-auto px-6 py-8">
      <div className="rounded-lg p-4 font-mono text-sm"
        style={{ background: '#FF525215', border: '1px solid #FF5252', color: '#FF5252' }}>
        {error}
      </div>
    </div>
  )

  const isRLActive = summary?.policy_mode === 'rl_contextual_bandit'

  // Weight chart data — exclude tone & sentiment (fixed), sort descending
  const weightData = Object.entries(summary?.current_weights || {})
    .filter(([k]) => !['tone', 'sentiment'].includes(k))
    .map(([signal, weight]) => ({ signal: signal.charAt(0).toUpperCase() + signal.slice(1), weight: parseFloat((weight).toFixed(3)) }))
    .sort((a, b) => b.weight - a.weight)

  // Signal conversion rates
  const convRates = summary?.signal_conversion_rates || {}

  // Performance by intent class
  const perfData = Array.isArray(perf) ? perf : []

  const INTENT_ORDER = ['Very Strong', 'Strong', 'Mild', 'Very Mild', 'No Chance']
  const INTENT_COLORS = {
    'Very Strong': '#69F0AE',
    'Strong':      '#CE93D8',
    'Mild':        '#FFD740',
    'Very Mild':   '#4FC3F7',
    'No Chance':   '#FF5252',
  }

  return (
    <div className="max-w-5xl mx-auto px-6 py-8 animate-fade-in" style={{ minHeight: '100vh' }}>

      {/* ── Header ── */}
      <div className="flex items-center gap-4 mb-1">
        <h1 className="font-mono text-2xl font-bold uppercase tracking-tight" style={{ color: '#E8EAF6' }}>
          Learning Insights
        </h1>
        {/* Policy mode badge — NEW Section 11 */}
        <PolicyModeBadge policyMode={summary?.policy_mode} />
      </div>
      <p className="text-xs font-mono mb-8" style={{ color: '#8B90B0' }}>
        {summary?.total_calls_learned ?? 0} outcomes recorded
        {' · '}
        Buffer: {summary?.buffer_size ?? 0} entries
      </p>

      <div className="grid grid-cols-2 gap-6 mb-6">

        {/* ── Adaptive Weights Chart ── */}
        <div
          className="rounded-xl p-5"
          style={{ background: '#151820', border: '1px solid #2A2D3E' }}
        >
          <h2 className="text-sm font-medium mb-1" style={{ color: '#E8EAF6' }}>
            Adaptive Weights
          </h2>
          {/* Rolling avg note — NEW (Section 11.2) */}
          {isRLActive && (
            <p className="text-xs mb-4" style={{ color: '#8B90B0', lineHeight: 1.6 }}>
              Rolling 500-call average of per-call W_t values.
              Each call receives bespoke weights based on its 15-dimensional context.
            </p>
          )}
          {!isRLActive && (
            <p className="text-xs mb-4" style={{ color: '#8B90B0' }}>
              Using initial weight priors — RL policy not yet trained.
            </p>
          )}

          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={weightData} layout="vertical" margin={{ left: 0, right: 20 }}>
              <XAxis
                type="number"
                domain={[0, 0.5]}
                tick={{ fill: '#8B90B0', fontSize: 11, fontFamily: 'JetBrains Mono' }}
                tickLine={false}
                axisLine={false}
              />
              <YAxis
                type="category"
                dataKey="signal"
                tick={{ fill: '#E8EAF6', fontSize: 12, fontFamily: 'JetBrains Mono' }}
                tickLine={false}
                axisLine={false}
                width={80}
              />
              <Tooltip content={<CustomTooltip />} cursor={{ fill: '#1E2130' }} />
              <Bar dataKey="weight" radius={[0, 4, 4, 0]}>
                {weightData.map((entry, i) => (
                  <Cell key={i} fill={i === 0 ? '#69F0AE' : '#4FC3F7'} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>

          {/* Fixed weights note */}
          <div className="flex gap-4 mt-1">
            <span className="text-[10px] font-mono" style={{ color: '#4A4F6A' }}>
              tone (fixed): {(summary?.current_weights?.tone ?? 0.03).toFixed(3)}
            </span>
            <span className="text-[10px] font-mono" style={{ color: '#4A4F6A' }}>
              sentiment (fixed): {(summary?.current_weights?.sentiment ?? 0.02).toFixed(3)}
            </span>
          </div>
        </div>

        {/* ── Signal Conversion Rates ── */}
        <div
          className="rounded-xl p-5"
          style={{ background: '#151820', border: '1px solid #2A2D3E' }}
        >
          <h2 className="text-sm font-medium mb-4" style={{ color: '#E8EAF6' }}>
            Signal Conversion Rates
          </h2>
          {Object.keys(convRates).length === 0
            ? <p className="text-xs" style={{ color: '#8B90B0' }}>No conversion data yet.</p>
            : Object.entries(convRates)
                .sort(([,a],[,b]) => b - a)
                .map(([signal, rate]) => (
                  <HBar
                    key={signal}
                    label={signal.charAt(0).toUpperCase() + signal.slice(1)}
                    value={rate}
                    color="#4FC3F7"
                    suffix="%"
                  />
                ))
          }
        </div>
      </div>

      {/* ── Intent Class Performance ── */}
      <div
        className="rounded-xl p-5"
        style={{ background: '#151820', border: '1px solid #2A2D3E' }}
      >
        <h2 className="text-sm font-medium mb-4" style={{ color: '#E8EAF6' }}>
          Intent Class Performance
        </h2>

        {perfData.length === 0
          ? <p className="text-xs" style={{ color: '#8B90B0' }}>No performance data yet.</p>
          : (
            <div className="flex flex-col gap-3">
              {INTENT_ORDER.map(cls => {
                const row = perfData.find(p => p.intent_class === cls)
                if (!row) return null
                const cvr = row.conversion_rate ?? 0
                const count = row.call_count ?? 0
                return (
                  <div key={cls} className="flex items-center gap-4">
                    <IntentPill intent={cls} />
                    <div className="flex-1 rounded-full overflow-hidden" style={{ background: '#0D0F14', height: 8 }}>
                      <div
                        style={{
                          width: `${Math.min(cvr * 100, 100)}%`,
                          height: '100%',
                          background: INTENT_COLORS[cls] || '#4FC3F7',
                          borderRadius: 9999,
                          transition: 'width 0.8s ease-out',
                        }}
                      />
                    </div>
                    <span
                      className="text-xs font-mono font-bold w-20 text-right"
                      style={{ color: INTENT_COLORS[cls] || '#E8EAF6' }}
                    >
                      {(cvr * 100).toFixed(0)}% CVR
                    </span>
                    <span className="text-xs font-mono w-16" style={{ color: '#8B90B0' }}>
                      {count} calls
                    </span>
                  </div>
                )
              })}
            </div>
          )
        }
      </div>

    </div>
  )
}
