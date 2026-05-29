"use client";

import Link from "next/link";
import { ArrowLeft, Clock, Code2 } from "lucide-react";
import type { ChapterFrontmatter } from "@/lib/mdx";
import { useLanguage } from "@/contexts/LanguageContext";

interface ChapterHeroProps {
  frontmatter: ChapterFrontmatter;
}

export function ChapterHero({ frontmatter }: ChapterHeroProps) {
  const { chapter, title, subtitle, duration, project, prev } = frontmatter;
  const { lang } = useLanguage();

  const prevLabel    = lang === "en" ? "Previous" : "上一章";
  const projectLabel = lang === "en" ? "Project:" : "实战：";

  return (
    <div className="not-prose mb-16 pt-8">
      {/* Breadcrumb */}
      <Link
        href={prev ? `/chapter/${prev}` : "/"}
        className="inline-flex items-center gap-2 text-xs text-[oklch(0.46_0.02_265)] hover:text-[oklch(0.68_0.18_42)] transition-colors duration-200 mb-8"
      >
        <ArrowLeft className="w-3.5 h-3.5" />
        {prev ? prevLabel : "RustForge"}
      </Link>

      {/* Chapter badge + meta */}
      <div className="flex flex-wrap items-center gap-3 mb-4">
        <span className="text-[10px] font-mono tracking-widest text-[oklch(0.68_0.18_42)] bg-[oklch(0.68_0.18_42_/_0.1)] border border-[oklch(0.68_0.18_42_/_0.3)] px-2.5 py-1 rounded">
          CH.{String(chapter).padStart(2, "0")}
        </span>
        <span className="flex items-center gap-1.5 text-xs text-[oklch(0.46_0.02_265)]">
          <Clock className="w-3.5 h-3.5" />
          {duration}
        </span>
        <span className="flex items-center gap-1.5 text-xs text-[oklch(0.46_0.02_265)]">
          <Code2 className="w-3.5 h-3.5" />
          {projectLabel} {project}
        </span>
      </div>

      {/* Title */}
      <h1 className="text-4xl md:text-6xl font-display font-black tracking-tighter leading-tight mb-3">
        <span className="text-[oklch(0.94_0.008_265)]">{title}</span>
      </h1>
      <p className="text-base text-[oklch(0.52_0.02_265)]">{subtitle}</p>

      {/* Divider */}
      <div className="mt-8 h-px bg-gradient-to-r from-[oklch(0.68_0.18_42_/_0.4)] via-[oklch(0.20_0.018_265)] to-transparent" />
    </div>
  );
}
