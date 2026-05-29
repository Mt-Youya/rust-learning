"use client";

import { useLanguage } from "@/contexts/LanguageContext";
import { cn } from "@/lib/utils";

interface LanguageToggleProps {
  className?: string;
}

export function LanguageToggle({ className }: LanguageToggleProps) {
  const { lang, toggle, t } = useLanguage();

  return (
    <button
      onClick={toggle}
      aria-label={t.lang.switchTo}
      title={t.lang.switchTo}
      className={cn(
        "flex items-center justify-center h-8 px-2 rounded-md",
        "text-xs font-mono font-semibold",
        "text-muted-foreground hover:text-foreground",
        "hover:bg-accent transition-colors duration-200",
        className
      )}
    >
      {lang === "zh" ? "EN" : "中"}
    </button>
  );
}
