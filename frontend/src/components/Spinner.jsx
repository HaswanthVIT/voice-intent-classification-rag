// src/components/Spinner.jsx
export default function Spinner({ size = 32, label = 'Loading...' }) {
  return (
    <div className="flex flex-col items-center justify-center gap-3 py-12">
      <div
        style={{
          width: size,
          height: size,
          border: `2px solid #2A2D3E`,
          borderTop: `2px solid #4FC3F7`,
          borderRadius: '50%',
          animation: 'spin 0.8s linear infinite',
        }}
      />
      {label && (
        <span className="font-mono text-xs" style={{ color: '#8B90B0' }}>
          {label}
        </span>
      )}
      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
    </div>
  )
}
