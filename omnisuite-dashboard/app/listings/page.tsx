"use client";

import { useQuery } from "@tanstack/react-query";
import { useState } from "react";
import api from "@/lib/api";

const { data: metrics } = useQuery({
  queryKey: ["metrics"],
  queryFn: async () => (await api.get("/metrics")).data,
});

export default function ListingsPage() {
  const [activeTab, setActiveTab] = useState<number | null>(null);
  const [search, setSearch] = useState("");

  const { data: tabs = [] } = useQuery({
    queryKey: ["tabs"],
    queryFn: async () => (await api.get("/tabs")).data,
  });

  const { data: listings = [], refetch } = useQuery({
    queryKey: ["listings", activeTab],
    queryFn: async () => {
      const url = activeTab ? `/listings?tab_id=${activeTab}` : "/listings";
      return (await api.get(url)).data;
    },
  });

  const filtered = listings.filter((item: any) =>
    item.title.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <main className="p-10">
      <h1 className="text-3xl font-bold mb-6">Listings</h1>

{/* ✅ Metrics */}
<div className="grid grid-cols-3 gap-4 mb-6">
  <div className="bg-white p-4 rounded shadow">
    <p className="text-gray-500">Total Listings</p>
    <h2 className="text-2xl font-bold">
      {metrics?.total_listings ?? 0}
    </h2>
  </div>

  <div className="bg-white p-4 rounded shadow">
    <p className="text-gray-500">Total Value</p>
    <h2 className="text-2xl font-bold">
      ${metrics?.total_value?.toFixed(2) ?? "0.00"}
    </h2>
  </div>

  <div className="bg-white p-4 rounded shadow">
    <p className="text-gray-500">Avg Price</p>
    <h2 className="text-2xl font-bold">
      ${metrics?.avg_price?.toFixed(2) ?? "0.00"}
    </h2>
  </div>
</div>

{/* ✅ Metrics */}
<div className="grid grid-cols-3 gap-4 mb-6">
  <div className="bg-white p-4 rounded shadow">
    <p className="text-gray-500">Total Listings</p>
    <h2 className="text-2xl font-bold">
      {metrics?.total_listings ?? 0}
    </h2>
  </div>

  <div className="bg-white p-4 rounded shadow">
    <p className="text-gray-500">Total Value</p>
    <h2 className="text-2xl font-bold">
      ${metrics?.total_value?.toFixed(2) ?? "0.00"}
    </h2>
  </div>

  <div className="bg-white p-4 rounded shadow">
    <p className="text-gray-500">Avg Price</p>
    <h2 className="text-2xl font-bold">
      ${metrics?.avg_price?.toFixed(2) ?? "0.00"}
    </h2>
  </div>
</div>

      {/* Tabs */}
      <div className="flex gap-2 mb-6 flex-wrap">
        <button
          onClick={() => setActiveTab(null)}
          className={`px-4 py-2 rounded ${
            activeTab === null ? "bg-blue-600 text-white" : "bg-gray-200"
          }`}
        >
          All
        </button>

        {tabs.map((tab: any) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-4 py-2 rounded ${
              activeTab === tab.id ? "bg-blue-600 text-white" : "bg-gray-200"
            }`}
          >
            {tab.name}
          </button>
        ))}

        <button
          onClick={async () => {
            const name = prompt("New tab name");
            if (!name) return;
            await api.post("/tabs", { name });
            location.reload();
          }}
          className="bg-green-600 text-white px-4 py-2 rounded"
        >
          + Tab
        </button>
      </div>

      {/* Search */}
      <input
        placeholder="Search..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="p-3 border rounded mb-6 w-full max-w-sm"
      />

      {/* Listings */}
      <div className="space-y-4">
        {filtered.map((item: any) => (
          <div key={item.id} className="p-4 bg-white rounded shadow flex justify-between">
            <div>
              <h2 className="font-bold">{item.title}</h2>
              <p>${item.price}</p>
            </div>

            <div className="flex gap-2">
              <button
                onClick={async () => {
                  await api.delete(`/listings/${item.id}`);
                  location.reload();
                }}
                className="bg-red-500 text-white px-4 py-2 rounded"
              >
                Delete
              </button>

              <button
                onClick={async () => {
                  const title = prompt("New title", item.title);
                  const price = prompt("New price", item.price);

                  if (!title || !price) return;

                  await api.put(`/listings/${item.id}`, {
                    title,
                    price: parseFloat(price),
                  });

                  location.reload();
                }}
                className="bg-yellow-500 text-white px-4 py-2 rounded"
              >
                Edit
              </button>
            </div>
          </div>
        ))}
      </div>
    </main>
  );
}