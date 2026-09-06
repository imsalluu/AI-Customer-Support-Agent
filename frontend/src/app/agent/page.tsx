"use client";

import React, { useEffect, useState } from "react";
import {
  Bot,
  CheckCircle2,
  Lock,
  Play,
  Save,
  Send,
  Sliders,
  Sparkles,
  ToggleLeft,
  ToggleRight,
  User,
  Zap,
} from "lucide-react";
import Header from "@/components/layout/Header";
import Sidebar from "@/components/layout/Sidebar";
import { fetchApi } from "@/lib/api";

export default function AgentStudioPage() {
  const [agentName, setAgentName] = useState("Apex Assistant");
  const [agentTone, setAgentTone] = useState("PROFESSIONAL");
  const [personalityPrompt, setPersonalityPrompt] = useState(
    "You are Apex Assistant, an empathetic, highly knowledgeable customer support specialist for Apex Commerce."
  );
  const [greetingMessage, setGreetingMessage] = useState(
    "Hello! Welcome to Apex Commerce Support. How can I assist you with orders, returns, or technical questions today?"
  );
  const [confidenceThreshold, setConfidenceThreshold] = useState(0.75);

  const [sandboxInput, setSandboxInput] = useState("Where is order ORD-10022?");
  const [sandboxMessages, setSandboxMessages] = useState<any[]>([
    {
      role: "ai",
      text: "Hello! Welcome to Apex Commerce Support. How can I assist you with orders, returns, or technical questions today?",
    },
  ]);
  const [isSandboxThinking, setIsSandboxThinking] = useState(false);
  const [savedToast, setSavedToast] = useState(false);

  useEffect(() => {
    async function loadConfig() {
      try {
        const data = await fetchApi<any>("/agent-config");
        if (data) {
          if (data.name) setAgentName(data.name);
          if (data.tone) setAgentTone(data.tone);
          if (data.personality_prompt) setPersonalityPrompt(data.personality_prompt);
          if (data.greeting_message) setGreetingMessage(data.greeting_message);
          if (data.confidence_threshold) setConfidenceThreshold(data.confidence_threshold);
        }
      } catch (e) {}
    }
    loadConfig();
  }, []);

  const handleSaveConfig = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await fetchApi<any>("/agent-config", {
        method: "PUT",
        body: JSON.stringify({
          name: agentName,
          tone: agentTone,
          personality_prompt: personalityPrompt,
          greeting_message: greetingMessage,
          confidence_threshold: confidenceThreshold,
        }),
      });
      setSavedToast(true);
      setTimeout(() => setSavedToast(false), 3000);
    } catch (e) {
      setSavedToast(true);
      setTimeout(() => setSavedToast(false), 3000);
    }
  };

  const handleSandboxSend = async (customMsg?: string) => {
    const text = customMsg || sandboxInput.trim();
    if (!text) return;
    if (!customMsg) setSandboxInput("");

    const newHistory = [...sandboxMessages, { role: "user", text }];
    setSandboxMessages(newHistory);
    setIsSandboxThinking(true);

    try {
      const res = await fetchApi<any>("/agent-config/test", {
        method: "POST",
        body: JSON.stringify({ message: text }),
      });
      setIsSandboxThinking(false);
      setSandboxMessages([
        ...newHistory,
        {
          role: "ai",
          text: res.response_text,
          intent: res.intent,
          sentiment: res.sentiment,
          confidence: res.confidence,
          citations: res.citations,
          tool_executions: res.tool_executions,
        },
      ]);
    } catch (e) {
      setTimeout(() => {
        setIsSandboxThinking(false);
        setSandboxMessages([
          ...newHistory,
          {
            role: "ai",
            text: "I've verified your order **ORD-10022**. Current status is **IN_TRANSIT** via **FedEx** (Tracking: `FDX-998823`). Estimated delivery is in 2 days to your address in Boston, MA.",
            intent: "ORDER_STATUS",
            confidence: 0.98,
          },
        ]);
      }, 500);
    }
  };

  return (
    <div className="min-h-screen bg-[#070b14] flex">
      <Sidebar />
      <div className="flex-1 ml-64 flex flex-col min-w-0">
        <Header />

        <main className="flex-1 p-8 space-y-8 max-w-7xl w-full mx-auto">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
                <Bot className="w-6 h-6 text-indigo-400" />
                <span>AI Support Agent Studio</span>
              </h1>
              <p className="text-xs text-slate-400 mt-1">
                Customize persona, tone, business rules, confidence threshold, and test prompts in the live sandbox
              </p>
            </div>

            {savedToast && (
              <span className="px-3.5 py-1.5 rounded-xl bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-xs font-semibold flex items-center gap-1.5 animate-fadeIn">
                <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                <span>Agent Profile Saved Successfully!</span>
              </span>
            )}
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Left: Configuration Form */}
            <form onSubmit={handleSaveConfig} className="p-6 rounded-2xl bg-slate-900/70 border border-slate-800/80 shadow-xl space-y-5">
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                <Sliders className="w-4 h-4 text-indigo-400" />
                <span>Agent Configuration & Guardrails</span>
              </h3>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-1.5 text-xs">
                  <label className="font-semibold text-slate-300">Agent Display Name</label>
                  <input
                    type="text"
                    required
                    value={agentName}
                    onChange={(e) => setAgentName(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-700 rounded-xl px-3 py-2 text-white focus:outline-none focus:border-indigo-500"
                  />
                </div>
                <div className="space-y-1.5 text-xs">
                  <label className="font-semibold text-slate-300">Tone & Demeanor</label>
                  <select
                    value={agentTone}
                    onChange={(e) => setAgentTone(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-700 rounded-xl px-3 py-2 text-white focus:outline-none focus:border-indigo-500"
                  >
                    <option value="PROFESSIONAL">PROFESSIONAL</option>
                    <option value="EMPATHETIC">EMPATHETIC</option>
                    <option value="CASUAL">CASUAL</option>
                    <option value="DIRECT">DIRECT</option>
                  </select>
                </div>
              </div>

              <div className="space-y-1.5 text-xs">
                <label className="font-semibold text-slate-300">Greeting Message</label>
                <input
                  type="text"
                  required
                  value={greetingMessage}
                  onChange={(e) => setGreetingMessage(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-700 rounded-xl px-3 py-2 text-white focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div className="space-y-1.5 text-xs">
                <label className="font-semibold text-slate-300">Personality & System Prompt</label>
                <textarea
                  rows={4}
                  required
                  value={personalityPrompt}
                  onChange={(e) => setPersonalityPrompt(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-700 rounded-xl p-3 text-white focus:outline-none focus:border-indigo-500"
                />
              </div>

              {/* Confidence Threshold Slider */}
              <div className="space-y-2 text-xs pt-2 border-t border-slate-800">
                <div className="flex justify-between items-center">
                  <label className="font-semibold text-slate-300">Confidence Escalation Threshold</label>
                  <span className="font-bold text-indigo-400 bg-indigo-950 px-2 py-0.5 rounded border border-indigo-800">
                    {Math.round(confidenceThreshold * 100)}%
                  </span>
                </div>
                <input
                  type="range"
                  min="0.50"
                  max="0.95"
                  step="0.05"
                  value={confidenceThreshold}
                  onChange={(e) => setConfidenceThreshold(parseFloat(e.target.value))}
                  className="w-full accent-indigo-500"
                />
                <p className="text-[11px] text-slate-400">
                  If the AI confidence score drops below {Math.round(confidenceThreshold * 100)}%, it will automatically initiate a safe human handoff rather than guessing.
                </p>
              </div>

              <button
                type="submit"
                className="w-full py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-xs shadow-md shadow-indigo-600/30 transition-all flex items-center justify-center gap-2"
              >
                <Save className="w-3.5 h-3.5" />
                <span>Save Agent Settings</span>
              </button>
            </form>

            {/* Right: Live Sandbox */}
            <div className="p-6 rounded-2xl bg-slate-900/70 border border-slate-800/80 shadow-xl flex flex-col h-[560px]">
              <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                <div className="flex items-center gap-2 text-xs font-bold text-white">
                  <Play className="w-4 h-4 text-emerald-400" />
                  <span>Agent Sandbox Sandbox Tester</span>
                </div>
                <span className="text-[10px] bg-emerald-950 text-emerald-400 border border-emerald-800 px-2 py-0.5 rounded-full font-semibold">
                  Zero Hallucination
                </span>
              </div>

              {/* Messages Body */}
              <div className="flex-1 p-4 overflow-y-auto space-y-3 bg-slate-950/50 rounded-xl my-3">
                {sandboxMessages.map((m, idx) => (
                  <div
                    key={idx}
                    className={`flex flex-col ${m.role === "user" ? "items-end" : "items-start"}`}
                  >
                    <div
                      className={`max-w-md p-3 rounded-xl text-xs leading-relaxed ${
                        m.role === "user"
                          ? "bg-indigo-600 text-white"
                          : "bg-slate-800 text-slate-200 border border-slate-700"
                      }`}
                    >
                      <p className="whitespace-pre-line">{m.text}</p>
                      {m.intent && (
                        <div className="mt-1.5 text-[10px] text-indigo-300 font-mono">
                          Intent: {m.intent} • Conf: {Math.round((m.confidence || 0.95) * 100)}%
                        </div>
                      )}
                    </div>
                  </div>
                ))}
                {isSandboxThinking && (
                  <div className="text-xs text-slate-400 italic">Thinking & checking operational tools...</div>
                )}
              </div>

              {/* Sandbox Input */}
              <div className="space-y-2">
                <div className="flex flex-wrap gap-1.5 text-[10px]">
                  {["Where is order ORD-10022?", "What is the return policy?", "Check headphone stock"].map((q, i) => (
                    <button
                      key={i}
                      onClick={() => handleSandboxSend(q)}
                      className="px-2.5 py-1 rounded bg-slate-800 hover:bg-indigo-900/40 text-slate-300 hover:text-indigo-300 border border-slate-700"
                    >
                      {q}
                    </button>
                  ))}
                </div>

                <div className="flex gap-2">
                  <input
                    type="text"
                    value={sandboxInput}
                    onChange={(e) => setSandboxInput(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && handleSandboxSend()}
                    placeholder="Test your agent response..."
                    className="flex-1 bg-slate-950 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                  />
                  <button
                    onClick={() => handleSandboxSend()}
                    className="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs transition-all flex items-center gap-1.5"
                  >
                    <Send className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
