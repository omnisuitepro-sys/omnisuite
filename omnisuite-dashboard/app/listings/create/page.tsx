"use client";

import { useState } from "react";
import api from "@/lib/api";
import { useRouter } from "next/navigation";

export default function CreateListingPage() {
  const [title, setTitle] = useState("");
  const [price, setPrice] = useState("");
  const router = useRouter();

  const handleSubmit = async (e: any) => {
    e.preventDefault();

    await api.post("/listings", {
      title,
      price: parseFloat(price),
    });

    router.push("/listings");
  };

  return (
    <main className="p-10">
      <h1 className="text-3xl font-bold mb-6">Create Listing</h1>

      <form onSubmit={handleSubmit} className="space-y-4 max-w-md">
        <input
          className="w-full p-3 border rounded"
          placeholder="Product title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />

        <input
          className="w-full p-3 border rounded"
          placeholder="Price"
          value={price}
          onChange={(e) => setPrice(e.target.value)}
        />

        <button className="bg-blue-600 text-white px-6 py-3 rounded">
          Create
        </button>
      </form>
    </main>
  );
}