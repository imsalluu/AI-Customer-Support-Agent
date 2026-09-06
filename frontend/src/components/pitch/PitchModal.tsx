"use client";

import React, { useState } from "react";
import {
  Award,
  BarChart,
  Bot,
  CheckCircle2,
  DollarSign,
  Globe,
  Layers,
  Sparkles,
  TrendingUp,
  X,
  Zap,
} from "lucide-react";

interface PitchModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function PitchModal({ isOpen, onClose }: PitchModalProps) {
  const [activeTab, setActiveTab] = useState<"deck" | "bangla" | "roi" | "arch">("deck");

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-fadeIn">
      <div className="bg-[#0f172a] border border-slate-700/80 rounded-2xl w-full max-w-4xl max-h-[90vh] flex flex-col overflow-hidden shadow-2xl shadow-indigo-500/10">
        {/* Modal Header */}
        <div className="p-6 border-b border-slate-800 flex items-center justify-between bg-gradient-to-r from-slate-900 via-indigo-950/40 to-slate-900">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-indigo-600 flex items-center justify-center text-white shadow-lg shadow-indigo-600/30">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-white flex items-center gap-2">
                SupportIQ AI — Commercial Executive Pitch & Deck
              </h2>
              <p className="text-xs text-slate-400">
                AI-Powered Customer Support Automation Platform • B2B SaaS Solution
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="w-9 h-9 rounded-xl bg-slate-800/80 hover:bg-slate-700 text-slate-400 hover:text-white flex items-center justify-center transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Tab Selector */}
        <div className="flex border-b border-slate-800 bg-slate-900/50 px-6 gap-2">
          {[
            { id: "deck", label: "Executive Pitch Deck", icon: Award },
            { id: "bangla", label: "বাংলা পিচ ডেক (Bangla Pitch)", icon: Globe },
            { id: "roi", label: "ROI & Cost Calculator", icon: DollarSign },
            { id: "arch", label: "Architecture & Safety", icon: Layers },
          ].map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`flex items-center gap-2 py-3.5 px-4 text-xs font-semibold border-b-2 transition-all ${
                  activeTab === tab.id
                    ? "border-indigo-500 text-indigo-400"
                    : "border-transparent text-slate-400 hover:text-slate-200"
                }`}
              >
                <Icon className="w-4 h-4" />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>

