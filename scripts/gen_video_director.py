#!/usr/bin/env python3
"""
RustForge Video Director 渲染脚本
根据 ch01.md 的 14 场景结构生成视频。

用法:
  python3 scripts/gen_video_director.py 1
"""

import os, sys, subprocess
from PIL import Image, ImageDraw, ImageFont

REPO      = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
VIDEO_DIR = os.path.join(REPO, "apps/web/public/videos")
WORK_DIR  = os.path.join(REPO, "scripts/_work")
os.makedirs(WORK_DIR, exist_ok=True)

W, H = 1920, 1080
FPS  = 24

BG      = (10,  10,  20)
BG2     = (16,  16,  32)
ACCENT  = (220, 110,  50)
ACCENT2 = (160,  70,  25)
WHITE   = (240, 240, 255)
GRAY    = (160, 160, 190)
DIM     = (90,  90, 120)
GRID_C  = (20,  20,  38)
GREEN   = (76,  175, 125)
BLUE    = (91,  155, 213)

CN_FONT   = "/System/Library/Fonts/STHeiti Medium.ttc"
MONO_FONT = "/System/Library/Fonts/Menlo.ttc"

# ── CH.01 的 14 场景，直接来自 ch01.md storyboard ──────────────────────────
# 格式: (场景标题, [要点列表], 时长秒, 场景类型)
# 类型: title / bullets / comparison / terminal / summary / cta
SCENES_CH01 = [
    ("Hook：Node.js 痛点",
     ["内存：200MB → 2048MB", "FATAL ERROR", "TypeScript 管不了内存和并发", "Rust 可以"],
     20, "intro"),

    ("本章三个目标",
     ["① 安装 Rust 环境", "② 理解 Cargo", "③ 跑第一个程序", "真正的入口不是语法，是工具链"],
     22, "bullets"),

    ("Rust 三大编译期保证",
     ["零运行时开销 — 无 GC，直接机器码", "内存安全 — 悬垂指针编译期拦截", "并发安全 — 数据竞争编译期消灭", "全部在编译期验证"],
     50, "bullets"),

    ("安装 rustup",
     ["curl --proto '=https' ... | sh", "rustc --version", "cargo --version", "rustc 和 cargo 都有版本号 = 环境 OK"],
     38, "terminal"),

    ("rustup ≈ nvm，但功能更多",
     ["nvm → Node.js 版本管理", "rustup → Rust 版本管理", "rustup 额外管理：组件 / 编译目标", "rustup ≈ nvm，但不完全等价"],
     22, "comparison"),

    ("Cargo = npm + webpack + jest",
     ["npm → 依赖管理", "webpack → 构建系统", "jest → 测试框架", "→ Cargo 全部内置，开箱即用"],
     32, "bullets"),

    ("cargo new 创建项目",
     ["cargo new temp-converter", "tree . → Cargo.toml + src/main.rs", "cat src/main.rs → fn main()", "cargo run → Hello, world!"],
     48, "terminal"),

    ("Cargo.toml ≈ package.json",
     ["name / version / edition = 2021", "[dependencies] 声明依赖", "TOML 格式，支持注释", "Cargo.lock ≈ pnpm-lock.yaml，应用必须提交"],
     40, "comparison"),

    ("npm vs cargo 命令速查",
     ["npm install → cargo add", "npm run build → cargo build --release", "npm test → cargo test", "npm publish → cargo publish"],
     25, "comparison"),

    ("cargo run 背后的流程",
     ["cargo run", "→ 读取 Cargo.toml", "→ 调用 rustc 编译 src/main.rs", "→ 执行 target/debug/  你只需要 cargo"],
     35, "bullets"),

    ("变量默认不可变",
     ["let x = 5;", "x = 6;  // ❌ cannot assign twice", "let mut x = 5;", "x = 6;  // ✓  mut = 显式声明可变"],
     42, "terminal"),

    ("三个初学者常见坑",
     ["坑① cargo run 慢 → 加 --release", "坑② Cargo.lock → 应用必须提交", "坑③ 不用直接调 rustc", "Cargo 会替你调用 rustc"],
     26, "bullets"),

    ("小结：核心记忆点",
     ["rustup → 工具链管理 ≈ nvm", "Cargo → 构建 + 依赖 + 测试", "Cargo.toml → 依赖声明 ≈ package.json", "「rustc 是发动机，Cargo 是整辆车」"],
     28, "summary"),

    ("练习：温度转换器",
     ["打开 RustForge 第一章练习", "cargo new temp-converter", "10 分钟完成，算真正入门", "下一章：Rust 类型系统"],
     25, "cta"),
]

