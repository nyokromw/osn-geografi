import type { Metadata } from "next";
import localFont from "next/font/local";
import { Analytics } from "@vercel/analytics/next";
import "./globals.css";

const sans = localFont({
  src: "./fonts/dm-sans.woff2",
  variable: "--atlas-sans",
  weight: "400 700",
  display: "swap",
});

const display = localFont({
  src: [
    { path: "./fonts/instrument-serif.woff2", weight: "400", style: "normal" },
    { path: "./fonts/instrument-serif-italic.woff2", weight: "400", style: "italic" },
  ],
  variable: "--atlas-serif",
  display: "swap",
});

export const metadata: Metadata = {
  title: "OSNGEO.id — Persiapan OSN Geografi",
  description: "Persiapkan OSN Geografi dengan tryout, latihan per topik, video, dan modul belajar.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="id" className={[sans.variable, display.variable].join(" ")}>
      <body>{children}<Analytics /></body>
    </html>
  );
}
