import { readdir } from "fs/promises";
import path from "path";

export type Locale = "zh" | "en";

export interface ChapterFrontmatter {
  title: string;
  subtitle: string;
  chapter: number;
  slug: string;
  duration: string;
  project: string;
  status: "available" | "locked" | "coming-soon";
  description: string;
  prev: string | null;
  next: string | null;
}

export interface ChapterModule {
  Component: React.ComponentType;
  frontmatter: ChapterFrontmatter;
}

// zh is the source of truth for available slugs
const ZH_DIR = path.join(process.cwd(), "src/content/zh/chapters");

/** All chapter slugs, derived from zh locale (source of truth). */
export async function getChapterSlugs(): Promise<string[]> {
  const files = await readdir(ZH_DIR);
  return files
    .filter((f) => f.endsWith(".mdx") || f.endsWith(".md"))
    .map((f) => f.replace(/\.(mdx|md)$/, ""));
}

/**
 * Load a chapter MDX module for a specific locale.
 * Returns null if the file doesn't exist for that locale — no automatic fallback.
 * Callers decide fallback behavior.
 */
export async function getChapterModule(
  slug: string,
  locale: Locale
): Promise<ChapterModule | null> {
  try {
    const mod =
      locale === "en"
        ? await import(`@/content/en/chapters/${slug}.mdx`)
        : await import(`@/content/zh/chapters/${slug}.mdx`);
    return {
      Component: mod.default as React.ComponentType,
      frontmatter: mod.frontmatter as ChapterFrontmatter,
    };
  } catch {
    return null;
  }
}