CHAPTERS_META = {
    1: ("basics-director", "CH.01", "入门：安装与 Cargo", "模块一 · Rust 核心基础"),
}


def get_font(size):
    try:
        return ImageFont.truetype(CN_FONT, size)
    except:
        return ImageFont.load_default()


def get_mono_font(size):
    try:
        return ImageFont.truetype(MONO_FONT, size)
    except:
        return ImageFont.load_default()


def get_text_size(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def wrap_text(text, font, max_width, draw):
    lines = []
    for paragraph in text.split('\n'):
        current = []
        for char in paragraph:
            current.append(char)
            w, _ = get_text_size(draw, ''.join(current), font)
            if w > max_width:
                current.pop()
                lines.append(''.join(current))
                current = [char]
        if current:
            lines.append(''.join(current))
    return lines


def draw_frame(img, scene_title, bullets, scene_idx, total_scenes,
               scene_type, bullet_progress=None, fade_in=1.0):
    draw = ImageDraw.Draw(img)

    # 背景渐变
    for y in range(H):
        ratio = y / H
        r = int(BG[0] + (BG2[0] - BG[0]) * ratio * 0.4)
        g = int(BG[1] + (BG2[1] - BG[1]) * ratio * 0.4)
        b = int(BG[2] + (BG2[2] - BG[2]) * ratio * 0.4)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # 网格
    for x in range(0, W, 60):
        draw.line([(x, 0), (x, H)], fill=GRID_C)
    for y in range(0, H, 60):
        draw.line([(0, y), (W, y)], fill=GRID_C)

    # 顶部 accent 线
    draw.rectangle([0, 0, W, 5], fill=ACCENT)

    # 进度条
    progress = scene_idx / total_scenes
    draw.rectangle([0, 0, int(W * progress), 4], fill=ACCENT2)

    # 场景类型标签（右上角小徽章）
    type_colors = {
        "intro": ACCENT, "bullets": BLUE, "comparison": GREEN,
        "terminal": (120, 180, 120), "summary": ACCENT, "cta": (200, 80, 120),
    }
    badge_color = type_colors.get(scene_type, GRAY)
    badge_font  = get_font(18)
    badge_text  = scene_type.upper()
    bw, bh = get_text_size(draw, badge_text, badge_font)
    bx = W - bw - 40
    draw.rounded_rectangle([bx - 10, 35, bx + bw + 10, 35 + bh + 10],
                            radius=6, fill=badge_color)
    draw.text((bx, 40), badge_text, font=badge_font, fill=WHITE)

    # 场景编号（左上角）
    label_font = get_font(18)
    draw.text((40, 42), f"CH.01  {scene_idx}/{total_scenes}", font=label_font, fill=GRAY)

    # 场景标题
    title_font = get_font(58)
    tw, th = get_text_size(draw, scene_title, title_font)
    tx = 100
    ty = 95
    # 标题淡入
    alpha = int(255 * fade_in)
    draw.text((tx, ty), scene_title, font=title_font,
              fill=(int(WHITE[0] * fade_in), int(WHITE[1] * fade_in), int(WHITE[2] * fade_in)))
    draw.rectangle([tx, ty + th + 12, tx + tw, ty + th + 17], fill=ACCENT)

    # 要点
    if scene_type == "terminal":
        bullet_font = get_mono_font(32)
    elif scene_type == "summary":
        bullet_font = get_font(40)
    else:
        bullet_font = get_font(36)

    y_pos = 210
    max_w = W - 200

    for idx, bullet in enumerate(bullets):
        if bullet_progress is not None:
            if idx < int(bullet_progress):
                alpha_f = 1.0
            elif idx == int(bullet_progress):
                alpha_f = bullet_progress - int(bullet_progress)
            else:
                alpha_f = 0.0
        else:
            alpha_f = 1.0

        if alpha_f <= 0:
            continue

        alpha_f *= fade_in
        fc = (int(WHITE[0] * alpha_f + DIM[0] * (1 - alpha_f)),
              int(WHITE[1] * alpha_f + DIM[1] * (1 - alpha_f)),
              int(WHITE[2] * alpha_f + DIM[2] * (1 - alpha_f)))

        dot_color = ACCENT if alpha_f > 0.5 else DIM
        if scene_type == "terminal":
            dot_color = GREEN if alpha_f > 0.5 else DIM
        elif scene_type == "summary" and idx == len(bullets) - 1:
            dot_color = ACCENT

        # 点
        draw.ellipse([116, y_pos + 12, 132, y_pos + 28], fill=dot_color)

        # 文字（自动换行）
        lines = wrap_text(bullet, bullet_font, max_w - 60, draw)
        for line in lines:
            draw.text((155, y_pos), line, font=bullet_font, fill=fc)
            y_pos += bullet_font.size + 8
        y_pos += 20

    # summary 场景：底部金句大字
    if scene_type == "summary" and (bullet_progress is None or bullet_progress >= len(bullets)):
        quote_font = get_font(44)
        quote = "rustc 是发动机，Cargo 是整辆车"
        qw, qh = get_text_size(draw, quote, quote_font)
        qx = (W - qw) // 2
        qy = H - 140
        draw.rounded_rectangle([qx - 24, qy - 14, qx + qw + 24, qy + qh + 14],
                                radius=10, fill=(30, 20, 10))
        draw.text((qx, qy), quote, font=quote_font, fill=ACCENT)


def generate_chapter(chapter_num):
    slug, ch_label, title, module = CHAPTERS_META[chapter_num]
    scenes = SCENES_CH01

    audio_file = os.path.join(VIDEO_DIR, f"ch{chapter_num:02d}-director.mp3")
    video_file = os.path.join(VIDEO_DIR, f"ch{chapter_num:02d}-director.mp4")

    if not os.path.exists(audio_file):
        print(f"⚠️  音频不存在: {audio_file}")
        return False

    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", audio_file],
        capture_output=True, text=True
    )
    try:
        audio_duration = float(result.stdout.strip())
    except:
        audio_duration = sum(s[2] for s in scenes)

    total_slide_time = sum(s[2] for s in scenes)
    time_scale = audio_duration / total_slide_time

    print(f"\n{'='*60}")
    print(f"{ch_label}  {title}")
    print(f"音频: {audio_duration:.1f}s | 场景: {len(scenes)} | 时间缩放: {time_scale:.3f}")
    print(f"{'='*60}")

    frames_dir = os.path.join(WORK_DIR, f"frames_{slug}")
    os.makedirs(frames_dir, exist_ok=True)

    frame_idx = 0
    for scene_idx, (scene_title, bullets, duration, scene_type) in enumerate(scenes, 1):
        scene_duration = duration * time_scale
        scene_frames   = int(scene_duration * FPS)
        bullet_count   = len(bullets)
        reveal_time    = scene_duration * 0.65

        for i in range(scene_frames):
            slide_time = i / FPS
            fade_in    = min(1.0, slide_time / 0.25)

            if slide_time < scene_duration * 0.12:
                bp = 0.0
            elif slide_time < scene_duration * 0.12 + reveal_time:
                bp = (slide_time - scene_duration * 0.12) / (reveal_time / bullet_count)
            else:
                bp = float(bullet_count)

            img = Image.new('RGB', (W, H), BG)
            draw_frame(img, scene_title, bullets, scene_idx, len(scenes),
                       scene_type, bp, fade_in)
            img.save(os.path.join(frames_dir, f"frame_{frame_idx:06d}.png"))
            frame_idx += 1

        print(f"  [{scene_idx:02d}/{len(scenes)}] {scene_title[:35]:<35}  {scene_frames}帧")

    # ffmpeg 合成
    print("\n合成视频中...")
    temp_vid = os.path.join(WORK_DIR, f"{slug}_tmp.mp4")
    subprocess.run([
        "ffmpeg", "-y", "-framerate", str(FPS),
        "-i", os.path.join(frames_dir, "frame_%06d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "22",
        temp_vid
    ], capture_output=True)

    subprocess.run([
        "ffmpeg", "-y", "-i", temp_vid, "-i", audio_file,
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
        video_file
    ], capture_output=True)

    import shutil
    shutil.rmtree(frames_dir, ignore_errors=True)
    if os.path.exists(temp_vid):
        os.remove(temp_vid)

    if os.path.exists(video_file):
        mb = os.path.getsize(video_file) / 1024 / 1024
        print(f"✅ 完成: {video_file}  ({mb:.1f} MB, {audio_duration:.0f}s)")
        return True
    else:
        print("❌ 视频合成失败")
        return False


if __name__ == "__main__":
    ch = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    generate_chapter(ch)
