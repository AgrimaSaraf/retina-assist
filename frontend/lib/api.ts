const API=process.env.NEXT_PUBLIC_API_URL||'http://localhost:8000';
export async function scoreFollowup(payload:any){const r=await fetch(`${API}/followup/risk`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)}); if(!r.ok) throw new Error('Unable to score'); return r.json();}
export async function analyzeRetina(file:File){const f=new FormData(); f.append('file',file); const r=await fetch(`${API}/screening/analyze`,{method:'POST',body:f}); const d=await r.json(); if(!r.ok) throw new Error(d?.detail?.message||'Unable to analyze'); return d;}
