"use client";
import Link from "next/link";
import "./globals.css";
import QueryProvider from "./QueryProvider";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="flex min-h-screen bg-gray-50 text-gray-800">
        <aside className="w-64 bg-white shadow-md p-6 flex flex-col">
          <h2 className="text-2xl font-bold mb-8">OmniSuite Pro</h2>
          <nav className="flex flex-col gap-3">
            <Link href="/" className="hover:text-blue-700">Status</Link>
            <Link href="/listings" className="hover:text-blue-700">Listings</Link>
            <Link href="/profits" className="hover:text-blue-700">Profits</Link>
            <Link href="/logs" className="hover:text-blue-700">Logs</Link>
            <Link href="/settings" className="hover:text-blue-700">Settings</Link>
          </nav>
        </aside>

        <QueryProvider>
          <main className="flex-1 p-10 overflow-y-auto">{children}</main>
        </QueryProvider>
      </body>
    </html>
  );
}