import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI Marketing Intelligence Platform",
  description: "Customer segmentation, campaign recommendations and marketing insights dashboard",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
