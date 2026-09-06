"use client";

import React, { useEffect, useState } from "react";
import {
  DollarSign,
  Mail,
  Package,
  Phone,
  Plus,
  Search,
  Ticket,
  User,
  Users,
} from "lucide-react";
import Header from "@/components/layout/Header";
import Sidebar from "@/components/layout/Sidebar";
import { fetchApi } from "@/lib/api";

export default function CustomersPage() {
  const [customers, setCustomers] = useState<any[]>([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCustomer, setSelectedCustomer] = useState<any | null>(null);

  useEffect(() => {
    async function loadCustomers() {
      try {
        const data = await fetchApi<any[]>("/customers");
        if (data && data.length > 0) {
          setCustomers(data);
          setSelectedCustomer(data[0]);
        }
      } catch (e) {
        const mockCusts = [
          {
            id: "c1",
            name: "Emma Watson",
            email: "emma.watson@example.com",
            phone: "+1-555-0101",
            total_orders: 3,
            lifetime_value: 728.98,
            tags: "VIP, Frequent Buyer",
            created_at: "2026-08-15T10:00:00Z",
          },
          {
            id: "c2",
            name: "David Miller",
            email: "david.miller@example.com",
            phone: "+1-555-0102",
            total_orders: 1,
            lifetime_value: 249.99,
            tags: "New Customer",
            created_at: "2026-09-01T12:00:00Z",
          },
          {
            id: "c3",
            name: "Sophia Chen",
            email: "sophia.chen@example.com",
            phone: "+1-555-0103",
            total_orders: 4,
            lifetime_value: 1120.50,
            tags: "VIP, Enterprise",
            created_at: "2026-07-20T14:30:00Z",
          },
          {
            id: "c4",
            name: "James Wilson",
            email: "james.wilson@example.com",
            phone: "+1-555-0104",
            total_orders: 2,
            lifetime_value: 448.00,
            tags: "Regular",
            created_at: "2026-08-28T09:15:00Z",
          },
        ];
        setCustomers(mockCusts);
        setSelectedCustomer(mockCusts[0]);
      }
    }
    loadCustomers();
  }, []);

  const filteredCustomers = customers.filter((c) => {
    if (!searchQuery) return true;
    const q = searchQuery.toLowerCase();
    return (
      c.name?.toLowerCase().includes(q) ||
      c.email?.toLowerCase().includes(q) ||
      c.phone?.toLowerCase().includes(q) ||
      c.tags?.toLowerCase().includes(q)
    );
  });

  return (
    <div className="min-h-screen bg-[#070b14] flex">
      <Sidebar />
      <div className="flex-1 ml-64 flex flex-col min-w-0">
        <Header />

        <main className="flex-1 p-8 space-y-6 max-w-7xl w-full mx-auto">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
                <Users className="w-6 h-6 text-indigo-400" />
                <span>Customer CRM Directory</span>
              </h1>
              <p className="text-xs text-slate-400 mt-1">
                Unified profiles, lifetime value, support history, and customer diagnostics
              </p>
            </div>
          </div>

          <div className="flex items-center gap-4 p-4 rounded-2xl bg-slate-900/60 border border-slate-800">
            <div className="relative flex-1 max-w-md">
              <Search className="w-3.5 h-3.5 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                placeholder="Search customers by name, email, phone, or VIP tag..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-8.5 pr-3 py-1.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
              />
            </div>
            <span className="text-xs text-slate-400 font-semibold">{filteredCustomers.length} Total Customers</span>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Customer Table */}
            <div className="lg:col-span-2 rounded-2xl bg-slate-900/70 border border-slate-800/80 overflow-hidden shadow-xl">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-950/80 text-slate-400 border-b border-slate-800 uppercase tracking-wider font-semibold">
                  <tr>
                    <th className="p-4">Customer</th>
                    <th className="p-4">Orders</th>
                    <th className="p-4">LTV</th>
                    <th className="p-4">Tags</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60 text-slate-300">
                  {filteredCustomers.map((c) => (
                    <tr
                      key={c.id}
                      onClick={() => setSelectedCustomer(c)}
                      className={`cursor-pointer transition-colors ${
                        selectedCustomer?.id === c.id ? "bg-indigo-950/40" : "hover:bg-slate-800/40"
                      }`}
                    >
                      <td className="p-4">
                        <div className="font-bold text-white">{c.name}</div>
                        <div className="text-[11px] text-slate-500">{c.email}</div>
                      </td>
                      <td className="p-4 font-semibold">{c.total_orders} Orders</td>
                      <td className="p-4 font-bold text-emerald-400">${c.lifetime_value}</td>
                      <td className="p-4">
                        <span className="text-[10px] bg-slate-800 text-indigo-300 border border-slate-700 px-2 py-0.5 rounded-full">
                          {c.tags || "Standard"}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Customer Detail Card (Right) */}
            <div className="p-6 rounded-2xl bg-slate-900/70 border border-slate-800/80 space-y-6 shadow-xl h-fit">
              {selectedCustomer ? (
                <>
                  <div className="text-center space-y-2 pb-4 border-b border-slate-800">
                    <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-indigo-600 to-purple-600 text-white font-bold text-xl flex items-center justify-center mx-auto shadow-lg shadow-indigo-600/30">
                      {selectedCustomer.name.charAt(0)}
                    </div>
                    <h3 className="text-base font-bold text-white">{selectedCustomer.name}</h3>
                    <p className="text-xs text-slate-400">{selectedCustomer.email}</p>
                    <span className="inline-block text-[10px] bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 px-2.5 py-0.5 rounded-full font-semibold">
                      {selectedCustomer.tags || "Customer"}
                    </span>
                  </div>

                  <div className="grid grid-cols-2 gap-3 text-center">
                    <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
                      <div className="text-base font-bold text-emerald-400">${selectedCustomer.lifetime_value}</div>
                      <div className="text-[10px] text-slate-400">Total Spent</div>
                    </div>
                    <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
                      <div className="text-base font-bold text-white">{selectedCustomer.total_orders}</div>
                      <div className="text-[10px] text-slate-400">Total Orders</div>
                    </div>
                  </div>

                  <div className="space-y-2 text-xs">
                    <div className="flex items-center gap-2 text-slate-300">
                      <Phone className="w-3.5 h-3.5 text-slate-500" />
                      <span>{selectedCustomer.phone || "No phone number"}</span>
                    </div>
                    <div className="flex items-center gap-2 text-slate-300">
                      <Mail className="w-3.5 h-3.5 text-slate-500" />
                      <span>{selectedCustomer.email}</span>
                    </div>
                  </div>
                </>
              ) : (
                <div className="text-xs text-slate-500 text-center py-10">Select a customer</div>
              )}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
