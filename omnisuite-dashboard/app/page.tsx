"use client";

import { useEffect, useState } from "react";

export default function Home() {
  const [status, setStatus] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  // ✅ TEMP: use Render URL (bypass domain issues)
  const API_URL = "https://omnisuite-api.onrender.com";

  useEffect(() => {
    async function fetchStatus() {
      try {
        const res = await fetch(`${API_URL}/alpha/status`);
        const data = await res.json();
        setStatus(data);
      } catch (err) {
        setStatus({ error: "Unable to reach API" });
      } finally {
        setLoading(false);
      }
    }

    fetchStatus();
  }, []);

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-12 bg-gray-50">
      <h1 className="text-3xl font-bold mb-6 text-gray-800">
        OmniSuite API Status
      </h1>

      {loading ? (
        <div className="text-gray-600">Checking...</div>
      ) : (
        <pre className="bg-white p-6 rounded-lg shadow text-gray-700 w-full max-w-xl overflow-auto text-sm">
          {JSON.stringify(status, null, 2)}
        </pre>
      )}
    </main>
  );
}