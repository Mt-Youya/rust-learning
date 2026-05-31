import type { Metadata } from "next";
import { Bricolage_Grotesque, JetBrains_Mono, Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Nav } from "@/components/layout/Nav";
import { Footer } from "@/components/layout/Footer";
import { Providers } from "./providers";
import { Analytics } from "@vercel/analytics/next";

const geistSans = Geist({
  subsets: ["latin"],
  variable: "--font-geist",
  display: "swap",
});

const geistMono = Geist_Mono({
  subsets: ["latin"],
  variable: "--font-geist-mono",
  display: "swap",
});

const bricolage = Bricolage_Grotesque({
  subsets: ["latin"],
  variable: "--font-bricolage",
  display: "swap",
  weight: ["400", "500", "600", "700", "800"],
  fallback: ["Arial Black", "Impact", "ui-sans-serif"],
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-jetbrains",
  display: "swap",
  weight: ["400", "500", "600"],
  fallback: ["ui-monospace", "monospace"],
});

export const metadata: Metadata = {
  title: "RustForge — 将前端思维锻造成全栈",
  description:
    "为前端工程师设计的 Rust 全栈学习路径。通过 3D 动画理解所有权、借用、异步，覆盖 Web 后端、DevOps、AI 集成。",
  keywords: ["Rust", "全栈", "前端转型", "学习", "异步", "Web开发", "DevOps", "AI"],
  icons: {
    icon: [
      { url: "/favicon.ico", sizes: "any" },
      { url: "/icon.svg", type: "image/svg+xml" },
    ],
    apple: "/apple-icon.png",
  },
  manifest: "/manifest.json",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const fontVars = [
    geistSans.variable,
    geistMono.variable,
    bricolage.variable,
    jetbrainsMono.variable,
  ].join(" ");

  return (
    // suppressHydrationWarning: next-themes injects class on client to avoid flash
    <html lang="zh-CN" className={fontVars} suppressHydrationWarning>
      <body className="antialiased bg-background text-foreground">
        <Providers>
          <Nav />
          <main>{children}</main>
          <Footer />
        </Providers>
        <Analytics />
      </body>
    </html>
  );
}
