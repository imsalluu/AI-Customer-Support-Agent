"use client";

import React, { useState } from "react";
import {
  Check,
  CheckCircle2,
  Copy,
  Globe,
  Layers,
  Mail,
  MessageSquare,
  Phone,
  Shield,
  Zap,
} from "lucide-react";
import Header from "@/components/layout/Header";
import Sidebar from "@/components/layout/Sidebar";

export default function ChannelsPage() {
  const [copied, setCopied] = useState(false);

  const embedCode = `<script 
  src="http://localhost:8000/widget/widget.js" 
  data-api-key="spiq_live_apex_demo_key_9921"
  data-api-url="http://localhost:8000/api/v1">
</script>`;

  const handleCopy = () => {
    navigator.clipboard.writeText(embedCode);
    setCopied(true);
    setTimeout(() => setCopied(false), 2500);
  };

  return (
    <div className="min-h-screen bg-[#070b14] flex">
      <Sidebar />
      <div className="flex-1 ml-64 flex flex-col min-w-0">
        <Header />

        <main className="flex-1 p-8 space-y-8 max-w-7xl w-full mx-auto">
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
              <Layers className="w-6 h-6 text-indigo-400" />
              <span>Multi-Channel Support Hub</span>
            </h1>
            <p className="text-xs text-slate-400 mt-1">
              Connect Website Live Chat, WhatsApp Cloud API, Messenger, and Inbound Email support channels
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* WebChat Channel */}
            <div className="p-6 rounded-2xl bg-slate-900/70 border border-slate-800 space-y-4 shadow-xl">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-indigo-600/20 text-indigo-400 flex items-center justify-center">
                    <Globe className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="text-sm font-bold text-white">Website Live Chat Widget</h3>
                    <p className="text-[11px] text-slate-400">Embeddable floating widget for any website or store</p>
                  </div>
                </div>
                <span className="text-[10px] bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 px-2 py-0.5 rounded-full font-bold">
                  ACTIVE
                </span>
              </div>

              <div className="space-y-2 text-xs">
                <div className="flex justify-between items-center text-slate-400">
                  <span>Embed Code Snippet</span>
                  <button
                    onClick={handleCopy}
                    className="flex items-center gap-1 text-indigo-400 hover:text-indigo-300 font-semibold"
                  >
                    {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                    <span>{copied ? "Copied to Clipboard!" : "Copy Code"}</span>
                  </button>
                </div>
                <pre className="p-3 rounded-xl bg-slate-950 border border-slate-800 text-[11px] font-mono text-indigo-200 overflow-x-auto">
                  {embedCode}
                </pre>
              </div>
            </div>

            {/* WhatsApp Channel */}
            <div className="p-6 rounded-2xl bg-slate-900/70 border border-slate-800 space-y-4 shadow-xl">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-emerald-600/20 text-emerald-400 flex items-center justify-center">
                    <Phone className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="text-sm font-bold text-white">WhatsApp Cloud API</h3>
                    <p className="text-[11px] text-slate-400">Official Meta Business Cloud API integration</p>
                  </div>
                </div>
                <span className="text-[10px] bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 px-2 py-0.5 rounded-full font-bold">
                  CONNECTED
                </span>
              </div>

              <div className="space-y-2 text-xs">
                <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
                  <div className="text-slate-400">Webhook Callback URL:</div>
                  <div className="font-mono text-indigo-300 text-[11px]">http://localhost:8000/api/v1/webhooks/whatsapp</div>
                </div>
                <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
                  <div className="text-slate-400">Verify Token:</div>
                  <div className="font-mono text-indigo-300 text-[11px]">supportiq_verify_token_secure</div>
                </div>
              </div>
            </div>

            {/* Messenger Channel */}
            <div className="p-6 rounded-2xl bg-slate-900/70 border border-slate-800 space-y-4 shadow-xl">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-blue-600/20 text-blue-400 flex items-center justify-center">
                    <MessageSquare className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="text-sm font-bold text-white">Facebook Messenger</h3>
                    <p className="text-[11px] text-slate-400">Meta Pages webhook connector</p>
                  </div>
                </div>
                <span className="text-[10px] bg-slate-800 text-slate-400 border border-slate-700 px-2 py-0.5 rounded-full font-bold">
                  READY TO CONNECT
                </span>
              </div>
              <p className="text-xs text-slate-400">
                Connect your brand's Facebook page to route all inbox queries to SupportIQ AI agents.
              </p>
            </div>

            {/* Email Channel */}
            <div className="p-6 rounded-2xl bg-slate-900/70 border border-slate-800 space-y-4 shadow-xl">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-purple-600/20 text-purple-400 flex items-center justify-center">
                    <Mail className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="text-sm font-bold text-white">Inbound Support Email</h3>
                    <p className="text-[11px] text-slate-400">support@apexcommerce.com forwarder</p>
                  </div>
                </div>
                <span className="text-[10px] bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 px-2 py-0.5 rounded-full font-bold">
                  ACTIVE
                </span>
              </div>
              <p className="text-xs text-slate-400">
                Inbound emails are automatically parsed, ticketed, and replied to with grounded RAG context.
              </p>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
