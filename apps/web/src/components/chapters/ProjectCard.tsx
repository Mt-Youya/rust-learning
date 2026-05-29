"use client";

import { Terminal, Clock, Wrench } from "lucide-react";
import { useLanguage } from "@/contexts/LanguageContext";

interface ProjectCardProps {
  title: string;
  description: string;
  skills: string[];
  command: string;
  difficulty?: string;
  estimatedTime?: string;
}

export function ProjectCard({
  title,
  description,
  skills,
  command,
  difficulty,
  estimatedTime,
}: ProjectCardProps) {
  const { lang } = useLanguage();
  const headerLabel   = lang === "en" ? "HANDS-ON PROJECT" : "实战项目";
  const defaultDiff   = lang === "en" ? "Beginner" : "初级";
  const displayDiff   = difficulty ?? defaultDiff;

  return (
    <div className="not-prose my-8 rounded-xl border border-[oklch(0.68_0.18_42_/_0.35)] bg-[oklch(0.68_0.18_42_/_0.05)] overflow-hidden">
      {/* Header */}
      <div className="px-6 py-4 border-b border-[oklch(0.68_0.18_42_/_0.2)] flex items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded border border-[oklch(0.68_0.18_42_/_0.4)] bg-[oklch(0.68_0.18_42_/_0.12)] flex items-center justify-center">
            <Wrench className="w-4 h-4 text-[oklch(0.68_0.18_42)]" />
          </div>
          <div>
            <div className="text-[10px] font-mono tracking-widest text-[oklch(0.68_0.18_42)] mb-0.5">
              {headerLabel}
            </div>
            <h3 className="text-sm font-semibold text-[oklch(0.88_0.008_265)] font-display">{title}</h3>
          </div>
        </div>
        <div className="flex items-center gap-3 text-xs text-[oklch(0.46_0.02_265)]">
          {estimatedTime && (
            <span className="flex items-center gap-1.5">
              <Clock className="w-3.5 h-3.5" />
              {estimatedTime}
            </span>
          )}
          <span className="px-2 py-0.5 rounded border border-[oklch(0.20_0.018_265)] text-[10px] font-mono">
            {displayDiff}
          </span>
        </div>
      </div>

      {/* Body */}
      <div className="px-6 py-4 space-y-4">
        <p className="text-sm text-[oklch(0.58_0.02_265)] leading-relaxed">{description}</p>

        {/* Skills */}
        <div className="flex flex-wrap gap-1.5">
          {skills.map((skill) => (
            <span
              key={skill}
              className="text-[11px] font-mono px-2 py-0.5 rounded bg-[oklch(0.16_0.015_265)] border border-[oklch(0.22_0.018_265)] text-[oklch(0.52_0.02_265)]"
            >
              {skill}
            </span>
          ))}
        </div>

        {/* Start command */}
        <div className="flex items-center gap-3 px-4 py-3 rounded-lg bg-[oklch(0.09_0.01_265)] border border-[oklch(0.20_0.018_265)]">
          <Terminal className="w-4 h-4 text-[oklch(0.68_0.18_42)] shrink-0" />
          <code className="text-xs font-mono text-[oklch(0.74_0.01_265)]">{command}</code>
        </div>
      </div>
    </div>
  );
}
