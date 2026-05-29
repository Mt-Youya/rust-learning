#!/usr/bin/env python3
"""
RustForge FishSpeech 本地 TTS 脚本

使用前需要先启动 FishSpeech API Server：
  cd ~/codes/python/fish-speech
  python tools/api_server.py --listen 0.0.0.0:8080 \
    --llama-checkpoint checkpoints/fish-speech-1.5 \
    --decoder-checkpoint checkpoints/fish-speech-1.5/firefly-gan-vq-fsq-8x1024-21hz-generator.pth

用法:
  python3 scripts/fishspeech_tts.py 1             # 生成第1章完整音频
  python3 scripts/fishspeech_tts.py 1 --preview   # 生成前3分钟预览
  python3 scripts/fishspeech_tts.py --text "你好" -o test.mp3
  python3 scripts/fishspeech_tts.py all           # 生成全部章节

输出: apps/web/public/videos/ch01.mp3
"""

import os
import re
import sys
import tempfile
import argparse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

REPO = Path(__file__).parent.parent
OUTPUT_DIR = REPO / "apps/web/public/videos"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ── FishSpeech API Server ─────────────────────────────────────────────────
API_URL = "http://127.0.0.1:8080/v1/tts"

# ── 推理参数 ──────────────────────────────────────────────────────────────
TEMPERATURE = 0.7
REPETITION_PENALTY = 1.3

# 固定参考音频路径（用来锁定音色，留空则用模型默认音色）
# 录一段 5-10 秒你喜欢的中文语音放到这里，音色会保持一致
REFERENCE_AUDIO = str(Path(__file__).parent / "reference_15s.wav")
REFERENCE_TEXT  = "大家好，欢迎来到 RustForge。我是你的讲师，这套课程专门为有两到五年 JavaScript 和 React 经验的前端工程师设计，带你从前端视角出发，系统地学习 Rust，一路走到全栈开发、运维部署，以及 AI 应用集成。"

# 并发线程数（FishSpeech server 单进程，建议 1-2，避免 OOM）
WORKERS = 1

# ── 代码块识别正则 ────────────────────────────────────────────────────────
# 匹配形如 cargo new xxx / let x = 5 / fn main() 等代码片段
CODE_PATTERNS = [
    r"^\s*(cargo|rustup|rustc|git|curl|cd|ls|mkdir|source|touch|cat)\s",
    r"^\s*(let|fn|pub|use|impl|struct|enum|match|if|for|while|loop|return)\s",
    r"^\s*\[.*\]\s*$",          # TOML 段落头 [package]
    r".*->\s*\w",               # 函数返回类型箭头
    r".*::\w",                  # 路径操作符 std::env
    r'^\s*".*"\s*$',            # 纯字符串字面量行
    r"^\s*\d+\s*$",             # 纯数字行
    r"^\s*[{}()\[\];,]+\s*$",   # 纯符号行
]
CODE_RE = re.compile("|".join(CODE_PATTERNS))


def get_script(chapter_num: int) -> str:
    """从 gen_audio.py 里取对应章节旁白脚本"""
    import importlib.util
    scripts_path = Path(__file__).parent / "gen_audio.py"
    spec = importlib.util.spec_from_file_location("gen_audio", scripts_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, "SCRIPTS", {}).get(chapter_num, "")


def clean_text_for_tts(text: str, max_chars: int = 0) -> str:
    """
    清理旁白文本：
    - 去掉屏幕标注、代码行
    - 把代码片段替换成自然语言占位
    - max_chars > 0 时截断（用于预览模式）
    """
    replacements = [
        ("（见屏幕代码）", ""),
        ("（屏幕上展示的代码里）", ""),
        ("在屏幕上展示的代码里", ""),
        ("屏幕上可以看到", ""),
        ("屏幕上展示了", ""),
        ("屏幕上可以看到具体的字段定义和类型标注，这是 Rust 强类型系统的体现。", ""),
    ]

    lines = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        for old, new in replacements:
            line = line.replace(old, new)
        line = line.strip()
        if not line:
            continue
        # 跳过纯代码行，替换成口语占位
        if CODE_RE.match(line):
            continue
        lines.append(line)

    result = "\n".join(lines)
    if max_chars > 0:
        result = result[:max_chars]
        # 在最后一个句号处截断，避免末尾句子不完整
        cut = max(result.rfind("。"), result.rfind("！"), result.rfind("？"))
        if cut > 0:
            result = result[:cut + 1]
    return result


def split_into_chunks(text: str, max_chars: int = 150) -> list[str]:
    """按句子切片，每片不超过 max_chars 字"""
    chunks = []
    for para in text.split("\n"):
        para = para.strip()
        if not para:
            continue
        parts = re.split(r"([。！？…]+)", para)
        buf = ""
        for i in range(0, len(parts), 2):
            seg = parts[i]
            punct = parts[i + 1] if i + 1 < len(parts) else ""
            buf += seg + punct
            if len(buf) >= max_chars:
                if buf.strip():
                    chunks.append(buf.strip())
                buf = ""
        if buf.strip():
            chunks.append(buf.strip())
    return chunks


