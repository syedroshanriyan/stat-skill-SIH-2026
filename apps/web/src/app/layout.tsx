import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "STAT-SKILL AI — AI-Powered Competency Intelligence Platform",
  description:
    "Institutional competency assessment, automated skill-gap analysis, iGOT/NSSTA personalized recommendations, grounded AI quizzes, and workforce analytics for Official Statistics and Enterprise Capacity Building.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link rel="dns-prefetch" href="https://fonts.googleapis.com" />
      </head>
      <body className="bg-warm-ivory text-ink antialiased min-h-screen">
        {children}
      </body>
    </html>
  );
}
