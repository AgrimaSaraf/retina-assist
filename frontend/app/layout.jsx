import "./globals.css";

export const metadata = {
  title: "RetinaAssist",
  description: "Human-centered AI for retinal screening research"
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
