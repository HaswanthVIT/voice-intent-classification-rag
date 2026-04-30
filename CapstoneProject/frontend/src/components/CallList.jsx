export default function CallList({ calls, selected, onSelect }) {
  const formatTime = (ts) => {
    if (!ts) return "";
    try { return new Date(ts).toLocaleString(); }
    catch { return ts; }
  };

  const intentColor = (intent) => {
    if (intent?.includes("High"))   return "text-green-400";
    if (intent?.includes("Medium")) return "text-yellow-400";
    return "text-red-400";
  };

  return (
    // ⚠️ w-full instead of w-1/4 — width is now controlled by the sidebar div in Dashboard
    <div className="w-full border-gray-800 bg-[#11131A] flex flex-col">
      <h2 className="p-4 text-lg font-bold border-b border-gray-800 sticky top-0 bg-[#11131A] z-10">
        Calls ({calls.length})
      </h2>

      {calls.length === 0 && (
        <div className="p-4 text-sm text-gray-500">No calls yet.</div>
      )}

      {calls.map((call) => (
        <div
          key={call.call_id}
          onClick={() => onSelect(call)}
          className={`p-4 cursor-pointer border-b border-gray-800 transition ${
            selected?.call_id === call.call_id
              ? "bg-blue-600"
              : "hover:bg-gray-800"
          }`}
        >
          <div className="font-semibold">{call.call_id}</div>
          <div className="text-xs text-gray-500 mt-0.5">{formatTime(call.timestamp)}</div>
          <div className={`text-xs font-medium mt-1 ${intentColor(call.intent_class)}`}>
            {call.intent_class}
          </div>
          <div className="flex gap-3 mt-1 text-xs text-gray-400">
            <span>Score: {call.intent_score?.toFixed(2)}</span>
          </div>
          <div className="flex gap-2 mt-2">
            {call.has_budget ? <span className="text-[10px] bg-green-900 text-green-300 px-1.5 py-0.5 rounded">Budget</span> : null}
            {call.has_visit  ? <span className="text-[10px] bg-blue-900 text-blue-300 px-1.5 py-0.5 rounded">Visit</span>   : null}
            {call.has_loan   ? <span className="text-[10px] bg-yellow-900 text-yellow-300 px-1.5 py-0.5 rounded">Loan</span> : null}
          </div>
        </div>
      ))}
    </div>
  );
}