"use client";
import Providers from "./providers";
import Link from "next/link";

export default function Layout({ children }: any) {
  return (
    <html>
      <body className="flex">
        <aside className="w-60 p-4 bg-gray-100">
          <Link href="/">Dashboard</Link><br/>
          <Link href="/listings">Listings</Link><br/>
          <Link href="/listings/create">Create</Link>
	<Link href="/scan">AI Scanner</Link>
        </aside>

        <main className="flex-1 p-6">
          <Providers>{children}</Providers>
        </main>
      </body>
    </html>
  );
}