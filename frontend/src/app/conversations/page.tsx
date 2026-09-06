"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import {
  AlertCircle,
  AlertTriangle,
  ArrowRight,
  Bot,
  CheckCircle,
  CheckCircle2,
  Clock,
  CornerDownLeft,
  DollarSign,
  ExternalLink,
  FileText,
  Filter,
  Globe,
  Headphones,
  Mail,
  MessageSquare,
  Package,
  Phone,
  Plus,
  RefreshCw,
  Search,
  Send,
  Shield,
  Sparkles,
  Ticket,
  Truck,
  User,
  UserCheck,
  UserX,
  Zap,
} from "lucide-react";
import Header from "@/components/layout/Header";
import Sidebar from "@/components/layout/Sidebar";
import { fetchApi } from "@/lib/api";

export default function ConversationsPage() {
  const [conversations, setConversations] = useState<any[]>([]);
  const [selectedConvId, setSelectedConvId] = useState<string | null>(null);
  const [activeConv, setActiveConv] = useState<any | null>(null);
  const [filterStatus, setFilterStatus] = useState<string>("ALL");
  const [searchQuery, setSearchQuery] = useState("");
  const [agentInput, setAgentInput] = useState("");
  const [loading, setLoading] = useState(true);

  // Load conversations
  useEffect(() => {
    async function loadConversations() {
      try {
        const data = await fetchApi<any[]>("/conversations");
        if (data && data.length > 0) {
          setConversations(data);
          setSelectedConvId(data[0].id);
          setActiveConv(data[0]);
        }
      } catch (e) {
        // Fallback default mock data for instant interaction
        const mockConvs = [
          {
            id: "conv-1",
            customer_name: "Emma Watson",
            customer_email: "emma.watson@example.com",
            customer_phone: "+1-555-0101",
            customer_total_orders: 3,
            customer_lifetime_value: 728.98,
            channel: "WEBCHAT",
            status: "RESOLVED",
            current_intent: "ORDER_STATUS",
            sentiment: "POSITIVE",
            confidence_score: 0.98,
            summary: "Customer verified status of order ORD-10022. AI verified In Transit via FedEx.",
            messages: [
              { id: "m1", sender_type: "CUSTOMER", content: "Hi! Can you check the status of my order ORD-10022?", created_at: "2026-09-06T14:10:00Z" },
              { id: "m2", sender_type: "AI", content: "I've verified your order **ORD-10022**. Current status is **IN_TRANSIT** via **FedEx** (Tracking: `FDX-998823`). Estimated delivery is in 2 days to your address in Boston, MA.", sources_json: "[]", tool_calls_json: '[{"tool_name": "get_order_status", "arguments": {"order_id_or_number": "ORD-10022"}, "output": {"found": true, "status": "IN_TRANSIT"}}]', created_at: "2026-09-06T14:10:02Z" },
              { id: "m3", sender_type: "CUSTOMER", content: "Awesome, thank you so much!", created_at: "2026-09-06T14:10:30Z" },
            ],
          },
          {
            id: "conv-2",
            customer_name: "David Miller",
            customer_email: "david.miller@example.com",
            customer_phone: "+1-555-0102",
            customer_total_orders: 1,
            customer_lifetime_value: 249.99,
            channel: "WHATSAPP",
            status: "WAITING_HUMAN",
            current_intent: "COMPLAINT",
            sentiment: "ANGRY",
            confidence_score: 1.0,
            summary: "Customer received incorrect color item with high frustration. AI auto-escalated to human specialist.",
            messages: [
              { id: "c2m1", sender_type: "CUSTOMER", content: "I ordered the Black headphones and you sent me Silver! This is completely unacceptable, connect me to a person right now!", created_at: "2026-09-06T16:00:00Z" },
              { id: "c2m2", sender_type: "AI", content: "I understand your frustration and I sincerely apologize for sending the wrong color. I have prioritized your request and am immediately transferring you to a human support specialist. An urgent ticket has been created.", tool_calls_json: '[{"tool_name": "request_human_agent", "arguments": {"reason": "Customer angry about wrong item", "urgency": "URGENT"}}]', created_at: "2026-09-06T16:00:01Z" },
            ],
          },
          {
            id: "conv-3",
            customer_name: "Sophia Chen",
            customer_email: "sophia.chen@example.com",
            customer_phone: "+1-555-0103",
            customer_total_orders: 4,
            customer_lifetime_value: 1120.50,
            channel: "EMAIL",
            status: "HUMAN_ACTIVE",
            current_intent: "PAYMENT",
            sentiment: "NEUTRAL",
            confidence_score: 0.85,
            summary: "Corporate invoice with VAT tax ID requested for Q3 filings. Handled by Marcus Vance.",
            messages: [
              { id: "c3m1", sender_type: "CUSTOMER", content: "Hello Support, we need a customized PDF VAT invoice for order ORD-10024 under corporate entity Chen Technologies.", created_at: "2026-09-06T12:00:00Z" },
              { id: "c3m2", sender_type: "AGENT", content: "Hello Sophia, I have generated and attached your official corporate VAT tax invoice for ORD-10024. Please let me know if you need any adjustments!", created_at: "2026-09-06T12:15:00Z" },
            ],
          },
        ];
        setConversations(mockConvs);
        setSelectedConvId(mockConvs[0].id);
        setActiveConv(mockConvs[0]);
      } finally {
        setLoading(false);
      }
    }
    loadConversations();
  }, []);

  const handleSelectConv = async (conv: any) => {
    setSelectedConvId(conv.id);
    try {
      const detailed = await fetchApi<any>(`/conversations/${conv.id}`);
      setActiveConv(detailed);
    } catch (e) {
      setActiveConv(conv);
    }
  };

  const handleTakeover = async () => {
    if (!activeConv) return;
    try {
      const updated = await fetchApi<any>(`/conversations/${activeConv.id}/takeover`, { method: "POST" });
      setActiveConv(updated);
      setConversations(conversations.map((c) => (c.id === updated.id ? updated : c)));
    } catch (e) {
      const updated = { ...activeConv, status: "HUMAN_ACTIVE" };
      setActiveConv(updated);
    }
  };

  const handleReleaseToAI = async () => {
    if (!activeConv) return;
    try {
      const updated = await fetchApi<any>(`/conversations/${activeConv.id}/release`, { method: "POST" });
      setActiveConv(updated);
      setConversations(conversations.map((c) => (c.id === updated.id ? updated : c)));
    } catch (e) {
      const updated = { ...activeConv, status: "AI_ACTIVE" };
      setActiveConv(updated);
    }
  };

  const handleResolve = async () => {
    if (!activeConv) return;
    try {
      const updated = await fetchApi<any>(`/conversations/${activeConv.id}/resolve`, { method: "POST" });
      setActiveConv(updated);
      setConversations(conversations.map((c) => (c.id === updated.id ? updated : c)));
    } catch (e) {
      const updated = { ...activeConv, status: "RESOLVED" };
      setActiveConv(updated);
    }
  };

  const handleSendAgentReply = async () => {
    if (!agentInput.trim() || !activeConv) return;
    const text = agentInput.trim();
    setAgentInput("");

    try {
      const newMsg = await fetchApi<any>(`/conversations/${activeConv.id}/messages`, {
        method: "POST",
        body: JSON.stringify({ content: text, sender_type: "AGENT" }),
      });
      const updatedMessages = [...(activeConv.messages || []), newMsg];
      const updatedConv = { ...activeConv, messages: updatedMessages, status: "HUMAN_ACTIVE" };
      setActiveConv(updatedConv);
      setConversations(conversations.map((c) => (c.id === updatedConv.id ? updatedConv : c)));
    } catch (e) {
      const mockMsg = {
        id: `m_${Date.now()}`,
        sender_type: "AGENT",
        content: text,
        created_at: new Date().toISOString(),
      };
      const updatedConv = {
        ...activeConv,
        status: "HUMAN_ACTIVE",
        messages: [...(activeConv.messages || []), mockMsg],
      };
      setActiveConv(updatedConv);
    }
  };

  const filteredConversations = conversations.filter((c) => {
    if (filterStatus !== "ALL" && c.status !== filterStatus) return false;
    if (searchQuery) {
      const q = searchQuery.toLowerCase();
      const matchName = c.customer_name?.toLowerCase().includes(q);
      const matchSummary = c.summary?.toLowerCase().includes(q);
      return matchName || matchSummary;
    }
    return true;
  });

  return (
    <div className="min-h-screen bg-[#070b14] flex">
      <Sidebar />
      <div className="flex-1 ml-64 flex flex-col min-w-0 h-screen">
        <Header />

        {/* 3-Column Layout */}
        <div className="flex-1 flex overflow-hidden">
          {/* Column 1: Conversations List (Left) */}
          <div className="w-80 bg-[#0a0f1d] border-r border-slate-800 flex flex-col h-full">
            {/* Search & Filter Header */}
            <div className="p-4 border-b border-slate-800/80 space-y-3">
              <div className="flex items-center justify-between">
                <h2 className="text-sm font-bold text-white flex items-center gap-2">
                  <MessageSquare className="w-4 h-4 text-indigo-400" />
                  <span>Support Inbox</span>
                </h2>
                <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-slate-800 text-slate-400">
                  {filteredConversations.length} Threads
                </span>
              </div>

              {/* Search Bar */}
              <div className="relative">
                <Search className="w-3.5 h-3.5 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2" />
                <input
                  type="text"
                  placeholder="Filter threads..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-800 rounded-xl pl-8.5 pr-3 py-1.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                />
              </div>

              {/* Status Filter Tabs */}
              <div className="flex gap-1 overflow-x-auto pb-1 text-[11px] font-semibold">
                {["ALL", "AI_ACTIVE", "WAITING_HUMAN", "HUMAN_ACTIVE", "RESOLVED"].map((st) => (
                  <button
                    key={st}
                    onClick={() => setFilterStatus(st)}
                    className={`px-2.5 py-1 rounded-lg transition-all whitespace-nowrap ${
                      filterStatus === st
                        ? "bg-indigo-600 text-white shadow-sm"
                        : "text-slate-400 hover:bg-slate-800 hover:text-slate-200"
                    }`}
                  >
                    {st.replace("_", " ")}
                  </button>
                ))}
              </div>
            </div>

            {/* Thread List */}
            <div className="flex-1 overflow-y-auto divide-y divide-slate-800/50">
              {filteredConversations.map((c) => {
                const isSelected = selectedConvId === c.id;
                return (
                  <div
                    key={c.id}
                    onClick={() => handleSelectConv(c)}
                    className={`p-4 cursor-pointer transition-colors ${
                      isSelected
                        ? "bg-slate-800/80 border-l-4 border-indigo-500"
                        : "hover:bg-slate-900/60"
                    }`}
                  >
                    <div className="flex items-center justify-between mb-1.5">
                      <div className="flex items-center gap-2">
                        <span className="text-xs font-bold text-white">{c.customer_name}</span>
                        {c.channel === "WHATSAPP" && <span className="text-[9px] bg-emerald-950 text-emerald-400 border border-emerald-800/50 px-1.5 rounded">WhatsApp</span>}
                        {c.channel === "WEBCHAT" && <span className="text-[9px] bg-indigo-950 text-indigo-400 border border-indigo-800/50 px-1.5 rounded">WebChat</span>}
                        {c.channel === "EMAIL" && <span className="text-[9px] bg-blue-950 text-blue-400 border border-blue-800/50 px-1.5 rounded">Email</span>}
                      </div>
                      <span className="text-[10px] text-slate-400">Live</span>
                    </div>

                    <p className="text-[11px] text-slate-300 line-clamp-2 leading-relaxed">
                      {c.summary || (c.messages && c.messages[c.messages.length - 1]?.content) || "No messages yet."}
                    </p>

                    <div className="flex items-center justify-between mt-2 pt-1">
                      <span
                        className={`text-[9px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full ${
                          c.status === "WAITING_HUMAN"
                            ? "bg-rose-500/20 text-rose-300 border border-rose-500/30"
                            : c.status === "HUMAN_ACTIVE"
                            ? "bg-purple-500/20 text-purple-300 border border-purple-500/30"
                            : c.status === "RESOLVED"
                            ? "bg-slate-800 text-slate-400"
                            : "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30"
                        }`}
                      >
                        {c.status.replace("_", " ")}
                      </span>

                      {c.sentiment && (
                        <span
                          className={`text-[9px] font-semibold px-1.5 py-0.5 rounded ${
                            c.sentiment === "ANGRY"
                              ? "bg-rose-950 text-rose-400"
                              : c.sentiment === "POSITIVE"
                              ? "bg-emerald-950 text-emerald-400"
                              : "bg-slate-800 text-slate-400"
                          }`}
                        >
                          {c.sentiment}
                        </span>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Column 2: Live Chat Stream & Action Controls (Center) */}
          <div className="flex-1 bg-[#090d16] flex flex-col h-full min-w-0 border-r border-slate-800">
            {activeConv ? (
              <>
                {/* Chat Top Controls */}
                <div className="p-4 bg-slate-900/80 border-b border-slate-800 flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-9 h-9 rounded-xl bg-indigo-600/30 border border-indigo-500/40 text-indigo-300 flex items-center justify-center font-bold text-xs">
                      {activeConv.customer_name?.charAt(0) || "C"}
                    </div>
                    <div>
                      <h3 className="text-sm font-bold text-white flex items-center gap-2">
                        {activeConv.customer_name}
                        <span className="text-[10px] text-slate-400 font-normal">({activeConv.customer_email || "No email"})</span>
                      </h3>
                      <div className="flex items-center gap-2 text-[11px] text-slate-400">
                        <span>Status: <strong className="text-indigo-400">{activeConv.status}</strong></span>
                        <span>•</span>
                        <span>Intent: <strong className="text-slate-200">{activeConv.current_intent}</strong></span>
                      </div>
                    </div>
                  </div>

                  {/* Takeover / Release / Resolve Buttons */}
                  <div className="flex items-center gap-2">
                    {activeConv.status === "HUMAN_ACTIVE" ? (
                      <button
                        onClick={handleReleaseToAI}
                        className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-indigo-600/20 text-indigo-300 border border-indigo-500/30 text-xs font-semibold hover:bg-indigo-600 hover:text-white transition-all"
                      >
                        <Bot className="w-3.5 h-3.5" />
                        <span>Return to AI</span>
                      </button>
                    ) : (
                      <button
                        onClick={handleTakeover}
                        className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-purple-600/20 text-purple-300 border border-purple-500/30 text-xs font-semibold hover:bg-purple-600 hover:text-white transition-all"
                      >
                        <UserCheck className="w-3.5 h-3.5" />
                        <span>Take Over</span>
                      </button>
                    )}

                    {activeConv.status !== "RESOLVED" && (
                      <button
                        onClick={handleResolve}
                        className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-emerald-600/20 text-emerald-300 border border-emerald-500/30 text-xs font-semibold hover:bg-emerald-600 hover:text-white transition-all"
                      >
                        <CheckCircle2 className="w-3.5 h-3.5" />
                        <span>Resolve</span>
                      </button>
                    )}
                  </div>
                </div>

                {/* Messages Stream */}
                <div className="flex-1 p-6 overflow-y-auto space-y-4 bg-slate-950/40">
                  {activeConv.messages?.map((msg: any) => {
                    const isCustomer = msg.sender_type === "CUSTOMER";
                    const isAi = msg.sender_type === "AI";
                    const isAgent = msg.sender_type === "AGENT";
                    const isSystem = msg.sender_type === "SYSTEM";

                    if (isSystem) {
                      return (
                        <div key={msg.id} className="flex justify-center my-2">
                          <span className="text-[11px] bg-slate-800 text-slate-400 px-3 py-1 rounded-full border border-slate-700">
                            {msg.content}
                          </span>
                        </div>
                      );
                    }

                    return (
                      <div
                        key={msg.id}
                        className={`flex flex-col ${isCustomer ? "items-start" : "items-end"}`}
                      >
                        <div className="flex items-center gap-1.5 mb-1 px-1">
                          <span className="text-[10px] font-bold text-slate-400 uppercase">
                            {isCustomer ? activeConv.customer_name : isAi ? "SupportIQ AI" : "Agent Alex"}
                          </span>
                        </div>

                        <div
                          className={`max-w-xl p-4 rounded-2xl text-xs md:text-sm leading-relaxed ${
                            isCustomer
                              ? "bg-slate-800 text-slate-100 border border-slate-700 rounded-tl-none"
                              : isAi
                              ? "bg-indigo-950/60 border border-indigo-500/30 text-indigo-100 rounded-tr-none shadow-md shadow-indigo-950/50"
                              : "bg-purple-950/60 border border-purple-500/30 text-purple-100 rounded-tr-none"
                          }`}
                        >
                          <p className="whitespace-pre-line">{msg.content}</p>

                          {/* Tool execution badge */}
                          {msg.tool_calls_json && msg.tool_calls_json !== "[]" && (
                            <div className="mt-2.5 pt-2 border-t border-indigo-500/20 flex flex-wrap gap-1.5">
                              {JSON.parse(msg.tool_calls_json).map((tc: any, tIdx: number) => (
                                <span
                                  key={tIdx}
                                  className="text-[10px] font-mono bg-indigo-900/40 text-indigo-300 border border-indigo-700/50 px-2 py-0.5 rounded-md flex items-center gap-1"
                                >
                                  <Zap className="w-3 h-3 text-indigo-400" />
                                  <span>{tc.tool_name}()</span>
                                </span>
                              ))}
                            </div>
                          )}

                          {/* Citations badge */}
                          {msg.sources_json && msg.sources_json !== "[]" && (
                            <div className="mt-2 pt-2 border-t border-indigo-500/20 text-[10px] text-indigo-300 flex items-center gap-1.5">
                              <FileText className="w-3 h-3 text-indigo-400" />
                              <span>Verified from Knowledge Base policy</span>
                            </div>
                          )}
                        </div>
                      </div>
                    );
                  })}
                </div>

                {/* Agent Reply Composer */}
                <div className="p-4 bg-slate-900/90 border-t border-slate-800 space-y-2">
                  <div className="flex gap-2">
                    <input
                      type="text"
                      value={agentInput}
                      onChange={(e) => setAgentInput(e.target.value)}
                      onKeyDown={(e) => e.key === "Enter" && handleSendAgentReply()}
                      placeholder="Type your official agent response (taking over chat)..."
                      className="flex-1 bg-slate-950 border border-slate-700 rounded-xl px-4 py-2.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                    />
                    <button
                      onClick={handleSendAgentReply}
                      className="px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs transition-all flex items-center gap-2 shadow-md shadow-indigo-600/30"
                    >
                      <Send className="w-3.5 h-3.5" />
                      <span>Reply</span>
                    </button>
                  </div>
                </div>
              </>
            ) : (
              <div className="flex-1 flex items-center justify-center text-slate-500 text-xs">
                Select a support conversation to view messages
              </div>
            )}
          </div>

          {/* Column 3: Customer 360 Diagnostics (Right) */}
          <div className="w-80 bg-[#0a0f1d] border-l border-slate-800 flex flex-col h-full overflow-y-auto p-5 space-y-6">
            {activeConv ? (
              <>
                {/* Customer Profile Card */}
                <div className="space-y-3 pb-4 border-b border-slate-800">
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Customer 360</span>
                    <span className="text-[10px] font-semibold bg-indigo-500/20 text-indigo-300 px-2 py-0.5 rounded-full border border-indigo-500/30">
                      VIP Client
                    </span>
                  </div>

                  <div>
                    <h3 className="text-sm font-bold text-white">{activeConv.customer_name}</h3>
                    <p className="text-xs text-slate-400">{activeConv.customer_email || "No email"}</p>
                    <p className="text-xs text-slate-400">{activeConv.customer_phone || "No phone"}</p>
                  </div>

                  <div className="grid grid-cols-2 gap-2 pt-1 text-center">
                    <div className="p-2.5 rounded-xl bg-slate-900 border border-slate-800">
                      <div className="text-xs font-bold text-white">${activeConv.customer_lifetime_value || 249.99}</div>
                      <div className="text-[10px] text-slate-400">Lifetime Value</div>
                    </div>
                    <div className="p-2.5 rounded-xl bg-slate-900 border border-slate-800">
                      <div className="text-xs font-bold text-white">{activeConv.customer_total_orders || 1} Orders</div>
                      <div className="text-[10px] text-slate-400">Total Purchases</div>
                    </div>
                  </div>
                </div>

                {/* AI Diagnostics Meter */}
                <div className="space-y-3 pb-4 border-b border-slate-800">
                  <span className="text-[10px] font-bold uppercase tracking-wider text-indigo-400">AI Diagnostics</span>

                  <div className="space-y-2 text-xs">
                    <div className="flex justify-between">
                      <span className="text-slate-400">Detected Intent:</span>
                      <span className="font-semibold text-white">{activeConv.current_intent}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">Customer Sentiment:</span>
                      <span
                        className={`font-semibold ${
                          activeConv.sentiment === "ANGRY"
                            ? "text-rose-400"
                            : activeConv.sentiment === "POSITIVE"
                            ? "text-emerald-400"
                            : "text-slate-300"
                        }`}
                      >
                        {activeConv.sentiment}
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-slate-400">Confidence Score:</span>
                      <span className="font-bold text-emerald-400">{Math.round((activeConv.confidence_score || 0.95) * 100)}%</span>
                    </div>
                    <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                      <div
                        className="bg-emerald-500 h-full rounded-full"
                        style={{ width: `${(activeConv.confidence_score || 0.95) * 100}%` }}
                      ></div>
                    </div>
                  </div>

                  {activeConv.summary && (
                    <div className="p-3 rounded-xl bg-slate-900/90 border border-slate-800 text-[11px] text-slate-300 leading-relaxed">
                      <strong className="text-white">Live Summary:</strong> {activeConv.summary}
                    </div>
                  )}
                </div>

                {/* Recent Orders Timeline */}
                <div className="space-y-3 pb-4 border-b border-slate-800">
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Recent Orders</span>
                    <Package className="w-3.5 h-3.5 text-slate-500" />
                  </div>

                  <div className="p-3 rounded-xl bg-slate-900 border border-slate-800 space-y-1.5 text-xs">
                    <div className="flex justify-between font-bold text-white">
                      <span>ORD-10022</span>
                      <span className="text-emerald-400 font-normal">IN_TRANSIT</span>
                    </div>
                    <p className="text-[11px] text-slate-400">Apex Pro Wireless Headphones</p>
                    <div className="flex items-center gap-1.5 text-[10px] text-indigo-300 font-mono">
                      <Truck className="w-3 h-3 text-indigo-400" />
                      <span>FedEx: FDX-998823</span>
                    </div>
                  </div>
                </div>

                {/* Quick Actions */}
                <div className="space-y-2">
                  <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Quick Actions</span>
                  <Link
                    href="/tickets"
                    className="w-full py-2 px-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold flex items-center justify-center gap-1.5 transition-colors"
                  >
                    <Plus className="w-3.5 h-3.5" />
                    <span>Create Support Ticket</span>
                  </Link>
                </div>
              </>
            ) : (
              <div className="text-xs text-slate-500">No conversation selected</div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
