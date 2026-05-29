"use client";

import { useState } from "react";
import { Check, Copy } from "lucide-react";
import { cn } from "@/lib/utils";

interface CodeBlockProps {
  code: string;
  language?: string;
  filename?: string;
  className?: string;
  showLineNumbers?: boolean;
}

export function CodeBlock({
  code,
  language = "rust",
  filename,
  className,
  showLineNumbers = false,
}: CodeBlockProps) {
  const [copied, setCopied] = useState(false);

  const copy = async () => {
    await navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 1800);
  };

  const lines = code.trim().split("\n");

  return (
    <div className={cn("relative rounded-lg overflow-hidden border border-[oklch(0.20_0.018_265)]", className)}>
      {/* Title bar */}
      <div className="flex items-center justify-between px-4 py-2.5 bg-[oklch(0.13_0.012_265)] border-b border-[oklch(0.20_0.018_265)]">
        <div className="flex items-center gap-3">
          {/* Traffic lights */}
          <div className="flex gap-1.5">
            <span className="w-3 h-3 rounded-full bg-[oklch(0.52_0.22_22_/_0.7)]" />
            <span className="w-3 h-3 rounded-full bg-[oklch(0.76_0.16_76_/_0.7)]" />
            <span className="w-3 h-3 rounded-full bg-[oklch(0.64_0.17_148_/_0.7)]" />
          </div>
          {filename && (
            <span className="text-xs font-mono text-[oklch(0.52_0.02_265)]">{filename}</span>
          )}
          {!filename && language && (
            <span className="text-xs font-mono text-[oklch(0.46_0.02_265)]">{language}</span>
          )}
        </div>
        <button
          onClick={copy}
          aria-label="复制代码"
          className={cn(
            "flex items-center gap-1.5 px-2.5 py-1 rounded text-xs transition-all duration-200",
            copied
              ? "text-[oklch(0.64_0.17_148)] bg-[oklch(0.64_0.17_148_/_0.1)]"
              : "text-[oklch(0.46_0.02_265)] hover:text-[oklch(0.82_0.01_265)] hover:bg-[oklch(0.20_0.018_265)]"
          )}
        >
          {copied ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
          {copied ? "已复制" : "复制"}
        </button>
      </div>

      {/* Code body */}
      <div className="relative bg-[oklch(0.09_0.01_265)] overflow-x-auto">
        <pre className="p-5 text-sm leading-relaxed">
          {lines.map((line, i) => (
            <div key={i} className="flex">
              {showLineNumbers && (
                <span className="select-none w-8 shrink-0 text-right mr-4 text-[oklch(0.35_0.02_265)] font-mono text-xs">
                  {i + 1}
                </span>
              )}
              <code
                className="font-mono"
                dangerouslySetInnerHTML={{ __html: highlightRust(line) }}
              />
            </div>
          ))}
        </pre>
      </div>
    </div>
  );
}

function highlightRust(line: string): string {
  const esc = line
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");

  return esc
    // Comments first
    .replace(/(\/\/.*$)/g, '<span class="token-comment">$1</span>')
    // Strings
    .replace(/(&quot;[^&]*&quot;|&quot;.*?&quot;)/g, '<span class="token-string">$1</span>')
    // Lifetimes
    .replace(/('[\w]+)/g, '<span class="token-lifetime">$1</span>')
    // Keywords
    .replace(
      /\b(let|mut|fn|pub|use|mod|struct|enum|impl|trait|type|return|if|else|match|for|while|loop|in|as|ref|async|await|move|where|dyn|self|Self|super|crate|true|false)\b/g,
      '<span class="token-keyword">$1</span>'
    )
    // Types
    .replace(
      /\b(String|str|i8|i16|i32|i64|i128|u8|u16|u32|u64|u128|f32|f64|bool|char|usize|isize|Vec|Option|Result|Box|Arc|Rc|Mutex|HashMap|HashSet|Ok|Err|Some|None)\b/g,
      '<span class="token-type">$1</span>'
    )
    // Macros
    .replace(/\b(\w+!)(?=\s*[(\[{])/g, '<span class="token-macro">$1</span>')
    // Numbers
    .replace(/\b(\d+(?:\.\d+)?(?:_\d+)*(?:u8|u16|u32|u64|usize|i32|i64|f32|f64)?)\b/g, '<span class="token-number">$1</span>')
    // Punctuation
    .replace(/(->|=>|::|\.\.\.?|[{}();,])/g, '<span class="token-punct">$1</span>');
}
