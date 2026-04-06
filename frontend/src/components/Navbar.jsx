// src/components/Navbar.jsx
import { NavLink } from 'react-router-dom'
import { Cpu, LayoutDashboard, List, TrendingUp } from 'lucide-react'

const LINKS = [
  { to: '/dashboard',   label: 'Dashboard',   icon: LayoutDashboard },
  { to: '/intent-list', label: 'Intent List',  icon: List },
  { to: '/insights',    label: 'Insights',     icon: TrendingUp },
]

export default function Navbar() {
  return (
    <nav
      className="sticky top-0 z-50 flex items-center justify-between px-6 h-14 border-b"
      style={{ background: '#0D0F14', borderColor: '#2A2D3E' }}
    >
      {/* Brand */}
      <div className="flex items-center gap-2">
        <Cpu size={18} style={{ color: '#4FC3F7' }} />
        <span
          className="font-mono text-sm font-bold tracking-widest uppercase"
          style={{ color: '#E8EAF6' }}
        >
          IntentLoop Pro
        </span>
      </div>

      {/* Nav links */}
      <div className="flex items-center gap-1">
        {LINKS.map(({ to, label, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `flex items-center gap-1.5 px-4 py-1.5 rounded text-xs font-medium transition-colors duration-150 ${
                isActive
                  ? 'text-[#E8EAF6] bg-[#1E2130]'
                  : 'text-[#8B90B0] hover:text-[#E8EAF6] hover:bg-[#1E2130]'
              }`
            }
          >
            <Icon size={13} />
            {label}
          </NavLink>
        ))}
      </div>

      {/* Pipeline status */}
      <div className="flex items-center gap-2">
        <span className="w-2 h-2 rounded-full bg-[#69F0AE] animate-pulse-slow" />
        <span className="font-mono text-xs text-[#8B90B0] tracking-widest uppercase">
          Pipeline Active
        </span>
      </div>
    </nav>
  )
}
