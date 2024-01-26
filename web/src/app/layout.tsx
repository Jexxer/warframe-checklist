import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Warframe Checklist",
  description: "A daily/weekly checklist for Warframe",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
