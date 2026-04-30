export default function TranscriptView({ call }) {
  if (!call) {
    return (
      <div className="w-2/4 p-6 flex items-center justify-center text-gray-500">
        No call selected
      </div>
    );
  }

  const segments = call.transcript_segments || [];
  const hasSegments = segments.length > 0;

  const isCustomer = (speaker) => speaker === call.customer_speaker_id;

  const formatTime = (sec) => {
    if (sec == null) return "";
    const m = Math.floor(sec / 60);
    const s = Math.floor(sec % 60);
    return `${m}:${s.toString().padStart(2, "0")}`;
  };

  return (
    <div className="w-2/4 flex flex-col border-r border-gray-800 overflow-hidden">

      {/* Header */}
      <div className="p-4 border-b border-gray-800 bg-[#11131A] sticky top-0 z-10">
        <h2 className="text-lg font-bold">Transcript</h2>
        {call.customer_speaker_id && (
          <div className="flex gap-6 mt-1 text-xs">
            <span className="text-blue-400">● Customer ({call.customer_speaker_id})</span>
            <span className="text-purple-400">● Sales Agent</span>
          </div>
        )}
      </div>

      {/* Chat area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {hasSegments ? (
          segments.map((seg, i) => {
            const customer = isCustomer(seg.speaker);
            return (
              <div
                key={i}
                className={`flex flex-col ${customer ? "items-start" : "items-end"}`}
              >
                {/* Speaker label + time */}
                <div className={`flex items-center gap-2 mb-1 text-xs text-gray-500 ${customer ? "flex-row" : "flex-row-reverse"}`}>
                  <span className={customer ? "text-blue-400" : "text-purple-400"}>
                    {customer ? "Customer" : "Sales"}
                  </span>
                  <span>{formatTime(seg.start)}</span>
                </div>

                {/* Bubble */}
                <div
                  className={`max-w-[75%] px-4 py-2.5 rounded-2xl text-sm leading-relaxed ${
                    customer
                      ? "bg-[#1E3A5F] text-blue-100 rounded-tl-sm"
                      : "bg-[#2D1B4E] text-purple-100 rounded-tr-sm"
                  }`}
                >
                  {seg.text}
                </div>
              </div>
            );
          })
        ) : (
          // Fallback plain text
          <div className="bg-[#1A1D26] p-4 rounded-lg text-sm text-gray-300 leading-relaxed whitespace-pre-wrap">
            {call.transcript || "No transcript available."}
          </div>
        )}
      </div>

    </div>
  );
}