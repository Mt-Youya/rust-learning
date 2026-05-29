/**
 * rehype-pretty-code wrapper that keeps a single Shiki highlighter instance
 * for the entire dev session.
 *
 * Referenced by absolute path string in next.config.ts so Turbopack can
 * serialize the loader options (strings are serializable; functions are not).
 * The loader worker resolves the path via import() and gets this function.
 */
import { getSingletonHighlighter } from "shiki";
import rehypePrettyCode from "rehype-pretty-code";

// One shared highlighter for all MDX files. Shiki's getSingletonHighlighter
// returns a cached instance on repeated calls — no re-initialization per file.
const highlighterPromise = getSingletonHighlighter({
  themes: ["vesper", "github-light"],
  langs: [
    "rust", "typescript", "javascript", "tsx", "jsx",
    "json", "toml", "yaml", "sql", "bash", "sh",
    "dockerfile", "markdown", "text",
  ],
});

export default function rehypeShiki() {
  return rehypePrettyCode({
    theme: { dark: "vesper", light: "github-light" },
    keepBackground: false,
    defaultLang: "rust",
    getHighlighter: () => highlighterPromise,
  });
}
