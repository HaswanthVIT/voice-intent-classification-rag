/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Module 4 Section 7.2 — Dark Mode Design Tokens
        'bg-base':        '#0D0F14',
        'bg-surface':     '#151820',
        'bg-elevated':    '#1E2130',
        'border-subtle':  '#2A2D3E',
        'text-primary':   '#E8EAF6',
        'text-secondary': '#8B90B0',
        'neon-blue':      '#4FC3F7',
        'neon-green':     '#69F0AE',
        'neon-amber':     '#FFD740',
        'neon-red':       '#FF5252',
        'neon-purple':    '#CE93D8',
        // Module 4 Section 7.2 — NEW speaker tokens
        'speaker-customer': '#80DEEA',
        'speaker-agent':    '#BCAAA4',
      },
      fontFamily: {
        mono: ['"JetBrains Mono"', '"Fira Code"', 'Consolas', 'monospace'],
        sans: ['"DM Sans"', 'system-ui', 'sans-serif'],
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'fade-in':    'fadeIn 0.3s ease-out',
        'slide-up':   'slideUp 0.3s ease-out',
      },
      keyframes: {
        fadeIn:  { from: { opacity: 0 }, to: { opacity: 1 } },
        slideUp: { from: { opacity: 0, transform: 'translateY(8px)' }, to: { opacity: 1, transform: 'translateY(0)' } },
      }
    },
  },
  plugins: [],
}
