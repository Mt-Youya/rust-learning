"use client";

import { useLanguage } from "@/contexts/LanguageContext";

export function Footer() {
  const { t } = useLanguage();
  return (
    <footer className="border-t border-border py-8 px-6">
      <div className="mx-auto max-w-7xl flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-muted-foreground">
        <span className="font-display font-bold text-foreground/60">RustForge</span>
        <span>{t.footer.tagline}</span>
        <span className="font-mono">{t.footer.builtWith}</span>
      </div>
    </footer>
  );
}
