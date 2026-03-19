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
        <div className="overflow-x-auto">
          <table className="min-w-full bg-white rounded-lg shadow">
            <thead className="bg-gray-100 text-left">
              <tr>
                <th className="p-4">ID</th>
                <th className="p-4">Title</th>
                <th className="p-4">Price</th>
              </tr>
            </thead>
            <tbody>
              {data.map((item: any) => (
                <tr key={item.id} className="border-t">
                  <td className="p-4">{item.id}</td>
                  <td className="p-4">{item.title}</td>
                  <td className="p-4">${item.price}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </main>
  );
}