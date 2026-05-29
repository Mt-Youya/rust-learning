"use client";

import { useLanguage } from "@/contexts/LanguageContext";

interface CompareBlockProps {
  concept: string;
  jsLabel?: string;
  rustLabel?: string;
  js: string;
  rust: string;
  insight?: string;
}

export function CompareBlock({
  concept,
  jsLabel = "JavaScript",
  rustLabel = "Rust",
  js,
  rust,
  insight,
}: CompareBlockProps) {
  const { lang } = useLanguage();
  const compareLabel = lang === "en" ? "Compare:" : "对比：";

  return (
    <div className="not-prose my-8 space-y-3">
      {/* Concept label */}
      <div className="flex items-center gap-3">
        <span className="text-xs font-mono text-[oklch(0.68_0.18_42)]">{compareLabel}</span>
        <span className="text-sm font-semibold text-[oklch(0.82_0.01_265)] font-display">{concept}</span>
        <div className="flex-1 h-px bg-[oklch(0.20_0.018_265)]" />
      </div>

      {/* Side-by-side code */}
      <div className="grid md:grid-cols-2 gap-3">
        {/* JS side */}
        <div className="rounded-lg border border-[oklch(0.20_0.018_265)] overflow-hidden">
          <div className="flex items-center gap-2 px-4 py-2 bg-[oklch(0.13_0.012_265)] border-b border-[oklch(0.20_0.018_265)]">
            <div className="w-3.5 h-3.5 rounded-sm bg-[oklch(0.76_0.16_76_/_0.8)] flex items-center justify-center">
              <span className="text-[7px] font-black text-[oklch(0.09_0.01_265)]">JS</span>
            </div>
            <span className="text-xs font-mono text-[oklch(0.46_0.02_265)]">{jsLabel}</span>
          </div>
          <pre className="p-4 text-xs font-mono text-[oklch(0.58_0.02_265)] leading-relaxed overflow-x-auto bg-[oklch(0.09_0.01_265)] m-0">
            <code>{js}</code>
          </pre>
        </div>

        {/* Rust side */}
        <div className="rounded-lg border border-[oklch(0.68_0.18_42_/_0.3)] overflow-hidden">
          <div className="flex items-center gap-2 px-4 py-2 bg-[oklch(0.68_0.18_42_/_0.08)] border-b border-[oklch(0.68_0.18_42_/_0.3)]">
            <div className="w-3.5 h-3.5 rounded-sm bg-[oklch(0.68_0.18_42)] flex items-center justify-center">
              <span className="text-[7px] font-black text-[oklch(0.09_0.01_265)]">Rs</span>
            </div>
            <span className="text-xs font-mono text-[oklch(0.68_0.18_42)]">{rustLabel}</span>
          </div>
          <pre className="p-4 text-xs font-mono text-[oklch(0.74_0.01_265)] leading-relaxed overflow-x-auto bg-[oklch(0.09_0.01_265)] m-0">
            <code>{rust}</code>
          </pre>
        </div>
      </div>

      {/* Insight */}
      {insight && (
        <div className="flex gap-3 px-4 py-3 rounded bg-[oklch(0.68_0.18_42_/_0.06)] border border-[oklch(0.68_0.18_42_/_0.2)]">
          <span className="text-[oklch(0.68_0.18_42)] shrink-0 text-sm font-mono">→</span>
          <p className="text-xs text-[oklch(0.60_0.02_265)] leading-relaxed">{insight}</p>
        </div>
      )}
    </div>
  );
}
