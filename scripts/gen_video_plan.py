#!/usr/bin/env python3
"""
RustForge 视频制作计划生成器
将章节 MDX 内容通过 OpenAI Responses API 转换为完整视频制作包

用法:
  python scripts/gen_video_plan.py --slug basics
  python scripts/gen_video_plan.py --slug ownership --model gpt-4.1
  python scripts/gen_video_plan.py --all
  python scripts/gen_video_plan.py --slug basics --dry-run

输出目录: scripts/_work/video_plans/{chapter_id}-{slug}/video_plan.md

环境变量:
  OPENAI_API_KEY   OpenAI API Key（必须）

依赖:
  pip install openai
"""

import os
import sys
import argparse
import logging
from pathlib import Path
from openai import OpenAI

# ── 路径配置 ──────────────────────────────────────────────────────────────
REPO_ROOT    = Path(__file__).resolve().parent.parent
SCRIPTS_DIR  = REPO_ROOT / "scripts"
CHAPTERS_DIR = REPO_ROOT / "apps/web/src/content/chapters"
WORK_DIR     = SCRIPTS_DIR / "_work/video_plans"
SKILL_FILE   = REPO_ROOT / ".claude/skills/rustforge-video-director/SKILL.md"
TEMPLATE_FILE = SCRIPTS_DIR / "prompts/chapter-to-video.user.md"

# ── 模型默认值 ────────────────────────────────────────────────────────────
DEFAULT_MODEL   = "gpt-4o"
DEFAULT_MINUTES = 8

# ── 章节映射：slug → (chapter_id, 标题, 章号, source_type) ──────────────
CHAPTERS: dict[str, tuple[str, str, int, str]] = {
    "basics":            ("ch01", "Getting Started",          1,  "rust_book"),
    "variables":         ("ch02", "变量、类型与函数",           2,  "mdx"),
    "ownership":         ("ch03", "所有权与借用",              3,  "rust_book"),
    "structs":           ("ch04", "结构体、枚举与模式匹配",     4,  "mdx"),
    "errors":            ("ch05", "错误处理",                  5,  "mdx"),
    "generics":          ("ch06", "泛型、Trait 与生命周期",     6,  "rust_book"),
    "collections":       ("ch07", "集合与函数式编程",           7,  "mdx"),
    "concurrency":       ("ch08", "并发编程",                  8,  "mdx"),
    "modules":           ("ch09", "模块系统与 Cargo 生态",      9,  "rust_book"),
    "testing":           ("ch10", "测试与代码质量",            10,  "mdx"),
    "cli":               ("ch11", "CLI 工具与 WebAssembly",    11,  "mdx"),
    "web-backend":       ("ch12", "Web 后端：Axum",            12,  "mdx"),
    "database":          ("ch13", "数据库与持久化",            13,  "mdx"),
    "auth":              ("ch14", "认证与安全",                14,  "mdx"),
    "project-fullstack": ("ch15", "实战项目一：全栈任务管理",   15,  "project"),
    "devops":            ("ch16", "运维基础：容器化与 CI/CD",   16,  "mdx"),
    "cloud-ops":         ("ch17", "云原生运维",                17,  "mdx"),
    "ai":                ("ch18", "AI 应用集成",               18,  "mdx"),
    "ai-ops":            ("ch19", "AI 运维：模型服务与 MLOps", 19,  "mdx"),
    "capstone":          ("ch20", "最终实战：AI 驱动的全栈服务",20,  "project"),
}

# ── 日志 ─────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("gen_video_plan")


# ── 读取文件 ──────────────────────────────────────────────────────────────

def read_skill() -> str:
    """读取 Video Director skill 提示词。"""
    if not SKILL_FILE.exists():
        log.error("Skill 文件不存在: %s", SKILL_FILE)
        sys.exit(1)
    return SKILL_FILE.read_text(encoding="utf-8")


def read_template() -> str:
    """读取 user prompt 模板文件。"""
    if not TEMPLATE_FILE.exists():
        log.error("模板文件不存在: %s", TEMPLATE_FILE)
        sys.exit(1)
    return TEMPLATE_FILE.read_text(encoding="utf-8")


def read_chapter_source(slug: str) -> str:
    """读取章节 MDX 源文件。"""
    mdx_path = CHAPTERS_DIR / f"{slug}.mdx"
    if not mdx_path.exists():
        log.error("章节文件不存在: %s", mdx_path)
        sys.exit(1)
    return mdx_path.read_text(encoding="utf-8")


# ── 构建 prompt ───────────────────────────────────────────────────────────

