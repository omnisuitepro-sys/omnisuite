"use client";

import Providers from "./providers";
import Link from "next/link";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="flex min-h-screen bg-gray-50 text-gray-800">
        
        {/* ✅ Sidebar */}
        <aside className="w-64 bg-white shadow-md p-6 flex flex-col">
          <h2 className="text-2xl font-bold mb-8">OmniSuite</h2>

          <nav className="flex flex-col gap-4">
            <Link href="/" className="hover:text-blue-600">
              Dashboard
            </Link>

            <Link href="/listings" className="hover:text-blue-600">
              Listings
            </Link>

            <Link href="/listings/create" className="hover:text-blue-600">
              + Create Listing
            </Link>
          </nav>
        </aside>

        {/* ✅ Main Content */}
        <main className="flex-1 p-10">
          <Providers>{children}</Providers>
        </main>

      </body>
    </html>
  );
}