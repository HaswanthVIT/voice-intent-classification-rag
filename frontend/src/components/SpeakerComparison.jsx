// src/components/SpeakerComparison.jsx — NEW (Section 9.4)
// Per-speaker signal comparison table

const FIELDS = [
  { key: 'has_budget',    label: 'has_budget' },
  { key: 'has_loan',      label: 'has_loan' },
  { key: 'has_visit',     label: 'has_visit' },
  { key: 'question_count',label: 'question_count' },
  { key: 'sentiment',     label: 'sentiment' },
]

export default function SpeakerComparison({ call }) {
  const { speakers_nlp, customer_speaker_id, speakers } = call

  // Graceful degradation when speakers_nlp is NULL
  if (!speakers_nlp || Object.keys(speakers_nlp).length === 0) {
    return (
      <div
        className="rounded-lg p-4"
        style={{ background: '#151820', border: '1px solid #2A2D3E' }}
      >
        <h3 className="text-sm font-medium mb-2" style={{ color: '#E8EAF6' }}>
          Per-Speaker Signals
        </h3>
        <p className="text-xs" style={{ color: '#8B90B0' }}>
          Speaker breakdown not available — diarization data absent for this call.
        </p>
      </div>
    )
  }

  const spkIds = Object.keys(speakers_nlp)

  return (
    <div
      className="rounded-lg p-4"
      style={{ background: '#151820', border: '1px solid #2A2D3E' }}
    >
      <h3 className="text-sm font-medium mb-1" style={{ color: '#E8EAF6' }}>
        Per-Speaker Signal Comparison
      </h3>
      <p className="text-xs mb-3" style={{ color: '#80DEEA' }}>
        Customer identified: {customer_speaker_id || 'UNKNOWN'}
      </p>

      <div className="overflow-x-auto">
        <table className="w-full text-xs font-mono">
          <thead>
            <tr>
              <th className="text-left py-2 pr-4" style={{ color: '#8B90B0', fontWeight: 500 }}>
                Signal
              </th>
              {spkIds.map(spk => {
                const isCustomer = spk === customer_speaker_id
                return (
                  <th
                    key={spk}
                    className="text-center py-2 px-3"
                    style={{
                      color: isCustomer ? '#80DEEA' : '#BCAAA4',
                      fontWeight: isCustomer ? 700 : 400,
                    }}
                  >
                    {isCustomer ? `${spk} ✓ Customer` : `${spk} Agent`}
                  </th>
                )
              })}
            </tr>
          </thead>
          <tbody>
            {FIELDS.map(({ key, label }) => (
              <tr
                key={key}
                style={{ borderTop: '1px solid #2A2D3E' }}
              >
                <td className="py-2 pr-4" style={{ color: '#8B90B0' }}>
                  {label}
                </td>
                {spkIds.map(spk => {
                  const isCustomer = spk === customer_speaker_id
                  const val = speakers_nlp[spk]?.[key]
                  return (
                    <td
                      key={spk}
                      className="py-2 px-3 text-center"
                      style={{ color: isCustomer ? '#E8EAF6' : '#4A4F6A' }}
                    >
                      {val !== undefined && val !== null ? String(val) : '—'}
                      {isCustomer && val !== undefined && val !== null && (
                        <span className="ml-1 text-[10px]" style={{ color: '#80DEEA' }}>
                          ← used
                        </span>
                      )}
                    </td>
                  )
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Per-speaker tone from Module 1 speakers{} */}
      {speakers && Object.keys(speakers).length > 0 && (
        <div className="mt-3 pt-3" style={{ borderTop: '1px solid #2A2D3E' }}>
          <p className="text-[10px] mb-2 uppercase tracking-wider" style={{ color: '#8B90B0' }}>
            Acoustic Baseline (Module 1)
          </p>
          <div className="flex gap-6">
            {Object.entries(speakers).map(([spk, data]) => {
              const isCustomer = spk === customer_speaker_id
              return (
                <div key={spk} className="flex flex-col gap-0.5">
                  <span
                    className="text-[10px] font-bold"
                    style={{ color: isCustomer ? '#80DEEA' : '#BCAAA4' }}
                  >
                    {spk}
                  </span>
                  <span className="text-[10px]" style={{ color: '#8B90B0' }}>
                    Tone: {data.tone}
                  </span>
                  <span className="text-[10px]" style={{ color: '#8B90B0' }}>
                    Δ Energy: {data.energy_delta?.toFixed(1)}%
                  </span>
                </div>
              )
            })}
          </div>
        </div>
      )}
    </div>
  )
}
