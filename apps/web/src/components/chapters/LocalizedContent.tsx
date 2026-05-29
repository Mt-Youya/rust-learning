"use client";

import { useLanguage } from "@/contexts/LanguageContext";

interface LocalizedContentProps {
  /** 中文版 MDX 渲染结果 */
  zh: React.ReactNode;
  /** 英文版 MDX 渲染结果（可为 null，此时 fallback 到 zh） */
  en: React.ReactNode | null;
}

/**
 * 根据当前语言显示对应的章节内容。
 * zh 和 en 均在服务端渲染（SSR），客户端只做切换显示。
 */
export function LocalizedContent({ zh, en }: LocalizedContentProps) {
  const { lang } = useLanguage();
  const showEn = lang === "en" && en !== null;
  return <>{showEn ? en : zh}</>;
}
