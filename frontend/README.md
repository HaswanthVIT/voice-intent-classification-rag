# Module 4 — Frontend Setup Guide
# Voice-Based AI System for Customer Intent Classification

## Complete File Structure

```
frontend/
├── index.html                        ← Entry HTML, loads Google Fonts
├── package.json                      ← All dependencies
├── vite.config.js                    ← Vite + /api proxy to Flask :5000
├── tailwind.config.js                ← All Module 4 design tokens (Section 7.2)
├── postcss.config.js
│
└── src/
    ├── main.jsx                      ← React root, wraps BrowserRouter
    ├── App.jsx                       ← Route definitions (4 views)
    ├── index.css                     ← Global CSS variables + base styles
    │
    ├── api/
    │   └── client.js                 ← Axios instance (ALL calls use this)
    │
    ├── components/
    │   ├── Navbar.jsx                ← Top nav: Dashboard / Intent List / Insights
    │   ├── IntentBadge.jsx           ← Section 7.3 exact color mapping
    │   ├── SignalBar.jsx             ← Single bar + SignalBreakdown (6-bar grid)
    │   ├── Spinner.jsx               ← Loading state
    │   ├── CallCard.jsx              ← Section 8.1 + customer_speaker_id tag (NEW)
    │   ├── MiniCallCard.jsx          ← Intent List compact row
    │   ├── OutcomeSubmitter.jsx      ← Section 9.6 — POST /outcome
    │   ├── TranscriptTab.jsx         ← Section 9.2 — speaker colour-coded (NEW)
    │   ├── SignalsTab.jsx            ← Section 9.3 — extended (NEW panels)
    │   ├── SpeakerComparison.jsx     ← Section 9.4 — NEW
    │   ├── RLWeightsPanel.jsx        ← Section 9.5 — NEW
    │   └── PolicyModeBadge.jsx       ← Section 11 — NEW
    │
    └── views/
        ├── Dashboard.jsx             ← View 1 — Section 8
        ├── CallDetail.jsx            ← View 2 — Section 9
        ├── IntentList.jsx            ← View 3 — Section 10
        └── InsightsPanel.jsx         ← View 4 — Section 11
```

## Setup Steps

```bash
# 1. Navigate to frontend folder
cd frontend

# 2. Install all dependencies
npm install

# 3. Start dev server (Flask must be running on :5000)
npm run dev

# Frontend runs at: http://localhost:5173
# API calls proxy:  /api/calls → http://localhost:5000/calls
```

## Routes

| URL                  | View            | Section |
|----------------------|-----------------|---------|
| /dashboard           | Dashboard       | 8       |
| /calls/:call_id      | Call Detail     | 9       |
| /intent-list         | Intent List     | 10      |
| /insights            | Insights Panel  | 11      |

## API Endpoints the Frontend Calls

| Method | Endpoint                    | Used In          |
|--------|-----------------------------|------------------|
| GET    | /calls                      | Dashboard        |
| GET    | /calls/:id                  | CallDetail       |
| POST   | /outcome                    | OutcomeSubmitter |
| GET    | /learning_summary           | InsightsPanel    |
| GET    | /performance                | InsightsPanel    |

## Key Design Rules (enforced in code)

- ALL API calls go through `src/api/client.js` — never raw fetch()
- NEVER hardcode Flask URL — always use /api Vite proxy
- Scores: toFixed(2) | Weights: toFixed(3) — everywhere
- All 4 views handle loading + error + empty states
- SpeakerComparison, RLWeightsPanel, TranscriptTab all degrade gracefully when
  diarization data (speakers_nlp, transcript_segments) is NULL
- Intent badge colors match Section 7.3 exactly
- speaker-customer (#80DEEA) and speaker-agent (#BCAAA4) tokens in Tailwind config

## Flask Backend — /performance Endpoint Expected Shape

The InsightsPanel expects GET /performance to return:
```json
[
  { "intent_class": "Very Strong", "conversion_rate": 0.85, "call_count": 34 },
  { "intent_class": "Strong",      "conversion_rate": 0.60, "call_count": 89 },
  { "intent_class": "Mild",        "conversion_rate": 0.25, "call_count": 72 },
  { "intent_class": "Very Mild",   "conversion_rate": 0.08, "call_count": 41 },
  { "intent_class": "No Chance",   "conversion_rate": 0.02, "call_count": 12 }
]
```
