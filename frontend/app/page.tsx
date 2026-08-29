import Link from "next/link";

export default function Home(){
  return <section>
    <div className="eyebrow">HUMAN-CENTERED AI · OPHTHALMOLOGY</div>
    <h1>RetinaAssist</h1>
    <p className="lede">
      A research platform for studying retinal AI decision support and the
      human workflows around ophthalmology follow-up.
    </p>
    <div className="warning">Research software only — not for patient-care decisions.</div>
    <div className="grid">
      <Link className="card" href="/screening">
        <span className="kicker">STUDY A</span>
        <h2>Retinal screening</h2>
        <p>Human–AI decision making with a validated model checkpoint.</p>
      </Link>
      <Link className="card" href="/followup">
        <span className="kicker">STUDY B</span>
        <h2>Follow-up workflow</h2>
        <p>Research-only prioritization and workflow evaluation.</p>
      </Link>
    </div>
  </section>
}
