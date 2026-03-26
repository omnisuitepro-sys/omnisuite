"use client";

export default function LogsPage() {
  return (
    <div className="space-y-4">
      <h1 className="text-3xl font-bold text-gray-800">System Logs</h1>
      <p className="text-gray-600">
        Real‑time activity audit of sync workers, orders, pricing updates, and background tasks.
      </p>
      <div className="mt-6 border rounded-lg p-6 bg-white shadow">
        <p className="text-gray-500">🧩 Log viewer component coming soon — will stream API and job events.</p>
      </div>
    </div>
  );
}