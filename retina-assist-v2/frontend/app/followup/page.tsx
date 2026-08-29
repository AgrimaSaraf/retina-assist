"use client";
import {useState} from "react";
import {scoreFollowup} from "@/lib/api";

export default function Followup(){
  const [form,setForm]=useState({
    age_band:"40-59",
    previous_missed_visits:0,
    lead_time_days:14,
    recommended_followup_days:30,
    visit_type:"retina",
    contact_available:true
  });
  const [result,setResult]=useState<any>(null);

  async function run(e:React.FormEvent){
    e.preventDefault();
    setResult(await scoreFollowup(form));
  }

  return <section>
    <div className="eyebrow">STUDY B</div>
    <h1>Follow-up sandbox</h1>
    <p className="lede">Synthetic-data workflow demo — not a clinical risk calculator.</p>
    <form className="panel form" onSubmit={run}>
      <label>Age band
        <select value={form.age_band} onChange={e=>setForm({...form,age_band:e.target.value})}>
          <option>0-17</option><option>18-39</option><option>40-59</option><option>60+</option>
        </select>
      </label>
      <label>Previous missed visits
        <input type="number" value={form.previous_missed_visits}
          onChange={e=>setForm({...form,previous_missed_visits:Number(e.target.value)})}/>
      </label>
      <label>Lead time days
        <input type="number" value={form.lead_time_days}
          onChange={e=>setForm({...form,lead_time_days:Number(e.target.value)})}/>
      </label>
      <label>Recommended follow-up days
        <input type="number" value={form.recommended_followup_days}
          onChange={e=>setForm({...form,recommended_followup_days:Number(e.target.value)})}/>
      </label>
      <label>Visit type
        <select value={form.visit_type} onChange={e=>setForm({...form,visit_type:e.target.value})}>
          <option value="routine">Routine</option><option value="retina">Retina</option>
          <option value="glaucoma">Glaucoma</option><option value="post_op">Post-op</option>
          <option value="other">Other</option>
        </select>
      </label>
      <label className="check">
        <input type="checkbox" checked={form.contact_available}
          onChange={e=>setForm({...form,contact_available:e.target.checked})}/>
        Contact channel available
      </label>
      <button>Run research baseline</button>
    </form>
    {result && <div className="panel">
      <div className="kicker">{result.model_status.toUpperCase()}</div>
      <div className="risk">{Math.round(result.probability*100)}%</div>
      <div className="pill">{result.risk_band} research band</div>
      <p>{result.note}</p>
    </div>}
  </section>
}
