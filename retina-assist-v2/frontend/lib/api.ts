const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function scoreFollowup(payload:any){
  const r=await fetch(`${API}/followup/risk`,{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify(payload)
  });
  if(!r.ok) throw new Error("Unable to score research case");
  return r.json();
}

export async function analyzeRetina(file:File){
  const form=new FormData();
  form.append("file",file);
  const r=await fetch(`${API}/screening/analyze`,{method:"POST",body:form});
  const data=await r.json();
  if(!r.ok) throw new Error(data?.detail?.message || "Unable to analyze image");
  return data;
}
