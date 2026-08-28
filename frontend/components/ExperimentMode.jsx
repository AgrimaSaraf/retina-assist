export default function ExperimentMode({ value, onChange }) {
  return (
    <label className="mode">
      <span>Study condition</span>
      <select value={value} onChange={(e) => onChange(e.target.value)}>
        <option value="no_ai">A · No AI</option>
        <option value="ai_only">B · AI prediction</option>
        <option value="ai_explanation">C · AI + explanation</option>
      </select>
    </label>
  );
}
