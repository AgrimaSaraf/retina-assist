export default function PredictionCard({ analysis, mode, error }) {
  const hideAI = mode === "no_ai";

  return (
    <article className="card">
      <h2>AI Decision Support</h2>

      {error && (
        <div className="modelMissing">
          <strong>Model unavailable</strong>
          <p>{error}</p>
          <small>This is intentional: RetinaAssist never substitutes random weights for a trained retinal model.</small>
        </div>
      )}

      {!analysis && !error && <div className="empty tall">Run an analysis to view model output.</div>}

      {analysis && hideAI && (
        <div className="empty tall">AI output hidden for the No-AI experimental condition.</div>
      )}

      {analysis && !hideAI && (
        <>
          <div className="prediction">
            <span>Predicted DR severity</span>
            <strong>{analysis.prediction}</strong>
            <em>{Math.round(analysis.confidence * 100)}% model confidence</em>
          </div>

          <h3>Class probabilities</h3>
          {Object.entries(analysis.probabilities).map(([name, value]) => (
            <div className="prob" key={name}>
              <span>{name}</span>
              <progress value={value} max="1" />
              <b>{Math.round(value * 100)}%</b>
            </div>
          ))}

          <h3>Image quality</h3>
          <div className="quality">{analysis.image_quality.score}/10</div>

          <div className="warning small">{analysis.disclaimer}</div>
        </>
      )}
    </article>
  );
}
