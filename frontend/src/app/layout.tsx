import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "SupportIQ AI — Autonomous Omnichannel Customer Support SaaS",
  description: "Enterprise AI Customer Support Platform powered by LangGraph, pgvector RAG, controlled business tools, and human-in-the-loop handoff.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="bg-[#090d16] text-slate-100 font-['Plus_Jakarta_Sans',sans-serif] min-h-screen antialiased selection:bg-indigo-500 selection:text-white">
        {children}
      </body>
    </html>
  );
}
