import Link from "next/link";
import { ArrowRight } from "lucide-react";

export function CallToAction() {
  return (
    <section className="py-32 border-t border-[oklch(0.16_0.015_265)] relative overflow-hidden">
      {/* Background glow */}
      <div
        className="absolute inset-0 pointer-events-none"
        style={{
          background:
            "radial-gradient(ellipse 60% 50% at 50% 100%, oklch(0.68 0.18 42 / 0.08) 0%, transparent 70%)",
        }}
      />

      <div className="relative mx-auto max-w-3xl px-6 text-center">
        <div className="text-xs font-mono tracking-widest text-[oklch(0.68_0.18_42)] mb-4 uppercase">
          准备好了吗
        </div>
        <h2 className="text-4xl md:text-5xl font-display font-black tracking-tight text-[oklch(0.94_0.008_265)] mb-5 leading-[1.05]">
          第一章：所有权与借用
          <br />
          <span className="text-[oklch(0.68_0.18_42)]">从内存可视化开始</span>
        </h2>
        <p className="text-sm text-[oklch(0.46_0.02_265)] mb-10 leading-relaxed max-w-md mx-auto">
          通过 3D 动画看见内存的分配与释放。
          理解 Rust 最核心的概念，构建第一个真正安全的命令行工具。
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <Link
            href="/chapter/basics"
            className="group flex items-center gap-2.5 px-8 py-4 rounded font-semibold text-sm bg-[oklch(0.68_0.18_42)] text-[oklch(0.09_0.01_265)] hover:bg-[oklch(0.74_0.20_48)] transition-all duration-300 shadow-[0_0_32px_oklch(0.68_0.18_42_/_0.3)] hover:shadow-[0_0_48px_oklch(0.74_0.20_48_/_0.45)]"
          >
            开始第一章
            <ArrowRight className="w-4 h-4 group-hover:translate-x-0.5 transition-transform duration-200" />
          </Link>
        </div>

        {/* Footnote */}
        <p className="mt-8 text-xs text-[oklch(0.35_0.02_265)]">
          完全免费 · 无需注册 · 随时开始
        </p>
      </div>
    </section>
  );
}
