"use client";

import { useQuery } from "@tanstack/react-query";
import api from "@/lib/api";

export default function ListingsPage() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["listings"],
    queryFn: async () => (await api.get("/listings")).data,
  });

  return (
    <main className="p-10">
      <h1 className="text-3xl font-bold mb-6">Listings</h1>

      {isLoading && <p>Loading listings...</p>}
      {error && <p className="text-red-600">Error loading data</p>}

      {data && (
        <pre className="bg-white p-4 rounded shadow">
          {JSON.stringify(data, null, 2)}
        </pre>
      )}
    </main>
  );
}