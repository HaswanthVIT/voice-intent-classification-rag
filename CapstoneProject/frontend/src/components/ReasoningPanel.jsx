export default function ReasoningPanel({ call }) {
  if (!call) return null;

  return (
    <div className="p-4">

      <h3 className="text-lg mb-3">Reasoning</h3>

      <ul className="text-sm space-y-2">
        {(call.reasoning || []).map((r, i) => (
          <li key={i}>• {r}</li>
        ))}
      </ul>

      <h4 className="mt-4 mb-2">Learning Insights</h4>

      <ul className="text-sm space-y-2">
        {(call.learning_insight || []).map((r, i) => (
          <li key={i}>• {r}</li>
        ))}
      </ul>

    </div>
  );
}