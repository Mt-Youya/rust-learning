import type { MDXComponents } from "mdx/types";
import Link from "next/link";

/**
 * Global MDX component overrides.
 * Maps every Markdown HTML element to on-brand styled versions.
 * Complex interactive components (OwnershipDiagram, etc.) are imported
 * directly inside .mdx files — they don't go here.
 */
export function useMDXComponents(components: MDXComponents): MDXComponents {
  return {
    // ── Headings ───────────────────────────────────────────────────
    h1: ({ children, ...props }) => (
      <h1
        className="mt-12 mb-4 text-3xl md:text-4xl font-display font-black tracking-tight text-[oklch(0.94_0.008_265)]"
        {...props}
      >
        {children}
      </h1>
    ),
    h2: ({ children, ...props }) => (
      <h2
        className="group mt-10 mb-4 text-xl md:text-2xl font-display font-bold tracking-tight text-[oklch(0.88_0.008_265)] scroll-mt-24"
        {...props}
      >
        {children}
      </h2>
    ),
    h3: ({ children, ...props }) => (
      <h3
        className="mt-8 mb-3 text-base font-display font-semibold text-[oklch(0.82_0.01_265)] scroll-mt-24"
        {...props}
      >
        {children}
      </h3>
    ),
    h4: ({ children, ...props }) => (
      <h4
        className="mt-6 mb-2 text-sm font-semibold text-[oklch(0.76_0.01_265)] uppercase tracking-wide scroll-mt-24"
        {...props}
      >
        {children}
      </h4>
    ),

    // ── Body text ──────────────────────────────────────────────────
    p: ({ children, ...props }) => (
      <p
        className="my-4 text-sm text-[oklch(0.64_0.015_265)] leading-[1.8] max-w-[68ch]"
        {...props}
      >
        {children}
      </p>
    ),
    strong: ({ children }) => (
      <strong className="font-semibold text-[oklch(0.84_0.008_265)]">{children}</strong>
    ),
    em: ({ children }) => (
      <em className="italic text-[oklch(0.72_0.015_265)]">{children}</em>
    ),

    // ── Links ──────────────────────────────────────────────────────
    a: ({ href = "#", children, ...props }) => {
      const isInternal = href.startsWith("/");
      if (isInternal) {
        return (
          <Link
            href={href}
            className="text-[oklch(0.68_0.18_42)] underline underline-offset-3 decoration-[oklch(0.68_0.18_42_/_0.4)] hover:decoration-[oklch(0.68_0.18_42)] transition-colors duration-200"
            {...props}
          >
            {children}
          </Link>
        );
      }
      return (
        <a
          href={href}
          target="_blank"
          rel="noopener noreferrer"
          className="text-[oklch(0.68_0.18_42)] underline underline-offset-3 decoration-[oklch(0.68_0.18_42_/_0.4)] hover:decoration-[oklch(0.68_0.18_42)] transition-colors duration-200"
          {...props}
        >
          {children}
        </a>
      );
    },

    // ── Code ───────────────────────────────────────────────────────
    // Inline code
    code: ({ children, ...props }) => (
      <code
        className="font-mono text-[0.8em] px-1.5 py-0.5 rounded bg-[oklch(0.16_0.015_265)] border border-[oklch(0.22_0.018_265)] text-[oklch(0.68_0.18_42)] not-italic"
        {...props}
      >
        {children}
      </code>
    ),
    // Fenced code block (rehype-pretty-code wraps in <figure> or <pre>)
    pre: ({ children, ...props }) => (
      <div className="my-6 rounded-xl overflow-hidden border border-[oklch(0.20_0.018_265)] bg-[oklch(0.09_0.01_265)]">
        {/* Traffic lights bar */}
        <div className="flex items-center gap-1.5 px-4 py-2.5 bg-[oklch(0.13_0.012_265)] border-b border-[oklch(0.20_0.018_265)]">
          <span className="w-2.5 h-2.5 rounded-full bg-[oklch(0.52_0.22_22_/_0.7)]" />
          <span className="w-2.5 h-2.5 rounded-full bg-[oklch(0.76_0.16_76_/_0.7)]" />
          <span className="w-2.5 h-2.5 rounded-full bg-[oklch(0.64_0.17_148_/_0.7)]" />
        </div>
        <pre
          className="overflow-x-auto p-5 text-[13px] leading-[1.7] [&_code]:bg-transparent [&_code]:border-0 [&_code]:px-0 [&_code]:py-0 [&_code]:text-inherit"
          {...props}
        >
          {children}
        </pre>
      </div>
    ),

    // ── Lists ──────────────────────────────────────────────────────
    ul: ({ children }) => (
      <ul className="my-4 space-y-1.5 pl-0">
        {children}
      </ul>
    ),
    ol: ({ children }) => (
      <ol className="my-4 space-y-1.5 pl-0 counter-reset-[item]">
        {children}
      </ol>
    ),
    li: ({ children }) => (
      <li className="flex gap-3 text-sm text-[oklch(0.64_0.015_265)] leading-relaxed before:content-['▸'] before:text-[oklch(0.68_0.18_42)] before:text-xs before:mt-1 before:shrink-0">
        <span>{children}</span>
      </li>
    ),

    // ── Table ──────────────────────────────────────────────────────
    table: ({ children }) => (
      <div className="my-6 overflow-x-auto rounded-lg border border-[oklch(0.20_0.018_265)]">
        <table className="w-full text-sm border-collapse">
          {children}
        </table>
      </div>
    ),
    thead: ({ children }) => (
      <thead className="bg-[oklch(0.13_0.012_265)] text-xs font-mono text-[oklch(0.52_0.02_265)] uppercase tracking-wide">
        {children}
      </thead>
    ),
    tbody: ({ children }) => (
      <tbody className="divide-y divide-[oklch(0.16_0.015_265)]">
        {children}
      </tbody>
    ),
    th: ({ children }) => (
      <th className="px-4 py-2.5 text-left font-semibold">{children}</th>
    ),
    td: ({ children }) => (
      <td className="px-4 py-2.5 text-[oklch(0.64_0.015_265)]">{children}</td>
    ),

    // ── Divider ────────────────────────────────────────────────────
    hr: () => (
      <hr className="my-10 border-0 h-px bg-gradient-to-r from-transparent via-[oklch(0.22_0.018_265)] to-transparent" />
    ),

    // ── Blockquote ─────────────────────────────────────────────────
    blockquote: ({ children }) => (
      <blockquote className="my-6 pl-4 border-l-2 border-[oklch(0.68_0.18_42_/_0.5)] text-[oklch(0.58_0.02_265)] italic text-sm leading-relaxed">
        {children}
      </blockquote>
    ),

    // Merge with any local overrides passed per-page
    ...components,
  };
}
