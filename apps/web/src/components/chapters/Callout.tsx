import { cn } from "@/lib/utils";
import { Lightbulb, Info, AlertTriangle, Zap } from "lucide-react";

type CalloutType = "tip" | "insight" | "warning" | "note";

const styles: Record<CalloutType, { border: string; bg: string; icon: string; Icon: React.ComponentType<{ className: string }> }> = {
  tip: {
    border: "border-[oklch(0.64_0.17_148_/_0.4)]",
    bg: "bg-[oklch(0.64_0.17_148_/_0.06)]",
    icon: "text-[oklch(0.64_0.17_148)]",
    Icon: Lightbulb,
  },
  insight: {
    border: "border-[oklch(0.68_0.18_42_/_0.4)]",
    bg: "bg-[oklch(0.68_0.18_42_/_0.06)]",
    icon: "text-[oklch(0.68_0.18_42)]",
    Icon: Zap,
  },
  warning: {
    border: "border-[oklch(0.76_0.16_76_/_0.4)]",
    bg: "bg-[oklch(0.76_0.16_76_/_0.06)]",
    icon: "text-[oklch(0.76_0.16_76)]",
    Icon: AlertTriangle,
  },
  note: {
    border: "border-[oklch(0.72_0.19_295_/_0.4)]",
    bg: "bg-[oklch(0.72_0.19_295_/_0.06)]",
    icon: "text-[oklch(0.72_0.19_295)]",
    Icon: Info,
  },
};

interface CalloutProps {
  type?: CalloutType;
  children: React.ReactNode;
}

export function Callout({ type = "note", children }: CalloutProps) {
  const s = styles[type];
  const { Icon } = s;

  return (
    <div className={cn("not-prose my-6 flex gap-4 rounded-lg border p-4", s.border, s.bg)}>
      <Icon className={cn("w-4 h-4 mt-0.5 shrink-0", s.icon)} />
      <div className="text-sm text-[oklch(0.70_0.01_265)] leading-relaxed [&_strong]:text-[oklch(0.88_0.008_265)] [&_code]:font-mono [&_code]:text-xs [&_code]:text-[oklch(0.68_0.18_42)]">
        {children}
      </div>
    </div>
  );
}
