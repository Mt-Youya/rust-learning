"use client";

import Link from "next/link";
import { ArrowLeft, ArrowRight } from "lucide-react";
import { useLanguage } from "@/contexts/LanguageContext";

interface ChapterNavProps {
  prev: string | null;
  next: string | null;
  chapter: number;
  total?: number;
}

export function ChapterNav({ prev, next, chapter, total = 8 }: ChapterNavProps) {
  const { lang } = useLanguage();
  const prevLabel = lang === "en" ? "Previous" : "上一章";
  const nextLabel = lang === "en" ? "Next" : "下一章";
  const homeLabel = lang === "en" ? "Home" : "返回首页";

  return (
    <nav className="relative z-10 border-t border-[oklch(0.16_0.015_265)] py-12">
      <div className="mx-auto max-w-3xl px-6 flex items-center justify-between gap-4">
        {prev ? (
          <Link
            href={`/chapter/${prev}`}
            className="group flex items-center gap-3 px-5 py-3.5 rounded-lg border border-[oklch(0.20_0.018_265)] hover:border-[oklch(0.35_0.02_265)] bg-[oklch(0.13_0.012_265)] hover:bg-[oklch(0.16_0.015_265)] transition-all duration-200"
          >
            <ArrowLeft className="w-4 h-4 text-[oklch(0.46_0.02_265)] group-hover:-translate-x-0.5 transition-transform duration-200" />
            <div>
              <div className="text-[10px] font-mono text-[oklch(0.40_0.02_265)]">{prevLabel}</div>
              <div className="text-sm font-semibold text-[oklch(0.82_0.01_265)]">
                CH.{String(chapter - 1).padStart(2, "0")}
              </div>
            </div>
          </Link>
        ) : (
          <Link
            href="/"
            className="group flex items-center gap-3 px-5 py-3.5 rounded-lg border border-[oklch(0.20_0.018_265)] hover:border-[oklch(0.35_0.02_265)] bg-[oklch(0.13_0.012_265)] hover:bg-[oklch(0.16_0.015_265)] transition-all duration-200"
          >
            <ArrowLeft className="w-4 h-4 text-[oklch(0.46_0.02_265)] group-hover:-translate-x-0.5 transition-transform duration-200" />
            <div className="text-sm font-semibold text-[oklch(0.82_0.01_265)]">{homeLabel}</div>
          </Link>
        )}

        <div className="text-xs font-mono text-[oklch(0.40_0.02_265)] hidden sm:block">
          {chapter} / {total}
        </div>

        {next ? (
          <Link
            href={`/chapter/${next}`}
            className="group flex items-center gap-3 px-5 py-3.5 rounded-lg border border-[oklch(0.68_0.18_42_/_0.35)] bg-[oklch(0.68_0.18_42_/_0.06)] hover:border-[oklch(0.68_0.18_42_/_0.6)] hover:bg-[oklch(0.68_0.18_42_/_0.12)] transition-all duration-200"
          >
            <div className="text-right">
              <div className="text-[10px] font-mono text-[oklch(0.68_0.18_42)]">{nextLabel}</div>
              <div className="text-sm font-semibold text-[oklch(0.82_0.01_265)]">
                CH.{String(chapter + 1).padStart(2, "0")}
              </div>
            </div>
            <ArrowRight className="w-4 h-4 text-[oklch(0.68_0.18_42)] group-hover:translate-x-0.5 transition-transform duration-200" />
          </Link>
        ) : (
          <div />
        )}
      </div>
    </nav>
  );
}
