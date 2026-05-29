"use client";

import dynamic from "next/dynamic";
import Link from "next/link";
import { ArrowRight, Star } from "lucide-react";
import { cn } from "@/lib/utils";

const OwnershipScene = dynamic(
  () => import("@/components/animations/OwnershipScene").then((m) => m.OwnershipScene),
  {
    ssr: false,
    loading: () => (
      <div className="absolute inset-0 flex items-center justify-center">
        <div className="w-1 h-1 rounded-full bg-[oklch(0.68_0.18_42)] animate-pulse-ring" />
      </div>
    ),
  }
);

export function Hero() {
  return (
    <section className="relative min-h-screen flex flex-col items-center justify-center overflow-hidden">
      {/* Three.js background scene */}
      <OwnershipScene className="absolute inset-0 pointer-events-none" />

      {/* Grid backdrop */}
      <div className="absolute inset-0 grid-bg opacity-30 pointer-events-none" />

      {/* Radial vignette */}
      <div
        className="absolute inset-0 pointer-events-none"
        style={{
          background: "radial-gradient(ellipse 80% 60% at 50% 50%, transparent 30%, oklch(0.09 0.01 265 / 0.7) 100%)",
        }}
      />

      {/* Rust glow orb */}
      <div
        className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[300px] pointer-events-none"
        style={{
          background: "radial-gradient(ellipse at center, oklch(0.68 0.18 42 / 0.06) 0%, transparent 70%)",
        }}
      />

      {/* Content */}
      <div className="relative z-10 mx-auto max-w-5xl px-6 text-center">
        {/* Badge */}
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full border border-[oklch(0.68_0.18_42_/_0.3)] bg-[oklch(0.68_0.18_42_/_0.06)] mb-8 animate-fade-up">
          <span className="w-1.5 h-1.5 rounded-full bg-[oklch(0.68_0.18_42)] animate-pulse" />
          <span className="text-xs font-mono text-[oklch(0.68_0.18_42)]">
            为前端工程师设计的 Rust 全栈路径
          </span>
        </div>

        {/* Main headline */}
        <h1 className="text-5xl md:text-7xl lg:text-8xl font-display font-black tracking-tighter leading-[0.95] mb-6 animate-fade-up stagger-1">
          <span className="text-[oklch(0.94_0.008_265)]">将前端思维</span>
          <br />
          <span
            className="text-[oklch(0.68_0.18_42)]"
            style={{
              textShadow: "0 0 40px oklch(0.68 0.18 42 / 0.35)",
            }}
          >
            锻造成全栈
          </span>
        </h1>

        {/* Subline */}
        <p className="text-base md:text-lg text-[oklch(0.52_0.02_265)] max-w-xl mx-auto mb-10 animate-fade-up stagger-2 leading-relaxed">
          从 JavaScript 视角出发，系统掌握{" "}
          <span className="text-[oklch(0.82_0.01_265)]">Rust</span> · 后端 ·
          DevOps · AI 集成。
          每个概念都有可视化动画，每章附实战案例。
        </p>

        {/* CTA group */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 animate-fade-up stagger-3">
          <Link
            href="/chapter/basics"
            className={cn(
              "group flex items-center gap-2.5 px-7 py-3.5 rounded font-semibold text-sm",
              "bg-[oklch(0.68_0.18_42)] text-[oklch(0.09_0.01_265)]",
              "hover:bg-[oklch(0.74_0.20_48)] transition-all duration-300",
              "shadow-[0_0_0_1px_oklch(0.68_0.18_42_/_0.5),_0_0_24px_oklch(0.68_0.18_42_/_0.25)]",
              "hover:shadow-[0_0_0_1px_oklch(0.74_0.20_48_/_0.8),_0_0_40px_oklch(0.74_0.20_48_/_0.35)]"
            )}
          >
            从第一章开始
            <ArrowRight className="w-4 h-4 transition-transform duration-200 group-hover:translate-x-0.5" />
          </Link>

          <Link
            href="/#curriculum"
            className="flex items-center gap-2 px-6 py-3.5 rounded font-semibold text-sm text-[oklch(0.60_0.02_265)] border border-[oklch(0.20_0.018_265)] hover:border-[oklch(0.35_0.02_265)] hover:text-[oklch(0.82_0.01_265)] hover:bg-[oklch(0.20_0.018_265)] transition-all duration-300"
          >
            查看课程地图
          </Link>
        </div>

        {/* Social proof */}
        <div className="mt-12 flex items-center justify-center gap-6 text-xs text-[oklch(0.40_0.02_265)] animate-fade-up stagger-4">
          <span className="flex items-center gap-1.5">
            <Star className="w-3.5 h-3.5 text-[oklch(0.68_0.18_42)]" />
            8 个系统章节
          </span>
          <span className="w-px h-3 bg-[oklch(0.22_0.018_265)]" />
          <span>动画 + 代码 + 实战</span>
          <span className="w-px h-3 bg-[oklch(0.22_0.018_265)]" />
          <span>完全免费开源</span>
        </div>
      </div>

      {/* Scroll indicator */}
      <div className="absolute bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2 animate-fade-up stagger-5">
        <span className="text-[10px] font-mono tracking-widest text-[oklch(0.35_0.02_265)] uppercase">
          滚动探索
        </span>
        <div className="w-px h-8 bg-gradient-to-b from-[oklch(0.35_0.02_265)] to-transparent" />
      </div>
    </section>
  );
}
