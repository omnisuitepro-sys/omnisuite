"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useQuery } from "@tanstack/react-query";
import api from "@/lib/api";

export default function CreateListingPage() {
  const [title, setTitle] = useState("");
  const [price, setPrice] = useState("");
  const [tabId, setTabId] = useState<number | null>(null);

  const router = useRouter();

  const { data: tabs = [] } = useQuery({
    queryKey: ["tabs"],
    queryFn: async () => (await api.get("/tabs")).data,
  });

  const handleSubmit = async (e: any) => {
    e.preventDefault();

    await api.post("/listings", {
      title,
      price: parseFloat(price),
      tab_id: tabId,
    });

    router.push("/listings");
  };

  return (
    <main className="p-10">
      <h1 className="text-3xl font-bold mb-6">Create Listing</h1>

      <form onSubmit={handleSubmit} className="space-y-4 max-w-md">

        <input
          className="w-full p-3 border rounded"
          placeholder="Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />

        <input
          className="w-full p-3 border rounded"
          placeholder="Price"
          value={price}
          onChange={(e) => setPrice(e.target.value)}
        />

        <select
          className="w-full p-3 border rounded"
          onChange={(e) => setTabId(parseInt(e.target.value))}
        >
          <option value="">Select Tab</option>
          {tabs.map((tab: any) => (
            <option key={tab.id} value={tab.id}>
              {tab.name}
            </option>
          ))}
        </select>

        <button className="bg-blue-600 text-white px-6 py-3 rounded">
          Create
        </button>
      </form>
    </main>
  );
}