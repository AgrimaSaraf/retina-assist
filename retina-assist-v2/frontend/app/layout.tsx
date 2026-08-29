import "./globals.css";
import Nav from "@/components/Nav";

export const metadata={
  title:"RetinaAssist Research",
  description:"Human-centered AI for ophthalmology research"
};

export default function Layout({children}:{children:React.ReactNode}){
  return <html lang="en"><body><Nav/><main className="shell">{children}</main></body></html>
}
