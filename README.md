# 🎙️ Voice-Based AI System for Customer Intent Classification

> **CSE Capstone Project** — Post-call voice intelligence pipeline that ranks sales leads by purchase intent using Multilingual ASR, Neural Speaker Diarization, RAG-grounded LLM scoring, and a Contextual Bandit Reinforcement Learning engine.

---

## Demo Link
- https://drive.google.com/file/d/1pNBxkjgVkyRWSJBqMMoyhVS6MuVlpi9f/view?usp=sharing

---

## 📌 Problem Statement

Sales agents currently follow up with all callers uniformly, regardless of intent. This leads to:

- Wasted effort on low-intent callers
- Missed conversions with high-intent customers
- Inconsistent human judgment — especially across Indian languages and dialects (Tamil, Hindi, English)

> **Core Question Answered:** *"Who should the agent call back first — and why?"*

---

## 💡 Solution Overview

A **post-call batch analysis pipeline** that processes recorded sales calls and outputs a **ranked customer list by purchase intent**, with full human-readable reasoning for every decision.

The system answers the prioritisation question through four tightly integrated modules:

```
Raw Audio (.wav / .mp3)
        │
   ┌────▼──────────────────────────────────────────┐
   │  MODULE 1 — Audio Processing & Diarization    │
   │  Pyannote + Whisper + Dialect-Aware Tone       │
   └────┬──────────────────────────────────────────┘
        │  transcript_segments, speakers{}, customer_tone, customer_speaker_id
   ┌────▼──────────────────────────────────────────┐
   │  MODULE 2 — NLP & Behavioral Analysis         │
   │  Speaker-Aware Keywords, Sentiment, Engagement │
   └────┬──────────────────────────────────────────┘
        │  has_budget, has_loan, has_visit, speakers_nlp{}, duration_norm
   ┌────▼──────────────────────────────────────────┐
   │  MODULE 3 — RAG + Contextual Bandit RL Engine │
   │  ChromaDB + Claude LLM + PyTorch MLP Policy   │
   └────┬──────────────────────────────────────────┘
        │  intent_score, intent_class, context_scores, rl_weights_used, reasoning
   ┌────▼──────────────────────────────────────────┐
   │  MODULE 4 — Dashboard, Storage & Feedback     │
   │  SQLite + Flask REST API + React Dashboard    │
   └───────────────────────────────────────────────┘
```

---

## 🧩 Module Breakdown

### Module 1 — Audio Processing, Speaker Diarization & Tone Classification

- Accepts `.wav` / `.mp3` recorded call files
- Runs **Pyannote speaker-diarization-3.1** to split audio into per-speaker timestamped segments
- Transcribes each speaker segment independently using **OpenAI Whisper (base)** at `temperature=0`
- Detects language: `en` / `hi` / `ta`
- Applies **dialect-aware normalization** via `DIALECT_PROFILE` (Tamil: 1.2, Hindi: 1.0, English: 0.9)
- Computes a **5-second cumulative speaker-isolated energy baseline** per speaker — eliminates agent monologue contamination from the 30-second wall-clock flaw
- Outputs per-speaker `tone` (Confident / Enthusiastic / Hesitant) and `energy_delta`
- Module 1 is **role-blind** — it does not decide who the customer is

**Key Innovation:** `energy_delta = ((E_current - E_baseline) / E_baseline) × 100`

| Delta Range | Tone Label |
|---|---|
| > +20% | Enthusiastic |
| −20% to +20% | Confident |
| < −20% | Hesitant |

---

### Module 2 — NLP & Behavioral Analysis

- Runs the full NLP pipeline on **both the full transcript and per-speaker segments independently**
- Keyword detection across 6 categories: `budget`, `loan`, `visit`, `urgency`, `comparison`, `specification`
- Intentionally **fires keyword flags regardless of negation** (e.g., "no budget" → `has_budget = 1`) — context suppression is Module 3's responsibility
- Computes `keyword_norm`, `question_norm`, `duration_norm = min(duration_sec / 300, 1.0)`, and `engagement_score`
- Outputs `speakers_nlp{}` — per-speaker NLP features for customer signal isolation
- Module 2 is also **role-blind** — populates NLP features for every detected speaker

