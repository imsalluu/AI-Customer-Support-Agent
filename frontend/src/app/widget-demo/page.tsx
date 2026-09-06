"use client";

import React, { useEffect } from "react";
import Link from "next/link";
import { ArrowLeft, Bot, CheckCircle2, Shield, ShoppingBag, Star, Zap } from "lucide-react";

export default function WidgetDemoPage() {
  useEffect(() => {
    // Load embeddable widget script
    const script = document.createElement("script");
    script.src = "/widget.js";
    script.setAttribute("data-api-key", "spiq_live_apex_demo_key_9921");
    script.setAttribute("data-api-url", "http://localhost:8000/api/v1");
    document.body.appendChild(script);

    return () => {
      // Cleanup widget container if unmounted
      const container = document.querySelector(".spiq-widget-container");
      if (container) container.remove();
    };
  }, []);

  return (
    <div className="min-h-screen bg-[#090d16] text-slate-100 flex flex-col">
      {/* Store Header */}
      <header className="bg-slate-900/90 border-b border-slate-800 px-8 py-4 flex items-center justify-between sticky top-0 z-20">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-indigo-600 flex items-center justify-center text-white font-bold">
            ⚡
          </div>
          <div>
            <h1 className="text-base font-bold text-white">Apex Commerce Storefront</h1>
            <p className="text-[10px] text-slate-400">Live Embeddable AI Support Widget Showcase</p>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <Link
            href="/dashboard"
            className="flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold transition-colors"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>Return to SaaS Dashboard</span>
          </Link>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-6 py-12 space-y-10 flex-1">
        <div className="p-6 rounded-2xl bg-gradient-to-r from-indigo-950/40 via-purple-950/30 to-slate-900 border border-indigo-500/30 text-center space-y-3">
          <span className="text-xs font-bold text-indigo-400 uppercase tracking-wider">Live Storefront Test</span>
          <h2 className="text-2xl md:text-3xl font-bold text-white">
            Embeddable SupportIQ AI Chat Widget in Action
          </h2>
          <p className="text-xs text-slate-300 max-w-2xl mx-auto leading-relaxed">
            Click the purple circular launcher in the bottom right corner of the screen. The widget interacts in real-time with the FastAPI backend, retrieves knowledge chunks with source citations, and executes operational tools.
          </p>
          <div className="flex flex-wrap justify-center gap-2 pt-2 text-[11px] text-indigo-200">
            <span className="bg-indigo-950 border border-indigo-800 px-3 py-1 rounded-full">💡 Ask: "Where is order ORD-10022?"</span>
            <span className="bg-indigo-950 border border-indigo-800 px-3 py-1 rounded-full">💡 Ask: "What is your return policy?"</span>
            <span className="bg-indigo-950 border border-indigo-800 px-3 py-1 rounded-full">💡 Ask: "Talk to human agent"</span>
          </div>
        </div>

        {/* Product Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-4 hover:border-indigo-500/50 transition-all">
            <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300">
              AUDIO • IN STOCK
            </span>
            <h3 className="text-base font-bold text-white">Apex Pro Wireless Headphones</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Premium active noise-cancelling headphones with 40-hour battery and USB-C quick charge.
            </p>
            <div className="flex items-center justify-between pt-2">
              <span className="text-xl font-extrabold text-indigo-400">$249.99</span>
              <button className="px-3.5 py-1.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs transition-colors">
                Add to Cart
              </button>
            </div>
          </div>

          <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-4 hover:border-indigo-500/50 transition-all">
            <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-purple-500/20 text-purple-300">
              FURNITURE • IN STOCK
            </span>
            <h3 className="text-base font-bold text-white">Ergonomic Mesh Office Chair</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Adjustable lumbar support breathable high-back desk chair designed for all-day posture.
            </p>
            <div className="flex items-center justify-between pt-2">
              <span className="text-xl font-extrabold text-indigo-400">$329.00</span>
              <button className="px-3.5 py-1.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs transition-colors">
                Add to Cart
              </button>
            </div>
          </div>

          <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-4 hover:border-indigo-500/50 transition-all">
            <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300">
              WEARABLES • IN STOCK
            </span>
            <h3 className="text-base font-bold text-white">Apex Smart Fitness Watch</h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Waterproof GPS smartwatch with heart rate, SpO2 sensor, and 14-day battery life.
            </p>
            <div className="flex items-center justify-between pt-2">
              <span className="text-xl font-extrabold text-indigo-400">$179.50</span>
              <button className="px-3.5 py-1.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs transition-colors">
                Add to Cart
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
