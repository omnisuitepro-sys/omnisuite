"use client";

import { useQuery } from "@tanstack/react-query";
import { useState } from "react";
import api from "@/lib/api";

export default function ListingsPage() {
  const [activeTab, setActiveTab] = useState<number | null>(null);

  const { data: tabs = [] } = useQuery({
    queryKey: ["tabs"],
    queryFn: async () => (await api.get("/tabs")).data,
  });

  const { data: listings = [] } = useQuery({
    queryKey: ["listings", activeTab],
    queryFn: async () => {
      const url = activeTab ? `/listings?tab_id=${activeTab}` : "/listings";
      return (await api.get(url)).data;
    },
  });

  return (
    <main>
      <h1>Listings</h1>

      {/* ✅ TAB BUTTONS */}
      <div className="flex gap-2 mb-4">
        <button onClick={() => setActiveTab(null)}>All</button>

        {tabs.map((tab: any) => (
          <button key={tab.id} onClick={() => setActiveTab(tab.id)}>
            {tab.name}
          </button>
        ))}

        {/* ✅ CREATE TAB */}
        <button
          onClick={async () => {
            const name = prompt("New tab name");
            if (!name) return;
            await api.post("/tabs", { name });
            location.reload();
          }}
        >
          + Tab
        </button>
      </div>

      {/* ✅ LISTINGS */}
      {listings.map((item: any) => (
        <div key={item.id}>
          {item.title} - ${item.price}
        </div>
      ))}
    </main>
  );
}