---

### Module 3 — RAG Intelligence & Contextual Bandit RL Engine

**Step 1 — RAG Retrieval:**  
Embeds full call transcript using `sentence-transformers/all-MiniLM-L6-v2` → queries ChromaDB for top-3 similar past calls and top-3 business rules.

**Step 2 — LLM Context Scoring:**  
Claude LLM performs two tasks:
- **Context Validation** — assigns `context_score` (0.0–1.0) per signal reflecting customer affirmation, inquiry, hedging, or negation
- **Holistic Scoring** — single `llm_holistic_score` based on full conversational arc (cognitive investment, urgency, comparison behavior)

**Step 3 — 15-Dimensional RL State Vector:**

| Dim | Feature | Source |
|---|---|---|
| s1–s3 | has_budget, has_loan, has_visit | Module 2 (customer-attributed) |
| s4–s5 | keyword_norm, question_norm | Module 2 |
| s6 | engagement_score | Module 2 (full-call composite) |
| s7 | tone_numeric | Module 1 customer_tone |
| s8 | sentiment_numeric | Module 2 sentiment |
| s9–s14 | ctx_budget, ctx_loan, ctx_visit, ctx_keyword, ctx_question, ctx_engagement | LLM output |
| s15 | duration_norm | Module 2 |

**Step 4 — Contextual Bandit Policy:**  
PyTorch MLP (15→64→64→6, SiLU + Softplus) maps S_t → Dirichlet α → bespoke `W_t` weights per call. Inference always uses Dirichlet **mean** — never samples — guaranteeing full determinism.

**Step 5 — Two-Layer Scoring:**

```
signal_score = Σ W_t[i] × signal[i] × context_score[i]
intent_score = 0.35 × signal_score + 0.65 × llm_holistic_score
```

**Step 6 — RL Learning (REINFORCE + KL Regularisation):**  
Reward via Intent Alignment Error: `R_effective = 1.0 − |normalized_outcome − intent_score|`  
Updates on 64-sample mini-batches from a 5,000-entry FIFO experience replay buffer.

---

### Module 4 — Dashboard, Storage & Outcome Feedback

- **Single source of truth** — exclusively owns and controls the SQLite database
- Orchestrates M1 → M2 → M3 via `run_pipeline()`
- Flask REST API with 8 endpoints covering calls, outcomes, RL learning, and pipeline execution
- Captures real agent outcomes (`converted` / `visited` / `follow_up` / `no_response` / `not_interested`) and triggers:
  1. SQLite update
  2. POST `/update_learning` → Module 3 REINFORCE gradient update
  3. `store_call_in_vectordb()` → ChromaDB for future RAG retrieval

**React Dashboard — 4 Views:**

| View | Description |
|---|---|
| Dashboard | Ranked call list with intent badges, signal breakdown bars, customer speaker tag |
| Call Detail | Speaker colour-coded transcript, per-speaker signal comparison, RL weights panel |
| Intent List | Categorical grouping — High / Medium / Low intent |
| Learning Insights | Adaptive weight chart, conversion rates, RL policy mode badge |

---

## 🎯 Intent Classification

| Intent Score | Intent Class | Business Action |
|---|---|---|
| 0.80 – 1.00 | 🟢 Very Strong | Call back immediately |
| 0.65 – 0.79 | 🟣 Strong | Call back within 24 hours |
| 0.45 – 0.64 | 🟡 Mild | Schedule when possible |
| 0.25 – 0.44 | 🔵 Very Mild | Low priority |
| 0.00 – 0.24 | 🔴 No Chance | Do not prioritise |

---

## 📊 Validation Metrics