        {/* Modal Body */}
        <div className="p-6 overflow-y-auto flex-1 space-y-6 text-sm text-slate-300">
          {activeTab === "deck" && (
            <div className="space-y-6">
              <div className="p-5 rounded-xl bg-gradient-to-br from-indigo-900/30 via-slate-800/40 to-purple-900/20 border border-indigo-500/20">
                <span className="text-xs font-bold text-indigo-400 uppercase tracking-wider">The Problem</span>
                <h3 className="text-lg font-bold text-white mt-1">E-Commerce & SaaS Support is Broken & Expensive</h3>
                <p className="mt-2 text-slate-300 leading-relaxed text-xs">
                  Human support teams cost $3,500+/agent/month, take 15+ minutes to respond after hours, and suffer from high turnover. Meanwhile, generic chatbots hallucinate answers, make false promises, and frustrate customers.
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="p-4 rounded-xl bg-slate-800/40 border border-slate-700/50">
                  <div className="w-8 h-8 rounded-lg bg-indigo-500/20 text-indigo-400 flex items-center justify-center font-bold mb-3">1</div>
                  <h4 className="font-bold text-white text-sm">70% Cost Reduction</h4>
                  <p className="text-xs text-slate-400 mt-1">Automates 84%+ of tier-1 support queries (orders, tracking, refunds, FAQ) instantly.</p>
                </div>
                <div className="p-4 rounded-xl bg-slate-800/40 border border-slate-700/50">
                  <div className="w-8 h-8 rounded-lg bg-emerald-500/20 text-emerald-400 flex items-center justify-center font-bold mb-3">2</div>
                  <h4 className="font-bold text-white text-sm">1.2s Instant Response</h4>
                  <p className="text-xs text-slate-400 mt-1">24/7 availability across Website Widget, WhatsApp, and Email with 0 queue wait time.</p>
                </div>
                <div className="p-4 rounded-xl bg-slate-800/40 border border-slate-700/50">
                  <div className="w-8 h-8 rounded-lg bg-purple-500/20 text-purple-400 flex items-center justify-center font-bold mb-3">3</div>
                  <h4 className="font-bold text-white text-sm">Zero Hallucination</h4>
                  <p className="text-xs text-slate-400 mt-1">Controlled database tool calls & pgvector RAG with exact document source citations.</p>
                </div>
              </div>

              <div className="p-4 rounded-xl bg-slate-800/30 border border-slate-700/50 space-y-2">
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400">Key Commercial Differentiators</h4>
                <div className="grid grid-cols-2 gap-2 text-xs">
                  <div className="flex items-center gap-2 text-slate-200">
                    <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                    <span>Live Human Handoff (HITL) with real-time takeover</span>
                  </div>
                  <div className="flex items-center gap-2 text-slate-200">
                    <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                    <span>Real-time sentiment escalation on angry customers</span>
                  </div>
                  <div className="flex items-center gap-2 text-slate-200">
                    <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                    <span>Automatic support ticket creation & SLA tracking</span>
                  </div>
                  <div className="flex items-center gap-2 text-slate-200">
                    <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                    <span>Multi-tenant isolation & enterprise RBAC</span>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === "bangla" && (
            <div className="space-y-5">
              <div className="p-5 rounded-xl bg-emerald-950/20 border border-emerald-500/30">
                <span className="text-xs font-bold text-emerald-400 uppercase tracking-wider">কাস্টমার পিচ সামারি</span>
                <h3 className="text-lg font-bold text-white mt-1">SupportIQ AI — আধুনিক B2B কাস্টমার সাপোর্ট অটোমেশন</h3>
                <p className="mt-2 text-slate-300 text-xs leading-relaxed">
                  SupportIQ AI হলো একটি সম্পূর্ণ এন্টারপ্রাইজ গ্রেড কাস্টমার সাপোর্ট প্ল্যাটফর্ম যা ওয়েবসাইট চ্যাট, হোয়াটসঅ্যাপ, এবং ইমেইলে স্বয়ংক্রিয়ভাবে কাস্টমারদের সব প্রশ্নের উত্তর দেয় এবং সমস্যা সমাধান করে।
                </p>
              </div>

              <div className="space-y-3 text-xs">
                <div className="p-3.5 rounded-xl bg-slate-800/40 border border-slate-700/50">
                  <h4 className="font-bold text-white text-sm text-indigo-300">১. কেন আপনার ব্যবসার জন্য SupportIQ AI প্রয়োজন?</h4>
                  <ul className="list-disc list-inside mt-2 space-y-1 text-slate-300">
                    <li><strong>২৪/৭ ইনস্ট্যান্ট রিপ্লাই:</strong> মাত্র ১.২ সেকেন্ডে অর্ডার ট্র্যাকিং, রিফান্ড পলিসি, ও প্রোডাক্ট ইনফো দেওয়া।</li>
                    <li><strong>৭০% সাপোর্ট খরচ সাশ্রয়:</strong> বাড়তি কাস্টমার কেয়ার টিম হায়ার না করেই হাজার হাজার কাস্টমার হ্যান্ডেল করুন।</li>
                    <li><strong>সরাসরি ডেটাবেজ কানেকশন:</strong> এআই কোনো ভুল বা মিথ্যা তথ্য বলবে না, সরাসরি লাইভ ডেটাবেজ থেকে চেক করে সঠিক উত্তর দেবে।</li>
                  </ul>
                </div>

                <div className="p-3.5 rounded-xl bg-slate-800/40 border border-slate-700/50">
                  <h4 className="font-bold text-white text-sm text-emerald-300">২. হিউম্যান হ্যান্ডঅফ ও টিকিট সিস্টেম</h4>
                  <p className="mt-1 text-slate-300">
                    যদি কাস্টমার কোনো কারণে অসন্তুষ্ট হয় বা রাগ করে, এআই স্বয়ংক্রিয়ভাবে তার সেন্টিমেন্ট বুঝে সাপোর্ট এজেন্টের কাছে ট্রান্সফার করবে এবং একটি আর্জেন্ট টিকিট ওপেন করবে।
                  </p>
                </div>

                <div className="p-3.5 rounded-xl bg-slate-800/40 border border-slate-700/50">
                  <h4 className="font-bold text-white text-sm text-purple-300">৩. সহজে ইন্টিগ্রেশন</h4>
                  <p className="mt-1 text-slate-300">
                    আপনার ওয়েবসাইটে মাত্র ১ লাইনের স্ক্রিপ্ট কোড বসিয়েই কয়েক মিনিটে এই চ্যাট উইজেট লাইভ করা যায়!
                  </p>
                </div>
              </div>
            </div>
          )}

          {activeTab === "roi" && (
            <div className="space-y-5">
              <div className="grid grid-cols-3 gap-4 text-center">
                <div className="p-4 rounded-xl bg-slate-800/40 border border-slate-700">
                  <div className="text-2xl font-bold text-indigo-400">$3,500/mo</div>
                  <div className="text-[11px] text-slate-400 mt-1">Average Human Agent Cost</div>
                </div>
                <div className="p-4 rounded-xl bg-indigo-950/40 border border-indigo-500/40">
                  <div className="text-2xl font-bold text-emerald-400">$299/mo</div>
                  <div className="text-[11px] text-slate-400 mt-1">SupportIQ Business Plan</div>
                </div>
                <div className="p-4 rounded-xl bg-slate-800/40 border border-slate-700">
                  <div className="text-2xl font-bold text-amber-400">91.4%</div>
                  <div className="text-[11px] text-slate-400 mt-1">Direct Operational Savings</div>
                </div>
              </div>

              <div className="p-4 rounded-xl bg-slate-800/40 border border-slate-700/50 space-y-3">
                <h4 className="text-sm font-bold text-white">Monthly Impact Model (Based on 10,000 inquiries)</h4>
                <div className="space-y-2 text-xs">
                  <div className="flex justify-between py-1 border-b border-slate-800">
                    <span className="text-slate-400">AI-Resolved Tier-1 Inquiries (85%)</span>
                    <span className="font-semibold text-white">8,500 conversations</span>
                  </div>
                  <div className="flex justify-between py-1 border-b border-slate-800">
                    <span className="text-slate-400">Support Hours Saved per Month</span>
                    <span className="font-semibold text-emerald-400">708 hours</span>
                  </div>
                  <div className="flex justify-between py-1 border-b border-slate-800">
                    <span className="text-slate-400">Customer Satisfaction (CSAT) Increase</span>
                    <span className="font-semibold text-indigo-400">+1.4 ★ (Average 4.8/5)</span>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === "arch" && (
            <div className="space-y-4 text-xs">
              <div className="p-4 rounded-xl bg-slate-800/40 border border-slate-700/50">
                <h4 className="font-bold text-white text-sm mb-2 text-indigo-400">Controlled Business Tools Architecture</h4>
                <p className="text-slate-300">
                  All sensitive business data operations run through 11 validated backend tools. The LLM is NEVER permitted to execute raw SQL, modify prices, invent refund approvals, or forge shipment tracking codes.
                </p>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div className="p-3 rounded-lg bg-slate-800/30 border border-slate-700/40">
                  <div className="font-semibold text-white">pgvector Knowledge Base</div>
                  <div className="text-slate-400 mt-1">Chunking with exact page, section, and document source citations.</div>
                </div>
                <div className="p-3 rounded-lg bg-slate-800/30 border border-slate-700/40">
                  <div className="font-semibold text-white">LangGraph State Machine</div>
                  <div className="text-slate-400 mt-1">Intent routing, sentiment evaluation, confidence thresholding, and HITL handoff.</div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Modal Footer */}
        <div className="p-4 border-t border-slate-800 bg-slate-900/80 flex items-center justify-between">
          <span className="text-xs text-slate-400">SupportIQ AI • Commercial Presentation</span>
          <button
            onClick={onClose}
            className="px-5 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs transition-colors"
          >
            Close Presentation
          </button>
        </div>
      </div>
    </div>
  );
}