def synthesize_chunk(text: str, output_wav: str, index: int = 0) -> tuple[int, bool]:
    """
    调用 FishSpeech API 合成单段音频。
    返回 (index, success) 用于并发场景排序。
    """
    try:
        import ormsgpack
        import requests

        payload = {
            "text": text,
            "format": "wav",
            "temperature": TEMPERATURE,
            "repetition_penalty": REPETITION_PENALTY,
            "streaming": False,
        }

        # 绑定参考音频以固定音色
        if REFERENCE_AUDIO and Path(REFERENCE_AUDIO).exists():
            payload["references"] = [{
                "audio": Path(REFERENCE_AUDIO).read_bytes(),
                "text": REFERENCE_TEXT,
            }]

        resp = requests.post(
            API_URL,
            data=ormsgpack.packb(payload, option=ormsgpack.OPT_SERIALIZE_PYDANTIC),
            headers={"Content-Type": "application/msgpack"},
            timeout=120,
        )
        if resp.status_code != 200:
            print(f"  [错误] 片段{index} API {resp.status_code}: {resp.text[:100]}")
            return index, False
        Path(output_wav).write_bytes(resp.content)
        return index, True

    except requests.exceptions.ConnectionError:
        print(f"  [连接失败] 无法连接 {API_URL}")
        print(f"  请先启动 FishSpeech Server")
        return index, False
    except Exception as e:
        print(f"  [异常] 片段{index}: {e}")
        return index, False


def concat_wavs_to_mp3(wav_files: list[str], output_mp3: str) -> bool:
    """用 ffmpeg 拼接 wav 片段输出 mp3"""
    import subprocess
    if not wav_files:
        return False
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        list_file = f.name
        for wav in wav_files:
            f.write(f"file '{wav}'\n")
    try:
        result = subprocess.run(
            ["ffmpeg", "-y", "-f", "concat", "-safe", "0",
             "-i", list_file, "-c:a", "libmp3lame", "-q:a", "2",
             "-ar", "44100", output_mp3],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"  [ffmpeg 错误] {result.stderr[-300:]}")
            return False
        return True
    finally:
        os.unlink(list_file)


def generate_audio(chapter_num: int, preview: bool = False) -> bool:
    """
    生成章节音频。
    preview=True 时只生成前约 1 分钟（01500 字）。
    """
    label = f"ch{chapter_num:02d}" + ("_preview" if preview else "")
    output_mp3 = OUTPUT_DIR / f"{label}.mp3"

    print(f"\n{'='*60}")
    print(f"  章节 {chapter_num} {'[预览1分钟]' if preview else ''} → {output_mp3.name}")
    print(f"{'='*60}")

    raw = get_script(chapter_num)
    if not raw.strip():
        print(f"  [警告] 第{chapter_num}章脚本为空")
        return False

    # 预览模式截取前 ~1500 字（约3分钟语速）
    text = clean_text_for_tts(raw, max_chars=600 if preview else 0)
    chunks = split_into_chunks(text, max_chars=100)
    print(f"  文本 {len(text)} 字，{len(chunks)} 个片段，{WORKERS} 线程")

    with tempfile.TemporaryDirectory() as tmpdir:
        wav_slots = {i: os.path.join(tmpdir, f"chunk_{i:04d}.wav") for i in range(len(chunks))}
        results = {}

        with ThreadPoolExecutor(max_workers=WORKERS) as pool:
            futures = {
                pool.submit(synthesize_chunk, chunk, wav_slots[i], i): i
                for i, chunk in enumerate(chunks)
            }
            done = 0
            for future in as_completed(futures):
                idx, ok = future.result()
                results[idx] = ok
                done += 1
                status = "✓" if ok else "✗"
                print(f"  [{done}/{len(chunks)}] {status} {chunks[idx][:35]}...")

        # 按原始顺序过滤成功的片段
        ordered_wavs = [wav_slots[i] for i in sorted(results) if results[i]]
        if not ordered_wavs:
            print("  [错误] 所有片段合成失败")
            return False

        print(f"\n  合并 {len(ordered_wavs)}/{len(chunks)} 个片段 → mp3...")
        ok = concat_wavs_to_mp3(ordered_wavs, str(output_mp3))

    if ok:
        size_mb = output_mp3.stat().st_size / 1024 / 1024
        print(f"  ✓ 完成: {output_mp3} ({size_mb:.1f} MB)")
    else:
        print("  ✗ 合并失败")
    return ok


def synthesize_text_to_file(text: str, output_path: str) -> bool:
    """合成任意文本到文件"""
    chunks = split_into_chunks(text)
    print(f"  {len(text)} 字，{len(chunks)} 个片段")
    with tempfile.TemporaryDirectory() as tmpdir:
        wavs = []
        for i, chunk in enumerate(chunks):
            wav = os.path.join(tmpdir, f"chunk_{i:04d}.wav")
            _, ok = synthesize_chunk(chunk, wav, i)
            if ok:
                wavs.append(wav)
        if not wavs:
            return False
        return concat_wavs_to_mp3(wavs, output_path)


def main():
    parser = argparse.ArgumentParser(description="RustForge FishSpeech TTS")
    parser.add_argument("chapter", nargs="?", help="章节号（1-16）或 all")
    parser.add_argument("--preview", action="store_true", help="只生成前3分钟预览")
    parser.add_argument("--text", help="直接合成指定文本")
    parser.add_argument("-o", "--output", default="output.mp3", help="输出路径")
    parser.add_argument("--workers", type=int, default=1, help="并发线程数")
    args = parser.parse_args()

    global WORKERS
    WORKERS = args.workers

    if args.text:
        print(f"合成文本 → {args.output}")
        sys.exit(0 if synthesize_text_to_file(args.text, args.output) else 1)

    if not args.chapter:
        parser.print_help()
        sys.exit(1)

    if args.chapter == "all":
        results = {ch: generate_audio(ch, args.preview) for ch in range(1, 17)}
        print("\n生成结果:")
        for ch, ok in results.items():
            print(f"  ch{ch:02d}: {'✓' if ok else '✗'}")
        sys.exit(0 if all(results.values()) else 1)

    try:
        ch = int(args.chapter)
    except ValueError:
        print(f"[错误] 章节号必须是数字，got: {args.chapter}")
        sys.exit(1)

    sys.exit(0 if generate_audio(ch, args.preview) else 1)


if __name__ == "__main__":
    main()
