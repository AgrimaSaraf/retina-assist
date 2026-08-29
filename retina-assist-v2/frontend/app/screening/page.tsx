"use client";
import {useState} from "react";
import {analyzeRetina} from "@/lib/api";

export default function Screening(){
  const [file,setFile]=useState<File|null>(null);
  const [message,setMessage]=useState("");
  const [result,setResult]=useState<any>(null);

  async function run(e:React.FormEvent){
    e.preventDefault(); setMessage(""); setResult(null);
    if(!file){setMessage("Choose an image first.");return;}
    try{setResult(await analyzeRetina(file));}
    catch(err:any){setMessage(err.message);}
  }

  return <section>
    <div className="eyebrow">STUDY A</div>
    <h1>Retinal screening</h1>
    <p className="lede">No validated checkpoint means no prediction.</p>
    <div className="warning">
      The API deliberately refuses to generate medical-looking output without a validated checkpoint.
    </div>
    <form className="panel form" onSubmit={run}>
      <label>Research image
        <input type="file" accept="image/jpeg,image/png" onChange={e=>setFile(e.target.files?.[0]||null)}/>
      </label>
      <button>Analyze</button>
    </form>
    {message && <div className="error">{message}</div>}
    {result && <div className="panel">
      <div className="kicker">RESEARCH OUTPUT</div>
      <h2>{result.label}</h2>
      <div className="risk">{Math.round(result.confidence*100)}%</div>
      <p>{result.warning}</p>
    </div>}
  </section>
}
