// src/api/client.js
// All API calls MUST use this instance — never raw fetch()
// Uses Vite proxy: /api → http://localhost:5000
//
// MOCK MODE: set VITE_USE_MOCK=true in .env.local to bypass Flask entirely.

import axios from 'axios'
import {
  MOCK_CALLS,
  MOCK_LEARNING_SUMMARY,
  MOCK_PERFORMANCE,
} from './mockData'

// ── Mock adapter ─────────────────────────────────────────────────────────────
const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true'

function mockResponse(data, delay = 350) {
  return new Promise(resolve =>
    setTimeout(() => resolve({ data }), delay)
  )
}

// Simulated outcome store so the UI feedback works in mock mode
const mockOutcomes = {}

function handleMock(method, url, body) {
  // GET /calls
  if (method === 'get' && url === '/calls') {
    const sorted = [...MOCK_CALLS].sort((a, b) => b.intent_score - a.intent_score)
    // Apply any stored outcomes
    const patched = sorted.map(c => ({
      ...c,
      outcome: mockOutcomes[c.call_id] ?? c.outcome,
    }))
    return mockResponse(patched)
  }

  // GET /calls/:id
  if (method === 'get' && url.startsWith('/calls/')) {
    const id   = url.split('/calls/')[1]
    const call = MOCK_CALLS.find(c => c.call_id === id)
    if (!call) return Promise.reject({ message: `Call ${id} not found`, status: 404 })
    return mockResponse({ ...call, outcome: mockOutcomes[id] ?? call.outcome })
  }

  // POST /outcome
  if (method === 'post' && url === '/outcome') {
    const { call_id, outcome } = body
    const ALLOWED = ['converted', 'visited', 'follow_up', 'no_response', 'not_interested']
    if (!ALLOWED.includes(outcome)) {
      return Promise.reject({ message: `Invalid outcome: ${outcome}`, status: 400 })
    }
    mockOutcomes[call_id] = outcome
    console.log(`[MOCK] Outcome stored: ${call_id} → ${outcome}`)
    return mockResponse({ status: 'success', call_id, outcome })
  }

  // GET /learning_summary
  if (method === 'get' && url === '/learning_summary') {
    return mockResponse(MOCK_LEARNING_SUMMARY)
  }

  // GET /performance
  if (method === 'get' && url === '/performance') {
    return mockResponse(MOCK_PERFORMANCE)
  }

  return Promise.reject({ message: `No mock handler for ${method.toUpperCase()} ${url}`, status: 501 })
}

// ── Real Axios client ─────────────────────────────────────────────────────────
const axiosClient = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
  timeout: 30000,
})

axiosClient.interceptors.response.use(
  res => res,
  err => {
    const msg = err.response?.data?.message || err.message || 'Unknown error'
    console.error('[API Error]', msg)
    return Promise.reject({ message: msg, status: err.response?.status })
  }
)

// ── Unified client facade ─────────────────────────────────────────────────────
const client = {
  get:  (url, config)       => USE_MOCK ? handleMock('get',  url, null) : axiosClient.get(url, config),
  post: (url, data, config) => USE_MOCK ? handleMock('post', url, data) : axiosClient.post(url, data, config),
}

export default client
