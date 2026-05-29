import { cn } from "@/lib/utils";

/**
 * RustForge Brand Logo
 *
 * 锻造锤图标 — 设计说明：
 *   • 底板：深色圆角方形，橙色细边框
 *   • 锤头：楔形（左高右低），暗示打击方向与力量感
 *   • 锤头顶线：细高光，增加金属质感
 *   • 锤柄：深橙色，与锤头形成层次，无需额外描边
 *   • Hover：锤头变亮 + 底板背景加深
 *
 * 使用方式：
 *   <Logo />                       — 默认：图标 + "RustForge" 文字
 *   <Logo size="lg" />             — sm / md(default) / lg / xl
 *   <Logo iconOnly />              — 只显示图标
 *   <Logo textOnly />              — 只显示文字
 *   <Logo className="..." />       — 外层容器额外样式
 */

type LogoSize = "sm" | "md" | "lg" | "xl";

interface LogoProps {
  size?: LogoSize;
  iconOnly?: boolean;
  textOnly?: boolean;
  className?: string;
  /** 不显示 hover 效果（嵌入静态场景时使用） */
  noHover?: boolean;
}

const SIZE_MAP: Record<LogoSize, { icon: number; text: string; gap: string }> = {
  sm: { icon: 20, text: "text-xs",  gap: "gap-1.5" },
  md: { icon: 28, text: "text-sm",  gap: "gap-2.5" },
  lg: { icon: 40, text: "text-xl",  gap: "gap-3" },
  xl: { icon: 64, text: "text-3xl", gap: "gap-4" },
};

export function HammerIcon({
  size = 28,
  className,
  noHover = false,
}: {
  size?: number;
  className?: string;
  noHover?: boolean;
}) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 28 28"
      fill="none"
      aria-hidden="true"
      className={className}
    >
      {/* 底板：深色圆角方形，橙色边框 */}
      <rect
        x="0.5" y="0.5" width="27" height="27" rx="5.5"
        fill="oklch(0.12 0.03 40)"
        stroke="oklch(0.65 0.17 42)"
        strokeWidth="1"
        className={noHover ? undefined : "transition-all duration-300 group-hover:fill-[oklch(0.17_0.05_42)] group-hover:stroke-[oklch(0.76_0.21_50)]"}
      />
      {/* 锤头：楔形（左高 9→15，右侧收 12.5→10.5），水平占 4→23 */}
      <path
        d="M4 9 L4 15 L16.5 15 L16.5 12.5 L23 10.5 L23 9 Z"
        fill="oklch(0.68 0.18 42)"
        className={noHover ? undefined : "transition-all duration-300 group-hover:fill-[oklch(0.77_0.22_50)]"}
      />
      {/* 锤头顶边高光线 */}
      <line
        x1="4" y1="9" x2="23" y2="9"
        stroke="oklch(0.82 0.09 58)"
        strokeWidth="0.65"
        opacity="0.55"
      />
      {/* 锤头正面/侧面分割线 */}
      <line
        x1="16.5" y1="12.5" x2="16.5" y2="15"
        stroke="oklch(0.50 0.14 36)"
        strokeWidth="0.6"
        opacity="0.7"
      />
      {/* 锤柄 */}
      <rect
        x="10" y="15" width="5.5" height="9" rx="1.5"
        fill="oklch(0.52 0.13 36)"
        className={noHover ? undefined : "transition-all duration-300 group-hover:fill-[oklch(0.60_0.16_42)]"}
      />
      {/* 锤柄末端（稍深，防止与深背景融合） */}
      <rect
        x="10" y="21" width="5.5" height="3" rx="1"
        fill="oklch(0.44 0.11 34)"
        className={noHover ? undefined : "transition-all duration-300 group-hover:fill-[oklch(0.52_0.14_40)]"}
      />
    </svg>
  );
}

export function Logo({
  size = "md",
  iconOnly = false,
  textOnly = false,
  className,
  noHover = false,
}: LogoProps) {
  const { icon, text, gap } = SIZE_MAP[size];

  return (
    <div className={cn("flex items-center", gap, className)}>
      {!textOnly && (
        <HammerIcon size={icon} noHover={noHover} />
      )}
      {!iconOnly && (
        <span
          className={cn(
            "font-display font-bold tracking-tight text-[oklch(0.94_0.008_265)] select-none",
            text
          )}
        >
          RustForge
        </span>
      )}
    </div>
  );
}
