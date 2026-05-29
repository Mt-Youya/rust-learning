"use client";

import Link from "next/link";
import { cn } from "@/lib/utils";
import { chapters, type Chapter } from "@/data/curriculum";
import { Lock, Clock, ChevronRight, Sparkles } from "lucide-react";
import { useRef, useEffect } from "react";

function ChapterNode({ chapter, index }: { chapter: Chapter; index: number }) {
  const isAvailable = chapter.status === "available";
  const isComingSoon = chapter.status === "coming-soon";

  const content = (
    <div
      className={cn(
        "group relative flex-shrink-0 w-72 rounded-lg border transition-all duration-300",
        isAvailable
          ? "border-[oklch(0.20_0.018_265)] bg-[oklch(0.13_0.012_265)] hover:border-[oklch(0.68_0.18_42_/_0.5)] hover:-translate-y-1 hover:shadow-[0_8px_32px_oklch(0.68_0.18_42_/_0.12)] cursor-pointer"
          : "border-[oklch(0.16_0.015_265)] bg-[oklch(0.11_0.012_265)] opacity-60 cursor-not-allowed"
      )}
    >
      {/* Chapter number strip */}
      <div className={cn(
        "absolute left-0 top-0 bottom-0 w-1 rounded-l-lg",
        isAvailable ? "bg-[oklch(0.68_0.18_42)]" : "bg-[oklch(0.22_0.018_265)]"
      )} />

      <div className="pl-5 pr-4 py-4 space-y-3">
        {/* Header */}
        <div className="flex items-start justify-between gap-2">
          <div>
            <div className={cn(
              "text-[10px] font-mono tracking-widest mb-1",
              isAvailable ? "text-[oklch(0.68_0.18_42)]" : "text-[oklch(0.40_0.02_265)]"
            )}>
              CH.{String(chapter.number).padStart(2, "0")}
            </div>
            <h3 className={cn(
              "text-sm font-semibold font-display leading-tight",
              isAvailable ? "text-[oklch(0.94_0.008_265)]" : "text-[oklch(0.52_0.02_265)]"
            )}>
              {chapter.title}
            </h3>
          </div>
          <div className="shrink-0 mt-0.5">
            {isComingSoon ? (
              <span className="text-[10px] font-mono px-2 py-0.5 rounded border border-[oklch(0.22_0.018_265)] text-[oklch(0.40_0.02_265)]">
                即将上线
              </span>
            ) : isAvailable ? (
              <ChevronRight className="w-4 h-4 text-[oklch(0.68_0.18_42)] opacity-0 group-hover:opacity-100 transition-opacity duration-200" />
            ) : (
              <Lock className="w-3.5 h-3.5 text-[oklch(0.40_0.02_265)]" />
            )}
          </div>
        </div>

        <p className="text-xs text-[oklch(0.46_0.02_265)] leading-relaxed line-clamp-2">
          {chapter.description}
        </p>

        {/* Concepts */}
        <div className="flex flex-wrap gap-1">
          {chapter.concepts.slice(0, 3).map((c) => (
            <span
              key={c}
              className="text-[10px] px-1.5 py-0.5 rounded bg-[oklch(0.16_0.015_265)] text-[oklch(0.46_0.02_265)] font-mono"
            >
              {c}
            </span>
          ))}
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between pt-1 border-t border-[oklch(0.16_0.015_265)]">
          <div className="flex items-center gap-1 text-[10px] text-[oklch(0.40_0.02_265)]">
            <Clock className="w-3 h-3" />
            {chapter.duration}
          </div>
          <div className="text-[10px] text-[oklch(0.40_0.02_265)] font-mono truncate max-w-[120px]">
            ⚡ {chapter.project}
          </div>
        </div>
      </div>
    </div>
  );

  return isAvailable ? (
    <Link href={`/chapter/${chapter.slug}`}>{content}</Link>
  ) : (
    <div>{content}</div>
  );
}

