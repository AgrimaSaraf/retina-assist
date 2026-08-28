"use client";

import { useState } from "react";
import RetinaViewer from "../components/RetinaViewer";
import PredictionCard from "../components/PredictionCard";
import ClinicianDecision from "../components/ClinicianDecision";
import ExperimentMode from "../components/ExperimentMode";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function Home() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [mode, setMode] = useState("ai_explanation");

  function chooseFile(e) {
    const selected = e.target.files?.[0];
    if (!selected) return;
    setFile(selected);
    setPreview(URL.createObjectURL(selected));
    setAnalysis(null);
    setError("");
  }

  async function analyze() {
    if (!file) return;
    setBusy(true);
    setError("");
    const form = new FormData();
    form.append("file", file);
    try {
      const res = await fetch(`${API}/analyze`, { method: "POST", body: form });
      const body = await res.json();
      if (!res.ok) {
        throw new Error(body?.detail?.message || body?.detail || "Analysis failed.");
      }
      setAnalysis(body);
    } catch (e) {
      setError(e.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <main>
      <aside className="sidebar">
        <div className="brand">◉ <span>RetinaAssist</span></div>
        <nav>
          <b>Dashboard</b>
          <span>New Analysis</span>
          <span>Study Mode</span>
          <span>Research</span>
        </nav>
        <div className="researchBadge">
          <strong>Research prototype</strong>
          <small>Not for diagnosis or patient-care decisions.</small>
        </div>
      </aside>

      <section className="workspace">
        <header>
          <div>
            <h1>Retinal Screening Workspace</h1>
            <p>Computer vision + human-AI interaction research</p>
          </div>
          <ExperimentMode value={mode} onChange={setMode} />
        </header>

        <div className="warning">
          RetinaAssist is an experimental research interface. Do not enter patient identifiers or use its output for clinical care.
        </div>

        <div className="grid">
          <RetinaViewer
            preview={preview}
            heatmap={analysis?.gradcam}
            onFile={chooseFile}
            onAnalyze={analyze}
            busy={busy}
          />
          <PredictionCard analysis={analysis} mode={mode} error={error} />
        </div>

        <ClinicianDecision
          mode={mode}
          aiPrediction={analysis?.prediction}
          aiConfidence={analysis?.confidence}
        />
      </section>
    </main>
  );
}
