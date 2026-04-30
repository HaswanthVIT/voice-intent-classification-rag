export default function RLPanel({ call }) {
  if (!call) return null;

  const weights = call.rl_weights_used || {};
  if (Object.keys(weights).length === 0) return null;

  return (
    <div className="bg-[#1A1D26] p-4 rounded-lg">
      <div className="text-xs text-gray-400 mb-3">RL Weights</div>
      <div className="space-y-2">
        {Object.entries(weights).map(([k, v]) => (
          <div key={k}>
            <div className="flex justify-between text-xs text-gray-300">
              <span className="capitalize">{k}</span>
              <span>{Number(v).toFixed(3)}</span>
            </div>
            <div className="bg-[#2A2D3E] h-2 rounded mt-1">
              <div
                className="bg-[#CE93D8] h-2 rounded transition-all"
                style={{ width: `${Math.min(v * 100, 100)}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}