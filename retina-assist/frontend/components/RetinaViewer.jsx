export default function RetinaViewer({ preview, heatmap, onFile, onAnalyze, busy }) {
  return (
    <article className="card">
      <div className="cardTitle">
        <div>
          <h2>Fundus Image</h2>
          <p>Use de-identified research images only.</p>
        </div>
        <label className="button secondary">
          Choose image
          <input hidden type="file" accept="image/png,image/jpeg" onChange={onFile} />
        </label>
      </div>

      <div className="imageStage">
        {preview ? <img src={preview} alt="Selected fundus image" /> : <div className="empty">No retinal image selected</div>}
      </div>

      <button className="button primary" disabled={!preview || busy} onClick={onAnalyze}>
        {busy ? "Analyzing…" : "Run AI Analysis"}
      </button>

      {heatmap && (
        <>
          <h3>Model-attention visualization</h3>
          <div className="imageStage heatmap">
            <img src={heatmap} alt="Grad-CAM model-attention visualization" />
          </div>
          <small>Grad-CAM indicates regions influencing the model; it does not prove a clinically meaningful lesion is present.</small>
        </>
      )}
    </article>
  );
}
