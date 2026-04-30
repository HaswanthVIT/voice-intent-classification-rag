import { useRef, useState } from "react";
import { uploadFile, processFile } from "../api/api";

const ACCEPTED = ".mp4,.mp3,.wav,.m4a,.webm";

const STATUS = {
  IDLE:       "idle",
  UPLOADING:  "uploading",
  PROCESSING: "processing",
  DONE:       "done",
  ERROR:      "error",
};

export default function UploadPanel({ onProcessingDone }) {
  const inputRef                = useRef(null);
  const [file, setFile]         = useState(null);
  const [status, setStatus]     = useState(STATUS.IDLE);
  const [message, setMessage]   = useState("");
  const [dragging, setDragging] = useState(false);

  const handleFile = (f) => {
    if (!f) return;
    setFile(f);
    setStatus(STATUS.IDLE);
    setMessage("");
  };

  const onDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    handleFile(e.dataTransfer.files[0]);
  };

  const handleProcess = async () => {
    if (!file) return;
    try {
      // Step 1 — upload
      setStatus(STATUS.UPLOADING);
      setMessage("Uploading file...");
      const { file_path } = await uploadFile(file);

      // Step 2 — run pipeline
      setStatus(STATUS.PROCESSING);
      setMessage("Running pipeline... this may take a few minutes.");
      const result = await processFile(file_path);

      setStatus(STATUS.DONE);
      setMessage(`✓ Done! Call ID: ${result.call_id} · ${result.intent_class}`);
      setFile(null);
      if (inputRef.current) inputRef.current.value = "";

      if (onProcessingDone) onProcessingDone();

    } catch (err) {
      console.error(err);
      setStatus(STATUS.ERROR);
      setMessage(err.message || "Something went wrong.");
    }
  };

  const reset = () => {
    setFile(null);
    setStatus(STATUS.IDLE);
    setMessage("");
    if (inputRef.current) inputRef.current.value = "";
  };

  const isProcessing = status === STATUS.UPLOADING || status === STATUS.PROCESSING;

  return (
    <div className="p-4 border-b border-gray-800 shrink-0">
      <div className="text-xs font-semibold text-gray-400 uppercase tracking-widest mb-3">
        Process New Call
      </div>

      {/* Drop zone */}
      <div
        onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
        onDragLeave={() => setDragging(false)}
        onDrop={onDrop}
        onClick={() => !isProcessing && inputRef.current?.click()}
        className={[
          "border-2 border-dashed rounded-lg p-4 text-center transition",
          isProcessing             ? "opacity-50 cursor-not-allowed" : "cursor-pointer",
          dragging                 ? "border-blue-400 bg-blue-900/20" : "",
          file && !dragging        ? "border-blue-600 bg-blue-900/10" : "",
          !file && !dragging       ? "border-gray-700 hover:border-gray-500" : "",
        ].join(" ")}
      >
        <input
          ref={inputRef}
          type="file"
          accept={ACCEPTED}
          className="hidden"
          onChange={(e) => handleFile(e.target.files[0])}
          disabled={isProcessing}
        />

        {file ? (
          <>
            <div className="text-blue-300 text-sm font-medium truncate">{file.name}</div>
            <div className="text-gray-500 text-xs mt-1">
              {(file.size / 1024 / 1024).toFixed(1)} MB
            </div>
          </>
        ) : (
          <>
            <div className="text-2xl mb-1">🎙️</div>
            <div className="text-gray-400 text-xs">Drop a file or click to browse</div>
            <div className="text-gray-600 text-xs mt-1">mp4 · mp3 · wav · m4a</div>
          </>
        )}
      </div>

      {/* Status message */}
      {message && (
        <div className={`mt-2 text-xs px-2 py-1.5 rounded flex items-center gap-2 ${
          status === STATUS.ERROR ? "bg-red-900/40 text-red-300"
          : status === STATUS.DONE  ? "bg-green-900/40 text-green-300"
          : "bg-blue-900/30 text-blue-300"
        }`}>
          {isProcessing && (
            <span className="w-2 h-2 rounded-full bg-blue-400 animate-pulse shrink-0" />
          )}
          {message}
        </div>
      )}

      {/* Buttons */}
      <div className="flex gap-2 mt-3">
        <button
          onClick={handleProcess}
          disabled={!file || isProcessing}
          className="flex-1 py-2 rounded-lg text-sm font-medium bg-blue-600 hover:bg-blue-500 disabled:opacity-40 disabled:cursor-not-allowed transition"
        >
          {isProcessing ? "Processing..." : "Run Pipeline"}
        </button>

        {(file || status !== STATUS.IDLE) && !isProcessing && (
          <button
            onClick={reset}
            className="px-3 py-2 rounded-lg text-sm text-gray-400 hover:text-white hover:bg-gray-800 transition"
          >
            ✕
          </button>
        )}
      </div>
    </div>
  );
}