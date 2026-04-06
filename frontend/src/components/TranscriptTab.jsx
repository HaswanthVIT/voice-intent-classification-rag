// src/components/TranscriptTab.jsx — EXTENDED (Section 9.2)
// Speaker colour-coded transcript + keyword highlighting in customer turns

const KEYWORD_COLORS = {
  budget:        '#FFD740', // neon-amber
  price:         '#FFD740',
  cost:          '#FFD740',
  lakhs:         '#FFD740',
  emi:           '#FFD740',
  loan:          '#4FC3F7', // neon-blue
  finance:       '#4FC3F7',
  bank:          '#4FC3F7',
  visit:         '#69F0AE', // neon-green
  'site visit':  '#69F0AE',
  schedule:      '#69F0AE',
  urgent:        '#FF5252', // neon-red
  immediately:   '#FF5252',
  compare:       '#CE93D8', // neon-purple
  difference:    '#CE93D8',
  '2bhk':        '#80DEEA', // specification
  '3bhk':        '#80DEEA',
  sqft:          '#80DEEA',
  amenities:     '#80DEEA',
}

const SPEAKER_COLORS = {
  customer: '#80DEEA', // speaker-customer token
  agent:    '#BCAAA4', // speaker-agent token
}

// Highlight keywords within a text string — returns array of JSX spans
function HighlightKeywords({ text }) {
  if (!text) return null

  // Build a sorted list of all keyword matches
  const lower = text.toLowerCase()
  const matches = []

  Object.entries(KEYWORD_COLORS).forEach(([kw, color]) => {
    let idx = 0
    while ((idx = lower.indexOf(kw, idx)) !== -1) {
      matches.push({ start: idx, end: idx + kw.length, color })
      idx += kw.length
    }
  })

  if (matches.length === 0) return <span>{text}</span>

  // Sort + deduplicate overlapping matches
  matches.sort((a, b) => a.start - b.start)
  const deduped = []
  let cursor = 0
  for (const m of matches) {
    if (m.start >= cursor) {
      deduped.push(m)
      cursor = m.end
    }
  }

  // Build spans
  const parts = []
  let pos = 0
  deduped.forEach((m, i) => {
    if (m.start > pos) {
      parts.push(<span key={`t${i}`}>{text.slice(pos, m.start)}</span>)
    }
    parts.push(
      <span
        key={`k${i}`}
        className="rounded px-0.5 font-bold"
        style={{ background: `${m.color}22`, color: m.color, borderBottom: `1px solid ${m.color}` }}
      >
        {text.slice(m.start, m.end)}
      </span>
    )
    pos = m.end
  })
  if (pos < text.length) {
    parts.push(<span key="last">{text.slice(pos)}</span>)
  }

  return <>{parts}</>
}

// Plain transcript fallback — keyword highlighted only
function PlainTranscript({ text }) {
  return (
    <div
      className="rounded-lg p-4"
      style={{ background: '#0D0F14', border: '1px solid #2A2D3E' }}
    >
      <p className="text-xs mb-3 uppercase tracking-widest font-mono" style={{ color: '#8B90B0' }}>
        Transcript — keywords highlighted
      </p>
      <p className="text-sm leading-relaxed" style={{ color: '#E8EAF6' }}>
        <HighlightKeywords text={text} />
      </p>
    </div>
  )
}

export default function TranscriptTab({ call }) {
  const { transcript_segments, transcript, customer_speaker_id } = call

  // Fallback: no diarization data → plain keyword-highlighted transcript
  if (!transcript_segments || transcript_segments.length === 0) {
    return <PlainTranscript text={transcript} />
  }

  return (
    <div className="flex flex-col gap-1">
      {/* Legend */}
      <div className="flex items-center gap-4 mb-3 px-1">
        <div className="flex items-center gap-1.5">
          <div className="w-3 h-3 rounded-sm" style={{ background: '#80DEEA33', border: '1px solid #80DEEA' }} />
          <span className="text-xs font-mono" style={{ color: '#8B90B0' }}>Customer</span>
        </div>
        <div className="flex items-center gap-1.5">
          <div className="w-3 h-3 rounded-sm" style={{ background: '#BCAAA433', border: '1px solid #BCAAA4' }} />
          <span className="text-xs font-mono" style={{ color: '#8B90B0' }}>Agent</span>
        </div>
        <span className="text-xs" style={{ color: '#4A4F6A' }}>
          Keywords highlighted in customer turns only
        </span>
      </div>

      {/* Speaker-attributed segments */}
      {transcript_segments.map((seg, i) => {
        const isCustomer = seg.speaker === customer_speaker_id
        const roleLabel  = isCustomer ? 'Customer' : 'Agent'
        const roleColor  = isCustomer ? SPEAKER_COLORS.customer : SPEAKER_COLORS.agent

        return (
          <div
            key={i}
            className="rounded-lg p-3 transition-colors"
            style={{
              borderLeft: `3px solid ${roleColor}`,
              background: isCustomer ? '#80DEEA0A' : 'transparent',
            }}
          >
            {/* Speaker label */}
            <div className="flex items-center gap-2 mb-1">
              <span
                className="text-[10px] font-mono font-bold uppercase tracking-wide"
                style={{ color: roleColor }}
              >
                {roleLabel}
              </span>
              <span className="text-[10px] font-mono" style={{ color: '#4A4F6A' }}>
                ({seg.speaker})
              </span>
            </div>

            {/* Text — keyword highlighted in customer turns only */}
            <p className="text-sm leading-relaxed font-mono" style={{ color: isCustomer ? '#E8EAF6' : '#8B90B0' }}>
              {isCustomer
                ? <HighlightKeywords text={seg.text} />
                : <span>{seg.text}</span>
              }
            </p>
          </div>
        )
      })}
    </div>
  )
}
