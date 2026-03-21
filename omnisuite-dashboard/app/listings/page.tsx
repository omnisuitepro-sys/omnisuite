"use client";

import { useQuery } from "@tanstack/react-query";
import api from "@/lib/api";

export default function ListingsPage() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["listings"],
    queryFn: async () => (await api.get("/listings")).data,
  });

  if (isLoading) return <p>Loading...</p>;
  if (error) return <p>Error loading listings</p>;

  return (
    <main className="p-10">
      <h1 className="text-3xl font-bold mb-6">Listings</h1>

      <div className="space-y-4">
        {data.map((item: any) => (
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