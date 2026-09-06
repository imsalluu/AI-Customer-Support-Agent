"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import {
  Activity,
  AlertTriangle,
  ArrowDownRight,
  ArrowUpRight,
  BarChart3,
  Bot,
  CheckCircle2,
  Clock,
  ExternalLink,
  Headphones,
  HelpCircle,
  Lightbulb,
  MessageSquare,
  ShieldCheck,
  Sparkles,
  Star,
  Ticket,
  TrendingUp,
  Users,
  Zap,
} from "lucide-react";
import Header from "@/components/layout/Header";
import Sidebar from "@/components/layout/Sidebar";
import { fetchApi } from "@/lib/api";

export default function DashboardPage() {
  const [overview, setOverview] = useState({
    total_conversations: 142,
    ai_resolved_count: 118,
    ai_resolution_rate: 84.5,
    human_escalated_count: 24,
    escalation_rate: 15.5,
    open_tickets_count: 12,
    total_tickets_count: 38,
    avg_response_time_seconds: 1.2,
    csat_score: 4.8,
    total_feedbacks: 89,
    positive_sentiment_percent: 76.5,
    negative_sentiment_percent: 8.2,
  });

  const [intents, setIntents] = useState([
    { intent: "ORDER_STATUS", count: 42, percentage: 35.0 },
    { intent: "SHIPPING", count: 28, percentage: 23.3 },
    { intent: "PRODUCT_INFO", count: 22, percentage: 18.3 },
    { intent: "RETURN", count: 15, percentage: 12.5 },
    { intent: "REFUND", count: 8, percentage: 6.7 },
    { intent: "COMPLAINT", count: 5, percentage: 4.2 },
  ]);

  const [insights, setInsights] = useState([
    {
      id: "ins-1",
      category: "Shipping & Fulfillment",
      title: "Shipping-related questions increased 24% this week",
      description: "Customers are inquiring about holiday transit timelines. Average response time remained 1.1s with 91% automated resolution.",
      metric_change: "+24% Volume",
      severity: "INFO",
      recommended_action: "Update the Shipping FAQ knowledge chunk with estimated holiday courier cutoffs.",
    },
    {
      id: "ins-2",
      category: "Refunds & Returns",
      title: "89% of Return inquiries resolved on first turn without escalation",
      description: "Controlled tool execution for get_order_status and RAG return policy retrieval eliminated manual agent intervention.",
      metric_change: "89% Auto-Resolved",
      severity: "SUCCESS",
      recommended_action: "Keep existing return policy knowledge base chunks active.",
    },
  ]);

  useEffect(() => {
    async function loadData() {
      try {
        const ov = await fetchApi<any>("/analytics/overview");
        if (ov) setOverview(ov);
      } catch (e) {}

      try {
        const ins = await fetchApi<any[]>("/analytics/insights");
        if (ins && ins.length > 0) setInsights(ins);
      } catch (e) {}

      try {
        const intList = await fetchApi<any[]>("/analytics/intents");
        if (intList && intList.length > 0) setIntents(intList);
      } catch (e) {}
    }
    loadData();
  }, []);

  return (
    <div className="min-h-screen bg-[#070b14] flex">
      <Sidebar />
      <div className="flex-1 ml-64 flex flex-col min-w-0">
        <Header />

        <main className="flex-1 p-8 space-y-8 max-w-7xl w-full mx-auto">
          {/* Top Welcome & KPI Header */}
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-2xl font-bold text-white tracking-tight">Support Intelligence Overview</h1>
                <span className="px-2.5 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 text-xs font-semibold">
                  Live Operations
                </span>
              </div>
              <p className="text-xs text-slate-400 mt-1">
                Real-time metrics, AI resolution performance, and proactive issue detection for Apex Commerce Inc.
              </p>
            </div>

            <div className="flex items-center gap-3">
              <Link
                href="/conversations"
                className="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs transition-all shadow-md shadow-indigo-600/30 flex items-center gap-2"
              >
                <MessageSquare className="w-3.5 h-3.5" />
                <span>Open Live Support Inbox</span>
              </Link>
            </div>
          </div>

          {/* KPI Summary Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {/* Card 1: AI Resolution Rate */}
            <div className="p-5 rounded-2xl bg-gradient-to-b from-slate-900/80 to-slate-900/40 border border-slate-800/80 shadow-lg relative overflow-hidden space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-medium text-slate-400">AI Resolution Rate</span>
                <div className="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-400 flex items-center justify-center">
                  <Bot className="w-4 h-4" />
                </div>
              </div>
              <div className="flex items-baseline gap-2">
                <span className="text-3xl font-extrabold text-white">{overview.ai_resolution_rate}%</span>
                <span className="text-xs text-emerald-400 font-semibold flex items-center">
                  <ArrowUpRight className="w-3.5 h-3.5" /> +4.2%
                </span>
              </div>
              <div className="text-[11px] text-slate-400">
                <strong className="text-slate-200">{overview.ai_resolved_count}</strong> of {overview.total_conversations} conversations resolved by AI
              </div>
              <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                <div className="bg-emerald-500 h-full rounded-full" style={{ width: `${overview.ai_resolution_rate}%` }}></div>
              </div>
            </div>

            {/* Card 2: Average Response Time */}
            <div className="p-5 rounded-2xl bg-gradient-to-b from-slate-900/80 to-slate-900/40 border border-slate-800/80 shadow-lg space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-medium text-slate-400">Avg AI Response Speed</span>
                <div className="w-8 h-8 rounded-lg bg-indigo-500/10 text-indigo-400 flex items-center justify-center">
                  <Zap className="w-4 h-4" />
                </div>
              </div>
              <div className="flex items-baseline gap-2">
                <span className="text-3xl font-extrabold text-indigo-300">{overview.avg_response_time_seconds}s</span>
                <span className="text-xs text-indigo-400 font-semibold flex items-center">
                  <TrendingUp className="w-3.5 h-3.5" /> 98.4% faster
                </span>
              </div>
              <div className="text-[11px] text-slate-400">
                Human agent avg benchmark: <span className="text-slate-300 font-medium">14.5 mins</span>
              </div>
              <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                <div className="bg-indigo-500 h-full rounded-full" style={{ width: "95%" }}></div>
              </div>
            </div>

            {/* Card 3: CSAT Score */}
            <div className="p-5 rounded-2xl bg-gradient-to-b from-slate-900/80 to-slate-900/40 border border-slate-800/80 shadow-lg space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-medium text-slate-400">Customer CSAT Score</span>
                <div className="w-8 h-8 rounded-lg bg-amber-500/10 text-amber-400 flex items-center justify-center">
                  <Star className="w-4 h-4 fill-amber-400" />
                </div>
              </div>
              <div className="flex items-baseline gap-2">
                <span className="text-3xl font-extrabold text-white">{overview.csat_score} <span className="text-sm font-normal text-slate-500">/ 5.0</span></span>
                <span className="text-xs text-amber-400 font-semibold">★ 96% Pos</span>
              </div>
              <div className="text-[11px] text-slate-400">
                Based on <strong className="text-slate-200">{overview.total_feedbacks}</strong> customer resolution ratings
              </div>
              <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                <div className="bg-amber-400 h-full rounded-full" style={{ width: `${(overview.csat_score / 5) * 100}%` }}></div>
              </div>
            </div>

            {/* Card 4: Open Tickets & Escalations */}
            <div className="p-5 rounded-2xl bg-gradient-to-b from-slate-900/80 to-slate-900/40 border border-slate-800/80 shadow-lg space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-medium text-slate-400">Escalated Tickets</span>
                <div className="w-8 h-8 rounded-lg bg-rose-500/10 text-rose-400 flex items-center justify-center">
                  <Ticket className="w-4 h-4" />
                </div>
              </div>
              <div className="flex items-baseline gap-2">
                <span className="text-3xl font-extrabold text-white">{overview.open_tickets_count}</span>
                <span className="text-xs text-slate-400 font-medium">of {overview.total_tickets_count} total</span>
              </div>
              <div className="text-[11px] text-slate-400">
                Escalation Rate: <strong className="text-rose-400">{overview.escalation_rate}%</strong> (Human Handled)
              </div>
              <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                <div className="bg-rose-500 h-full rounded-full" style={{ width: `${overview.escalation_rate * 2}%` }}></div>
              </div>
            </div>
          </div>

          {/* AI Weekly Proactive Support Insights Card */}
          <div className="p-6 rounded-2xl bg-gradient-to-r from-indigo-950/40 via-purple-950/30 to-slate-900 border border-indigo-500/30 shadow-xl space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <div className="w-8 h-8 rounded-xl bg-indigo-600 flex items-center justify-center text-white shadow-md shadow-indigo-600/30">
                  <Sparkles className="w-4 h-4" />
                </div>
                <div>
                  <h3 className="text-sm font-bold text-white">AI Support Intelligence — Weekly Diagnostics</h3>
                  <p className="text-[11px] text-slate-400">Autonomous pattern recognition & bottleneck detection</p>
                </div>
              </div>
              <span className="text-[11px] px-2.5 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 font-semibold">
                Updated Today
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
              {insights.map((ins) => (
                <div key={ins.id} className="p-4 rounded-xl bg-slate-900/80 border border-slate-800/90 space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-bold uppercase tracking-wider text-indigo-400">{ins.category}</span>
                    <span className="text-xs font-bold text-emerald-400 bg-emerald-950/40 border border-emerald-500/30 px-2 py-0.5 rounded-md">
                      {ins.metric_change}
                    </span>
                  </div>
                  <h4 className="text-xs font-bold text-white">{ins.title}</h4>
                  <p className="text-[11px] text-slate-400 leading-relaxed">{ins.description}</p>
                  {ins.recommended_action && (
                    <div className="pt-2 border-t border-slate-800/60 flex items-center gap-1.5 text-[11px] text-amber-300 font-medium">
                      <Lightbulb className="w-3.5 h-3.5 text-amber-400 shrink-0" />
                      <span>Action: {ins.recommended_action}</span>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Bottom Grid: 7-Day Volume Trend & Intent Distribution */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Left 2 Cols: 7-Day Conversation Volume */}
            <div className="lg:col-span-2 p-6 rounded-2xl bg-slate-900/70 border border-slate-800/80 shadow-xl space-y-6">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-sm font-bold text-white">7-Day Conversation & Resolution Trends</h3>
                  <p className="text-[11px] text-slate-400">Daily support query volume categorized by resolution path</p>
                </div>
                <div className="flex items-center gap-4 text-xs">
                  <div className="flex items-center gap-1.5 text-slate-300">
                    <span className="w-2.5 h-2.5 rounded-full bg-indigo-500"></span>
                    <span>AI Resolved</span>
                  </div>
                  <div className="flex items-center gap-1.5 text-slate-300">
                    <span className="w-2.5 h-2.5 rounded-full bg-rose-400"></span>
                    <span>Human Escalated</span>
                  </div>
                </div>
              </div>

              {/* Bar Chart Visualization */}
              <div className="h-48 flex items-end gap-4 pt-4 border-b border-slate-800 pb-2">
                {[
                  { day: "Mon", ai: 18, human: 3 },
                  { day: "Tue", ai: 24, human: 4 },
                  { day: "Wed", ai: 21, human: 2 },
                  { day: "Thu", ai: 28, human: 5 },
                  { day: "Fri", ai: 32, human: 6 },
                  { day: "Sat", ai: 19, human: 2 },
                  { day: "Sun", ai: 16, human: 2 },
                ].map((d, idx) => {
                  const maxVal = 38;
                  const aiHeight = (d.ai / maxVal) * 100;
                  const humanHeight = (d.human / maxVal) * 100;
                  return (
                    <div key={idx} className="flex-1 flex flex-col items-center gap-2 h-full justify-end">
                      <div className="w-full max-w-[36px] flex flex-col gap-1 items-center justify-end h-full">
                        <div
                          className="w-full bg-rose-400/80 rounded-t-md transition-all hover:bg-rose-400"
                          style={{ height: `${humanHeight}%` }}
                          title={`Human: ${d.human}`}
                        ></div>
                        <div
                          className="w-full bg-indigo-600 rounded-b-md transition-all hover:bg-indigo-500"
                          style={{ height: `${aiHeight}%` }}
                          title={`AI Resolved: ${d.ai}`}
                        ></div>
                      </div>
                      <span className="text-[11px] text-slate-400 font-medium">{d.day}</span>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Right 1 Col: Top Support Intents */}
            <div className="p-6 rounded-2xl bg-slate-900/70 border border-slate-800/80 shadow-xl space-y-4">
              <div>
                <h3 className="text-sm font-bold text-white">Top Support Inquiries (Intents)</h3>
                <p className="text-[11px] text-slate-400">Classified automatically by LangGraph classifier</p>
              </div>

              <div className="space-y-3.5 pt-2">
                {intents.map((item, idx) => (
                  <div key={idx} className="space-y-1.5">
                    <div className="flex justify-between text-xs font-medium">
                      <span className="text-slate-300">{item.intent.replace("_", " ")}</span>
                      <span className="text-slate-400 font-semibold">{item.count} ({item.percentage}%)</span>
                    </div>
                    <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                      <div
                        className={`h-full rounded-full ${
                          idx === 0 ? "bg-indigo-500" : idx === 1 ? "bg-purple-500" : idx === 2 ? "bg-blue-500" : "bg-slate-500"
                        }`}
                        style={{ width: `${item.percentage}%` }}
                      ></div>
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
