import Link from "next/link";
export default function Nav(){
  return <nav className="nav">
    <Link className="brand" href="/">RetinaAssist</Link>
    <div className="links">
      <Link href="/screening">Screening</Link>
      <Link href="/followup">Follow-up</Link>
    </div>
  </nav>
}
