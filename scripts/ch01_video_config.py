# ══════════════════════════════════════════════════════════════════
# ch01_video_config.py — gen_video.py 章节配置片段
# Track E · ch01 Getting Started · RustForge Enhanced Edition
# 生成时间：2026-05-27
#
# 使用方式：
#   from scripts.ch01_video_config import CHAPTER_1_CONFIG
#   或直接 merge 到 gen_video.py 的 CHAPTERS 字典中
# ══════════════════════════════════════════════════════════════════

# ── Chapter 1 Config ───────────────────────────────────────────────
CHAPTER_1_CONFIG = {
    "id": 1,
    "title": "Getting Started · Rust 工具链与第一个项目",
    "slug": "basics",
    "script_file": "scripts/ch01_narration.txt",
    "srt_file": "scripts/ch01_subtitles.srt",
    "scenes_file": "scripts/ch01_scenes.yaml",
    "audio_output": "asset/audio/ch01.mp3",
    "video_output": "asset/video/ch01.mp4",
    "thumbnail_output": "assets/thumbnails/ch01_thumb.jpg",

    # ── 幻灯片时间轴（与旁白时间戳对齐）───────────────────────────
    "slides": [
        {
            "timestamp": "00:00",
            "type": "three_scene",
            "scene_id": "memory-leak-burst",
            "duration": 20,
        },
        {
            "timestamp": "00:20",
            "type": "title",
            "text": "第一章 · Getting Started",
            "subtitle": "Rust 工具链与第一个项目",
        },
        {
            "timestamp": "00:38",
            "type": "agenda",
            "items": [
                "① 装好 Rust 环境（rustup）",
                "② 理解 Cargo 是什么",
                "③ 跑起来第一个程序",
            ],
            "animation": "slide_in_stagger",
        },
        {
            "timestamp": "00:45",
            "type": "three_scene",
            "scene_id": "rust-shield-trio",
            "duration": 50,
        },
        {
            "timestamp": "01:35",
            "type": "title_card",
            "text": "安装 rustup",
        },
        {
            "timestamp": "02:15",
            "type": "three_scene",
            "scene_id": "toolchain-3d-compare",
            "duration": 25,
        },
        {
            "timestamp": "02:40",
            "type": "three_scene",
            "scene_id": "cargo-particle-merge",
            "duration": 35,
        },
        {
            "timestamp": "03:15",
            "type": "title_card",
            "text": "cargo new 实战",
        },
        {
            "timestamp": "04:05",
            "type": "comparison",
            "left_label": "package.json",
            "right_label": "Cargo.toml",
        },
        {
            "timestamp": "04:25",
            "type": "three_scene",
            "scene_id": "cargo-pipeline-3d",
            "duration": 30,
        },
        {
            "timestamp": "04:45",
            "type": "three_scene",
            "scene_id": "cargo-vs-npm",
            "duration": 25,
        },
        {
            "timestamp": "05:10",
            "type": "three_scene",
            "scene_id": "immutable-lock",
            "duration": 40,
        },
        {
            "timestamp": "05:50",
            "type": "warning_cards",
            "items": [
                "坑① cargo run 慢 → --release",
                "坑② Cargo.lock → 应用必须提交",
                "坑③ 不用直接调 rustc",
            ],
            "animation": "bounce_in",
        },
        {
            "timestamp": "06:15",
            "type": "summary",
            "items": [
                "rustup → 工具链管理（≈ nvm）",
                "Cargo → 构建 + 依赖 + 测试",
                "Cargo.toml → 依赖声明（≈ package.json）",
                "let 不可变 · let mut 可变",
            ],
            "highlight_last": "rustc 是发动机，Cargo 是整辆车",
            "highlight_color": "#e77c3a",
        },
        {
            "timestamp": "06:45",
            "type": "cta",
            "text": "打开 RustForge 完成第一章练习",
            "sub_text": "温度转换器 · 10 分钟",
            "url_hint": "链接在描述区",
        },
    ],

    # ── 终端录制片段时间轴 ────────────────────────────────────────
    "terminal_clips": [
        {
            "timestamp": "01:45",
            "label": "rustup 安装验证",
            "commands": [
                "rustc --version",
                "cargo --version",
                "rustup --version",
                "rustup component add clippy",
            ],
            "asset": "assets/terminal/ch01/scene_004_rustup.mp4",
            "duration": 20,
        },
        {
            "timestamp": "03:18",
            "label": "cargo new + cargo run",
            "commands": [
                "cargo new temp-converter",
                "cd temp-converter",
                "tree . --charset=unicode",
                "cargo run",
                "cargo build --release",
                "ls -lh target/release/temp-converter",
            ],
            "asset": "assets/terminal/ch01/scene_007_cargo_new.mp4",
            "duration": 48,
        },
        {
            "timestamp": "05:14",
            "label": "变量不可变编译报错演示",
            "commands": [
                "# let x = 5; x = 6; 报错演示",
                "cargo build 2>&1",
                "# 修复：加 mut",
                "cargo run",
            ],
            "asset": "assets/terminal/ch01/scene_011_immutable.mp4",
            "duration": 32,
        },
    ],

    # ── 代码展示时间轴 ────────────────────────────────────────────
    "code_blocks": [
        {
            "timestamp": "03:42",
            "lang": "rust",
            "label": "main.rs 默认 Hello World",
            "code": 'fn main() {\n    println!("Hello, world!");\n}',
            "highlight_lines": [1, 2, 3],
            "note": "注意 println! 后面的感叹号——这是宏，不是函数",
        },
        {
            "timestamp": "04:10",
            "lang": "toml",
            "label": "Cargo.toml 结构",
            "code": (
                "[package]\n"
                'name = "temp-converter"\n'
                'version = "0.1.0"\n'
                'edition = "2021"  # TOML 支持注释\n\n'
                "[dependencies]\n"
                "# cargo add serde 后自动填入"
            ),
            "highlight_lines": [4],
            "note": "edition = 2021 是当前推荐版本",
        },
        {
            "timestamp": "05:14",
            "lang": "rust",
            "label": "let 不可变报错",
            "code": (
                "fn main() {\n"
                "    let x = 5;\n"
                "    x = 6;  // ❌ cannot assign twice to immutable variable\n"
                "}"
            ),
            "highlight_lines": [3],
            "error_line": 3,
        },
        {
            "timestamp": "05:28",
            "lang": "rust",
            "label": "let mut 修复",
            "code": (
                "fn main() {\n"
                "    let mut x = 5;\n"
                "    x = 6;  // ✓\n"
                '    println!("{}", x);  // 输出 6\n'
                "}"
            ),
            "highlight_lines": [2],
        },
    ],

    # ── Three.js 场景时间轴 ───────────────────────────────────────
    "three_scenes": [
        {
            "timestamp": "00:00",
            "scene_id": "memory-leak-burst",
            "component": "MemoryLeakBurstScene",
            "duration": 20,
        },
        {
            "timestamp": "00:45",
            "scene_id": "rust-shield-trio",
            "component": "RustShieldTrioScene",
            "duration": 50,
        },
        {
            "timestamp": "02:15",
            "scene_id": "toolchain-3d-compare",
            "component": "ToolchainCompareScene",
            "duration": 25,
        },
        {
            "timestamp": "02:40",
            "scene_id": "cargo-particle-merge",
            "component": "CargoParticleMergeScene",
            "duration": 35,
        },
        {
            "timestamp": "04:25",
            "scene_id": "cargo-pipeline-3d",
            "component": "CargoPipeline3DScene",
            "duration": 30,
        },
        {
            "timestamp": "04:45",
            "scene_id": "cargo-vs-npm",
            "component": "CargoVsNpmBubblesScene",
            "duration": 25,
        },
        {
            "timestamp": "05:10",
            "scene_id": "immutable-lock",
            "component": "ImmutableLockScene",
            "duration": 40,
        },
    ],

    # ── TTS 配置（CosyVoice / edge-tts）──────────────────────────
    "tts": {
        "voice": "zh-CN-YunxiNeural",
        "speed": 1.05,
        "pitch": 0,
        "pause_map": {
            0.5: 500,
            0.8: 800,
            1.0: 1000,
            1.5: 1500,
            2.0: 2000,
        },
        "emphasis_words": [
            "编译期", "不可变", "Cargo", "rustup", "rustc",
            "零运行时开销", "内存安全", "并发安全",
        ],
    },

    # ── 背景音乐配置 ──────────────────────────────────────────────
    "background_music": {
        "enabled": True,
        "style": "minimal_tech_ambient",
        "bpm": 90,
        "volume": 0.07,
        "duck_during_code_demo": True,
        "duck_volume": 0.03,
        "duck_during_three_scene": False,
        "three_scene_volume": 0.05,
        "track_suggestions": [
            "Epidemic Sound: Futuristic Ambient Lo-fi",
            "Pixabay: Technology Background",
            "自制：4/4拍，90BPM，钢琴+pad，无鼓",
        ],
        "transition_style": {
            "hook_to_content": "cross_fade_2s",
            "code_demo_entry": "duck_fade_1s",
            "three_scene_entry": "volume_swell",
            "summary_to_cta": "fadeout_into_silence",
        },
    },

    # ── 渲染参数 ──────────────────────────────────────────────────
    "render": {
        "resolution": "1920x1080",
        "fps": 30,
        "format": "mp4",
        "codec": "h264",
        "crf": 18,
        "audio_codec": "aac",
        "audio_bitrate": "192k",
        "total_duration_seconds": 430,
        "output_path": "asset/video/ch01.mp4",
        "cdn_path": "videos/ch01.mp4",
    },

    # ── 发布元数据 ────────────────────────────────────────────────
    "publish": {
        "title": "Rust 入门第一课：工具链、Cargo 与第一个项目 | RustForge",
        "title_candidates": [
            "Rust 入门第一步：安装环境与 Cargo 基础",
            "前端转 Rust 第一课，你真正需要的不是语法！",
            "Hello World 不是重点，Cargo 才是 Rust 的入口",
            "Rust rustup Cargo 安装教程 前端工程师入门",
        ],
        "description": (
            "本视频面向有前端背景的开发者，系统讲解 Rust 入门第一章："
            "安装 rustup、理解 Cargo 与 npm 的对应关系、创建并运行第一个项目、"
            "理解变量不可变设计。配套练习在 RustForge 网站完成温度转换器项目。"
        ),
        "tags": [
            "Rust", "Rust教程", "前端工程师学Rust",
            "Cargo", "rustup", "编程入门",
            "TypeScript转Rust", "系统编程",
        ],
        "chapters_timestamp": [
            {"time": "00:00", "title": "开场：为什么前端工程师学 Rust"},
            {"time": "00:45", "title": "Rust 三大优势"},
            {"time": "01:35", "title": "安装 rustup"},
            {"time": "02:40", "title": "Cargo 是什么"},
            {"time": "03:15", "title": "cargo new 创建项目"},
            {"time": "04:05", "title": "Cargo.toml 详解"},
            {"time": "05:10", "title": "变量不可变演示"},
            {"time": "06:15", "title": "小结与练习引导"},
        ],
    },

    # ── Supabase 更新 payload ─────────────────────────────────────
    "supabase_update": {
        "table": "chapters",
        "match": {"id": "ch01"},
        "update": {
            "video_url": "https://cdn.rustforge.dev/videos/ch01.mp4",
            "video_duration_seconds": 430,
            "video_status": "ready",
            "video_thumbnail_url": "https://cdn.rustforge.dev/thumbnails/ch01_thumb.jpg",
            "video_updated_at": "2026-05-27T00:00:00Z",
        },
    },
}

# ── 快速验证 ─────────────────────────────────────────────────────
if __name__ == "__main__":
    three_ids = {s["scene_id"] for s in CHAPTER_1_CONFIG["three_scenes"]}
    slide_three_ids = {
        s["scene_id"]
        for s in CHAPTER_1_CONFIG["slides"]
        if s.get("type") == "three_scene"
    }
    print(f"Three.js 场景数：{len(three_ids)}")
    print(f"幻灯片时间轴条数：{len(CHAPTER_1_CONFIG['slides'])}")
    print(f"代码块数：{len(CHAPTER_1_CONFIG['code_blocks'])}")
    print(f"终端录制片段：{len(CHAPTER_1_CONFIG['terminal_clips'])}")
    print(f"总时长：{CHAPTER_1_CONFIG['render']['total_duration_seconds']}s")

    # 检查 three_scenes 中的 scene_id 在 slides 中都有对应
    missing = three_ids - slide_three_ids
    if missing:
        print(f"[WARN] 以下 scene_id 在 slides 中无对应：{missing}")
    else:
        print("[OK] 所有 Three.js 场景在 slides 中均有对应")