| Metric | Target | What It Proves |
|---|---|---|
| **Decile Lift** | Top 20% calls → 60–80% of all conversions | Eliminates ~80% of wasted outbound sales effort |
| **Cohen's Kappa** | κ > 0.65 | System replicates expert human judgment, not just keyword matching |
| **Adversarial Trap Pass Rate** | 100% | System cannot be fooled by surface-level misleading signals |
| **Intent Alignment Error (IAE)** | Mean IAE < 0.20 after 50+ outcomes | RL agent actively learning and improving calibration over time |

---

## 🛡️ Adversarial Edge Cases Handled

| Trap | Input Signal | Expected System Behaviour |
|---|---|---|
| **Polite Refusal** | Positive tone + "absolutely cannot afford it now" | `ctx_budget = 0.0` → Low intent score despite positive sentiment |
| **Quiet Buyer** | Hesitant tone + highly specific EMI/spec questions | LLM reads cognitive investment → Medium-high holistic score |
| **Time-Waster** | Long call, many questions — all irrelevant to purchasing | LLM scrutinises question relevance → Low holistic score |
| **Agent Monologue** | Agent speaks first 45s before customer says a word | Pyannote waits; cumulative baseline accumulates only customer voice |

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Automatic Speech Recognition | OpenAI Whisper (base), `temperature=0` |
| Speaker Diarization | Pyannote audio 3.1.1 (HuggingFace) |
| Acoustic Feature Extraction | Librosa |
| NLP / Sentiment | NLTK VADER (TextBlob fallback) |
| Vector Database | ChromaDB (PersistentClient, local) |
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 |
| LLM Context Scoring | Claude claude-sonnet-4-20250514 (Anthropic API), `temperature=0` |
| RL Policy Network | PyTorch MLP + Dirichlet distribution |
| Storage | SQLite |
| Backend API | Flask |
| Frontend Framework | React 18 + Vite |
| Styling | Tailwind CSS (dark mode) |
| Charts | Recharts |
| HTTP Client | Axios |
| Routing | React Router v6 |

---

## 📁 Project Structure

```
voice-intent-classification-rag/
├── CapstoneProject/
│   ├── module1/
│   │   ├── audio_processor.py       # Main entry: process_audio()
│   │   ├── diarizer.py              # Pyannote pipeline + segment merging
│   │   ├── asr.py                   # Per-speaker Whisper transcription
│   │   ├── feature_extractor.py     # Pitch, speech rate, pause ratio
│   │   ├── dialect_normalizer.py    # DIALECT_PROFILE energy normalization
│   │   ├── speaker_isolator.py      # 5s cumulative baseline per speaker
│   │   ├── tone_classifier.py       # Delta-based tone classification
│   │   ├── validator.py
│   │   └── storage.py
│   │
│   ├── module2/
│   │   ├── nlp_processor.py         # Main entry: process_text()
│   │   ├── keyword_extractor.py     # KEYWORD_DICT + binary flag detection
│   │   ├── question_detector.py
│   │   ├── sentiment_analyzer.py    # VADER + TextBlob fallback
│   │   ├── engagement_scorer.py
│   │   ├── speaker_nlp.py           # Per-speaker NLP extraction
│   │   └── normalizer.py
│   │
│   ├── module3/
│   │   ├── intent_engine.py         # Main entry: process_intent()
│   │   ├── rag_retriever.py         # ChromaDB retrieval + storage
│   │   ├── llm_client.py            # Claude API + fallback scoring
│   │   ├── scorer.py                # State vector + signal + intent score
│   │   ├── classifier.py            # classify_intent()
│   │   ├── rl_agent.py              # IntentPolicyNetwork + Dirichlet weights
│   │   ├── learning.py              # REINFORCE + IAE reward + buffer
│   │   ├── prompts.py               # SYSTEM_PROMPT + prompt assembly
│   │   ├── rl_policy.pt             # Saved PyTorch policy weights
│   │   └── experience_buffer.json   # FIFO replay buffer (max 5,000 entries)
│   │
│   ├── module4/
│   │   ├── app.py                   # Flask app — registers all routes
│   │   ├── db_handler.py            # SQLite schema + store_result()
│   │   ├── outcome_handler.py       # update_outcome() + RL trigger
│   │   ├── orchestrator.py          # run_pipeline(): M1→M2→M3
│   │   ├── api_client.py            # HTTP calls to Module 3
│   │   ├── insights.py              # /learning_summary + /performance
│   │   └── routes/
│   │       ├── calls.py
│   │       ├── outcome.py
│   │       ├── learning.py
│   │       ├── pipeline.py
│   │       └── call_data.py
│   │
│   ├── frontend/
│   │   └── src/
│   │       ├── components/
│   │       │   ├── Dashboard.jsx
│   │       │   ├── CallCard.jsx
│   │       │   ├── CallDetailView.jsx
│   │       │   ├── TranscriptTab.jsx        # Speaker colour-coded rendering
│   │       │   ├── SignalsTab.jsx
│   │       │   ├── SpeakerComparison.jsx    # Per-speaker NLP signal table
│   │       │   ├── RLWeightsPanel.jsx       # rl_weights_used bar chart
│   │       │   ├── InsightsPanel.jsx        # Policy mode badge + weight chart
│   │       │   ├── IntentList.jsx
│   │       │   ├── OutcomeSubmitter.jsx
│   │       │   └── IntentBadge.jsx
│   │       └── api/
│   │           └── client.js                # Axios instance (Vite proxy /api)
│   │
│   └── data/
│       ├── calls.db                         # SQLite database
│       ├── audio/                           # Stored call audio files
│       └── chromadb/                        # ChromaDB vector store
│           ├── past_calls/
│           └── business_rules/
│
├── .gitignore
└── README.md
```

