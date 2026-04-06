// src/components/IntentBadge.jsx
// Implements Section 7.3 intent badge color mapping EXACTLY

const BADGE_MAP = {
  'Very Strong': { bg: '#69F0AE', text: '#0D0F14', msg: 'Call back immediately' },
  'Strong':      { bg: '#CE93D8', text: '#0D0F14', msg: 'Call back within 24hrs' },
  'Mild':        { bg: '#FFD740', text: '#0D0F14', msg: 'Schedule when possible' },
  'Very Mild':   { bg: '#4FC3F7', text: '#0D0F14', msg: 'Low priority' },
  'No Chance':   { bg: '#FF5252', text: '#0D0F14', msg: 'Do not prioritise' },
}

export default function IntentBadge({ intent, showMsg = false, size = 'md' }) {
  const config = BADGE_MAP[intent] || { bg: '#2A2D3E', text: '#8B90B0', msg: '' }
  const px = size === 'sm' ? 'px-2 py-0.5 text-[10px]' : 'px-3 py-1 text-xs'

  return (
    <span className="inline-flex flex-col items-start gap-0.5">
      <span
        className={`${px} rounded font-mono font-bold uppercase tracking-wide`}
        style={{ background: config.bg, color: config.text }}
      >
        {intent || 'Unknown'}
      </span>
      {showMsg && (
        <span className="text-[10px]" style={{ color: '#8B90B0' }}>
          {config.msg}
        </span>
      )}
    </span>
  )
}

// Export raw config for border/color usage elsewhere
export const INTENT_COLORS = BADGE_MAP