def build_user_prompt(
    template: str,
    chapter_id: str,
    title: str,
    source_type: str,
    duration_minutes: int,
    source_content: str,
) -> str:
    return (
        template
        .replace("{{chapter_id}}", chapter_id)
        .replace("{{title}}", title)
        .replace("{{source_type}}", source_type)
        .replace("{{duration_minutes}}", str(duration_minutes))
        .replace("{{source_content}}", source_content)
    )


# ── 调用 OpenAI ───────────────────────────────────────────────────────────

def call_openai(
    client: OpenAI,
    model: str,
    skill: str,
    user_prompt: str,
) -> str:
    """调用 OpenAI Responses API，返回生成文本。"""
    log.info("调用 OpenAI  model=%s  skill=%d chars  prompt=%d chars",
             model, len(skill), len(user_prompt))

    response = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": skill},
            {"role": "user",   "content": user_prompt},
        ],
    )
    return response.output_text


# ── 写出结果 ──────────────────────────────────────────────────────────────

def write_output(chapter_id: str, slug: str, content: str) -> Path:
    """将生成内容写入 _work/video_plans/{chapter_id}-{slug}/video_plan.md。"""
    out_dir = WORK_DIR / f"{chapter_id}-{slug}"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "video_plan.md"
    out_file.write_text(content, encoding="utf-8")
    return out_file


# ── 处理单章 ──────────────────────────────────────────────────────────────

def process_chapter(
    slug: str,
    model: str,
    duration_minutes: int,
    dry_run: bool,
    client: OpenAI | None,
    skill: str,
    template: str,
) -> bool:
    """处理单个章节，返回是否成功。"""
    if slug not in CHAPTERS:
        log.error("未知 slug: %s  可用: %s", slug, ", ".join(CHAPTERS))
        return False

    chapter_id, title, chapter_num, source_type = CHAPTERS[slug]
    log.info("── CH%02d  %s  [%s]", chapter_num, title, slug)

    source_content = read_chapter_source(slug)
    log.info("   源文件  %d chars", len(source_content))

    user_prompt = build_user_prompt(
        template, chapter_id, title, source_type, duration_minutes, source_content
    )

    if dry_run:
        log.info("   [dry-run] 跳过 API 调用")
        log.info("   system prompt: %d chars", len(skill))
        log.info("   user prompt:   %d chars", len(user_prompt))
        return True

    output = call_openai(client, model, skill, user_prompt)
    out_file = write_output(chapter_id, slug, output)
    log.info("   ✓ 写出 → %s  (%d chars)", out_file.relative_to(REPO_ROOT), len(output))
    return True


# ── CLI ───────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="RustForge 视频制作计划生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python scripts/gen_video_plan.py --slug basics
  python scripts/gen_video_plan.py --slug ownership --model gpt-4.1
  python scripts/gen_video_plan.py --all --model o4-mini
  python scripts/gen_video_plan.py --slug basics --dry-run

可用 slug:
  """ + "  ".join(sorted(CHAPTERS)),
    )

    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--slug",  metavar="SLUG", help="章节 slug（如 basics, ownership）")
    target.add_argument("--all",   action="store_true", help="处理全部 20 个章节")

    parser.add_argument(
        "--model",
        default=os.environ.get("OPENAI_MODEL", DEFAULT_MODEL),
        help=f"OpenAI 模型名（默认 {DEFAULT_MODEL}，可用 gpt-4.1 / o4-mini）",
    )
    parser.add_argument(
        "--minutes",
        type=int,
        default=DEFAULT_MINUTES,
        help=f"目标视频时长（分钟，默认 {DEFAULT_MINUTES}）",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="不调用 API，只验证文件和 prompt 构建",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # 验证 API Key
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key and not args.dry_run:
        log.error("未设置 OPENAI_API_KEY 环境变量")
        sys.exit(1)

    # 读取公共文件
    skill    = read_skill()
    template = read_template()
    client   = OpenAI(api_key=api_key) if not args.dry_run else None

    log.info("model=%s  dry_run=%s  skill=%d chars",
             args.model, args.dry_run, len(skill))

    # 决定处理哪些 slug
    slugs = list(CHAPTERS) if args.all else [args.slug]

    ok = failed = 0
    for slug in slugs:
        success = process_chapter(
            slug         = slug,
            model        = args.model,
            duration_minutes = args.minutes,
            dry_run      = args.dry_run,
            client       = client,
            skill        = skill,
            template     = template,
        )
        if success:
            ok += 1
        else:
            failed += 1

    log.info("完成  成功=%d  失败=%d", ok, failed)
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
