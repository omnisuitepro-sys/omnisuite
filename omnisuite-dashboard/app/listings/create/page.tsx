"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import api from "@/lib/api";

export default function CreatePage() {
  const [title, setTitle] = useState("");
  const [price, setPrice] = useState("");
  const [tabId, setTabId] = useState<number | null>(null);

  const router = useRouter();

  const { data: tabs = [] } = useQuery({
    queryKey: ["tabs"],
    queryFn: async () => (await api.get("/tabs")).data,
  });

  const submit = async (e: any) => {
    e.preventDefault();

    await api.post("/listings", {
      title,
      price: parseFloat(price),
      tab_id: tabId,
    });

    router.push("/listings");
  };

  return (
    <form onSubmit={submit} className="space-y-4">
      
      <input
        placeholder="Title"
        onChange={(e) => setTitle(e.target.value)}
      />

      <input
        placeholder="Price"
        onChange={(e) => setPrice(e.target.value)}
      />

      {/* ✅ TAB SELECT */}
      <select onChange={(e) => setTabId(parseInt(e.target.value))}>
        <option value="">Select Tab</option>
        {tabs.map((tab: any) => (
          <option key={tab.id} value={tab.id}>
            {tab.name}
          </option>
        ))}
      </select>

      <button>Create</button>
    </form>
  );
}