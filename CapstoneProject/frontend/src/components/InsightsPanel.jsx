import RLPanel from "./RLPanel";
import ReasoningPanel from "./ReasoningPanel";

export default function InsightsPanel({ call }) {
  if (!call) {
    return (
      <div className="w-1/4 p-6 bg-[#11131A] flex items-center justify-center text-gray-500">
        No insights
      </div>
    );
  }

  const intentColor = (intent) => {
    if (intent?.includes("High"))   return "text-green-400";
    if (intent?.includes("Medium")) return "text-yellow-400";
    return "text-red-400";
  };

  const scoreBar = (val) => (
    <div className="bg-[#2A2D3E] h-2 rounded mt-1">
      <div
        className="bg-blue-500 h-2 rounded transition-all"
        style={{ width: `${Math.min((val ?? 0) * 100, 100)}%` }}
      />
    </div>
  );

  const contextScores = call.context_scores || {};

  return (
    <div className="w-1/4 bg-[#11131A] border-l border-gray-800 overflow-y-auto flex flex-col">
      <h2 className="p-4 text-lg font-bold border-b border-gray-800 sticky top-0 bg-[#11131A] z-10">
        Insights
      </h2>

      <div className="p-4 space-y-4">

        {/* Intent */}
        <div className="bg-[#1A1D26] p-4 rounded-lg">
          <div className="text-xs text-gray-400 mb-1">Intent Class</div>
          <div className={`text-xl font-bold ${intentColor(call.intent_class)}`}>
            {call.intent_class || "—"}
          </div>
        </div>

        {/* Scores */}
        <div className="bg-[#1A1D26] p-4 rounded-lg space-y-3">
          <div>
            <div className="flex justify-between text-xs text-gray-400">
              <span>Intent Score</span>
              <span>{call.intent_score?.toFixed(3)}</span>
            </div>
            {scoreBar(call.intent_score)}
          </div>
          <div>
            <div className="flex justify-between text-xs text-gray-400">
              <span>Signal Score</span>
              <span>{call.signal_score?.toFixed(3)}</span>
            </div>
            {scoreBar(call.signal_score)}
          </div>
        </div>

        {/* Signal Flags */}
        <div className="bg-[#1A1D26] p-4 rounded-lg">
          <div className="text-xs text-gray-400 mb-2">Signal Flags</div>
          <div className="flex gap-2 flex-wrap">
            <span className={`text-xs px-2 py-1 rounded ${call.has_budget ? "bg-green-900 text-green-300" : "bg-gray-800 text-gray-500"}`}>
              {call.has_budget ? "✓" : "✗"} Budget
            </span>
            <span className={`text-xs px-2 py-1 rounded ${call.has_visit ? "bg-blue-900 text-blue-300" : "bg-gray-800 text-gray-500"}`}>
              {call.has_visit ? "✓" : "✗"} Visit
            </span>
            <span className={`text-xs px-2 py-1 rounded ${call.has_loan ? "bg-yellow-900 text-yellow-300" : "bg-gray-800 text-gray-500"}`}>
              {call.has_loan ? "✓" : "✗"} Loan
            </span>
          </div>
        </div>

        {/* Context Scores */}
        {Object.keys(contextScores).length > 0 && (
          <div className="bg-[#1A1D26] p-4 rounded-lg">
            <div className="text-xs text-gray-400 mb-3">Context Scores</div>
            <div className="space-y-2">
              {Object.entries(contextScores).map(([k, v]) => (
                <div key={k}>
                  <div className="flex justify-between text-xs text-gray-300">
                    <span className="capitalize">{k}</span>
                    <span>{Number(v).toFixed(2)}</span>
                  </div>
                  {scoreBar(v)}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* RL Weights */}
        <RLPanel call={call} />

        {/* Reasoning + Learning */}
        <ReasoningPanel call={call} />

      </div>
    </div>
  );
}