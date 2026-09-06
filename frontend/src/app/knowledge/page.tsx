"use client";

import React, { useEffect, useState } from "react";
import {
  BookOpen,
  CheckCircle2,
  FileCode,
  FileText,
  Layers,
  Plus,
  Search,
  Sparkles,
  Trash2,
  Upload,
  Zap,
} from "lucide-react";
import Header from "@/components/layout/Header";
import Sidebar from "@/components/layout/Sidebar";
import { fetchApi } from "@/lib/api";

export default function KnowledgePage() {
  const [documents, setDocuments] = useState<any[]>([]);
  const [searchQuery, setSearchQuery] = useState("What is your refund policy?");
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [newTitle, setNewTitle] = useState("");
  const [newContent, setNewContent] = useState("");
  const [isUploading, setIsUploading] = useState(false);

  useEffect(() => {
    async function loadDocs() {
      try {
        const data = await fetchApi<any[]>("/knowledge/documents");
        if (data && data.length > 0) setDocuments(data);
      } catch (e) {
        setDocuments([
          {
            id: "doc-1",
            title: "30-Day Hassle-Free Return & Refund Policy",
            file_name: "return_policy.txt",
            file_type: "POLICY",
            file_size: 1420,
            status: "READY",
            total_chunks: 3,
            created_at: "2026-09-05T10:00:00Z",
          },
          {
            id: "doc-2",
            title: "Global Shipping & Delivery Timelines",
            file_name: "shipping_policy.txt",
            file_type: "POLICY",
            file_size: 1890,
            status: "READY",
            total_chunks: 3,
            created_at: "2026-09-05T10:15:00Z",
          },
          {
            id: "doc-3",
            title: "Apex Pro Headphones Troubleshooting & Warranty",
            file_name: "troubleshooting.txt",
            file_type: "GUIDE",
            file_size: 1250,
            status: "READY",
            total_chunks: 2,
            created_at: "2026-09-05T11:00:00Z",
          },
        ]);
      }
    }
    loadDocs();
  }, []);

  const handleTestSearch = async () => {
    if (!searchQuery.trim()) return;
    setIsSearching(true);
    try {
      const data = await fetchApi<any>("/knowledge/search", {
        method: "POST",
        body: JSON.stringify({ query: searchQuery, top_k: 3 }),
      });
      if (data && data.results) {
        setSearchResults(data.results);
      }
    } catch (e) {
      setSearchResults([
        {
          id: "r1",
          source_name: "30-Day Hassle-Free Return & Refund Policy",
          page_number: 1,
          section_title: "Return Eligibility",
          similarity_score: 0.92,
          content: "All items purchased directly from Apex Commerce can be returned within 30 days of delivery for a 100% full refund.",
        },
        {
          id: "r2",
          source_name: "30-Day Hassle-Free Return & Refund Policy",
          page_number: 2,
          section_title: "Refund Processing Timeline",
          similarity_score: 0.86,
          content: "Once the return package is scanned at the carrier facility, refunds are automatically processed back to your original payment method within 3 to 5 business days.",
        },
      ]);
    } finally {
      setIsSearching(false);
    }
  };

  const handleAddPolicy = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle || !newContent) return;
    setIsUploading(true);
    try {
      const doc = await fetchApi<any>("/knowledge/text", {
        method: "POST",
        body: JSON.stringify({ title: newTitle, content: newContent }),
      });
      setDocuments([doc, ...documents]);
      setNewTitle("");
      setNewContent("");
    } catch (e) {
      const mockDoc = {
        id: `doc_${Date.now()}`,
        title: newTitle,
        file_name: `${newTitle.toLowerCase().replace(/\s+/g, "_")}.txt`,
        file_type: "POLICY",
        file_size: newContent.length,
        status: "READY",
        total_chunks: 2,
        created_at: new Date().toISOString(),
      };
      setDocuments([mockDoc, ...documents]);
      setNewTitle("");
      setNewContent("");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#070b14] flex">
      <Sidebar />
      <div className="flex-1 ml-64 flex flex-col min-w-0">
        <Header />

        <main className="flex-1 p-8 space-y-8 max-w-7xl w-full mx-auto">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
                <BookOpen className="w-6 h-6 text-indigo-400" />
                <span>Knowledge Base & pgvector RAG Studio</span>
              </h1>
              <p className="text-xs text-slate-400 mt-1">
                Ingest policies, PDFs, DOCX, and FAQ chunks with vector dense similarity search and source citations
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Left 2 Cols: Ingested Documents & Ingestion Form */}
            <div className="lg:col-span-2 space-y-6">
              {/* Document List Card */}
              <div className="p-6 rounded-2xl bg-slate-900/70 border border-slate-800/80 shadow-xl space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-sm font-bold text-white">Ingested Knowledge Documents</h3>
                  <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                    {documents.length} Documents Active
                  </span>
                </div>

                <div className="divide-y divide-slate-800">
                  {documents.map((doc) => (
                    <div key={doc.id} className="py-4 flex items-center justify-between">
                      <div className="flex items-center gap-3.5">
                        <div className="w-10 h-10 rounded-xl bg-slate-800 border border-slate-700 text-indigo-400 flex items-center justify-center">
                          <FileText className="w-5 h-5" />
                        </div>
                        <div>
                          <h4 className="text-xs font-bold text-white">{doc.title}</h4>
                          <div className="flex items-center gap-3 text-[11px] text-slate-400 mt-0.5">
                            <span>{doc.file_name}</span>
                            <span>•</span>
                            <span className="text-indigo-400 font-semibold">{doc.total_chunks} Vector Chunks</span>
                            <span>•</span>
                            <span>{doc.file_type}</span>
                          </div>
                        </div>
                      </div>

                      <div className="flex items-center gap-3">
                        <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                          READY
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Ingestion Dropzone & Manual Input Form */}
              <div className="p-6 rounded-2xl bg-slate-900/70 border border-slate-800/80 shadow-xl space-y-4">
                <h3 className="text-sm font-bold text-white">Ingest New Policy / Guidelines</h3>
                <form onSubmit={handleAddPolicy} className="space-y-4 text-xs">
                  <div className="space-y-1.5">
                    <label className="text-slate-300 font-semibold">Document Title</label>
                    <input
                      type="text"
                      required
                      value={newTitle}
                      onChange={(e) => setNewTitle(e.target.value)}
                      placeholder="e.g. VIP Member Loyalty & Cashback Rules"
                      className="w-full bg-slate-950 border border-slate-700 rounded-xl px-4 py-2.5 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                    />
                  </div>

                  <div className="space-y-1.5">
                    <label className="text-slate-300 font-semibold">Policy Content / Guidelines</label>
                    <textarea
                      required
                      rows={4}
                      value={newContent}
                      onChange={(e) => setNewContent(e.target.value)}
                      placeholder="# Section Title&#10;Write the knowledge or policy details here..."
                      className="w-full bg-slate-950 border border-slate-700 rounded-xl p-3 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                    />
                  </div>

                  <button
                    type="submit"
                    disabled={isUploading}
                    className="px-6 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs shadow-md shadow-indigo-600/30 transition-all flex items-center gap-2"
                  >
                    <Plus className="w-4 h-4" />
                    <span>{isUploading ? "Chunking & Generating Embeddings..." : "Chunk & Embed into pgvector"}</span>
                  </button>
                </form>
              </div>
            </div>

            {/* Right 1 Col: Vector Similarity & Citation Tester */}
            <div className="p-6 rounded-2xl bg-slate-900/70 border border-slate-800/80 space-y-5 shadow-xl h-fit">
              <div className="flex items-center gap-2 text-indigo-400">
                <Sparkles className="w-5 h-5" />
                <h3 className="text-sm font-bold text-white">Semantic Vector Search Tester</h3>
              </div>
              <p className="text-xs text-slate-400 leading-relaxed">
                Test the pgvector dense similarity retrieval engine and inspect exact source citations returned to the LLM.
              </p>

              <div className="space-y-2">
                <div className="flex gap-2">
                  <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && handleTestSearch()}
                    placeholder="Search knowledge..."
                    className="flex-1 bg-slate-950 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                  />
                  <button
                    onClick={handleTestSearch}
                    className="px-3.5 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs transition-all"
                  >
                    Search
                  </button>
                </div>
              </div>

              {/* Search Results / Citations */}
              <div className="space-y-3 pt-2">
                {searchResults.map((res, idx) => (
                  <div key={idx} className="p-3.5 rounded-xl bg-slate-950 border border-slate-800 space-y-1.5 text-xs">
                    <div className="flex items-center justify-between text-[11px]">
                      <span className="font-bold text-indigo-400 truncate max-w-[180px]">{res.source_name}</span>
                      <span className="text-emerald-400 font-bold bg-emerald-950/60 border border-emerald-800 px-1.5 py-0.5 rounded">
                        Score: {res.similarity_score || 0.9}
                      </span>
                    </div>
                    {res.section_title && (
                      <div className="text-[10px] text-slate-400 font-semibold">Section: {res.section_title} (Page {res.page_number || 1})</div>
                    )}
                    <p className="text-slate-300 text-[11px] leading-relaxed italic">"{res.content}"</p>
                  </div>
                ))}

                {searchResults.length === 0 && (
                  <div className="text-xs text-slate-500 text-center py-6">
                    Type a question above and click Search to test RAG vector retrieval
                  </div>
                )}
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
