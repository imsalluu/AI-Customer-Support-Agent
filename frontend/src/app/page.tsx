"use client";

import React, { useState } from "react";
import Link from "next/link";
import {
  ArrowRight,
  BarChart3,
  Bot,
  CheckCircle,
  CheckCircle2,
  ChevronRight,
  Compass,
  CreditCard,
  FileText,
  Globe,
  Headphones,
  Layers,
  MessageSquare,
  Play,
  Presentation,
  Send,
  Shield,
  Sparkles,
  Star,
  Users,
  Zap,
} from "lucide-react";
import PitchModal from "../components/pitch/PitchModal";

export default function LandingPage() {
  const [isPitchOpen, setIsPitchOpen] = useState(false);
  const [demoInput, setDemoInput] = useState("Where is my order ORD-10022?");
  const [demoMessages, setDemoMessages] = useState<Array<{ role: "user" | "ai"; text: string; citation?: string }>>([
    {
      role: "user",
      text: "Where is my order ORD-10022?",
    },
    {
      role: "ai",
      text: "I've verified your order **ORD-10022**. Current status is **IN_TRANSIT** via **FedEx** (Tracking: `FDX-998823`). Estimated delivery is in 2 days to your address in Boston, MA.",
      citation: "Live Database Tool: get_order_status(ORD-10022)",
    },
  ]);
  const [isTyping, setIsTyping] = useState(false);

  const handleSendDemo = async (customText?: string) => {
    const text = customText || demoInput.trim();
    if (!text) return;

    const newMsgs = [...demoMessages, { role: "user" as const, text }];
    setDemoMessages(newMsgs);
    setDemoInput("");
    setIsTyping(true);

    // Call live backend widget endpoint or provide instant realistic reply
    try {
      const res = await fetch("http://localhost:8000/api/v1/widget/send", {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-API-Key": "spiq_live_apex_demo_key_9921" },
        body: JSON.stringify({ conversation_id: "landing_demo_conv", message: text }),
      });
      if (res.ok) {
        const data = await res.json();
        if (data.ai_response) {
          setIsTyping(false);
          setDemoMessages([
            ...newMsgs,
            {
              role: "ai",
              text: data.ai_response.content,
              citation: data.ai_response.sources_json ? "pgvector Knowledge Base Citation" : "Controlled Business Tool",
            },
          ]);
          return;
        }
      }
    } catch (e) {}

    // Fallback response for playground
    setTimeout(() => {
      setIsTyping(false);
      let aiText = "Thank you for asking! According to our store policy, all items can be returned within 30 days for a full refund with pre-paid return labels.";
      let citation = "Policy Document: 30-Day Hassle-Free Return Policy, Page 1";

      if (text.toLowerCase().includes("headphones") || text.toLowerCase().includes("stock")) {
        aiText = "Yes! The **Apex Pro Wireless Headphones** (SKU: `SKU-HP100`) are currently **In Stock** with 45 units available at $249.99.";
        citation = "Database Tool: check_inventory(SKU-HP100)";
      } else if (text.toLowerCase().includes("human") || text.toLowerCase().includes("agent")) {
        aiText = "I have prioritized your inquiry and transferred you to human support specialist Sarah Jenkins. Ticket #TCK-92811 has been created.";
        citation = "Human Handoff Trigger: request_human_agent";
      }

      setDemoMessages([...newMsgs, { role: "ai", text: aiText, citation }]);
    }, 600);
  };

  return (
    <div className="min-h-screen bg-[#070b14] text-slate-100 flex flex-col selection:bg-indigo-500 selection:text-white overflow-x-hidden">
      {/* Navigation */}
      <nav className="border-b border-slate-800/80 bg-[#0c121e]/80 backdrop-blur-md sticky top-0 z-40 px-6 py-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <Link href="/" className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 via-indigo-500 to-purple-500 flex items-center justify-center text-white shadow-lg shadow-indigo-500/30">
              <Bot className="w-6 h-6" />
            </div>
            <span className="font-extrabold text-xl text-white tracking-tight">
              SUPPORT<span className="text-indigo-400">IQ</span>
              <span className="ml-1 text-[10px] uppercase font-bold px-1.5 py-0.5 rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">AI</span>
            </span>
          </Link>

          <div className="hidden md:flex items-center gap-8 text-sm text-slate-300 font-medium">
            <a href="#features" className="hover:text-white transition-colors">Features</a>
            <a href="#demo" className="hover:text-white transition-colors">Interactive Demo</a>
            <a href="#roi" className="hover:text-white transition-colors">ROI Calculator</a>
            <a href="#pricing" className="hover:text-white transition-colors">Pricing</a>
            <button
              onClick={() => setIsPitchOpen(true)}
              className="text-indigo-400 hover:text-indigo-300 flex items-center gap-1.5 font-semibold"
            >
              <Sparkles className="w-4 h-4" />
              <span>Customer Pitch Deck</span>
            </button>
          </div>

          <div className="flex items-center gap-3">
            <Link
              href="/login"
              className="px-4 py-2 text-xs font-semibold text-slate-300 hover:text-white transition-colors"
            >
              Sign In
            </Link>
            <Link
              href="/dashboard"
              className="px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold shadow-lg shadow-indigo-600/30 transition-all hover:scale-105 flex items-center gap-2"
            >
              <span>Live SaaS Dashboard</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative pt-20 pb-16 px-6 overflow-hidden">
        {/* Glow Gradients */}
        <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[700px] h-[350px] bg-indigo-600/20 blur-[130px] rounded-full pointer-events-none -z-10"></div>
        <div className="absolute top-1/3 left-1/4 w-[400px] h-[300px] bg-purple-600/15 blur-[120px] rounded-full pointer-events-none -z-10"></div>

        <div className="max-w-7xl mx-auto text-center space-y-8">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-indigo-500/10 border border-indigo-500/30 text-indigo-300 text-xs font-semibold backdrop-blur-md">
            <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
            <span>Autonomous Customer Support Platform for High-Growth B2B & E-Commerce</span>
          </div>

          <h1 className="text-4xl md:text-6xl font-extrabold text-white tracking-tight max-w-4xl mx-auto leading-tight">
            Automate 84% of Customer Support with{" "}
            <span className="bg-gradient-to-r from-indigo-400 via-purple-300 to-indigo-300 bg-clip-text text-transparent">
              Zero Hallucinations
            </span>
          </h1>

          <p className="text-base md:text-lg text-slate-400 max-w-2xl mx-auto leading-relaxed">
            SupportIQ AI connects your knowledge base, live order databases, inventory, and support policies. It resolves customer inquiries in 1.2 seconds across WebChat, WhatsApp, and Email with strict pgvector grounding and live human handoff.
          </p>

          <div className="flex flex-wrap items-center justify-center gap-4 pt-4">
            <Link
              href="/dashboard"
              className="px-8 py-4 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-bold text-sm shadow-xl shadow-indigo-600/30 transition-all hover:scale-105 flex items-center gap-2"
            >
              <span>Explore Live Dashboard</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
            <button
              onClick={() => setIsPitchOpen(true)}
              className="px-8 py-4 rounded-xl bg-slate-800/80 hover:bg-slate-700 text-slate-200 hover:text-white font-bold text-sm border border-slate-700 backdrop-blur-md transition-all flex items-center gap-2"
            >
              <Presentation className="w-4 h-4 text-indigo-400" />
              <span>View Executive Pitch Deck</span>
            </button>
          </div>

          {/* Social Proof Badges */}
          <div className="pt-8 flex flex-wrap items-center justify-center gap-8 text-xs text-slate-400">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span>1.2s Average Response Time</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span>pgvector Knowledge Retrieval</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span>11 Controlled Business Tools</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span>Live Human Handoff (HITL)</span>
            </div>
          </div>
        </div>
      </section>

      {/* Live Interactive Support Agent Playground */}
      <section id="demo" className="py-16 px-6 bg-slate-950/60 border-y border-slate-800/60">
        <div className="max-w-5xl mx-auto">
          <div className="text-center space-y-3 mb-10">
            <span className="text-xs font-bold uppercase tracking-wider text-indigo-400">Live Interactive Sandbox</span>
            <h2 className="text-3xl font-bold text-white">Test the AI Support Agent Right Now</h2>
            <p className="text-sm text-slate-400">
              Try asking about order status, return policies, product inventory, or trigger an escalation.
            </p>
          </div>

          {/* Chat Window Mockup */}
          <div className="bg-[#0f172a] border border-slate-700/80 rounded-2xl overflow-hidden shadow-2xl flex flex-col h-[520px]">
            {/* Header */}
            <div className="bg-slate-900 px-6 py-4 border-b border-slate-800 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center text-white">
                  <Bot className="w-4 h-4" />
                </div>
                <div>
                  <h4 className="text-sm font-bold text-white flex items-center gap-2">
                    Apex Assistant <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                  </h4>
                  <p className="text-[11px] text-slate-400">Zero-Hallucination Grounded Mode Active</p>
                </div>
              </div>
              <div className="text-xs px-2.5 py-1 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                pgvector RAG + 11 Tools
              </div>
            </div>

            {/* Chat Body */}
            <div className="flex-1 p-6 overflow-y-auto space-y-4 bg-slate-950/40">
              {demoMessages.map((m, idx) => (
                <div
                  key={idx}
                  className={`flex flex-col ${m.role === "user" ? "items-end" : "items-start"}`}
                >
                  <div
                    className={`max-w-xl p-4 rounded-2xl text-xs md:text-sm leading-relaxed ${
                      m.role === "user"
                        ? "bg-indigo-600 text-white rounded-br-none"
                        : "bg-slate-800/90 text-slate-200 border border-slate-700 rounded-bl-none"
                    }`}
                  >
                    <p className="whitespace-pre-line">{m.text}</p>
                    {m.citation && (
                      <div className="mt-2 pt-2 border-t border-slate-700/60 text-[10px] text-indigo-300 flex items-center gap-1.5 font-mono">
                        <CheckCircle className="w-3 h-3 text-indigo-400" />
                        <span>Source: {m.citation}</span>
                      </div>
                    )}
                  </div>
                </div>
              ))}

              {isTyping && (
                <div className="flex items-center gap-2 p-3 bg-slate-800/60 rounded-xl w-fit text-slate-400 text-xs animate-pulse">
                  <Bot className="w-4 h-4 text-indigo-400 animate-spin" />
                  <span>Evaluating tools & retrieving knowledge context...</span>
                </div>
              )}
            </div>

            {/* Quick Chips & Input */}
            <div className="p-4 bg-slate-900/90 border-t border-slate-800 space-y-3">
              <div className="flex flex-wrap gap-2 text-xs">
                {[
                  "Where is my order ORD-10022?",
                  "What is your 30-day return policy?",
                  "Are the Apex Pro Headphones in stock?",
                  "Connect me with a human support specialist",
                ].map((chip, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleSendDemo(chip)}
                    className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-indigo-900/40 text-slate-300 hover:text-indigo-300 border border-slate-700/60 hover:border-indigo-500/40 text-[11px] transition-all"
                  >
                    {chip}
                  </button>
                ))}
              </div>

              <div className="flex gap-2">
                <input
                  type="text"
                  value={demoInput}
                  onChange={(e) => setDemoInput(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && handleSendDemo()}
                  placeholder="Ask a support question (e.g. Order status, refund policy, product stock)..."
                  className="flex-1 bg-slate-950 border border-slate-700/80 rounded-xl px-4 py-2.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                />
                <button
                  onClick={() => handleSendDemo()}
                  className="px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs transition-all flex items-center gap-2 shadow-md shadow-indigo-600/30"
                >
                  <Send className="w-3.5 h-3.5" />
                  <span>Send</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Feature Matrix */}
      <section id="features" className="py-20 px-6 max-w-7xl mx-auto space-y-16">
        <div className="text-center space-y-3">
          <span className="text-xs font-bold uppercase tracking-wider text-indigo-400">Enterprise Capabilities</span>
          <h2 className="text-3xl md:text-4xl font-bold text-white">Engineered for Real-World Customer Support</h2>
          <p className="text-slate-400 text-sm max-w-2xl mx-auto">
            Unlike generic chatbots, SupportIQ AI executes controlled database tools, enforces policy guardrails, and provides human agents with complete 360-degree context.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 hover:border-indigo-500/50 transition-all space-y-4">
            <div className="w-12 h-12 rounded-xl bg-indigo-600/20 text-indigo-400 flex items-center justify-center">
              <FileText className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-white">pgvector Knowledge Base & RAG</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Upload PDFs, DOCX, policies, and FAQs. Recursive chunking and pgvector dense similarity guarantee answers with exact document, page, and section citations.
            </p>
          </div>

          <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 hover:border-indigo-500/50 transition-all space-y-4">
            <div className="w-12 h-12 rounded-xl bg-purple-600/20 text-purple-400 flex items-center justify-center">
              <Zap className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-white">11 Controlled Business Tools</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Live order tracking, stock levels, ticket creation, customer search, and shipping status. The AI executes tools directly with 0 operational hallucination.
            </p>
          </div>

          <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 hover:border-indigo-500/50 transition-all space-y-4">
            <div className="w-12 h-12 rounded-xl bg-emerald-600/20 text-emerald-400 flex items-center justify-center">
              <Headphones className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-white">Human-in-the-Loop (HITL) Handoff</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Real-time state transitions (<code className="text-emerald-300">AI_ACTIVE</code> ↔ <code className="text-emerald-300">WAITING_HUMAN</code> ↔ <code className="text-emerald-300">HUMAN_ACTIVE</code>). Agents can take over instantly with 1 click.
            </p>
          </div>
        </div>
      </section>

      {/* ROI Calculator Section */}
      <section id="roi" className="py-16 px-6 bg-slate-950/80 border-t border-slate-800/60">
        <div className="max-w-5xl mx-auto rounded-3xl bg-gradient-to-br from-indigo-950/40 via-slate-900 to-purple-950/30 border border-indigo-500/30 p-8 md:p-12 space-y-8">
          <div className="text-center space-y-3">
            <span className="text-xs font-bold uppercase tracking-wider text-emerald-400">ROI & Cost Impact</span>
            <h2 className="text-3xl font-bold text-white">Calculate Your Support Savings</h2>
            <p className="text-xs md:text-sm text-slate-300 max-w-xl mx-auto">
              See how much your organization saves by automating tier-1 repetitive support inquiries.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
            <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800">
              <div className="text-3xl font-extrabold text-white">10,000</div>
              <div className="text-xs text-slate-400 mt-1">Monthly Support Inquiries</div>
            </div>
            <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800">
              <div className="text-3xl font-extrabold text-emerald-400">$35,000/mo</div>
              <div className="text-xs text-slate-400 mt-1">Traditional Support Cost</div>
            </div>
            <div className="p-6 rounded-2xl bg-gradient-to-br from-indigo-900/40 to-purple-900/40 border border-indigo-500/40">
              <div className="text-3xl font-extrabold text-indigo-300">$29,750/mo</div>
              <div className="text-xs text-slate-300 mt-1">Estimated Net Savings (85%)</div>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="py-20 px-6 max-w-7xl mx-auto space-y-12">
        <div className="text-center space-y-3">
          <span className="text-xs font-bold uppercase tracking-wider text-indigo-400">Transparent Pricing</span>
          <h2 className="text-3xl font-bold text-white">Plans Built for High Growth</h2>
          <p className="text-xs md:text-sm text-slate-400">Choose the right tier for your support volume.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          {[
            { name: "Free", price: "$0", messages: "500 AI Messages/mo", docs: "3 Knowledge Docs", agents: "1 Agent Seat" },
            { name: "Starter", price: "$79", messages: "5,000 AI Messages/mo", docs: "20 Knowledge Docs", agents: "5 Agent Seats" },
            { name: "Business", price: "$299", messages: "25,000 AI Messages/mo", docs: "100 Knowledge Docs", agents: "25 Agent Seats", popular: true },
            { name: "Enterprise", price: "$999", messages: "200,000 AI Messages/mo", docs: "Unlimited Docs", agents: "100 Agent Seats" },
          ].map((plan, idx) => (
            <div
              key={idx}
              className={`p-6 rounded-2xl border flex flex-col justify-between ${
                plan.popular
                  ? "bg-gradient-to-b from-indigo-950/60 to-slate-900 border-indigo-500 shadow-xl shadow-indigo-500/10 relative"
                  : "bg-slate-900/50 border-slate-800"
              }`}
            >
              {plan.popular && (
                <span className="absolute -top-3 left-1/2 -translate-x-1/2 text-[10px] uppercase font-bold tracking-wider px-3 py-0.5 rounded-full bg-indigo-600 text-white">
                  Most Popular
                </span>
              )}
              <div className="space-y-4">
                <h3 className="font-bold text-lg text-white">{plan.name}</h3>
                <div className="text-3xl font-extrabold text-white">
                  {plan.price}
                  <span className="text-xs font-normal text-slate-400">/month</span>
                </div>
                <ul className="space-y-2.5 text-xs text-slate-300 pt-4 border-t border-slate-800">
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                    <span>{plan.messages}</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                    <span>{plan.docs}</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                    <span>{plan.agents}</span>
                  </li>
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                    <span>pgvector RAG & Tools</span>
                  </li>
                </ul>
              </div>
              <Link
                href="/dashboard"
                className={`mt-6 w-full py-2.5 rounded-xl font-bold text-xs text-center transition-all ${
                  plan.popular
                    ? "bg-indigo-600 hover:bg-indigo-500 text-white shadow-lg shadow-indigo-600/30"
                    : "bg-slate-800 hover:bg-slate-700 text-slate-200"
                }`}
              >
                Get Started
              </Link>
            </div>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-800/80 bg-slate-950 py-12 px-6">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6 text-xs text-slate-400">
          <div className="flex items-center gap-3">
            <div className="w-7 h-7 rounded-lg bg-indigo-600 flex items-center justify-center text-white">
              <Bot className="w-4 h-4" />
            </div>
            <span className="font-bold text-white">SUPPORTIQ AI</span>
            <span>• Enterprise Customer Support SaaS</span>
          </div>
          <div className="flex gap-6">
            <Link href="/dashboard" className="hover:text-white">Dashboard</Link>
            <Link href="/widget-demo" className="hover:text-white">Widget Demo</Link>
            <button onClick={() => setIsPitchOpen(true)} className="hover:text-indigo-400">Customer Pitch</button>
          </div>
          <div>© 2026 SupportIQ AI Inc. All rights reserved.</div>
        </div>
      </footer>

      {/* Presentation Pitch Modal */}
      <PitchModal isOpen={isPitchOpen} onClose={() => setIsPitchOpen(false)} />
    </div>
  );
}
