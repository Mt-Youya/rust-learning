"use client";

import { useEffect, useRef, useState } from "react";
import { cn } from "@/lib/utils";

type Step = "bind" | "move" | "invalidate" | "borrow";

interface MemoryCell {
  id: string;
  label: string;
  value: string;
  owner: string | null;
  borrowed: boolean;
  invalid: boolean;
}

const STEPS: { step: Step; title: string; desc: string; code: string }[] = [
  {
    step: "bind",
    title: "1. 绑定：所有权创建",
    desc: "变量 s1 获得字符串 \"hello\" 的所有权。内存分配在堆上，s1 是唯一拥有者。",
    code: `let s1 = String::from("hello");
// s1 拥有 "hello" 的所有权
// 栈: s1 → { ptr, len: 5, cap: 5 }
// 堆: ["h","e","l","l","o"]`,
  },
  {
    step: "move",
    title: "2. 移动：所有权转移",
    desc: "将 s1 赋值给 s2，所有权完全转移。这不是复制，是移动 (Move)。",
    code: `let s2 = s1; // 所有权从 s1 → s2
// s1 现在无效，不再拥有任何数据
// s2 成为新的唯一所有者`,
  },
  {
    step: "invalidate",
    title: "3. 失效：编译器保护",
    desc: "尝试使用已移动的 s1 会导致编译错误。这在编译期就被阻止，零运行时开销。",
    code: `println!("{}", s1); // ✗ 编译错误！
// error[E0382]: borrow of moved value: 's1'
// s1 的值已移动到 s2

println!("{}", s2); // ✓ s2 有效`,
  },
  {
    step: "borrow",
    title: "4. 借用：临时使用",
    desc: "借用 (&) 允许临时使用值而不转移所有权。借用结束后，s1 依然有效。",
    code: `let s1 = String::from("hello");
let len = calculate(&s1); // 借用 s1
// s1 所有权未改变，借用期间不可修改
println!("s1={s1}, len={len}"); // ✓ 两者都有效

fn calculate(s: &String) -> usize {
    s.len() // s 是借用，函数结束自动归还
}`,
  },
];

export function OwnershipDiagram() {
  const [activeStep, setActiveStep] = useState(0);
  const [animating, setAnimating] = useState(false);
  const timeoutRef = useRef<ReturnType<typeof setTimeout>>(null);

  const step = STEPS[activeStep];

  const cells: MemoryCell[] = (() => {
    switch (step.step) {
      case "bind":
        return [
          { id: "s1", label: "s1", value: '"hello"', owner: "s1", borrowed: false, invalid: false },
        ];
      case "move":
        return [
          { id: "s1", label: "s1", value: "—", owner: null, borrowed: false, invalid: true },
          { id: "s2", label: "s2", value: '"hello"', owner: "s2", borrowed: false, invalid: false },
        ];
      case "invalidate":
        return [
          { id: "s1", label: "s1", value: "✗ 已移动", owner: null, borrowed: false, invalid: true },
          { id: "s2", label: "s2", value: '"hello"', owner: "s2", borrowed: false, invalid: false },
        ];
      case "borrow":
        return [
          { id: "s1", label: "s1", value: '"hello"', owner: "s1", borrowed: true, invalid: false },
          { id: "len", label: "len", value: "5 (借用结果)", owner: null, borrowed: false, invalid: false },
        ];
    }
  })();

  function advance() {
    if (animating) return;
    setAnimating(true);
    if (timeoutRef.current) clearTimeout(timeoutRef.current);
    timeoutRef.current = setTimeout(() => {
      setActiveStep((s) => (s + 1) % STEPS.length);
      setAnimating(false);
    }, 150);
  };

  useEffect(() => () => { if (timeoutRef.current) clearTimeout(timeoutRef.current); }, []);

  return (
    <div className="rounded-lg border border-[oklch(0.20_0.018_265)] bg-[oklch(0.11_0.012_265)] overflow-hidden">
      {/* Step tabs */}
      <div className="flex border-b border-[oklch(0.20_0.018_265)]">
        {STEPS.map((s, i) => (
          <button
            key={s.step}
            onClick={() => { setActiveStep(i); }}
            className={cn(
              "flex-1 py-3 text-xs font-mono transition-colors duration-200 border-b-2 -mb-px",
              i === activeStep
                ? "border-[oklch(0.68_0.18_42)] text-[oklch(0.68_0.18_42)] bg-[oklch(0.68_0.18_42_/_0.06)]"
                : "border-transparent text-[oklch(0.52_0.02_265)] hover:text-[oklch(0.82_0.01_265)]"
            )}
          >
            {i + 1}
          </button>
        ))}
      </div>

      <div className="p-6 space-y-5">
        {/* Title + description */}
        <div>
          <p className="text-sm font-semibold text-[oklch(0.82_0.01_265)] mb-1">{step.title}</p>
          <p className="text-xs text-[oklch(0.52_0.02_265)] leading-relaxed">{step.desc}</p>
        </div>

        {/* Memory visualization */}
        <div className="flex flex-wrap gap-3">
          {cells.map((cell) => (
            <div
              key={cell.id}
              className={cn(
                "rounded border px-4 py-3 min-w-[120px] transition-all duration-300",
                cell.invalid
                  ? "border-[oklch(0.52_0.22_22_/_0.4)] bg-[oklch(0.52_0.22_22_/_0.06)]"
                  : cell.borrowed
                    ? "border-[oklch(0.72_0.19_295_/_0.5)] bg-[oklch(0.72_0.19_295_/_0.06)]"
                    : "border-[oklch(0.68_0.18_42_/_0.4)] bg-[oklch(0.68_0.18_42_/_0.06)]"
              )}
            >
              <div className={cn(
                "text-xs font-mono font-bold mb-1",
                cell.invalid ? "text-[oklch(0.52_0.22_22)]"
                  : cell.borrowed ? "text-[oklch(0.72_0.19_295)]"
                  : "text-[oklch(0.68_0.18_42)]"
              )}>
                {cell.label}
              </div>
              <div className={cn(
                "text-xs font-mono",
                cell.invalid ? "text-[oklch(0.46_0.02_265)] line-through" : "text-[oklch(0.82_0.01_265)]"
              )}>
                {cell.value}
              </div>
              {cell.borrowed && (
                <div className="text-[10px] text-[oklch(0.72_0.19_295)] mt-1">借用中</div>
              )}
              {cell.owner && (
                <div className="text-[10px] text-[oklch(0.52_0.02_265)] mt-1">owner: {cell.owner}</div>
              )}
            </div>
          ))}
        </div>

        {/* Code block */}
        <pre className="relative rounded border border-[oklch(0.20_0.018_265)] bg-[oklch(0.09_0.01_265)] p-4 text-xs leading-relaxed overflow-x-auto">
          <code className="font-mono text-[oklch(0.78_0.01_265)]">{step.code}</code>
        </pre>

        {/* Next step button */}
        <button
          onClick={advance}
          disabled={animating}
          className={cn(
            "w-full py-2.5 rounded text-xs font-mono font-semibold transition-all duration-200",
            "bg-[oklch(0.68_0.18_42_/_0.12)] border border-[oklch(0.68_0.18_42_/_0.35)]",
            "text-[oklch(0.68_0.18_42)] hover:bg-[oklch(0.68_0.18_42_/_0.22)] hover:border-[oklch(0.68_0.18_42_/_0.6)]",
            "disabled:opacity-40 disabled:cursor-not-allowed"
          )}
        >
          {activeStep < STEPS.length - 1 ? "下一步 →" : "重新开始 ↺"}
        </button>
      </div>
    </div>
  );
}
