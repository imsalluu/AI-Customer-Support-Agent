"use client";

import React, { useEffect, useState } from "react";
import {
  Activity,
  ArrowUpRight,
  BarChart3,
  Bot,
  Clock,
  DollarSign,
  Headphones,
  HelpCircle,
  Lightbulb,
  MessageSquare,
  Shield,
  Smile,
  Sparkles,
  Star,
  Ticket,
  TrendingUp,
  Zap,
} from "lucide-react";
import Header from "@/components/layout/Header";
import Sidebar from "@/components/layout/Sidebar";
import { fetchApi } from "@/lib/api";

export default function AnalyticsPage() {
  const [sentimentData, setSentimentData] = useState([
    { sentiment: "POSITIVE", count: 68, percentage: 65.0, color: "bg-emerald-500", text: "text-emerald-400" },
    { sentiment: "NEUTRAL", count: 26, percentage: 25.0, color: "bg-slate-500", text: "text-slate-300" },
    { sentiment: "NEGATIVE", count: 8, percentage: 7.5, color: "bg-amber-500", text: "text-amber-400" },
    { sentiment: "ANGRY", count: 3, percentage: 2.5, color: "bg-rose-500", text: "text-rose-400" },
  ]);

  const [intentData, setIntentData] = useState([
    { intent: "ORDER_STATUS", count: 42, percentage: 35.0 },
    { intent: "SHIPPING", count: 28, percentage: 23.3 },
    { intent: "PRODUCT_INFO", count: 22, percentage: 18.3 },
    { intent: "RETURN", count: 15, percentage: 12.5 },
    { intent: "REFUND", count: 8, percentage: 6.7 },
    { intent: "COMPLAINT", count: 5, percentage: 4.2 },
  ]);

  return (
    <div className="min-h-screen bg-[#070b14] flex">
      <Sidebar />
      <div className="flex-1 ml-64 flex flex-col min-w-0">
        <Header />

        <main className="flex-1 p-8 space-y-8 max-w-7xl w-full mx-auto">
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
              <BarChart3 className="w-6 h-6 text-indigo-400" />
              <span>Deep Support Analytics & Intelligence</span>
            </h1>
            <p className="text-xs text-slate-400 mt-1">
              Customer sentiment trends, CSAT breakdowns, AI resolution vs human escalation, and operational metrics
            </p>
          </div>

          {/* KPI Cards */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="p-5 rounded-2xl bg-slate-900/70 border border-slate-800 space-y-2">
              <span className="text-xs text-slate-400">Total CSAT Rating</span>
              <div className="text-2xl font-bold text-white flex items-center gap-2">
                <span>4.8 / 5.0</span>
                <Star className="w-4 h-4 fill-amber-400 text-amber-400" />
              </div>
              <p className="text-[11px] text-emerald-400 font-semibold">+0.6 vs last month</p>
            </div>
            <div className="p-5 rounded-2xl bg-slate-900/70 border border-slate-800 space-y-2">
              <span className="text-xs text-slate-400">AI Direct Resolution</span>
              <div className="text-2xl font-bold text-emerald-400">84.5%</div>
              <p className="text-[11px] text-slate-400">118 of 142 handled without human</p>
            </div>
            <div className="p-5 rounded-2xl bg-slate-900/70 border border-slate-800 space-y-2">
              <span className="text-xs text-slate-400">Escalation Rate</span>
              <div className="text-2xl font-bold text-indigo-300">15.5%</div>
              <p className="text-[11px] text-slate-400">24 escalated to support agents</p>
            </div>
            <div className="p-5 rounded-2xl bg-slate-900/70 border border-slate-800 space-y-2">
              <span className="text-xs text-slate-400">Avg Time Saved / Ticket</span>
              <div className="text-2xl font-bold text-purple-400">13.3 mins</div>
              <p className="text-[11px] text-slate-400">Instant database tool lookups</p>
            </div>
          </div>

          {/* Sentiment Breakdown & Intent Clustering */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Sentiment Breakdown */}
            <div className="p-6 rounded-2xl bg-slate-900/70 border border-slate-800/80 space-y-6 shadow-xl">
              <div>
                <h3 className="text-sm font-bold text-white flex items-center gap-2">
                  <Smile className="w-4 h-4 text-emerald-400" />
                  <span>Customer Sentiment Distribution</span>
                </h3>
                <p className="text-[11px] text-slate-400">Real-time classification based on linguistic emotion markers</p>
              </div>

              {/* Progress Bar Distribution */}
              <div className="space-y-4">
                {sentimentData.map((s, idx) => (
                  <div key={idx} className="space-y-1.5">
                    <div className="flex justify-between text-xs font-semibold">
                      <span className={s.text}>{s.sentiment}</span>
                      <span className="text-slate-300">{s.count} ({s.percentage}%)</span>
                    </div>
                    <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
                      <div className={`h-full rounded-full ${s.color}`} style={{ width: `${s.percentage}%` }}></div>
                    </div>
                  </div>
                ))}
              </div>

              <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 text-xs text-slate-300 space-y-1">
                <strong className="text-white">Angry Sentiment Escalation Guard:</strong>
                <p className="text-slate-400 text-[11px]">
                  When a customer message is classified as ANGRY (2.5% of total volume), SupportIQ AI immediately halts automated text, generates an urgent ticket, and pages human support agents.
                </p>
              </div>
            </div>

            {/* Support Intent Clustering */}
            <div className="p-6 rounded-2xl bg-slate-900/70 border border-slate-800/80 space-y-6 shadow-xl">
              <div>
                <h3 className="text-sm font-bold text-white flex items-center gap-2">
                  <Activity className="w-4 h-4 text-indigo-400" />
                  <span>Support Inquiries by Intent Category</span>
                </h3>
                <p className="text-[11px] text-slate-400">Top recurring customer problems and automated solutions</p>
              </div>

              <div className="space-y-3.5">
                {intentData.map((item, idx) => (
                  <div key={idx} className="flex items-center justify-between p-3 rounded-xl bg-slate-950 border border-slate-800 text-xs">
                    <div className="flex items-center gap-3">
                      <span className="w-6 h-6 rounded-lg bg-indigo-950 text-indigo-400 flex items-center justify-center font-bold text-[10px]">
                        {idx + 1}
                      </span>
                      <span className="font-semibold text-white">{item.intent.replace("_", " ")}</span>
                    </div>
                    <div className="flex items-center gap-3">
                      <span className="text-slate-400 font-mono">{item.count} threads</span>
                      <span className="text-indigo-400 font-bold bg-indigo-950/60 border border-indigo-800 px-2 py-0.5 rounded">
                        {item.percentage}%
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
