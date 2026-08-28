"use client";
import { useState } from "react";

const labels = ["No DR", "Mild", "Moderate", "Severe", "Proliferative DR"];

export default function ClinicianDecision({ mode, aiPrediction, aiConfidence }) {
  const [initial, setInitial] = useState("");
  const [initialConfidence, setInitialConfidence] = useState(3);
  const [revealed, setRevealed] = useState(false);
  const [finalDecision, setFinalDecision] = useState("");

  return (
    <article className="card decision">
      <h2>Clinician Decision</h2>
      <p>Research workflow: capture an independent judgment before revealing AI.</p>

      <div className="decisionGrid">
        <label>
          Initial assessment
          <select value={initial} onChange={(e) => setInitial(e.target.value)}>
            <option value="">Select…</option>
            {labels.map(x => <option key={x}>{x}</option>)}
          </select>
        </label>

        <label>
          Initial confidence · {initialConfidence}/5
          <input type="range" min="1" max="5" value={initialConfidence}
                 onChange={(e) => setInitialConfidence(Number(e.target.value))} />
        </label>
      </div>

      {mode !== "no_ai" && (
        <button className="button secondary" disabled={!initial} onClick={() => setRevealed(true)}>
          Lock initial decision & reveal AI
        </button>
      )}

      {revealed && (
        <div className="aiReveal">
          <strong>AI: {aiPrediction || "Model not available"}</strong>
          {aiConfidence != null && <span>{Math.round(aiConfidence * 100)}% confidence</span>}
        </div>
      )}

      {(mode === "no_ai" || revealed) && (
        <label>
          Final assessment
          <select value={finalDecision} onChange={(e) => setFinalDecision(e.target.value)}>
            <option value="">Select…</option>
            {labels.map(x => <option key={x}>{x}</option>)}
          </select>
        </label>
      )}

      <small>
        Production study instrumentation should save de-identified interaction events to an approved research datastore.
      </small>
    </article>
  );
}
