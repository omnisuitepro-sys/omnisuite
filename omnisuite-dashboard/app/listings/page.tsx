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

      {isLoading && <p>Loading...</p>}
      {error && <p className="text-red-600">Error loading listings</p>}

      {data && (
        <div className="space-y-4">
          {data.map((item: any) => (
            <div key={item.id} className="p-4 bg-white rounded shadow">
              <h2 className="font-bold">{item.title}</h2>
              <p>${item.price}</p>
            </div>
          ))}
        </div>
      )}
    </main>
  );
}