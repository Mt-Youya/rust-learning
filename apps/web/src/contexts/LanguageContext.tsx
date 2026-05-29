"use client";

import { createContext, useContext, useEffect, useState } from "react";
import { zh } from "@/locales/zh";
import { en } from "@/locales/en";
import type { Translations } from "@/locales/zh";

type Lang = "zh" | "en";

interface LanguageContextValue {
  lang: Lang;
  t: Translations;
  toggle: () => void;
}

const LanguageContext = createContext<LanguageContextValue>({
  lang: "zh",
  t: zh,
  toggle: () => {},
});

const STORAGE_KEY = "rustforge-lang";

export function LanguageProvider({ children }: { children: React.ReactNode }) {
  const [lang, setLang] = useState<Lang>("zh");

  // Read from localStorage on mount
  useEffect(() => {
    const stored = localStorage.getItem(STORAGE_KEY) as Lang | null;
    if (stored === "zh" || stored === "en") setLang(stored);
  }, []);

  // Sync lang attribute on <html>
  useEffect(() => {
    document.documentElement.lang = lang === "zh" ? "zh-CN" : "en";
  }, [lang]);

  const toggle = () => {
    const next = lang === "zh" ? "en" : "zh";
    setLang(next);
    localStorage.setItem(STORAGE_KEY, next);
  };

  return (
    <LanguageContext.Provider value={{ lang, t: lang === "zh" ? zh : en, toggle }}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  return useContext(LanguageContext);
}
