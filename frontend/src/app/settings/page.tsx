"use client";

import React, { useState } from "react";
import {
  CreditCard,
  Key,
  Plus,
  RefreshCw,
  Settings,
  Shield,
  User,
  Users,
} from "lucide-react";
import Header from "@/components/layout/Header";
import Sidebar from "@/components/layout/Sidebar";

export default function SettingsPage() {
  const [apiKey, setApiKey] = useState("spiq_live_apex_demo_key_9921");
  const [copiedKey, setCopiedKey] = useState(false);

  const teamMembers = [
    { name: "Alex Mercer", email: "alex@supportiq.ai", role: "OWNER", status: "Active" },
    { name: "Sarah Jenkins", email: "sarah.support@supportiq.ai", role: "SUPPORT_AGENT", status: "Active" },
    { name: "Marcus Vance", email: "marcus.agent@supportiq.ai", role: "SUPPORT_AGENT", status: "Active" },
  ];

  return (
    <div className="min-h-screen bg-[#070b14] flex">
      <Sidebar />
      <div className="flex-1 ml-64 flex flex-col min-w-0">
        <Header />

        <main className="flex-1 p-8 space-y-8 max-w-7xl w-full mx-auto">
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
              <Settings className="w-6 h-6 text-indigo-400" />
              <span>Settings & Organization Management</span>
            </h1>
            <p className="text-xs text-slate-400 mt-1">
              API Keys, Multi-tenant permissions, team access, and subscription plan metrics
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Left 2 Cols: API Keys & Team Members */}
            <div className="lg:col-span-2 space-y-6">
              {/* API Key Card */}
              <div className="p-6 rounded-2xl bg-slate-900/70 border border-slate-800 space-y-4 shadow-xl">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2.5">
                    <Key className="w-4 h-4 text-indigo-400" />
                    <h3 className="text-sm font-bold text-white">Organization Public API Key</h3>
                  </div>
                  <span className="text-[10px] bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 px-2 py-0.5 rounded-full font-bold">
                    LIVE
                  </span>
                </div>
                <p className="text-xs text-slate-400">
                  Use this key in your website chat widget script tags or REST integrations.
                </p>
                <div className="flex gap-2">
                  <input
                    type="text"
                    readOnly
                    value={apiKey}
                    className="flex-1 bg-slate-950 border border-slate-700 rounded-xl px-4 py-2 text-xs font-mono text-indigo-300"
                  />
                  <button
                    onClick={() => {
                      navigator.clipboard.writeText(apiKey);
                      setCopiedKey(true);
                      setTimeout(() => setCopiedKey(false), 2000);
                    }}
                    className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold"
                  >
                    {copiedKey ? "Copied!" : "Copy"}
                  </button>
                </div>
              </div>

              {/* Team Members Card */}
              <div className="p-6 rounded-2xl bg-slate-900/70 border border-slate-800 space-y-4 shadow-xl">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2.5">
                    <Users className="w-4 h-4 text-indigo-400" />
                    <h3 className="text-sm font-bold text-white">Team Members & RBAC Roles</h3>
                  </div>
                  <button className="px-3 py-1.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold flex items-center gap-1.5">
                    <Plus className="w-3.5 h-3.5" />
                    <span>Invite Member</span>
                  </button>
                </div>

                <div className="divide-y divide-slate-800">
                  {teamMembers.map((m, idx) => (
                    <div key={idx} className="py-3.5 flex items-center justify-between text-xs">
                      <div>
                        <div className="font-bold text-white">{m.name}</div>
                        <div className="text-[11px] text-slate-400">{m.email}</div>
                      </div>
                      <div className="flex items-center gap-3">
                        <span className="font-semibold text-indigo-400 bg-indigo-950 px-2.5 py-0.5 rounded border border-indigo-800 text-[10px]">
                          {m.role}
                        </span>
                        <span className="text-[10px] text-emerald-400">{m.status}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Right 1 Col: Subscription Plan Card */}
            <div className="p-6 rounded-2xl bg-slate-900/70 border border-slate-800 space-y-5 shadow-xl h-fit">
              <div className="flex items-center gap-2 text-indigo-400">
                <CreditCard className="w-5 h-5" />
                <h3 className="text-sm font-bold text-white">Current Subscription</h3>
              </div>

              <div className="p-4 rounded-xl bg-gradient-to-br from-indigo-950/60 to-purple-950/40 border border-indigo-500/30 space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-xs font-bold text-white">Business Plan</span>
                  <span className="text-sm font-extrabold text-emerald-400">$299/mo</span>
                </div>
                <p className="text-[11px] text-slate-300">
                  25,000 AI Messages, 100 Knowledge Documents, 25 Support Agent seats.
                </p>
              </div>

              <div className="space-y-3 text-xs">
                <div className="space-y-1">
                  <div className="flex justify-between text-slate-400">
                    <span>Monthly AI Messages:</span>
                    <span className="font-semibold text-white">1,420 / 25,000</span>
                  </div>
                  <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                    <div className="bg-indigo-500 h-full rounded-full" style={{ width: "6%" }}></div>
                  </div>
                </div>

                <div className="space-y-1">
                  <div className="flex justify-between text-slate-400">
                    <span>Knowledge Documents:</span>
                    <span className="font-semibold text-white">3 / 100</span>
                  </div>
                  <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                    <div className="bg-purple-500 h-full rounded-full" style={{ width: "3%" }}></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
