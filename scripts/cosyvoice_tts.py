#!/usr/bin/env python3
"""
CosyVoice2 TTS 集成模块
直接调用本地 CosyVoice 仓库的 Python SDK

用法:
  python cosyvoice_tts.py "要合成的文本" -o output.wav
  python cosyvoice_tts.py --chapter 1 -o ch01.wav
  python cosyvoice_tts.py --list-spks

依赖:
  本地已有 /Users/yonjay/codes/python/CosyVoice 仓库
  pip install torchaudio
"""

import os
import sys
import argparse
from pathlib import Path

COSYVOICE_DIR = "/Users/yonjay/codes/python/CosyVoice"
MODEL_DIR = os.path.join(COSYVOICE_DIR, "pretrained_models/CosyVoice2-0.5B")
DEFAULT_SPK = "中文女"


def load_model():
    sys.path.insert(0, os.path.join(COSYVOICE_DIR, "third_party/Matcha-TTS"))
    sys.path.insert(0, COSYVOICE_DIR)
    from cosyvoice.cli.cosyvoice import AutoModel
    return AutoModel(model_dir=MODEL_DIR)


def synthesize(text, output_path="output.wav", spk=DEFAULT_SPK):
    import torchaudio
    model = load_model()

    print(f"  音色: {spk}")
    print(f"  文本长度: {len(text)} 字")

    chunks = []
    for i, result in enumerate(model.inference_sft(text, spk, stream=False)):
        chunks.append(result["tts_speech"])

    if not chunks:
        print("  错误: 未生成任何音频")
        return False

    import torch
    audio = torch.cat(chunks, dim=-1)
    torchaudio.save(output_path, audio, model.sample_rate)

    size_kb = Path(output_path).stat().st_size / 1024
    print(f"  完成: {output_path} ({size_kb:.1f} KB)")
    return True


def list_spks():
    model = load_model()
    spks = model.list_available_spks()
    print("可用音色:")
    for spk in spks:
        print(f"  {spk}")


def get_chapter_script_3min(chapter_num):
    scripts = {
        1: """
欢迎来到 RustForge 3分钟精华版。第一章：入门。

作为前端工程师，你可能遇到过这些问题：Node 服务内存泄漏、高并发抖动、CLI 工具体积大。TypeScript 把类型错误提前到编译期，Rust 更进一步——内存错误和并发 Bug 也在编译期捕获。

安装 Rust 只需一行命令：curl 管道给 sh 执行。rustup 是 Rust 的版本管理器，就像 nvm。安装完成后，rustc 编译器、cargo 构建工具、标准库一应俱全。

Cargo 是 Rust 的核心工具，同时做了 npm、webpack、jest 的工作。cargo new 创建项目，cargo build 编译，cargo test 运行测试，--release 生产优化。

和 npm 对比：cargo add 添加依赖，cargo run 编译并运行，cargo publish 发布到 crates.io。

Rust 变量默认不可变，let mut 显式声明可变。这是设计理念：明确表达我要修改的意图。

第一章核心：rustup 管工具链，Cargo 管项目，编译期捕获错误，零运行时开销。
""",
        2: """
第二章：变量与类型系统。

TypeScript 类型编译后消失，运行时还是 JavaScript。Rust 类型影响内存布局和函数约定，类型错误往往是内存安全的信号。

整数类型：i32 默认，u8 用于字节，usize 专用于数组索引。字符串：&str 是只读引用视图，String 是堆上所有者。函数参数用 &str，存储修改用 String。

元组是固定长度的异构集合，用点语法访问或解构。Vec 是动态数组，vec! 宏创建，类比 JavaScript Array。

函数必须标注参数和返回类型。最后一行无分号是表达式，作为返回值。if-else 也是表达式。

第二章核心：类型即内存布局，表达式与语句是 Rust 核心设计，类型推断让你少写字但不损失安全。
""",
        3: """
第三章：所有权与借用。

栈后进先出，大小编译时确定。堆动态分配，灵活但需要管理。Rust 所有权系统在编译期自动管理内存。

所有权三条规则：每个值有且只有一个所有者；所有者离开作用域，值自动释放。违反规则编译错误。

let s2 = s1 对于 String 是所有权转移，s1 失效。这防止了 double free。整数等 Copy 类型则是复制。

借用规则：多个不可变引用，或一个可变引用。引用不能比数据活得更长。编译期检查，彻底防止数据竞争。

第三章核心：所有权是 Rust 最核心的创新，编译器帮你管理内存无需 GC，借用规则在编译期消灭数据竞争。
""",
    }
    return scripts.get(chapter_num, f"第{chapter_num}章脚本待添加")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CosyVoice2 本地 TTS 工具")
    parser.add_argument("text", nargs="?", help="要合成的文本")
    parser.add_argument("-o", "--output", default="output.wav", help="输出文件 (.wav)")
    parser.add_argument("-v", "--voice", default=DEFAULT_SPK, help=f"音色（默认: {DEFAULT_SPK}）")
    parser.add_argument("--chapter", type=int, help="生成指定章节的 3min 脚本")
    parser.add_argument("--list-spks", action="store_true", help="列出所有可用音色")

    args = parser.parse_args()

    if args.list_spks:
        list_spks()
        sys.exit(0)

    if args.chapter:
        text = get_chapter_script_3min(args.chapter)
        output = args.output if args.output != "output.wav" else f"ch{args.chapter:02d}-3min.wav"
    elif args.text:
        text = args.text
        output = args.output
    else:
        parser.print_help()
        sys.exit(1)

    success = synthesize(text, output_path=output, spk=args.voice)
    sys.exit(0 if success else 1)
