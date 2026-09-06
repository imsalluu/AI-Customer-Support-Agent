"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  BarChart3,
  Bot,
  Compass,
  FileText,
  Headphones,
  LayoutDashboard,
  Layers,
  MessageSquare,
  Settings,
  Ticket,
  Users,
  ExternalLink,
  Sparkles,
} from "lucide-react";

interface NavItem {
  name: string;
  href: string;
  icon: React.ComponentType<{ className?: string }>;
  badge?: string;
  badgeColor?: string;
}

const navItems: NavItem[] = [
  { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
  { name: "Support Inbox", href: "/conversations", icon: MessageSquare, badge: "3 Live", badgeColor: "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30" },
  { name: "Customers CRM", href: "/customers", icon: Users },
  { name: "Support Tickets", href: "/tickets", icon: Ticket, badge: "2 Urgent", badgeColor: "bg-rose-500/20 text-rose-400 border border-rose-500/30" },
  { name: "Knowledge & RAG", href: "/knowledge", icon: FileText },
  { name: "AI Analytics", href: "/analytics", icon: BarChart3 },
  { name: "Agent Studio", href: "/agent", icon: Bot, badge: "AI Active", badgeColor: "bg-indigo-500/20 text-indigo-400 border border-indigo-500/30" },
  { name: "Channels", href: "/channels", icon: Layers },
  { name: "Settings & Billing", href: "/settings", icon: Settings },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 bg-[#0c121e] border-r border-slate-800/80 flex flex-col h-screen fixed top-0 left-0 z-40">
      {/* Brand Header */}
      <div className="p-5 border-b border-slate-800/60 flex items-center justify-between">
        <Link href="/dashboard" className="flex items-center gap-3 group">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 via-indigo-500 to-purple-500 flex items-center justify-center text-white shadow-lg shadow-indigo-500/30 group-hover:scale-105 transition-transform">
            <Bot className="w-6 h-6" />
          </div>
          <div>
            <span className="font-bold text-lg text-white tracking-tight flex items-center gap-1.5">
              SUPPORT<span className="text-indigo-400">IQ</span>
              <span className="text-[10px] uppercase font-bold px-1.5 py-0.5 rounded bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">AI</span>
            </span>
            <p className="text-[11px] text-slate-400 font-medium">Apex Commerce Inc.</p>
          </div>
        </Link>
      </div>

      {/* Navigation Links */}
      <div className="flex-1 overflow-y-auto px-3 py-4 space-y-1">
        <div className="px-3 pb-2 text-[10px] font-bold uppercase tracking-wider text-slate-400">
          Core Operations
        </div>
        {navItems.map((item) => {
          const isActive = pathname === item.href;
          const Icon = item.icon;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center justify-between px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all ${
                isActive
                  ? "bg-indigo-600 text-white shadow-md shadow-indigo-600/30 font-semibold"
                  : "text-slate-400 hover:text-slate-100 hover:bg-slate-800/60"
              }`}
            >
              <div className="flex items-center gap-3">
                <Icon className={`w-4.5 h-4.5 ${isActive ? "text-white" : "text-slate-400"}`} />
                <span>{item.name}</span>
              </div>
              {item.badge && (
                <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full ${item.badgeColor}`}>
                  {item.badge}
                </span>
              )}
            </Link>
          );
        })}

        <div className="pt-4 px-3 pb-2 text-[10px] font-bold uppercase tracking-wider text-slate-400">
          Testing Sandbox
        </div>
        <Link
          href="/widget-demo"
          target="_blank"
          className="flex items-center justify-between px-3.5 py-2.5 rounded-xl text-sm font-medium text-indigo-300 bg-indigo-950/40 border border-indigo-800/40 hover:bg-indigo-900/50 transition-all group"
        >
          <div className="flex items-center gap-3">
            <Compass className="w-4.5 h-4.5 text-indigo-400" />
            <span>Storefront Widget Demo</span>
          </div>
          <ExternalLink className="w-3.5 h-3.5 opacity-60 group-hover:opacity-100 transition-opacity" />
        </Link>
      </div>

      {/* Bottom Status & Plan Card */}
      <div className="p-4 border-t border-slate-800/60 bg-[#080d16]">
        <div className="p-3 rounded-xl bg-slate-800/40 border border-slate-700/50 flex flex-col gap-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-300 flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              Business Plan
            </span>
            <span className="text-[11px] text-slate-400">1,420 / 25k</span>
          </div>
          <div className="w-full bg-slate-700/50 rounded-full h-1.5 overflow-hidden">
            <div className="bg-indigo-500 h-full rounded-full" style={{ width: "6%" }}></div>
          </div>
          <p className="text-[10px] text-slate-400">
            pgvector RAG & 11 Tools Active
          </p>
        </div>
      </div>
    </aside>
  );
}