export function Curriculum() {
  const scrollRef = useRef<HTMLDivElement>(null);

  // Drag-to-scroll
  useEffect(() => {
    const el = scrollRef.current;
    if (!el) return;
    let isDown = false;
    let startX = 0;
    let scrollLeft = 0;

    const onDown = (e: MouseEvent) => {
      isDown = true;
      el.style.cursor = "grabbing";
      startX = e.pageX - el.offsetLeft;
      scrollLeft = el.scrollLeft;
    };
    const onUp = () => { isDown = false; el.style.cursor = "grab"; };
    const onMove = (e: MouseEvent) => {
      if (!isDown) return;
      e.preventDefault();
      const x = e.pageX - el.offsetLeft;
      el.scrollLeft = scrollLeft - (x - startX) * 1.5;
    };

    el.style.cursor = "grab";
    el.addEventListener("mousedown", onDown);
    window.addEventListener("mouseup", onUp);
    el.addEventListener("mousemove", onMove);
    return () => {
      el.removeEventListener("mousedown", onDown);
      window.removeEventListener("mouseup", onUp);
      el.removeEventListener("mousemove", onMove);
    };
  }, []);

  return (
    <section id="curriculum" className="py-32 relative">
      {/* Section header */}
      <div className="mx-auto max-w-7xl px-6 mb-12">
        <div className="flex items-end justify-between gap-4">
          <div>
            <div className="text-xs font-mono tracking-widest text-[oklch(0.68_0.18_42)] mb-3 uppercase">
              课程地图
            </div>
            <h2 className="text-3xl md:text-4xl font-display font-black tracking-tight text-[oklch(0.94_0.008_265)]">
              从零到全栈的路径
            </h2>
          </div>
          <p className="hidden md:block text-sm text-[oklch(0.46_0.02_265)] max-w-xs text-right">
            拖拽横向浏览 · 每章节有实战项目和视频
          </p>
        </div>

        {/* Timeline connector */}
        <div className="mt-8 relative">
          <div className="absolute top-5 left-0 right-0 h-px bg-gradient-to-r from-transparent via-[oklch(0.20_0.018_265)] to-transparent" />
          <div className="absolute top-5 left-0 w-24 h-px bg-gradient-to-r from-[oklch(0.68_0.18_42_/_0.5)] to-transparent" />
        </div>
      </div>

      {/* Horizontal scroll track */}
      <div
        ref={scrollRef}
        className="flex gap-4 px-6 pb-4 overflow-x-auto select-none"
        style={{
          scrollbarWidth: "none",
          msOverflowStyle: "none",
          paddingLeft: "calc((100vw - 1280px) / 2 + 24px)",
          paddingRight: "calc((100vw - 1280px) / 2 + 24px)",
        }}
      >
        {chapters.map((chapter, i) => (
          <div key={chapter.id} className="flex items-start gap-4">
            <ChapterNode chapter={chapter} index={i} />
            {i < chapters.length - 1 && (
              <div className="flex items-center self-center shrink-0 mt-2">
                <div className="w-6 h-px bg-[oklch(0.20_0.018_265)]" />
                <div className="w-1 h-1 rounded-full bg-[oklch(0.30_0.02_265)]" />
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Legend */}
      <div className="mx-auto max-w-7xl px-6 mt-6">
        <div className="flex items-center gap-6 text-xs text-[oklch(0.40_0.02_265)]">
          <span className="flex items-center gap-2">
            <span className="w-3 h-3 rounded border border-[oklch(0.68_0.18_42_/_0.5)] bg-[oklch(0.68_0.18_42_/_0.08)]" />
            可学习
          </span>
          <span className="flex items-center gap-2">
            <span className="w-3 h-3 rounded border border-[oklch(0.16_0.015_265)] bg-[oklch(0.11_0.012_265)] opacity-60" />
            即将上线
          </span>
          <span className="flex items-center gap-2 ml-auto">
            <Sparkles className="w-3 h-3 text-[oklch(0.68_0.18_42)]" />
            每章附实战项目
          </span>
        </div>
      </div>
    </section>
  );
}
