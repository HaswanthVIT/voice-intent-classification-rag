import { useEffect, useState } from "react";
import { fetchCalls } from "../api/api";
import CallList from "../components/CallList";
import TranscriptView from "../components/TranscriptView";
import InsightsPanel from "../components/InsightsPanel";
import UploadPanel from "../components/UploadPanel";

export default function Dashboard() {
  const [calls, setCalls]       = useState([]);
  const [selected, setSelected] = useState(null);
  const [loading, setLoading]   = useState(true);
  const [error, setError]       = useState(null);

  useEffect(() => { load(); }, []);

  const safeParse = (val, def) => {
    try {
      if (!val) return def;
      if (typeof val === "object") return val;
      return JSON.parse(val);
    } catch { return def; }
  };

  const normalize = (call) => ({
    ...call,
    reasoning:           safeParse(call.reasoning, []),
    learning_insight:    safeParse(call.learning_insight, []),
    evidence_refs:       safeParse(call.evidence_refs, []),
    transcript_segments: safeParse(call.transcript_segments, []),
    state_vector:        safeParse(call.state_vector, []),
    context_scores:      safeParse(call.context_scores, {}),
    rl_weights_used:     safeParse(call.rl_weights_used, {}),
    has_budget:   Number(call.has_budget  ?? 0),
    has_loan:     Number(call.has_loan    ?? 0),
    has_visit:    Number(call.has_visit   ?? 0),
    intent_score: parseFloat(call.intent_score ?? 0),
    signal_score: parseFloat(call.signal_score ?? 0),
    confidence:   parseFloat(call.confidence   ?? 0),
    transcript:   call.transcript || "",
  });

  const load = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await fetchCalls();
      const cleaned = Array.isArray(data) ? data.map(normalize) : [];
      setCalls(cleaned);
      if (cleaned.length > 0) setSelected(cleaned[0]);
    } catch (err) {
      console.error("Failed to load calls:", err);
      setError("Failed to load calls. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  // Re-fetch after pipeline finishes and auto-select the newest call
  const handleProcessingDone = async () => {
    try {
      const data = await fetchCalls();
      const cleaned = Array.isArray(data) ? data.map(normalize) : [];
      setCalls(cleaned);
      if (cleaned.length > 0) setSelected(cleaned[cleaned.length - 1]);
    } catch (err) {
      console.error("Refresh failed:", err);
    }
  };

  if (loading) return (
    <div className="flex h-screen items-center justify-center bg-[#0D0F14] text-white text-lg">
      Loading calls...
    </div>
  );

  if (error) return (
    <div className="flex h-screen items-center justify-center bg-[#0D0F14] text-red-400 text-lg">
      {error}
    </div>
  );

  return (
    <div className="flex h-screen bg-[#0D0F14] text-white overflow-hidden">

      {/* Left sidebar — upload panel on top, call list scrolls below */}
      <div className="w-1/4 flex flex-col border-r border-gray-800 bg-[#11131A] overflow-hidden">
        <UploadPanel onProcessingDone={handleProcessingDone} />
        <div className="flex-1 overflow-y-auto">
          <CallList calls={calls} selected={selected} onSelect={setSelected} />
        </div>
      </div>

      <TranscriptView call={selected} />
      <InsightsPanel call={selected} />
    </div>
  );
}