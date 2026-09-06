"use client";

import React, { useState } from "react";
import Link from "next/link";
import {
  Bell,
  Bot,
  Compass,
  FileText,
  LogOut,
  Presentation,
  Search,
  Shield,
  Sparkles,
  User,
} from "lucide-react";
import PitchModal from "../pitch/PitchModal";

export default function Header() {
  const [isPitchOpen, setIsPitchOpen] = useState(false);
  const [isProfileOpen, setIsProfileOpen] = useState(false);

  return (
    <>
      <header className="h-16 bg-[#0c121e]/90 backdrop-blur-md border-b border-slate-800/80 sticky top-0 z-30 flex items-center justify-between px-6 pl-70">
        {/* Search & Breadcrumb */}
        <div className="flex items-center gap-4 flex-1 max-w-md">
          <div className="relative w-full">
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Search conversations, tickets, customers, or SKUs... (⌘K)"
              className="w-full bg-slate-900/80 border border-slate-800/80 rounded-xl pl-9.5 pr-4 py-2 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500/80 transition-colors"
            />
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-3">
          {/* Customer Pitch Button */}
          <button
            onClick={() => setIsPitchOpen(true)}
            className="flex items-center gap-2 px-3.5 py-1.5 rounded-xl bg-gradient-to-r from-indigo-600/20 via-purple-600/20 to-indigo-600/20 border border-indigo-500/30 text-indigo-300 hover:text-white hover:border-indigo-500 text-xs font-semibold shadow-sm transition-all"
          >
            <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
            <span>Customer Pitch Deck</span>
          </button>

          {/* Live Status Pill */}
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-emerald-950/30 border border-emerald-500/30 text-emerald-400 text-xs font-medium">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span>AI Gateway Online</span>
          </div>

          {/* User Profile */}
          <div className="relative">
            <button
              onClick={() => setIsProfileOpen(!isProfileOpen)}
              className="flex items-center gap-2.5 p-1.5 rounded-xl hover:bg-slate-800/60 transition-colors"
            >
              <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center font-bold text-white text-xs">
                AM
              </div>
              <div className="text-left hidden md:block">
                <div className="text-xs font-semibold text-white">Alex Mercer</div>
                <div className="text-[10px] text-slate-400">Lead Admin</div>
              </div>
            </button>

            {isProfileOpen && (
              <div className="absolute right-0 mt-2 w-52 bg-[#0f172a] border border-slate-700/80 rounded-xl shadow-xl py-1.5 z-50 animate-fadeIn">
                <div className="px-3.5 py-2 border-b border-slate-800">
                  <div className="text-xs font-bold text-white">Apex Commerce Inc.</div>
                  <div className="text-[10px] text-slate-400">alex@supportiq.ai</div>
                </div>
                <Link
                  href="/settings"
                  onClick={() => setIsProfileOpen(false)}
                  className="flex items-center gap-2.5 px-3.5 py-2 text-xs text-slate-300 hover:bg-slate-800 hover:text-white"
                >
                  <User className="w-3.5 h-3.5" />
                  <span>Account Settings</span>
                </Link>
                <Link
                  href="/agent"
                  onClick={() => setIsProfileOpen(false)}
                  className="flex items-center gap-2.5 px-3.5 py-2 text-xs text-slate-300 hover:bg-slate-800 hover:text-white"
                >
                  <Bot className="w-3.5 h-3.5" />
                  <span>Agent Configuration</span>
                </Link>
                <div className="border-t border-slate-800 my-1"></div>
                <Link
                  href="/login"
                  onClick={() => setIsProfileOpen(false)}
                  className="flex items-center gap-2.5 px-3.5 py-2 text-xs text-rose-400 hover:bg-rose-500/10"
                >
                  <LogOut className="w-3.5 h-3.5" />
                  <span>Sign Out</span>
                </Link>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Presentation Pitch Modal */}
      <PitchModal isOpen={isPitchOpen} onClose={() => setIsPitchOpen(false)} />
    </>
  );
}
