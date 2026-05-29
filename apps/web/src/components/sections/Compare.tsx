"use client";

import { useRef, useEffect } from "react";
import { cn } from "@/lib/utils";
import { jsRustComparisons } from "@/data/curriculum";

function CompareCard({
  comparison,
  index,
}: {
  comparison: (typeof jsRustComparisons)[0];
  index: number;
}) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const obs = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          el.style.opacity = "1";
          el.style.transform = "translateY(0)";
          obs.unobserve(el);
        }
      },
      { threshold: 0.15 }
    );
    obs.observe(el);
    return () => obs.disconnect();
  }, []);

  return (
    <div
      ref={ref}
      className="transition-all duration-700"
      style={{
        opacity: 0,
        transform: "translateY(24px)",
        transitionDelay: `${index * 120}ms`,
      }}
    >
      {/* Concept label */}
      <div className="flex items-center gap-3 mb-4">
        <span className="text-[10px] font-mono tracking-widest text-[oklch(0.68_0.18_42)] uppercase">
          {String(index + 1).padStart(2, "0")}
        </span>
        <h3 className="text-base font-semibold font-display text-[oklch(0.94_0.008_265)]">
          {comparison.concept}
        </h3>
        <div className="flex-1 h-px bg-[oklch(0.20_0.018_265)]" />
      </div>

      {/* Side-by-side code */}
      <div className="grid md:grid-cols-2 gap-3">
        {/* JS side */}
        <div className="rounded-lg border border-[oklch(0.20_0.018_265)] overflow-hidden">
          <div className="flex items-center gap-2 px-4 py-2 bg-[oklch(0.13_0.012_265)] border-b border-[oklch(0.20_0.018_265)]">
            <div className="w-3 h-3 rounded-sm bg-[oklch(0.76_0.16_76_/_0.7)] flex items-center justify-center">
              <span className="text-[8px] font-bold text-[oklch(0.09_0.01_265)]">JS</span>
            </div>
            <span className="text-xs font-mono text-[oklch(0.46_0.02_265)]">JavaScript</span>
          </div>
          <pre className="p-4 text-xs font-mono text-[oklch(0.60_0.02_265)] leading-relaxed overflow-x-auto bg-[oklch(0.09_0.01_265)]">
            <code>{comparison.js}</code>
          </pre>
        </div>

        {/* Rust side */}
        <div className="rounded-lg border border-[oklch(0.68_0.18_42_/_0.3)] overflow-hidden">
          <div className="flex items-center gap-2 px-4 py-2 bg-[oklch(0.68_0.18_42_/_0.08)] border-b border-[oklch(0.68_0.18_42_/_0.3)]">
            <div className="w-3 h-3 rounded-sm bg-[oklch(0.68_0.18_42)] flex items-center justify-center">
              <span className="text-[8px] font-bold text-[oklch(0.09_0.01_265)]">Rs</span>
            </div>
            <span className="text-xs font-mono text-[oklch(0.68_0.18_42)]">Rust</span>
          </div>
          <pre className="p-4 text-xs font-mono text-[oklch(0.72_0.01_265)] leading-relaxed overflow-x-auto bg-[oklch(0.09_0.01_265)]">
            <code>{comparison.rust}</code>
          </pre>
        </div>
      </div>

      {/* Insight */}
      <div className="mt-3 flex gap-3 px-4 py-3 rounded bg-[oklch(0.68_0.18_42_/_0.06)] border border-[oklch(0.68_0.18_42_/_0.2)]">
        <span className="text-[oklch(0.68_0.18_42)] shrink-0 text-sm">→</span>
        <p className="text-xs text-[oklch(0.60_0.02_265)] leading-relaxed">{comparison.insight}</p>
      </div>
    </div>
  );
}

export function Compare() {
  return (
    <section id="compare" className="py-32 border-t border-[oklch(0.16_0.015_265)]">
      <div className="mx-auto max-w-5xl px-6">
        {/* Header */}
        <div className="mb-16">
          <div className="text-xs font-mono tracking-widest text-[oklch(0.68_0.18_42)] mb-3 uppercase">
            前端视角
          </div>
          <h2 className="text-3xl md:text-4xl font-display font-black tracking-tight text-[oklch(0.94_0.008_265)] mb-4">
            JavaScript 开发者
            <br />
            <span className="text-[oklch(0.52_0.02_265)]">看 Rust 的三个关键转变</span>
          </h2>
          <p className="text-sm text-[oklch(0.46_0.02_265)] max-w-lg">
            不是从零开始，而是从你已经知道的出发。
            这些对比帮你建立思维模型，而不是死记语法。
          </p>
        </div>

        {/* Comparison cards */}
        <div className="space-y-12">
          {jsRustComparisons.map((c, i) => (
            <CompareCard key={c.concept} comparison={c} index={i} />
          ))}
        </div>
      </div>
    </section>
  );
}
