import { notFound } from "next/navigation";
import type { Metadata } from "next";
import { getChapterSlugs, getChapterModule } from "@/lib/mdx";
import { OwnershipSceneClient } from "@/components/animations/OwnershipSceneClient";
import { LocalizedContent } from "@/components/chapters/LocalizedContent";
import { ChapterNav } from "@/components/chapters/ChapterNav";

interface PageProps {
  params: Promise<{ slug: string }>;
}

export async function generateStaticParams() {
  const slugs = await getChapterSlugs();
  return slugs.map((slug) => ({ slug }));
}

export const dynamicParams = false;

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { slug } = await params;
  const mod = await getChapterModule(slug, "zh");
  if (!mod) return { title: "RustForge" };
  const { frontmatter: fm } = mod;
  return {
    title: `第 ${fm.chapter} 章：${fm.title} — RustForge`,
    description: fm.description,
  };
}

export default async function ChapterPage({ params }: PageProps) {
  const { slug } = await params;

  const [zhMod, enMod] = await Promise.all([
    getChapterModule(slug, "zh"),
    getChapterModule(slug, "en"),
  ]);

  if (!zhMod) notFound();

  const { frontmatter: fm } = zhMod;
  const ZhComponent = zhMod.Component;
  const EnComponent = enMod?.Component ?? null;
  const isOwnership = slug === "ownership";

  return (
    <div className="pt-16">
      {isOwnership && (
        <div className="fixed inset-0 pointer-events-none z-0 opacity-20">
          <OwnershipSceneClient className="w-full h-full" />
        </div>
      )}

      <article className="relative z-10 mx-auto max-w-3xl px-6 py-16">
        <LocalizedContent
          zh={<ZhComponent />}
          en={EnComponent ? <EnComponent /> : null}
        />
      </article>

      <ChapterNav
        prev={fm.prev}
        next={fm.next}
        chapter={fm.chapter}
      />
    </div>
  );
}
