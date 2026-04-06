import { Routes, Route, Navigate } from 'react-router-dom'
import Navbar from './components/Navbar'
import Dashboard from './views/Dashboard'
import CallDetail from './views/CallDetail'
import IntentList from './views/IntentList'
import InsightsPanel from './views/InsightsPanel'

export default function App() {
  return (
    <div className="min-h-screen" style={{ background: '#0D0F14' }}>
      <Navbar />
      <Routes>
        <Route path="/"            element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard"   element={<Dashboard />} />
        <Route path="/calls/:id"   element={<CallDetail />} />
        <Route path="/intent-list" element={<IntentList />} />
        <Route path="/insights"    element={<InsightsPanel />} />
      </Routes>
    </div>
  )
}