---

## 🚀 Setup & Installation

### Prerequisites

- Python 3.10+
- Node.js 18+
- A HuggingFace account with access granted to `pyannote/speaker-diarization-3.1`
- An Anthropic API key

### 1. Clone the Repository

```bash
git clone https://github.com/HaswanthVIT/voice-intent-classification-rag.git
cd voice-intent-classification-rag/CapstoneProject
```

### 2. Backend — Python Environment

```bash
pip install -r requirements.txt
```

**`requirements.txt`**
```
pyannote.audio==3.1.1
openai-whisper
librosa>=0.10.0
soundfile
torch>=2.0.0
numpy
nltk
vaderSentiment
textblob
chromadb>=0.4.0
sentence-transformers
anthropic
flask
python-dotenv
requests
```

One-time NLTK download:
```bash
python -c "import nltk; nltk.download('vader_lexicon')"
```

### 3. Environment Variables

Create a `.env` file inside `CapstoneProject/module1/` and `CapstoneProject/module3/`:

```env
# module1/.env
HF_TOKEN=hf_your_huggingface_token_here

# module3/.env
ANTHROPIC_API_KEY=sk-ant-your_anthropic_key_here
```

> ⚠️ **Never commit `.env` files.** Both are listed in `.gitignore`.

### 4. HuggingFace Model Setup

