"use client";

import React, { useEffect, useState } from "react";
import {
  AlertCircle,
  AlertTriangle,
  CheckCircle2,
  Clock,
  Filter,
  Plus,
  Search,
  Ticket,
  User,
} from "lucide-react";
import Header from "@/components/layout/Header";
import Sidebar from "@/components/layout/Sidebar";
import { fetchApi } from "@/lib/api";

export default function TicketsPage() {
  const [tickets, setTickets] = useState<any[]>([]);
  const [filterPriority, setFilterPriority] = useState<string>("ALL");
  const [searchQuery, setSearchQuery] = useState("");
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);

  // New ticket form state
  const [newSubject, setNewSubject] = useState("");
  const [newDesc, setNewDesc] = useState("");
  const [newPriority, setNewPriority] = useState("MEDIUM");
  const [newCategory, setNewCategory] = useState("GENERAL");

  useEffect(() => {
    async function loadTickets() {
      try {
        const data = await fetchApi<any[]>("/tickets");
        if (data && data.length > 0) setTickets(data);
      } catch (e) {
        setTickets([
          {
            id: "tck-1",
            ticket_number: "TCK-92811",
            subject: "Urgent: Wrong color delivered (Silver instead of Black)",
            description: "Customer received Silver headphones instead of Black on order ORD-10023. Urgent replacement needed.",
            status: "OPEN",
            priority: "URGENT",
            category: "COMPLAINT",
            customer_name: "David Miller",
            assigned_agent_name: "Sarah Jenkins",
            created_at: "2026-09-06T16:00:00Z",
          },
          {
            id: "tck-2",
            ticket_number: "TCK-92812",
            subject: "Bulk invoice copy request for Q3 tax filing",
            description: "Customer requesting PDF corporate tax invoice with VAT ID for order ORD-10024.",
            status: "IN_PROGRESS",
            priority: "MEDIUM",
            category: "PAYMENT",
            customer_name: "Sophia Chen",
            assigned_agent_name: "Marcus Vance",
            created_at: "2026-09-06T12:00:00Z",
          },
          {
            id: "tck-3",
            ticket_number: "TCK-92813",
            subject: "Return label generated for Smart Watch",
            description: "Pre-paid RMA label generated for 30-day return on order ORD-10021.",
            status: "RESOLVED",
            priority: "LOW",
            category: "RETURN",
            customer_name: "Emma Watson",
            assigned_agent_name: "Sarah Jenkins",
            created_at: "2026-09-05T09:30:00Z",
          },
        ]);
      }
    }
    loadTickets();
  }, []);

  const handleCreateTicket = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const created = await fetchApi<any>("/tickets", {
        method: "POST",
        body: JSON.stringify({
          customer_id: "demo_cust_1",
          subject: newSubject,
          description: newDesc,
          priority: newPriority,
          category: newCategory,
        }),
      });
      setTickets([created, ...tickets]);
      setIsCreateModalOpen(false);
      setNewSubject("");
      setNewDesc("");
    } catch (e) {
      const mockNew = {
        id: `tck_${Date.now()}`,
        ticket_number: `TCK-${Math.floor(10000 + Math.random() * 90000)}`,
        subject: newSubject,
        description: newDesc,
        status: "OPEN",
        priority: newPriority,
        category: newCategory,
        customer_name: "Walk-in Customer",
        created_at: new Date().toISOString(),
      };
      setTickets([mockNew, ...tickets]);
      setIsCreateModalOpen(false);
      setNewSubject("");
      setNewDesc("");
    }
  };

  const handleUpdateStatus = async (ticketId: string, nextStatus: string) => {
    try {
      await fetchApi<any>(`/tickets/${ticketId}`, {
        method: "PUT",
        body: JSON.stringify({ status: nextStatus }),
      });
      setTickets(tickets.map((t) => (t.id === ticketId ? { ...t, status: nextStatus } : t)));
    } catch (e) {
      setTickets(tickets.map((t) => (t.id === ticketId ? { ...t, status: nextStatus } : t)));
    }
  };

  const columns = ["OPEN", "IN_PROGRESS", "WAITING_CUSTOMER", "RESOLVED"];

  const filteredTickets = tickets.filter((t) => {
    if (filterPriority !== "ALL" && t.priority !== filterPriority) return false;
    if (searchQuery) {
      const q = searchQuery.toLowerCase();
      return (
        t.ticket_number?.toLowerCase().includes(q) ||
        t.subject?.toLowerCase().includes(q) ||
        t.customer_name?.toLowerCase().includes(q)
      );
    }
    return true;
  });

  return (
    <div className="min-h-screen bg-[#070b14] flex">
      <Sidebar />
      <div className="flex-1 ml-64 flex flex-col min-w-0">
        <Header />

        <main className="flex-1 p-8 space-y-6 max-w-7xl w-full mx-auto">
          {/* Header */}
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
                <Ticket className="w-6 h-6 text-indigo-400" />
                <span>Support Ticket Management</span>
              </h1>
              <p className="text-xs text-slate-400 mt-1">
                Kanban lifecycle tracking, SLA timers, and automatic AI escalation handling
              </p>
            </div>

            <div className="flex items-center gap-3">
              <button
                onClick={() => setIsCreateModalOpen(true)}
                className="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs transition-all shadow-md shadow-indigo-600/30 flex items-center gap-2"
              >
                <Plus className="w-4 h-4" />
                <span>Create New Ticket</span>
              </button>
            </div>
          </div>

          {/* Search & Priority Filter */}
          <div className="flex flex-wrap items-center justify-between gap-4 p-4 rounded-2xl bg-slate-900/60 border border-slate-800">
            <div className="relative flex-1 max-w-md">
              <Search className="w-3.5 h-3.5 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                placeholder="Search ticket #, subject, or customer..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-8.5 pr-3 py-1.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
              />
            </div>

            <div className="flex items-center gap-2 text-xs font-semibold">
              <span className="text-slate-400">Priority:</span>
              {["ALL", "URGENT", "HIGH", "MEDIUM", "LOW"].map((p) => (
                <button
                  key={p}
                  onClick={() => setFilterPriority(p)}
                  className={`px-3 py-1 rounded-lg transition-all ${
                    filterPriority === p
                      ? "bg-indigo-600 text-white shadow-sm"
                      : "text-slate-400 hover:bg-slate-800 hover:text-slate-200"
                  }`}
                >
                  {p}
                </button>
              ))}
            </div>
          </div>

          {/* Kanban Board */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {columns.map((colStatus) => {
              const colTickets = filteredTickets.filter((t) => t.status === colStatus);
              return (
                <div key={colStatus} className="flex flex-col gap-3">
                  <div className="flex items-center justify-between px-2">
                    <span className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-2">
                      <span
                        className={`w-2 h-2 rounded-full ${
                          colStatus === "OPEN"
                            ? "bg-indigo-400"
                            : colStatus === "IN_PROGRESS"
                            ? "bg-purple-400"
                            : colStatus === "WAITING_CUSTOMER"
                            ? "bg-amber-400"
                            : "bg-emerald-400"
                        }`}
                      ></span>
                      <span>{colStatus.replace("_", " ")}</span>
                    </span>
                    <span className="text-xs font-bold text-slate-400 bg-slate-800/80 px-2 py-0.5 rounded-full">
                      {colTickets.length}
                    </span>
                  </div>

                  {/* Ticket Cards List */}
                  <div className="space-y-3 flex-1 min-h-[400px] p-2 rounded-2xl bg-slate-900/40 border border-slate-800/60">
                    {colTickets.map((t) => (
                      <div
                        key={t.id}
                        className="p-4 rounded-xl bg-slate-800/80 border border-slate-700/60 shadow-md space-y-2.5 hover:border-indigo-500/50 transition-all"
                      >
                        <div className="flex items-center justify-between">
                          <span className="text-xs font-mono font-bold text-indigo-400">{t.ticket_number}</span>
                          <span
                            className={`text-[9px] font-bold px-2 py-0.5 rounded-full ${
                              t.priority === "URGENT"
                                ? "bg-rose-500/20 text-rose-300 border border-rose-500/30"
                                : t.priority === "HIGH"
                                ? "bg-amber-500/20 text-amber-300 border border-amber-500/30"
                                : "bg-slate-700 text-slate-300"
                            }`}
                          >
                            {t.priority}
                          </span>
                        </div>

                        <h4 className="text-xs font-bold text-white line-clamp-2 leading-relaxed">{t.subject}</h4>
                        <p className="text-[11px] text-slate-400 line-clamp-2">{t.description}</p>

                        <div className="pt-2 border-t border-slate-700/50 flex items-center justify-between text-[10px] text-slate-400">
                          <span className="flex items-center gap-1">
                            <User className="w-3 h-3 text-slate-500" />
                            <span>{t.customer_name || "Customer"}</span>
                          </span>
                          <span>{t.category}</span>
                        </div>

                        {/* Status Progression dropdown */}
                        <div className="pt-1 flex gap-1 justify-end">
                          {colStatus !== "RESOLVED" && (
                            <button
                              onClick={() => handleUpdateStatus(t.id, "RESOLVED")}
                              className="text-[10px] bg-emerald-950/60 text-emerald-400 border border-emerald-800/50 hover:bg-emerald-900 px-2 py-0.5 rounded transition-colors"
                            >
                              ✓ Resolve
                            </button>
                          )}
                          {colStatus === "OPEN" && (
                            <button
                              onClick={() => handleUpdateStatus(t.id, "IN_PROGRESS")}
                              className="text-[10px] bg-purple-950/60 text-purple-400 border border-purple-800/50 hover:bg-purple-900 px-2 py-0.5 rounded transition-colors"
                            >
                              → In Progress
                            </button>
                          )}
                        </div>
                      </div>
                    ))}

                    {colTickets.length === 0 && (
                      <div className="h-32 flex items-center justify-center text-xs text-slate-600 italic">
                        No tickets in {colStatus.toLowerCase()}
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </main>

        {/* Create Ticket Modal */}
        {isCreateModalOpen && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-fadeIn">
            <div className="bg-[#0f172a] border border-slate-700 rounded-2xl w-full max-w-lg p-6 space-y-4 shadow-2xl">
              <h3 className="text-base font-bold text-white">Create Support Ticket</h3>
              <form onSubmit={handleCreateTicket} className="space-y-4 text-xs">
                <div className="space-y-1.5">
                  <label className="text-slate-300 font-semibold">Subject / Title</label>
                  <input
                    type="text"
                    required
                    value={newSubject}
                    onChange={(e) => setNewSubject(e.target.value)}
                    placeholder="e.g. Broken item replacement"
                    className="w-full bg-slate-950 border border-slate-700 rounded-xl px-3 py-2 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                  />
                </div>

                <div className="space-y-1.5">
                  <label className="text-slate-300 font-semibold">Description</label>
                  <textarea
                    required
                    rows={3}
                    value={newDesc}
                    onChange={(e) => setNewDesc(e.target.value)}
                    placeholder="Detailed explanation of customer issue..."
                    className="w-full bg-slate-950 border border-slate-700 rounded-xl px-3 py-2 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-1.5">
                    <label className="text-slate-300 font-semibold">Priority</label>
                    <select
                      value={newPriority}
                      onChange={(e) => setNewPriority(e.target.value)}
                      className="w-full bg-slate-950 border border-slate-700 rounded-xl px-3 py-2 text-white"
                    >
                      <option value="LOW">LOW</option>
                      <option value="MEDIUM">MEDIUM</option>
                      <option value="HIGH">HIGH</option>
                      <option value="URGENT">URGENT</option>
                    </select>
                  </div>
                  <div className="space-y-1.5">
                    <label className="text-slate-300 font-semibold">Category</label>
                    <select
                      value={newCategory}
                      onChange={(e) => setNewCategory(e.target.value)}
                      className="w-full bg-slate-950 border border-slate-700 rounded-xl px-3 py-2 text-white"
                    >
                      <option value="ORDER_STATUS">ORDER_STATUS</option>
                      <option value="RETURN">RETURN</option>
                      <option value="REFUND">REFUND</option>
                      <option value="SHIPPING">SHIPPING</option>
                      <option value="COMPLAINT">COMPLAINT</option>
                      <option value="TECHNICAL">TECHNICAL</option>
                      <option value="GENERAL">GENERAL</option>
                    </select>
                  </div>
                </div>

                <div className="flex justify-end gap-3 pt-4 border-t border-slate-800">
                  <button
                    type="button"
                    onClick={() => setIsCreateModalOpen(false)}
                    className="px-4 py-2 rounded-xl bg-slate-800 text-slate-300 hover:bg-slate-700 font-semibold"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="px-5 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold"
                  >
                    Create Ticket
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
