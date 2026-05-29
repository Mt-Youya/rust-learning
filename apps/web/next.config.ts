import type { NextConfig } from "next";
import createMDX from "@next/mdx";
import path from "path";

// Absolute path to the Shiki singleton plugin module.
// Passing a string (not a function) keeps Turbopack loader options
// serializable. The loader worker resolves the path via import() at
// compile time and gets the pre-configured rehype-pretty-code plugin.
const rehypeShikiPlugin = path.resolve("./src/lib/rehype-shiki.mjs");

const nextConfig: NextConfig = {
  pageExtensions: ["js", "jsx", "md", "mdx", "ts", "tsx"],
  experimental: {
    optimizePackageImports: [
      "lucide-react",
      "three",
      "@react-three/fiber",
      "@react-three/drei",
      "gsap",
    ],
  },
};

const withMDX = createMDX({
  options: {
    remarkPlugins: ["remark-gfm"],
    rehypePlugins: [
      "rehype-slug",
      ["rehype-autolink-headings", { behavior: "wrap" }],
      rehypeShikiPlugin,
    ],
  },
});

export default withMDX(nextConfig);
