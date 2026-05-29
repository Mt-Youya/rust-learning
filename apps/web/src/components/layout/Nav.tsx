"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { useState, useEffect } from "react";
import { Menu, X } from "lucide-react";
import { Logo } from "@/components/ui/Logo";
import { ThemeToggle } from "@/components/ui/ThemeToggle";
import { LanguageToggle } from "@/components/ui/LanguageToggle";
import { useLanguage } from "@/contexts/LanguageContext";

export function Nav() {
  const [scrolled, setScrolled] = useState(false);
  const [open, setOpen] = useState(false);
  const pathname = usePathname();
  const { t } = useLanguage();

  const links = [
    { href: "/#curriculum", label: t.nav.curriculum },
    { href: "/chapter/basics", label: t.nav.chapter1 },
    { href: "/#compare", label: t.nav.compare },
  ];

  useEffect(() => {
    const handler = () => setScrolled(window.scrollY > 40);
    window.addEventListener("scroll", handler, { passive: true });
    return () => window.removeEventListener("scroll", handler);
  }, []);

  // Close mobile menu on route change
  useEffect(() => {
    setOpen(false);
  }, [pathname]);

  return (
    <header
      className={cn(
        "fixed top-0 left-0 right-0 z-50 transition-all duration-500",
        scrolled
          ? "bg-background/[0.92] backdrop-blur-xl border-b border-border"
          : "bg-transparent"
      )}
    >
      <nav className="mx-auto max-w-7xl px-4 sm:px-6 h-16 flex items-center justify-between">
        {/* Logo */}
        <Link href="/" className="group shrink-0" aria-label={t.nav.home}>
          <Logo size="md" />
        </Link>

        {/* Desktop links */}
        <ul className="hidden md:flex items-center gap-1">
          {links.map((l) => (
            <li key={l.href}>
              <Link
                href={l.href}
                className={cn(
                  "px-3 py-1.5 rounded text-sm transition-colors duration-200",
                  pathname === l.href
                    ? "text-primary bg-rust-surface"
                    : "text-muted-foreground hover:text-foreground hover:bg-accent"
                )}
              >
                {l.label}
              </Link>
            </li>
          ))}
        </ul>

        {/* Desktop right: toggles + CTA */}
        <div className="hidden md:flex items-center gap-1">
          <LanguageToggle />
          <ThemeToggle />
          <div className="w-px h-5 bg-border mx-1" />
          <Link
            href="/chapter/ownership"
            className={cn(
              "px-4 py-1.5 rounded text-sm font-semibold transition-all duration-200",
              "bg-primary text-primary-foreground",
              "hover:bg-rust-bright",
              "shadow-[0_0_16px_oklch(0.68_0.18_42_/_0.25)]",
              "hover:shadow-[0_0_24px_oklch(0.68_0.18_42_/_0.4)]"
            )}
          >
            {t.nav.startLearning}
          </Link>
        </div>

        {/* Mobile right: toggles + hamburger */}
        <div className="md:hidden flex items-center gap-1">
          <LanguageToggle />
          <ThemeToggle />
          <button
            className="p-2 text-muted-foreground hover:text-foreground hover:bg-accent rounded-md transition-colors"
            onClick={() => setOpen(!open)}
            aria-label={open ? t.nav.closeMenu : t.nav.openMenu}
            aria-expanded={open}
          >
            {open ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </nav>

      {/* Mobile menu — animated slide-down */}
      <div
        className={cn(
          "md:hidden border-t border-border bg-background/[0.96] backdrop-blur-xl",
          "overflow-hidden transition-all duration-300 ease-out",
          open ? "max-h-96 opacity-100" : "max-h-0 opacity-0 pointer-events-none"
        )}
        aria-hidden={!open}
      >
        <div className="px-4 py-3 space-y-1">
          {links.map((l) => (
            <Link
              key={l.href}
              href={l.href}
              onClick={() => setOpen(false)}
              className={cn(
                "flex items-center px-3 py-2.5 rounded text-sm transition-colors",
                pathname === l.href
                  ? "text-primary bg-rust-surface"
                  : "text-muted-foreground hover:text-foreground hover:bg-accent"
              )}
            >
              {l.label}
            </Link>
          ))}
          <div className="pt-2 pb-1">
            <Link
              href="/chapter/ownership"
              onClick={() => setOpen(false)}
              className="flex items-center justify-center px-3 py-2.5 rounded text-sm font-semibold bg-primary text-primary-foreground hover:bg-rust-bright transition-colors"
            >
              {t.nav.startLearning}
            </Link>
          </div>
        </div>
      </div>
    </header>
  );
}