1. Create an account at [huggingface.co](https://huggingface.co)
2. Accept the model terms at: `https://huggingface.co/pyannote/speaker-diarization-3.1`
3. Generate a token at: `https://huggingface.co/settings/tokens`
4. Add the token to `module1/.env` as `HF_TOKEN`

### 5. Load Business Rules into ChromaDB

```bash
python module3/rag_retriever.py --load-rules data/business_rules.json
```

### 6. Frontend — React

```bash
cd frontend
npm install
npm run dev
```

The Vite dev server proxies `/api` → `http://localhost:5000` (Flask backend).

### 7. Start the Flask Backend

```bash
python module4/app.py
```

---

## 🔌 REST API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/calls` | All calls sorted by `intent_score DESC` |
| `GET` | `/calls/{call_id}` | Full record — all fields including speaker and RL data |
| `GET` | `/calls/{call_id}/intent` | Intent score, class, confidence, reasoning |
| `GET` | `/call_data/{call_id}` | Customer-attributed signals for Module 3 RL update |
| `POST` | `/outcome` | Submit agent outcome → triggers RL update + ChromaDB storage |
| `GET` | `/learning_summary` | Rolling weight averages, conversion rates, policy mode |
| `GET` | `/performance` | Conversion rates grouped by intent class |
| `POST` | `/run_pipeline` | Run full pipeline on an audio file |

**Allowed outcome values:** `converted` · `visited` · `follow_up` · `no_response` · `not_interested`

---

## 🔁 RL Feedback Loop

```
Agent submits outcome via Dashboard
             │
   Step 1 → SQLite: SET outcome = ?
             │
   Step 2 → POST /update_learning (Module 3)
             │   Computes IAE reward
             │   REINFORCE on 64-sample mini-batch
             │   Saves rl_policy.pt
             │
   Step 3 → store_call_in_vectordb()
             │   Call transcript + metadata → ChromaDB past_calls
             │   Available as RAG evidence for future calls
```

**Reward Function (IAE):**

```
R_effective = 1.0 − |normalized_outcome − intent_score|
```

| Outcome | Normalized Value |
|---|---|
| converted | 1.00 |
| visited | 0.85 |
| follow_up | 0.65 |
| no_response | 0.45 |
| not_interested | 0.25 |

---

## 🎨 UI Design System

All four dashboard views use a consistent dark mode token set:

| Token | Hex | Usage |
|---|---|---|
| bg-base | `#0D0F14` | Page background |
| bg-surface | `#151820` | Card/panel background |
| neon-green | `#69F0AE` | Very Strong intent badge |
| neon-purple | `#CE93D8` | Strong intent badge |
| neon-amber | `#FFD740` | Mild intent + highlights |
| neon-blue | `#4FC3F7` | Very Mild + links |
| neon-red | `#FF5252` | No Chance + errors |
| speaker-customer | `#80DEEA` | Customer turn highlight in Transcript tab |
| speaker-agent | `#BCAAA4` | Agent turn highlight in Transcript tab |

---

## 🧪 Capstone Defense Checklist

- [ ] Decile Lift computed on 100 labelled calls (Cumulative Gains chart prepared)
- [ ] Cohen's Kappa computed against 2–3 human raters on 30–50 transcripts
- [ ] Adversarial Trap Pass Rate tested on 10–15 designed trap transcripts
- [ ] IAE before/after RL plotted across 50+ outcome submissions
- [ ] KL divergence tracked — regularised vs. unregularised comparison prepared
- [ ] Speaker Attribution Accuracy verified (≥ 85% target on 10–15 test calls)
- [ ] Baseline Delta Stability verified across 3 runs (variance < 0.5 pp)

---

## ❓ Why This Architecture?

**Why RAG?**  
A static script sees "budget" in "I don't have a budget" and incorrectly scores intent high. The RAG-powered LLM understands narrative context and assigns `context_score = 0.0` to suppress negated signals.

**Why Contextual Bandit (not DQN/PPO)?**  
Each sales call is an independent episode — scoring Call A has zero effect on Call B's state. A Contextual Bandit is the mathematically correct formulation for this stateless, per-episode optimization problem.

**Why Dirichlet Distribution (not Gaussian)?**  
The 6 RL output weights must proportionally sum to 0.95 (a simplex constraint). Independent Gaussian outputs cannot enforce this. The Dirichlet distribution is the mathematically correct distribution for proportional allocations.

**Why 65% LLM / 35% Signal Score?**  
Purchase intent lives in the narrative arc — progressive engagement, implicit urgency, subtle negation — none of which keyword flags alone can capture. The 65/35 split grounds LLM judgment in verifiable evidence while prioritising contextual understanding.

**Why Experience Replay?**  
Updating the policy on a single sample (batch size = 1) causes highly unstable gradient descent and catastrophic forgetting. The 5,000-entry FIFO buffer with 64-sample mini-batches ensures stable, diverse gradient updates.

---

## 📄 License

This project was developed as a CSE Final Year Capstone Project. All components are intended for academic and educational purposes.

---

## 👥 Contributors

- Naman Agrawal
- Nitharshana BR
- S Haswanth

