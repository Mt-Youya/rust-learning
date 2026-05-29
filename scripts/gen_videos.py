#!/usr/bin/env python3
"""
RustForge 完整视频生成脚本
- 每章 8-15 分钟详细讲解
- ChatTTS 音频，段落级时间戳
- 精确对齐 VTT 字幕
- PIL 渲染中文无乱码

运行：/opt/miniconda3/bin/python3 scripts/gen_videos.py [章节号]
示例：/opt/miniconda3/bin/python3 scripts/gen_videos.py 1
      /opt/miniconda3/bin/python3 scripts/gen_videos.py all
"""

import os, sys, math, textwrap, subprocess
import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFont

# ── 路径配置 ──────────────────────────────────────────────────────────────
REPO_ROOT   = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
VIDEO_OUT   = os.path.join(REPO_ROOT, "apps/web/public/videos")
SUB_OUT     = os.path.join(REPO_ROOT, "apps/web/public/subtitles")
WORK_DIR    = os.path.join(REPO_ROOT, "scripts/_work")
os.makedirs(VIDEO_OUT, exist_ok=True)
os.makedirs(SUB_OUT,   exist_ok=True)
os.makedirs(WORK_DIR,  exist_ok=True)

# ── 字体配置 ──────────────────────────────────────────────────────────────
FONT_CN   = "/System/Library/Fonts/STHeiti Medium.ttc"
FONT_MONO = "/System/Library/Fonts/SFNSMono.ttf"
FONT_SONG = "/System/Library/Fonts/Supplemental/Songti.ttc"

# ── 视频参数 ──────────────────────────────────────────────────────────────
W, H   = 1920, 1080
FPS    = 24
SAMPLE = 24000

# ── 颜色主题（RustForge dark） ─────────────────────────────────────────────
BG       = (15,  15,  25)
BG2      = (22,  22,  38)
ACCENT   = (220, 110,  50)   # Rust orange
TEXT_H   = (255, 255, 255)
TEXT_B   = (200, 200, 220)
TEXT_DIM = (120, 120, 150)
CODE_BG  = (18,  18,  30)
CODE_FG  = (200, 220, 255)
CODE_KW  = (210, 100,  70)   # keywords
CODE_STR = (130, 190, 110)   # strings
CODE_CMT = (100, 120, 100)   # comments
SUB_BG   = (0,   0,   0,  180)

# ══════════════════════════════════════════════════════════════════════════
# 章节脚本数据结构：每个段落 = (字幕文字, 讲解文字, 代码块或None, 标题或None)
# ══════════════════════════════════════════════════════════════════════════

CHAPTERS = {}

# ── 第 1 章 ────────────────────────────────────────────────────────────────
CHAPTERS[1] = {
    "title": "Rust 基础",
    "subtitle": "从 JavaScript 到 Rust 的思维迁移",
    "slug": "ch01-basics",
    "segments": [
        {
            "title": "欢迎 & 课程介绍",
            "subtitle": "RustForge 第一章",
            "speech": "大家好，欢迎来到 RustForge。我是这门课的讲师。这套课程专门为有两到五年 JavaScript 和 React 经验的前端工程师设计，帮你系统地过渡到 Rust 全栈开发。",
            "code": None,
        },
        {
            "title": "为什么前端工程师学 Rust？",
            "subtitle": "告别运行时惊喜",
            "speech": "你已经掌握了 JavaScript 的异步模型、模块系统、工具链思维。Rust 不会推翻这些，它会在上面加一层更精确的控制。用 JS 写 Web 很快，但你总在跟 undefined is not a function、内存泄漏、并发 bug 打交道。Rust 的答案是：把这些问题变成编译错误，在代码运行前就解决掉。",
            "code": None,
        },
        {
            "title": "TypeScript vs Rust 类型系统",
            "subtitle": "类比理解",
            "speech": "从前端视角来理解：TypeScript 把 JS 的类型错误提前到编译期，Rust 把内存错误和并发 bug 也提前到编译期。区别是 Rust 更彻底，零运行时开销，没有垃圾回收，没有 any 类型逃生舱。",
            "code": "// TypeScript\nlet name: string = \"Alice\";\nlet age: number = 30;\n\n// Rust\nlet name: &str = \"Alice\";\nlet age: i32 = 30;\n// 类型推断，通常可以省略\nlet age = 30_i32;",
        },
        {
            "title": "变量与不可变性",
            "subtitle": "默认 const，需要时才 mut",
            "speech": "在 JavaScript 里，你用 let 和 const。在 Rust 里，所有变量默认就是不可变的，相当于默认就是 const。如果你需要修改一个变量，必须显式加 mut 关键字。这个设计强迫你思考：这个值到底需不需要改变？编译器会帮你守住这条线。",
            "code": "// JavaScript\nlet count = 0;\ncount = 1;  // OK\n\n// Rust\nlet count = 0;       // 不可变，相当于 const\n// count = 1;         // 编译错误！\nlet mut count = 0;   // 显式声明可变\ncount = 1;           // OK\n\n// shadowing：可以重新绑定同名变量\nlet x = 5;\nlet x = x + 1;  // 新的 x，不是修改",
        },
        {
            "title": "基础类型系统",
            "subtitle": "整数、浮点、布尔、字符",
            "speech": "Rust 的数字类型比 JavaScript 精细得多。整数有 i8、i16、i32、i64、i128，以及无符号的 u8 到 u128，还有跟平台相关的 isize 和 usize。最常用的是 i32 和 usize。浮点数有 f32 和 f64，默认推断为 f64。布尔值就是 bool，字符类型 char 是 Unicode 标量，占 4 字节，不是 ASCII。",
            "code": "let x: i32 = -42;         // 有符号 32 位整数\nlet y: u64 = 1_000_000;   // 下划线增加可读性\nlet f: f64 = 3.14;\nlet b: bool = true;\nlet c: char = '🦀';       // Unicode 字符\n\n// 类型转换必须显式（不像 JS 隐式转换）\nlet x = 42_i32;\nlet y = x as f64;         // i32 → f64\nlet z = y as i32;         // f64 → i32（截断）",
        },
        {
            "title": "String 和 &str 的区别",
            "subtitle": "前端最常见的困惑",
            "speech": "这是前端转 Rust 最常见的困惑点之一。String 是堆分配的、可增长的字符串，类似 JavaScript 里 new 出来的对象。&str 是字符串切片，是对一段字符串数据的引用，通常是字符串字面量或 String 的一部分。函数参数用 &str 更灵活，因为它既能接受字面量也能接受 String 的引用。",
            "code": "// &str：字符串切片，编译期已知，存在程序数据段\nlet s1: &str = \"hello world\";\n\n// String：堆分配，运行时可增长\nlet mut s2: String = String::from(\"hello\");\ns2.push_str(\" world\");  // 可以修改\n\n// String → &str（借用）\nlet s3: &str = &s2;\n\n// 函数参数推荐用 &str，更灵活\nfn greet(name: &str) {\n    println!(\"Hello, {}!\", name);\n}\ngreet(\"Alice\");          // 字面量\ngreet(&s2);              // String 的引用",
        },
        {
            "title": "函数定义",
            "subtitle": "最后一个表达式即返回值",
            "speech": "Rust 函数用 fn 关键字声明，参数类型和返回类型都必须显式标注。和 JavaScript 最大的区别是：Rust 函数不需要 return 关键字。最后一个表达式的值就是返回值。注意：有分号结尾是语句，没有分号才是表达式，才会作为返回值。如果需要提前返回，才用 return。",
            "code": "// JavaScript\nfunction add(a, b) {\n  return a + b;\n}\n\n// Rust\nfn add(a: i32, b: i32) -> i32 {\n    a + b  // 没有分号 = 表达式 = 返回值\n}\n\n// 提前返回用 return\nfn divide(a: f64, b: f64) -> Option<f64> {\n    if b == 0.0 {\n        return None;  // 提前返回\n    }\n    Some(a / b)  // 正常返回\n}\n\n// 没有返回值的函数返回 ()\nfn print_hello() {\n    println!(\"Hello!\");  // 隐式返回 ()\n}",
        },
        {
            "title": "控制流：if 表达式",
            "subtitle": "if 可以赋值",
            "speech": "Rust 的 if 是表达式，不是语句。这意味着你可以把 if 的结果直接赋给变量，类似 JavaScript 的三元运算符，但更清晰。注意每个分支必须返回同一种类型，否则编译错误。",
            "code": "// JavaScript 三元\nconst label = age >= 18 ? \"adult\" : \"minor\";\n\n// Rust if 表达式\nlet label = if age >= 18 { \"adult\" } else { \"minor\" };\n\n// 多行 if 表达式\nlet score = 85;\nlet grade = if score >= 90 {\n    \"A\"\n} else if score >= 80 {\n    \"B\"\n} else if score >= 70 {\n    \"C\"\n} else {\n    \"F\"\n};\nprintln!(\"Grade: {}\", grade);",
        },
        {
            "title": "循环：loop、while、for",
            "subtitle": "for 迭代器是核心",
            "speech": "Rust 有三种循环。loop 是无限循环，可以用 break 带出返回值。while 和 JavaScript 一样。最常用的是 for 配合迭代器，语法和 JavaScript 的 for...of 很像，但底层是迭代器协议，性能极好，不会越界。",
            "code": "// loop 可以返回值\nlet result = loop {\n    let x = get_value();\n    if x > 10 { break x * 2; }  // break 带值\n};\n\n// while\nlet mut n = 0;\nwhile n < 5 { n += 1; }\n\n// for + 迭代器（最惯用）\nlet nums = vec![1, 2, 3, 4, 5];\nfor n in &nums {\n    println!(\"{}\", n);\n}\n\n// 范围\nfor i in 0..10 { /* 0-9 */ }\nfor i in 0..=10 { /* 0-10 */ }\n\n// enumerate 同时获取索引\nfor (i, v) in nums.iter().enumerate() {\n    println!(\"{}: {}\", i, v);\n}",
        },
        {
            "title": "match 模式匹配",
            "subtitle": "比 switch 强大十倍",
            "speech": "match 是 Rust 最强大的控制流语句。它类似 switch，但功能强大得多，支持多种模式匹配，而且编译器会检查你是否覆盖了所有情况。如果漏掉了某个枚举变体，编译器直接报错，不会出现运行时的 fall-through 问题。",
            "code": "let num = 7;\nlet description = match num {\n    1         => \"one\",\n    2 | 3     => \"two or three\",   // 多值\n    4..=9     => \"four to nine\",   // 范围\n    _         => \"other\",          // 通配符\n};\n\n// 解构匹配\nenum Direction { North, South, East, West }\nlet dir = Direction::North;\nmatch dir {\n    Direction::North => println!(\"Going north\"),\n    Direction::South => println!(\"Going south\"),\n    Direction::East  => println!(\"Going east\"),\n    Direction::West  => println!(\"Going west\"),\n    // 不需要 _ 因为已穷举所有变体\n}",
        },
        {
            "title": "Option：告别 null",
            "subtitle": "用类型系统消灭 null pointer",
            "speech": "JavaScript 里的 undefined 和 null 是无数 bug 的来源。Rust 没有 null。需要表达「可能没有值」这个概念时，用 Option 枚举。Some 包装有值的情况，None 表示没有值。你必须处理两种情况，编译器不让你忘。",
            "code": "// JavaScript：容易忘记处理 null\nfunction findUser(id) {\n  return users.find(u => u.id === id); // 可能是 undefined\n}\nconst user = findUser(42);\nconsole.log(user.name); // 可能 crash！\n\n// Rust：必须处理两种情况\nfn find_user(id: u32) -> Option<User> {\n    users.iter().find(|u| u.id == id).cloned()\n}\n\n// 用 match 处理\nmatch find_user(42) {\n    Some(user) => println!(\"Found: {}\", user.name),\n    None       => println!(\"Not found\"),\n}\n\n// 或者用 if let（更简洁）\nif let Some(user) = find_user(42) {\n    println!(\"Found: {}\", user.name);\n}",
        },
        {
            "title": "Result：显式错误处理",
            "subtitle": "? 运算符让错误传播更优雅",
            "speech": "Rust 没有异常。函数通过返回 Result 类型来表达可能失败的操作。Ok 包装成功的值，Err 包装错误。? 运算符是语法糖：如果结果是 Err，自动 return 错误；如果是 Ok，自动解包继续执行。这让错误处理既安全又简洁。",
            "code": "use std::num::ParseIntError;\n\n// 返回 Result 的函数\nfn parse_age(s: &str) -> Result<u32, ParseIntError> {\n    let age: u32 = s.parse()?;  // ? 自动传播错误\n    Ok(age)\n}\n\n// 调用方必须处理\nmatch parse_age(\"25\") {\n    Ok(age)  => println!(\"Age: {}\", age),\n    Err(e)   => println!(\"Error: {}\", e),\n}\n\n// 链式 ? 操作\nfn read_and_parse(path: &str) -> Result<i32, Box<dyn std::error::Error>> {\n    let content = std::fs::read_to_string(path)?;\n    let num: i32 = content.trim().parse()?;\n    Ok(num)\n}",
        },
        {
            "title": "实战项目：TODO CLI",
            "subtitle": "综合练习基础知识",
            "speech": "本章的实战项目是一个命令行 TODO 工具。功能包括：添加任务、列出所有任务、标记完成、删除任务，数据用 JSON 文件持久化。你会用到本章学到的所有知识：枚举、match、Option、Result、文件 IO。运行 cargo new todo-cli 开始吧！",
            "code": "# 创建项目\ncargo new todo-cli\ncd todo-cli\n\n# Cargo.toml 添加依赖\n[dependencies]\nserde = { version = \"1\", features = [\"derive\"] }\nserde_json = \"1\"\n\n# 运行\ncargo run -- add \"学习 Rust 所有权\"\ncargo run -- list\ncargo run -- done 1\ncargo run -- remove 1",
        },
        {
            "title": "第一章总结",
            "subtitle": "你已掌握的内容",
            "speech": "第一章到这里。你已经掌握了 Rust 的变量与不可变性、基础类型系统、String 和 &str 的区别、函数定义和表达式返回值、if 表达式、三种循环方式、强大的 match 模式匹配，以及 Option 和 Result 两种核心枚举。下一章我们进入 Rust 最核心的概念——所有权与借用，这是真正让 Rust 与众不同的地方。",
            "code": None,
        },
    ],
}

# ── 第 2 章 ────────────────────────────────────────────────────────────────
CHAPTERS[2] = {
    "title": "所有权与借用",
    "subtitle": "Rust 内存安全的核心机制",
    "slug": "ch02-ownership",
    "segments": [
        {
            "title": "内存管理的三条路",
            "subtitle": "GC vs 手动 vs 所有权",
            "speech": "欢迎来到第二章，所有权与借用。这是 Rust 最独特、也是最重要的概念。很多人学 Rust 卡在这里，但一旦理解透彻，你会发现它的设计极其优雅。先理解三种内存管理方式。JavaScript 用垃圾回收，运行时自动管理，代价是 GC 暂停和不可预测的性能。C 语言手动 malloc 和 free，代价是容易出现内存泄漏和野指针。Rust 选择了第三条路：所有权系统，在编译期静态分析内存，零运行时开销。",
            "code": None,
        },
        {
            "title": "所有权三条规则",
            "subtitle": "背住这三条，所有权就懂了",
            "speech": "所有权只有三条规则。第一：每个值只有一个所有者，是唯一的变量。第二：当所有者离开作用域，值被自动释放，不需要 free，不需要 GC。第三：同一时间，要么有多个不可变引用，要么只有一个可变引用，两者不能共存。这三条规则让 Rust 在编译期就能证明你的代码没有内存安全问题。",
            "code": "{\n    let s = String::from(\"hello\"); // s 进入作用域，堆内存分配\n    // s 可以正常使用\n    println!(\"{}\", s);\n}   // s 离开作用域，drop 自动调用，堆内存释放\n    // 等价于 C 的 free(s)，但完全自动、绝对安全",
        },
        {
            "title": "Move 语义",
            "subtitle": "所有权的转移",
            "speech": "Move 是所有权的核心。当你把一个值赋给另一个变量，所有权就转移了，原来的变量就不能再用了。这和 JavaScript 的引用传递不同。JavaScript 里两个变量指向同一个对象；Rust 里所有权只有一个，转移后原变量失效。为什么？因为两个变量指向同一块堆内存，如果都自动 drop，就会 double free——Rust 在编译期禁止了这种情况。",
            "code": "// JavaScript：两个变量指向同一对象\nconst a = { name: \"Alice\" };\nconst b = a;  // 引用复制\na.name = \"Bob\";  // b.name 也变了\n\n// Rust：所有权转移（Move）\nlet s1 = String::from(\"hello\");\nlet s2 = s1;  // s1 的所有权转移给 s2\n// println!(\"{}\", s1);  // 编译错误！s1 已移动\nprintln!(\"{}\", s2);     // OK\n\n// 如果需要两份独立数据，用 clone\nlet s1 = String::from(\"hello\");\nlet s2 = s1.clone();  // 深拷贝堆数据\nprintln!(\"{} {}\", s1, s2);  // 两个都可以用",
        },
        {
            "title": "Copy 类型",
            "subtitle": "栈数据默认复制",
            "speech": "但等等，整数赋值不会 move 吗？对，因为基础类型实现了 Copy trait。Copy 类型的值存在栈上，赋值时直接复制，不涉及堆内存，所以不需要 Move 语义。实现了 Copy 的类型有：所有整数、浮点数、布尔值、字符，以及只包含 Copy 类型的元组和数组。String 没有实现 Copy，因为它有堆内存。",
            "code": "// Copy 类型：赋值后两个变量都可以用\nlet x = 5;\nlet y = x;  // x 被复制（不是 move）\nprintln!(\"{} {}\", x, y);  // 都可以用\n\n// Copy 类型包括：\nlet a: i32 = 42;        // ✓ Copy\nlet b: f64 = 3.14;      // ✓ Copy\nlet c: bool = true;     // ✓ Copy\nlet d: char = 'R';      // ✓ Copy\nlet e: (i32, i32) = (1, 2);  // ✓ Copy（成员都是 Copy）\n\n// 不是 Copy 的：\nlet s: String = String::from(\"hi\");  // ✗ 堆分配\nlet v: Vec<i32> = vec![1, 2, 3];     // ✗ 堆分配",
        },
        {
            "title": "函数与所有权",
            "subtitle": "传参也会发生 Move",
            "speech": "把值传给函数和赋值给变量遵循同样的规则。传 String 给函数，所有权转移进去，函数结束后就被释放了，调用方不能再用。要避免这个问题，要么函数返回所有权，要么用借用。借用才是 Rust 代码的常见写法。",
            "code": "fn takes_ownership(s: String) {\n    println!(\"{}\", s);\n}   // s 被 drop，堆内存释放\n\nfn makes_copy(n: i32) {\n    println!(\"{}\", n);\n}   // n 是 Copy，只复制，原变量不受影响\n\nlet s = String::from(\"hello\");\ntakes_ownership(s);\n// println!(\"{}\", s);  // 编译错误！s 已被移走\n\nlet n = 42;\nmakes_copy(n);\nprintln!(\"{}\", n);  // OK，n 是 Copy",
        },
        {
            "title": "借用与引用",
            "subtitle": "& 符号：借用不获取所有权",
            "speech": "借用让你临时使用一个值而不获取所有权。用 & 符号借用，得到一个引用。引用就像指针，但永远有效，不会是 null，不会悬空。借用的规则：借用期间，原所有者还是所有者；函数拿到引用，可以读取但默认不能修改；函数结束后引用消失，所有权没有变化。",
            "code": "fn calculate_length(s: &String) -> usize {\n    s.len()  // 读取 s，但不获取所有权\n}  // s（引用）离开作用域，但它指向的 String 不受影响\n\nlet s = String::from(\"hello\");\nlet len = calculate_length(&s);  // & 表示传引用\nprintln!(\"'{}' 的长度是 {}\", s, len);  // s 还可以用！\n\n// 同时有多个不可变引用，完全合法\nlet r1 = &s;\nlet r2 = &s;\nlet r3 = &s;\nprintln!(\"{} {} {}\", r1, r2, r3);  // OK",
        },
        {
            "title": "可变引用",
            "subtitle": "同一时间只能有一个",
            "speech": "如果你需要通过引用修改值，用 &mut。但有严格限制：同一时间，某个值只能有一个可变引用。为什么？为了防止数据竞争。如果两个可变引用同时指向同一数据，它们可能同时修改，导致不一致——这是并发 bug 的根源。Rust 在编译期就禁止了这种情况，不需要锁，不需要运行时检查。",
            "code": "let mut s = String::from(\"hello\");\n\n// 可变引用：允许修改\nlet r = &mut s;\nr.push_str(\" world\");\nprintln!(\"{}\", r);\n\n// 同一时间只能有一个可变引用\nlet r1 = &mut s;\n// let r2 = &mut s;  // 编译错误！r1 还在使用中\n\n// 可变引用和不可变引用不能共存\nlet r1 = &s;      // 不可变引用\nlet r2 = &s;      // OK，可以多个\n// let r3 = &mut s;  // 编译错误！r1 和 r2 还活着",
        },
        {
            "title": "悬空引用",
            "subtitle": "编译器阻止所有悬空指针",
            "speech": "C 语言里，函数返回局部变量的指针，是经典的悬空指针 bug，运行时才 crash。Rust 编译器直接禁止这种写法。如果你试图返回一个指向局部变量的引用，编译失败，给出清晰的错误说明。要返回数据，返回所有权，不要返回引用。",
            "code": "// 这段代码无法编译\nfn dangle() -> &String {\n    let s = String::from(\"hello\");\n    &s  // 编译错误：s 在这里被 drop，返回悬空引用！\n}\n\n// 正确做法：返回所有权\nfn no_dangle() -> String {\n    let s = String::from(\"hello\");\n    s  // 所有权转移给调用方，不会被 drop\n}",
        },
        {
            "title": "字符串切片 &str",
            "subtitle": "借用字符串的一部分",
            "speech": "字符串切片是 String 或字符串字面量的一个片段引用。语法是 &s[start..end]。这就是为什么字符串字面量的类型是 &str，而不是 String——它是对程序数据段中字符串数据的引用，有静态生命周期。理解了借用，&str 就自然了。",
            "code": "let s = String::from(\"hello world\");\n\n// 切片：借用 s 的一部分\nlet hello = &s[0..5];   // \"hello\"\nlet world = &s[6..11];  // \"world\"\n\n// 字符串字面量就是 &str\nlet s: &str = \"hello\";  // 存在程序数据段，'static 生命周期\n\n// 函数参数用 &str 比 &String 更灵活\nfn first_word(s: &str) -> &str {\n    let bytes = s.as_bytes();\n    for (i, &byte) in bytes.iter().enumerate() {\n        if byte == b' ' {\n            return &s[..i];\n        }\n    }\n    &s[..]\n}",
        },
        {
            "title": "生命周期基础",
            "subtitle": "编译器如何验证引用有效性",
            "speech": "生命周期是 Rust 确保引用始终有效的机制。编译器会分析每个引用的存活范围，确保引用不会比它指向的数据活得更长。大多数情况下编译器能自动推断，不需要你手写生命周期注解。只有在某些情况下，比如函数返回引用，且有多个输入引用时，才需要显式标注。生命周期注解不改变任何引用的存活时间，只是给编译器提供信息。",
            "code": "// 大多数情况自动推断，不需要写\nfn first_word(s: &str) -> &str { /* ... */ }\n\n// 需要显式标注的情况：\n// 'a 是生命周期参数，表示返回的引用\n// 至少和输入引用一样长\nfn longest<'a>(x: &'a str, y: &'a str) -> &'a str {\n    if x.len() > y.len() { x } else { y }\n}\n\nlet s1 = String::from(\"long string\");\nlet result;\n{\n    let s2 = String::from(\"xyz\");\n    result = longest(s1.as_str(), s2.as_str());\n    println!(\"{}\", result);  // OK：在 s2 的生命周期内\n}",
        },
        {
            "title": "实战项目：字符串处理器",
            "subtitle": "深刻体验所有权",
            "speech": "本章实战项目是一个字符串处理器，命令行工具，支持统计单词数、反转字符串、统计字符频率等操作。这个项目会让你深刻体验 String 和 &str 的区别，理解什么时候该 clone，什么时候该借用，什么时候该转移所有权。",
            "code": "# 功能示例\ncargo run -- count \"hello world rust\"     # 3\ncargo run -- reverse \"hello\"              # olleh\ncargo run -- freq \"hello world\"           # h:1 e:1 l:3 o:2 ...\ncargo run -- upper \"hello\"               # HELLO",
        },
        {
            "title": "第二章总结",
            "subtitle": "所有权是 Rust 的灵魂",
            "speech": "第二章总结。你已经理解了所有权的三条规则、Move 语义和 Copy 类型的区别、借用和引用的使用方式、可变引用的唯一性约束、Rust 如何在编译期阻止悬空指针，以及生命周期的基本概念。所有权是 Rust 的灵魂，理解了它，你就打通了 Rust 的任督二脉。下一章：异步与并发，Rust 如何在不牺牲安全性的前提下实现高性能异步。",
            "code": None,
        },
    ],
}

# ── 第 3 章 ────────────────────────────────────────────────────────────────
CHAPTERS[3] = {
    "title": "异步与并发",
    "subtitle": "Tokio、Future、Channel",
    "slug": "ch03-async",
    "segments": [
        {
            "title": "Rust 异步模型概览",
            "subtitle": "async/await 语法，Tokio 运行时",
            "speech": "欢迎来到第三章，异步与并发。Rust 的异步模型和 JavaScript 有很多相似之处，都用 async/await 语法，但有一个关键差别：Rust 的 async 函数返回的是一个 Future，它不会自动执行——你需要一个运行时来驱动它。最流行的运行时是 Tokio，类似 Node.js 的事件循环，但性能高出一个数量级，可以处理数十万并发连接。",
            "code": "// JavaScript\nasync function fetchUser(id) {\n  const res = await fetch(`/api/users/${id}`);\n  return res.json();\n}\n\n// Rust\nasync fn fetch_user(id: u32) -> reqwest::Result<User> {\n    let url = format!(\"/api/users/{}\", id);\n    let user: User = reqwest::get(&url)\n        .await?          // 等待 HTTP 响应\n        .json()\n        .await?;         // 解析 JSON\n    Ok(user)\n}",
        },
        {
            "title": "Tokio 运行时配置",
            "subtitle": "#[tokio::main] 宏",
            "speech": "在 Cargo.toml 里添加 Tokio 依赖，在 main 函数加上 #[tokio::main] 宏注解，它会把 main 函数变成异步运行时的入口点。这个宏展开后实际上是创建了一个 Tokio 运行时，启动多线程线程池，然后在上面运行你的 async main。",
            "code": "# Cargo.toml\n[dependencies]\ntokio   = { version = \"1\", features = [\"full\"] }\nreqwest = { version = \"0.12\", features = [\"json\"] }\nserde   = { version = \"1\",   features = [\"derive\"] }\n\n// main.rs\n#[tokio::main]\nasync fn main() {\n    // 现在可以在这里用 .await 了\n    let result = fetch_data().await;\n    println!(\"{:?}\", result);\n}\n\nasync fn fetch_data() -> String {\n    // 模拟异步操作\n    tokio::time::sleep(std::time::Duration::from_millis(100)).await;\n    \"data\".to_string()\n}",
        },
        {
            "title": "tokio::spawn：并发任务",
            "subtitle": "类比 Promise.all",
            "speech": "tokio::spawn 用来启动独立的并发任务，类似 JavaScript 的 Promise.all，但更灵活。每个 spawn 的任务在 Tokio 的线程池上独立运行，互不阻塞。join! 宏等待多个 Future 并发完成，比顺序 await 快得多——如果每个请求需要 100ms，串行需要 300ms，并发只需要 100ms。",
            "code": "use tokio::task::JoinHandle;\n\n#[tokio::main]\nasync fn main() {\n    // 并发启动三个任务\n    let h1: JoinHandle<String> = tokio::spawn(async {\n        fetch_url(\"https://api1.example.com\").await\n    });\n    let h2 = tokio::spawn(async {\n        fetch_url(\"https://api2.example.com\").await\n    });\n    let h3 = tokio::spawn(async {\n        fetch_url(\"https://api3.example.com\").await\n    });\n\n    // 等待所有任务完成\n    let (r1, r2, r3) = tokio::join!(h1, h2, h3);\n    println!(\"{:?} {:?} {:?}\", r1, r2, r3);\n}",
        },
        {
            "title": "Channel：任务间通信",
            "subtitle": "比共享内存更安全",
            "speech": "Channel 是任务间通信的推荐方式，比共享内存更安全。Tokio 提供 mpsc channel，即多生产者单消费者模式。发送方可以 clone，在多个任务里使用；接收方唯一。这个模式在并发爬虫、消息处理管道中极其常见。",
            "code": "use tokio::sync::mpsc;\n\n#[tokio::main]\nasync fn main() {\n    let (tx, mut rx) = mpsc::channel::<String>(32); // 缓冲 32 条\n\n    // 多个生产者\n    for i in 0..5 {\n        let tx_clone = tx.clone();\n        tokio::spawn(async move {\n            let result = format!(\"task {} done\", i);\n            tx_clone.send(result).await.unwrap();\n        });\n    }\n    drop(tx);  // 关闭原始发送方\n\n    // 消费者：接收所有消息\n    while let Some(msg) = rx.recv().await {\n        println!(\"收到：{}\", msg);\n    }\n    // rx.recv() 返回 None 时，所有发送方已关闭，循环结束\n}",
        },
        {
            "title": "select!：等待多个 Future",
            "subtitle": "第一个完成的获胜",
            "speech": "select! 宏同时等待多个 Future，第一个完成的那个被处理，其余的被取消。这在实现超时、竞速、取消逻辑时非常有用。比如给请求加超时，用 select! 同时等待请求完成和定时器触发，哪个先来处理哪个。",
            "code": "use tokio::time::{timeout, Duration};\n\n// 方法一：timeout 包装\nasync fn fetch_with_timeout(url: &str) -> Result<String, &str> {\n    timeout(\n        Duration::from_secs(5),\n        fetch_url(url)\n    ).await.map_err(|_| \"timeout\")\n}\n\n// 方法二：select! 宏\nasync fn race() {\n    tokio::select! {\n        result = fetch_url(\"https://api1.com\") => {\n            println!(\"API1 先到：{}\", result);\n        }\n        result = fetch_url(\"https://api2.com\") => {\n            println!(\"API2 先到：{}\", result);\n        }\n        _ = tokio::time::sleep(Duration::from_secs(3)) => {\n            println!(\"超时！\");\n        }\n    }\n}",
        },
        {
            "title": "并发安全：Send + Sync",
            "subtitle": "类型系统保证线程安全",
            "speech": "Rust 的并发安全来自类型系统的两个 trait。Send 表示类型可以跨线程发送，Sync 表示类型可以跨线程共享引用。大多数类型自动实现这两个 trait。如果你的类型包含不安全的成分，比如裸指针，编译器会拒绝跨线程使用。这彻底消灭了数据竞争——不是靠运行时检测，而是编译期证明。",
            "code": "// Arc：原子引用计数，可以跨线程 clone\n// Mutex：互斥锁，保护可变数据\nuse std::sync::{Arc, Mutex};\n\nlet shared = Arc::new(Mutex::new(vec![]));\n\nlet mut handles = vec![];\nfor i in 0..10 {\n    let shared_clone = Arc::clone(&shared);\n    handles.push(tokio::spawn(async move {\n        let mut data = shared_clone.lock().await; // Tokio async Mutex\n        data.push(i);\n    }));\n}\n\n// 等待所有任务\nfor h in handles { h.await.unwrap(); }\nlet data = shared.lock().await;\nprintln!(\"{:?}\", *data);",
        },
        {
            "title": "实战项目：并发爬虫",
            "subtitle": "同时抓取多个页面",
            "speech": "本章实战项目是一个并发 Web 爬虫。接受一个 URL 列表，同时发起所有 HTTP 请求，通过 Channel 收集结果，限制最大并发数防止过载。这是 Rust 异步最典型的使用场景：大量 IO 密集型任务，Tokio 的线程池让它们真正并发执行，资源占用极低。",
            "code": "use tokio::sync::{mpsc, Semaphore};\nuse std::sync::Arc;\n\nasync fn crawl(urls: Vec<String>) -> Vec<String> {\n    let sem = Arc::new(Semaphore::new(10)); // 最多 10 个并发\n    let (tx, mut rx) = mpsc::channel(100);\n\n    for url in urls {\n        let sem   = Arc::clone(&sem);\n        let tx    = tx.clone();\n        tokio::spawn(async move {\n            let _permit = sem.acquire().await.unwrap();\n            let body = reqwest::get(&url).await\n                .and_then(|r| r.text().await)\n                .unwrap_or_default();\n            tx.send(body).await.ok();\n        });\n    }\n    drop(tx);\n\n    let mut results = vec![];\n    while let Some(body) = rx.recv().await {\n        results.push(body);\n    }\n    results\n}",
        },
        {
            "title": "第三章总结",
            "subtitle": "异步是 Rust 后端的核心优势",
            "speech": "第三章总结。你已经掌握了 Tokio 运行时的配置和使用，async/await 语法，tokio::spawn 启动并发任务，mpsc Channel 实现任务间通信，select! 处理竞速和超时，以及 Send 和 Sync 类型系统的线程安全保证。Rust 的异步性能非常出色，可以轻松处理数万并发连接，内存占用比 Node.js 低几倍。下一章我们用这些知识构建一个完整的 Web API。",
            "code": None,
        },
    ],
}

# ── 第 4 章 ────────────────────────────────────────────────────────────────
CHAPTERS[4] = {
    "title": "Web 后端开发",
    "subtitle": "Axum + REST API 实战",
    "slug": "ch04-web-backend",
    "segments": [
        {
            "title": "为什么选 Axum？",
            "subtitle": "Tokio 官方出品，类型安全路由",
            "speech": "欢迎来到第四章，Web 后端开发。最流行的 Rust Web 框架是 Axum，由 Tokio 团队出品，设计理念和 Express、Fastify 很像，但类型安全程度高出一个量级。路由定义直观，中间件灵活，和 Tokio 生态无缝集成。另外还有 Actix-web，性能测试里经常第一，但 API 风格不同。本课用 Axum，更符合现代 Rust 的惯用风格。",
            "code": "# Cargo.toml\n[dependencies]\naxum      = \"0.8\"\ntokio     = { version = \"1\", features = [\"full\"] }\nserde     = { version = \"1\", features = [\"derive\"] }\nserde_json = \"1\"\ntower     = \"0.5\"\ntower-http = { version = \"0.6\", features = [\"cors\", \"trace\"] }",
        },
        {
            "title": "基础路由与 Handler",
            "subtitle": "和 Express 的对比",
            "speech": "路由定义非常直观，用 Router::new 创建路由器，route 方法注册路径和 handler，get、post、put、delete 指定 HTTP 方法。handler 就是普通的 async 函数，返回任何实现了 IntoResponse 的类型——字符串、JSON、状态码、元组都可以。",
            "code": "// Express.js\napp.get('/users/:id', (req, res) => {\n  res.json({ id: req.params.id });\n});\n\n// Axum\nuse axum::{Router, routing::get, extract::Path, Json};\nuse serde::Serialize;\n\n#[derive(Serialize)]\nstruct User { id: u32, name: String }\n\nasync fn get_user(Path(id): Path<u32>) -> Json<User> {\n    Json(User { id, name: \"Alice\".to_string() })\n}\n\n#[tokio::main]\nasync fn main() {\n    let app = Router::new()\n        .route(\"/users/:id\", get(get_user));\n    let listener = tokio::net::TcpListener::bind(\"0.0.0.0:3000\").await.unwrap();\n    axum::serve(listener, app).await.unwrap();\n}",
        },
        {
            "title": "提取器：自动解析请求",
            "subtitle": "类型驱动的请求处理",
            "speech": "Axum 最强大的特性是提取器，通过函数参数类型，自动从请求中提取你需要的数据。Path 提取 URL 路径参数，Query 提取查询字符串，Json 提取请求体并自动反序列化，State 提取应用共享状态。如果提取失败，自动返回 400 Bad Request，不需要手写校验代码。",
            "code": "use axum::extract::{Path, Query, State, Json};\nuse serde::Deserialize;\n\n#[derive(Deserialize)]\nstruct Pagination { page: Option<u32>, limit: Option<u32> }\n\n#[derive(Deserialize)]\nstruct CreatePost { title: String, content: String }\n\n// 多个提取器组合\nasync fn list_posts(\n    State(db): State<DbPool>,           // 数据库连接池\n    Query(p):  Query<Pagination>,        // ?page=1&limit=10\n) -> Json<Vec<Post>> {\n    let posts = db.list(p.page.unwrap_or(1), p.limit.unwrap_or(10)).await;\n    Json(posts)\n}\n\nasync fn create_post(\n    State(db):    State<DbPool>,\n    Json(input):  Json<CreatePost>,      // 请求 body\n) -> (StatusCode, Json<Post>) {\n    let post = db.create(input.title, input.content).await;\n    (StatusCode::CREATED, Json(post))\n}",
        },
        {
            "title": "错误处理",
            "subtitle": "Result 转 HTTP 响应",
            "speech": "Rust 没有异常，用 Result 类型处理错误。Axum handler 可以直接返回 Result，只需要错误类型实现 IntoResponse trait。推荐定义一个应用级的 AppError 枚举，覆盖所有可能的错误情况，统一转换成合适的 HTTP 状态码和错误消息。",
            "code": "use axum::{http::StatusCode, response::{IntoResponse, Response}};\n\n// 定义应用错误类型\nenum AppError {\n    NotFound(String),\n    Unauthorized,\n    Internal(anyhow::Error),\n}\n\n// 实现 IntoResponse：错误 → HTTP 响应\nimpl IntoResponse for AppError {\n    fn into_response(self) -> Response {\n        let (status, msg) = match self {\n            AppError::NotFound(m)  => (StatusCode::NOT_FOUND, m),\n            AppError::Unauthorized => (StatusCode::UNAUTHORIZED, \"未授权\".into()),\n            AppError::Internal(e)  => (StatusCode::INTERNAL_SERVER_ERROR, e.to_string()),\n        };\n        (status, Json(serde_json::json!({ \"error\": msg }))).into_response()\n    }\n}\n\n// Handler 返回 Result<T, AppError>\nasync fn get_post(Path(id): Path<u32>) -> Result<Json<Post>, AppError> {\n    let post = db.find(id).await.ok_or(AppError::NotFound(\"帖子不存在\".into()))?;\n    Ok(Json(post))\n}",
        },
        {
            "title": "中间件：Tower Layer",
            "subtitle": "日志、CORS、认证",
            "speech": "Axum 的中间件用 Tower Layer 模式，非常灵活。tower-http crate 提供了日志、限流、CORS、压缩等常用中间件，直接 .layer() 添加即可。认证中间件可以检查 JWT，把用户信息注入到请求扩展里，后续 handler 通过 Extension 提取器取出来。",
            "code": "use tower_http::{trace::TraceLayer, cors::CorsLayer};\nuse axum::middleware;\n\n// JWT 认证中间件\nasync fn auth_middleware(\n    mut req: Request,\n    next: Next,\n) -> Result<Response, AppError> {\n    let token = req.headers()\n        .get(\"Authorization\")\n        .and_then(|v| v.to_str().ok())\n        .and_then(|s| s.strip_prefix(\"Bearer \"))\n        .ok_or(AppError::Unauthorized)?;\n\n    let user_id = verify_jwt(token)?;\n    req.extensions_mut().insert(UserId(user_id));\n    Ok(next.run(req).await)\n}\n\nlet app = Router::new()\n    .route(\"/posts\", get(list_posts))\n    .route_layer(middleware::from_fn(auth_middleware)) // 需要认证\n    .layer(TraceLayer::new_for_http())   // 请求日志\n    .layer(CorsLayer::permissive());     // CORS",
        },
        {
            "title": "AppState：共享应用状态",
            "subtitle": "数据库连接池等全局资源",
            "speech": "应用级的共享状态，比如数据库连接池、配置、缓存，用 AppState 结构体包装，通过 with_state 传给路由。因为 Axum 是多线程的，AppState 必须实现 Clone，通常用 Arc 包装需要共享的资源。这个模式和 Express 的 app.locals 类似，但完全类型安全。",
            "code": "use std::sync::Arc;\nuse sqlx::PgPool;\n\n#[derive(Clone)]\nstruct AppState {\n    db:     PgPool,\n    config: Arc<Config>,\n}\n\n#[tokio::main]\nasync fn main() {\n    let pool = PgPool::connect(&std::env::var(\"DATABASE_URL\").unwrap())\n        .await.unwrap();\n\n    let state = AppState {\n        db:     pool,\n        config: Arc::new(Config::from_env()),\n    };\n\n    let app = Router::new()\n        .route(\"/users\",    get(list_users).post(create_user))\n        .route(\"/users/:id\", get(get_user).delete(delete_user))\n        .with_state(state);\n\n    axum::serve(\n        tokio::net::TcpListener::bind(\"0.0.0.0:3000\").await.unwrap(),\n        app\n    ).await.unwrap();\n}",
        },
        {
            "title": "实战项目：博客 REST API",
            "subtitle": "完整 CRUD + 分页 + 认证",
            "speech": "本章实战项目是一个完整的博客 REST API。包括用户注册和登录、JWT 认证、文章的创建、查询、更新、删除，以及分页查询。这是一个生产级 API 的完整实现，覆盖了实际工作中最常见的后端功能。",
            "code": "# API 端点\nPOST /api/auth/register  - 注册\nPOST /api/auth/login     - 登录，返回 JWT\n\nGET    /api/posts          - 列出文章（分页）\nPOST   /api/posts          - 创建文章 [需要认证]\nGET    /api/posts/:id      - 获取单篇\nPUT    /api/posts/:id      - 更新文章 [需要认证]\nDELETE /api/posts/:id      - 删除文章 [需要认证]\n\n# 响应格式\n{ \"data\": [...], \"total\": 100, \"page\": 1, \"limit\": 10 }",
        },
        {
            "title": "第四章总结",
            "subtitle": "Axum 是现代 Rust Web 开发的最佳选择",
            "speech": "第四章总结。你已经掌握了 Axum 路由定义和 handler 编写，提取器自动解析请求参数，Result 类型的错误处理，Tower 中间件的使用，以及 AppState 共享状态模式。Rust Web 框架在性能测试里通常名列前茅，比 Node.js 快 5 到 10 倍，内存占用只有十分之一。下一章我们加入数据库，用 SQLx 实现真正的数据持久化。",
            "code": None,
        },
    ],
}

# ── 第 5 章 ────────────────────────────────────────────────────────────────
CHAPTERS[5] = {
    "title": "数据库与持久化",
    "subtitle": "SQLx + PostgreSQL 类型安全查询",
    "slug": "ch05-database",
    "segments": [
        {
            "title": "为什么选 SQLx？",
            "subtitle": "编译期验证 SQL",
            "speech": "欢迎来到第五章，数据库与持久化。我们用 SQLx 连接 PostgreSQL。SQLx 是 Rust 最流行的数据库库，核心特性是：在编译期验证你的 SQL。你写的 SQL 有语法错误，编译失败。查询结果和 Rust 结构体不匹配，编译失败。引用了不存在的列，编译失败。这在其他语言里是做不到的——Prisma 也只能到运行时才检查。",
            "code": "# Cargo.toml\n[dependencies]\nsqlx = { version = \"0.8\", features = [\n    \"postgres\",\n    \"runtime-tokio\",\n    \"uuid\",\n    \"time\",\n    \"migrate\"\n] }\ntokio     = { version = \"1\", features = [\"full\"] }\nuuid      = { version = \"1\",  features = [\"v4\"] }\ndotenvy   = \"0.15\"",
        },
        {
            "title": "连接池配置",
            "subtitle": "PgPool：可 clone 的共享连接池",
            "speech": "SQLx 的连接池是 Arc 包装的，可以安全 clone 传递给多个 handler。PgPool::connect 自动根据 URL 参数配置池大小，也可以用 PgPoolOptions 精细控制最大连接数、超时时间等。推荐把连接字符串放在环境变量里，用 dotenvy 在开发时从 .env 文件读取。",
            "code": "use sqlx::PgPool;\nuse sqlx::postgres::PgPoolOptions;\n\n#[tokio::main]\nasync fn main() {\n    dotenvy::dotenv().ok();  // 加载 .env 文件\n    let database_url = std::env::var(\"DATABASE_URL\")\n        .expect(\"DATABASE_URL 未设置\");\n\n    // 简单方式\n    let pool = PgPool::connect(&database_url).await.unwrap();\n\n    // 精细控制\n    let pool = PgPoolOptions::new()\n        .max_connections(20)\n        .acquire_timeout(std::time::Duration::from_secs(5))\n        .connect(&database_url)\n        .await.unwrap();\n\n    println!(\"数据库连接成功，连接池：{} 个\", pool.size());\n}",
        },
        {
            "title": "数据库迁移",
            "subtitle": "sqlx migrate：版本化的 schema 管理",
            "speech": "SQLx 内置迁移管理，类似 Prisma Migrate 但更透明。安装 SQLx CLI 之后，用 sqlx migrate add 创建 SQL 文件，sqlx migrate run 执行，sqlx migrate revert 回滚。迁移文件是普通的 SQL 文件，你完全掌控 schema。在应用启动时用 sqlx::migrate! 宏自动运行待执行迁移，非常适合 CI/CD 流程。",
            "code": "# 安装 CLI\ncargo install sqlx-cli\n\n# 创建迁移\nsqlx migrate add create_users_table\nsqlx migrate add create_posts_table\n\n# 执行\nsqlx migrate run\n\n# 回滚\nsqlx migrate revert\n\n-- migrations/20240101_create_users_table.sql\nCREATE TABLE users (\n    id            UUID        PRIMARY KEY DEFAULT gen_random_uuid(),\n    email         TEXT        NOT NULL UNIQUE,\n    username      TEXT        NOT NULL UNIQUE,\n    password_hash TEXT        NOT NULL,\n    created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()\n);\nCREATE INDEX users_email_idx ON users(email);",
        },
        {
            "title": "query_as! 宏：编译期验证",
            "subtitle": "SQL 错误在编译时暴露",
            "speech": "query_as! 宏是 SQLx 的杀手特性。第一个参数是结果映射到的 Rust 类型，然后是 SQL 语句，最后是参数。这个宏在编译时连接数据库验证：SQL 语法是否正确，参数类型是否匹配，返回的列是否和结构体字段对应。需要在开发机器上设置 DATABASE_URL，或者用 SQLX_OFFLINE 模式从缓存验证。",
            "code": "use sqlx::PgPool;\nuse uuid::Uuid;\n\n#[derive(Debug, sqlx::FromRow)]\nstruct User {\n    id:         Uuid,\n    email:      String,\n    username:   String,\n}\n\n// 查询单个用户\nasync fn find_user(pool: &PgPool, email: &str) -> sqlx::Result<Option<User>> {\n    sqlx::query_as!(\n        User,\n        \"SELECT id, email, username FROM users WHERE email = $1\",\n        email\n    )\n    .fetch_optional(pool)  // 0或1条结果\n    .await\n}\n\n// 插入并返回\nasync fn create_user(pool: &PgPool, email: &str, username: &str, hash: &str)\n    -> sqlx::Result<User>\n{\n    sqlx::query_as!(\n        User,\n        \"INSERT INTO users (email, username, password_hash)\n         VALUES ($1, $2, $3)\n         RETURNING id, email, username\",\n        email, username, hash\n    )\n    .fetch_one(pool)\n    .await\n}",
        },
        {
            "title": "fetch 方法对比",
            "subtitle": "根据预期结果数量选择",
            "speech": "SQLx 提供几种 fetch 方法，根据你期望的结果数量选择。fetch_one 期望恰好一条，没有就报错。fetch_optional 返回 Option，有则 Some，无则 None。fetch_all 返回 Vec，适合 SELECT 多条。fetch 返回流，适合处理大量数据时逐条处理，不一次性加载到内存。execute 用于 INSERT、UPDATE、DELETE，返回影响的行数。",
            "code": "// 期望恰好一条（没有则 Error）\nlet user = sqlx::query_as!(User, \"SELECT ... WHERE id = $1\", id)\n    .fetch_one(pool).await?;\n\n// 可能没有（返回 Option）\nlet user = sqlx::query_as!(User, \"SELECT ... WHERE email = $1\", email)\n    .fetch_optional(pool).await?;\n\n// 所有结果（返回 Vec）\nlet users = sqlx::query_as!(User, \"SELECT ... LIMIT $1\", limit)\n    .fetch_all(pool).await?;\n\n// 流式处理（大量数据）\nlet mut stream = sqlx::query_as!(User, \"SELECT ...\")\n    .fetch(pool);\nwhile let Some(user) = stream.try_next().await? {\n    process(user);\n}\n\n// INSERT/UPDATE/DELETE\nlet rows = sqlx::query!(\"DELETE FROM users WHERE id = $1\", id)\n    .execute(pool).await?.rows_affected();",
        },
        {
            "title": "事务处理",
            "subtitle": "pool.begin() 自动回滚",
            "speech": "事务处理非常直观。pool.begin() 开启事务，得到 Transaction 对象。在 transaction 上执行操作，最后 commit 提交。如果中途出现错误提前返回，transaction 的 Drop 实现会自动回滚——这是 Rust 所有权系统的又一个实际应用，RAII 模式保证资源自动清理。",
            "code": "async fn transfer_credits(\n    pool:    &PgPool,\n    from_id: Uuid,\n    to_id:   Uuid,\n    amount:  i64,\n) -> sqlx::Result<()> {\n    let mut tx = pool.begin().await?;  // 开启事务\n\n    // 检查余额\n    let balance = sqlx::query_scalar!(\n        \"SELECT balance FROM accounts WHERE id = $1\", from_id\n    ).fetch_one(&mut *tx).await?;\n\n    if balance < amount {\n        return Err(sqlx::Error::RowNotFound); // tx drop → 自动回滚\n    }\n\n    sqlx::query!(\n        \"UPDATE accounts SET balance = balance - $1 WHERE id = $2\",\n        amount, from_id\n    ).execute(&mut *tx).await?;\n\n    sqlx::query!(\n        \"UPDATE accounts SET balance = balance + $1 WHERE id = $2\",\n        amount, to_id\n    ).execute(&mut *tx).await?;\n\n    tx.commit().await?;  // 提交\n    Ok(())\n}",
        },
        {
            "title": "与 Axum 集成",
            "subtitle": "PgPool 作为 AppState",
            "speech": "把 PgPool 作为 AppState 的字段传入路由，每个 handler 通过 State 提取器获取。这是标准的 Axum 加 SQLx 模式。所有 handler 共享同一个连接池，连接池负责管理并发连接，不需要每次请求都新建连接。",
            "code": "use axum::{extract::{Path, State}, routing::get, Json, Router};\nuse sqlx::PgPool;\n\n#[derive(Clone)]\nstruct AppState { db: PgPool }\n\n#[tokio::main]\nasync fn main() {\n    dotenvy::dotenv().ok();\n    let pool = PgPool::connect(&std::env::var(\"DATABASE_URL\").unwrap())\n        .await.unwrap();\n    sqlx::migrate!(\"./migrations\").run(&pool).await.unwrap(); // 自动迁移\n\n    let app = Router::new()\n        .route(\"/users/:id\", get(get_user))\n        .with_state(AppState { db: pool });\n\n    axum::serve(\n        tokio::net::TcpListener::bind(\"0.0.0.0:3000\").await.unwrap(),\n        app\n    ).await.unwrap();\n}\n\nasync fn get_user(\n    State(state): State<AppState>,\n    Path(id):     Path<Uuid>,\n) -> Result<Json<User>, StatusCode> {\n    sqlx::query_as!(User, \"SELECT * FROM users WHERE id = $1\", id)\n        .fetch_optional(&state.db).await\n        .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?\n        .map(Json)\n        .ok_or(StatusCode::NOT_FOUND)\n}",
        },
        {
            "title": "第五章总结",
            "subtitle": "告别 ORM 魔法，掌握真正的数据控制权",
            "speech": "第五章总结。你已经掌握了 SQLx 的核心特性：编译期 SQL 验证，连接池的配置和使用，数据库迁移管理，query_as! 宏的各种 fetch 方法，事务处理和自动回滚，以及与 Axum 的集成方式。下一章我们把前端 Next.js 和 Rust 后端结合起来，构建一个完整的全栈实时应用。",
            "code": None,
        },
    ],
}

# ── 第 6 章 ────────────────────────────────────────────────────────────────
CHAPTERS[6] = {
    "title": "全栈项目实战",
    "subtitle": "Next.js + Axum 完整架构",
    "slug": "ch06-fullstack",
    "segments": [
        {
            "title": "全栈架构总览",
            "subtitle": "前后端如何协作",
            "speech": "欢迎来到第六章，全栈项目实战。这章把前面所有章节的知识整合起来，构建一个生产就绪的全栈应用。架构是：前端用 Next.js 16，通过 HTTP API 和 WebSocket 与 Rust 后端通信，后端用 Axum 加 SQLx 连接 PostgreSQL。前端用 Server Components 做首屏渲染，用 WebSocket 做实时更新。这是现代全栈应用的标准架构。",
            "code": "前端 (Next.js 16 + TypeScript)\n├── App Router + Server Components\n├── 实时更新 (WebSocket 客户端)\n└── JWT 认证 (cookie-based)\n         │ HTTP / WebSocket\n后端 (Axum + Tokio)\n├── REST API (/api/*)\n├── WebSocket 端点 (/ws)\n├── JWT 认证中间件\n└── PostgreSQL via SQLx",
        },
        {
            "title": "ts-rs：前后端类型共享",
            "subtitle": "Rust 类型自动生成 TypeScript",
            "speech": "全栈 Rust 最大的优势之一——用 ts-rs crate，可以从 Rust 类型自动生成 TypeScript 类型定义。你只需在 Rust 结构体上加 #[derive(TS)] 和 #[ts(export)] 注解，运行 cargo test，TypeScript 类型文件自动写入前端目录。后端修改结构体，TypeScript 编译器报告所有需要更新的前端代码。彻底消灭前后端类型不一致的问题。",
            "code": "// backend/src/models.rs\nuse ts_rs::TS;\n\n#[derive(Debug, Serialize, Deserialize, TS)]\n#[ts(export, export_to = \"../frontend/src/types/\")]\npub struct Task {\n    pub id:          Uuid,\n    pub title:       String,\n    pub description: Option<String>,\n    pub status:      TaskStatus,\n    pub assignee_id: Option<Uuid>,\n    pub created_at:  String,\n}\n\n#[derive(Debug, Serialize, Deserialize, TS)]\n#[ts(export, export_to = \"../frontend/src/types/\")]\npub enum TaskStatus { Todo, InProgress, Done }\n\n// 运行后自动生成：\n// frontend/src/types/Task.ts\nexport interface Task {\n  id: string;\n  title: string;\n  description: string | null;\n  status: TaskStatus;\n  assignee_id: string | null;\n  created_at: string;\n}\nexport type TaskStatus = \"Todo\" | \"InProgress\" | \"Done\";",
        },
        {
            "title": "WebSocket 后端实现",
            "subtitle": "广播 channel + Axum WebSocket",
            "speech": "实时功能的核心是广播 channel。创建一个 broadcast Sender，所有连接的 WebSocket 客户端各自订阅。当有任务更新时，向 channel 发送事件，所有订阅者都会收到。Tokio 的 select! 同时等待接收广播事件和客户端消息，哪个先来处理哪个，客户端断开时退出循环。",
            "code": "use axum::extract::ws::{Message, WebSocket, WebSocketUpgrade};\nuse tokio::sync::broadcast;\nuse serde::{Deserialize, Serialize};\n\n#[derive(Clone, Serialize, Deserialize)]\n#[serde(tag = \"type\", content = \"data\")]\npub enum WsEvent {\n    TaskCreated(Task),\n    TaskUpdated(Task),\n    TaskDeleted { id: String },\n}\n\npub type Board = Arc<broadcast::Sender<WsEvent>>;\n\nasync fn handle_socket(mut socket: WebSocket, tx: Board) {\n    let mut rx = tx.subscribe();\n    loop {\n        tokio::select! {\n            Ok(event) = rx.recv() => {\n                let msg = serde_json::to_string(&event).unwrap();\n                if socket.send(Message::Text(msg)).await.is_err() { break; }\n            }\n            Some(Ok(Message::Text(_))) = socket.recv() => { /* 处理客户端消息 */ }\n            else => break,\n        }\n    }\n}",
        },
        {
            "title": "WebSocket 前端 Hook",
            "subtitle": "React useBoard Hook",
            "speech": "前端用 React hook 封装 WebSocket 连接。useBoard hook 管理 WebSocket 连接的建立和关闭，处理接收到的事件，更新本地任务状态。根据事件类型，TaskCreated 追加任务，TaskUpdated 替换对应任务，TaskDeleted 过滤删除。组件卸载时关闭连接，清理资源。",
            "code": "// frontend/src/hooks/useBoard.ts\nimport { useEffect, useRef, useState } from \"react\";\nimport type { Task, WsEvent } from \"@/types\";\n\nexport function useBoard(boardId: string) {\n  const [tasks, setTasks] = useState<Task[]>([]);\n  const ws = useRef<WebSocket | null>(null);\n\n  useEffect(() => {\n    ws.current = new WebSocket(\n      `${process.env.NEXT_PUBLIC_WS_URL}/ws/board/${boardId}`\n    );\n    ws.current.onmessage = (e) => {\n      const event: WsEvent = JSON.parse(e.data);\n      setTasks(prev => {\n        if (event.type === \"TaskCreated\") return [...prev, event.data];\n        if (event.type === \"TaskUpdated\")\n          return prev.map(t => t.id === event.data.id ? event.data : t);\n        if (event.type === \"TaskDeleted\")\n          return prev.filter(t => t.id !== event.data.id);\n        return prev;\n      });\n    };\n    return () => ws.current?.close();\n  }, [boardId]);\n\n  return { tasks };\n}",
        },
        {
            "title": "Server Components + Rust API",
            "subtitle": "服务端直接调用，消灭首屏 loading",
            "speech": "Next.js Server Components 可以直接调用 Rust API，完全在服务端执行，不经过浏览器。页面加载时已经有数据，没有 loading 状态的闪烁。用 cookies 读取 auth token，服务端认证，然后 fetch 数据，把初始任务列表作为 props 传给客户端的 TaskBoard 组件。TaskBoard 接收初始数据，后续通过 WebSocket 实时更新。",
            "code": "// frontend/src/app/board/[id]/page.tsx\nimport { cookies } from \"next/headers\";\nimport { api } from \"@/lib/api\";\nimport { TaskBoard } from \"@/components/TaskBoard\";\n\nexport default async function BoardPage({\n  params,\n}: {\n  params: Promise<{ id: string }>;\n}) {\n  const { id } = await params;\n  const cookieStore = await cookies();\n  const token = cookieStore.get(\"auth_token\")?.value;\n  if (!token) redirect(\"/login\");\n\n  // Server Component 直接调用 Rust API\n  // 在服务端执行，不经过浏览器，首屏有数据\n  const tasks = await api.tasks.list(token);\n\n  return (\n    <main>\n      <h1>任务板</h1>\n      {/* 初始数据来自服务器，后续通过 WebSocket 实时更新 */}\n      <TaskBoard initialTasks={tasks} boardId={id} />\n    </main>\n  );\n}",
        },
        {
            "title": "实战项目：实时协作任务板",
            "subtitle": "完整全栈应用",
            "speech": "本章实战是实时协作任务板，类似简化版 Trello。功能包括：多用户同时操作，任务变化实时同步，任务拖拽（可选），JWT cookie 认证，完整的 CRUD API。这是一个真正的生产就绪应用，前端工程师会觉得很亲切，因为 Next.js 部分和你熟悉的完全一样，Rust 后端则用了前五章学到的所有技术。",
            "code": "# 启动开发环境\n\n# 终端 1：PostgreSQL\ndocker run -e POSTGRES_PASSWORD=password -p 5432:5432 postgres:16\n\n# 终端 2：Rust 后端\ncd backend && cargo run\n# 服务器启动在 http://localhost:3001\n\n# 终端 3：Next.js 前端\ncd frontend && pnpm dev\n# 访问 http://localhost:3000",
        },
        {
            "title": "第六章总结",
            "subtitle": "前后端类型安全的全栈方案",
            "speech": "第六章总结。你已经掌握了 Monorepo 项目结构，ts-rs 自动同步 Rust 类型到 TypeScript，Axum WebSocket 加 React 客户端的实时通信，类型安全 API 客户端的设计，Server Components 直接调用 Rust API，以及 JWT Cookie 认证流程。下一章：DevOps 与部署，把这个项目打包进 Docker，配置 CI/CD，推上生产环境。",
            "code": None,
        },
    ],
}

# ── 第 7 章 ────────────────────────────────────────────────────────────────
CHAPTERS[7] = {
    "title": "DevOps 与部署",
    "subtitle": "Docker · CI/CD · Kubernetes",
    "slug": "ch07-devops",
    "segments": [
        {
            "title": "Rust 的 DevOps 优势",
            "subtitle": "单一静态二进制，20MB 镜像",
            "speech": "欢迎来到第七章，DevOps 与部署。Rust 编译出的是单一静态二进制文件，没有运行时依赖，不像 Node.js 需要 node_modules，不像 Python 需要虚拟环境。这让容器化极其简单。Node.js 镜像通常三四百兆，Rust 镜像用多阶段构建，最终只有十到二十兆，减少超过九成的大小，拉取更快，攻击面更小。",
            "code": "# 镜像大小对比\nNode.js:  基础镜像(100MB) + node(50MB) + node_modules(200MB) = 350MB+\nRust:     FROM debian:slim + 单一二进制 = 15-25MB\n\n# 启动时间对比\nNode.js:  ~500ms（加载 JS 运行时）\nRust:     ~5ms（直接执行二进制）\n\n# 内存对比（相同负载）\nNode.js:  ~200MB\nRust:     ~20MB",
        },
        {
            "title": "Docker 多阶段构建",
            "subtitle": "编译阶段和运行阶段分离",
            "speech": "多阶段构建是 Rust Docker 的关键技巧。第一阶段用完整的 Rust 工具链编译，大约两个 GB，但不进入最终镜像。第二阶段用极简的 Debian slim 基础镜像，只复制编译好的二进制。关键优化：先复制 Cargo.toml 和 Cargo.lock，构建一次依赖层，再复制源码重新编译应用。这样只有代码变化时才重新编译应用逻辑，依赖层被 Docker 缓存，CI 速度快很多。",
            "code": "# Dockerfile\nFROM rust:1.78-slim AS builder\nWORKDIR /app\n\n# 先复制依赖文件，利用 Docker 缓存\nCOPY Cargo.toml Cargo.lock ./\nRUN mkdir src && echo \"fn main() {}\" > src/main.rs\nRUN cargo build --release  # 只编译依赖\nRUN rm -rf src\n\n# 再复制真正的源码，只重新编译应用\nCOPY src ./src\nRUN touch src/main.rs && cargo build --release\n\nFROM debian:bookworm-slim AS runtime\nRUN apt-get update && apt-get install -y ca-certificates \\\n    && rm -rf /var/lib/apt/lists/*\nRUN useradd -m appuser\nUSER appuser\nCOPY --from=builder /app/target/release/blog-api .\nEXPOSE 3000\nCMD [\"./blog-api\"]",
        },
        {
            "title": "Docker Compose：本地开发",
            "subtitle": "一键启动完整环境",
            "speech": "Docker Compose 让你一条命令启动完整的本地开发环境：PostgreSQL、后端、前端。服务间通过服务名互相访问，健康检查确保 PostgreSQL 就绪后再启动后端。数据卷持久化数据库数据，重启不丢失。这是现代全栈开发的标准工作流。",
            "code": "# docker-compose.yml\nservices:\n  postgres:\n    image: postgres:16-alpine\n    environment:\n      POSTGRES_USER:     rustforge\n      POSTGRES_PASSWORD: development\n      POSTGRES_DB:       rustforge_db\n    ports: [\"5432:5432\"]\n    healthcheck:\n      test: [\"CMD-SHELL\", \"pg_isready -U rustforge\"]\n      interval: 5s\n\n  backend:\n    build: ./backend\n    ports: [\"3001:3000\"]\n    environment:\n      DATABASE_URL: postgres://rustforge:development@postgres/rustforge_db\n    depends_on:\n      postgres: { condition: service_healthy }\n\n  frontend:\n    build: ./frontend\n    ports: [\"3000:3000\"]\n    depends_on: [backend]\n\n# 一键启动\ndocker compose up -d",
        },
        {
            "title": "GitHub Actions CI/CD",
            "subtitle": "自动测试、构建、部署",
            "speech": "GitHub Actions 流水线：推送代码自动触发。先跑 cargo fmt 格式检查，cargo clippy 代码质量检查，cargo test 运行测试。测试通过后，只有推送到 main 分支才构建 Docker 镜像，推送到容器仓库，然后部署到生产服务器。用 Swatinem/rust-cache 缓存编译产物，把 CI 时间从十几分钟压到两三分钟。",
            "code": "# .github/workflows/ci.yml\nname: CI/CD\non:\n  push: { branches: [main] }\n  pull_request: { branches: [main] }\n\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - uses: dtolnay/rust-toolchain@stable\n        with: { components: clippy, rustfmt }\n      - uses: Swatinem/rust-cache@v2  # 缓存编译产物\n      - run: cargo fmt --check\n      - run: cargo clippy -- -D warnings\n      - run: cargo test\n\n  deploy:\n    needs: test\n    if: github.ref == 'refs/heads/main'\n    runs-on: ubuntu-latest\n    steps:\n      - uses: docker/build-push-action@v5\n        with:\n          push: true\n          tags: ghcr.io/${{ github.repository }}:${{ github.sha }}",
        },
        {
            "title": "Kubernetes 部署",
            "subtitle": "低内存占用，高并发",
            "speech": "Kubernetes 部署 Rust 服务有天然优势。内存限制可以设置得很低，Node.js 通常需要 256 到 512 MB，Rust 64 MB 绰绰有余。在大规模集群里，几百个 Pod 的内存差异意味着显著更低的云账单。三副本部署，Kubernetes 自动负载均衡，readinessProbe 确保只有健康实例接收流量。",
            "code": "# k8s/deployment.yaml\napiVersion: apps/v1\nkind: Deployment\nspec:\n  replicas: 3\n  template:\n    spec:\n      containers:\n        - name: blog-api\n          image: ghcr.io/your-org/blog-api:latest\n          env:\n            - name: DATABASE_URL\n              valueFrom:\n                secretKeyRef:   # 从 K8s Secret 读取\n                  name: db-secret\n                  key: url\n          resources:\n            requests: { cpu: 100m, memory: 64Mi }\n            limits:   { cpu: 500m, memory: 128Mi }  # Rust 内存极低！\n          readinessProbe:\n            httpGet: { path: /health, port: 3000 }\n            initialDelaySeconds: 5",
        },
        {
            "title": "优雅关闭与健康检查",
            "subtitle": "生产环境必备",
            "speech": "生产环境必须正确处理关闭信号。Kubernetes 发送 SIGTERM 时，应用应该停止接受新请求，等待当前请求处理完毕，然后退出。Axum 的 with_graceful_shutdown 配合 Tokio 的信号处理，可以实现完美的优雅关闭。健康检查端点返回服务状态，Kubernetes 靠它判断实例是否就绪。",
            "code": "async fn health() -> Json<Value> {\n    Json(json!({ \"status\": \"ok\", \"version\": env!(\"CARGO_PKG_VERSION\") }))\n}\n\n#[tokio::main]\nasync fn main() {\n    let app = Router::new().route(\"/health\", get(health));\n    axum::serve(\n        tokio::net::TcpListener::bind(\"0.0.0.0:3000\").await.unwrap(),\n        app\n    )\n    .with_graceful_shutdown(shutdown_signal())  // 优雅关闭\n    .await.unwrap();\n}\n\nasync fn shutdown_signal() {\n    tokio::select! {\n        _ = tokio::signal::ctrl_c() => {},\n        _ = async {\n            tokio::signal::unix::signal(\n                tokio::signal::unix::SignalKind::terminate()\n            ).unwrap().recv().await;\n        } => {},\n    }\n    println!(\"收到关闭信号，等待请求处理完毕...\");\n}",
        },
        {
            "title": "第七章总结",
            "subtitle": "Rust 让 DevOps 变得简单",
            "speech": "第七章总结。你已经掌握了 Docker 多阶段构建，把 Rust 应用打包成 20MB 镜像，Docker Compose 本地开发环境一键启动，GitHub Actions CI/CD 自动化测试和部署，Kubernetes Deployment 加 Service 配置，优雅关闭和健康检查的实现，以及 tracing 结构化日志。最后一章：Rust 加 AI 集成，用 Rust 的性能优势驱动 AI 应用。",
            "code": None,
        },
    ],
}

# ── 第 8 章 ────────────────────────────────────────────────────────────────
CHAPTERS[8] = {
    "title": "Rust + AI 集成",
    "subtitle": "LLM API · RAG · Agent",
    "slug": "ch08-ai",
    "segments": [
        {
            "title": "为什么用 Rust 做 AI 后端？",
            "subtitle": "IO 密集型任务的甜区",
            "speech": "欢迎来到最后一章，Rust 加 AI 集成。AI 应用通常瓶颈在网络 IO，也就是调用 LLM API 的等待时间，而不是 CPU 计算。这正是 Rust 异步模型的甜区。Tokio 可以同时处理数千个 LLM 请求，内存占用极低。Rust 的 Stream trait 天然适合 SSE 流式响应。向量计算有 SIMD 支持，比 Python 快 10 倍以上。编译成单一二进制，可以部署到 Cloudflare Workers、Fly.io 边缘节点。",
            "code": None,
        },
        {
            "title": "调用 OpenAI / Claude API",
            "subtitle": "reqwest + serde 类型安全",
            "speech": "调用 LLM API，用 reqwest 发 HTTP 请求，用 serde 做 JSON 序列化和反序列化。Rust 的 serde 让 JSON 处理完全类型安全。如果 API 返回的字段和你定义的结构体不匹配，编译或解析时立即报错——不会在运行时才发现字段拼错了。这和 JavaScript 里 response.json() 直接用完全不同，Rust 强迫你事先定义好数据结构。",
            "code": "use reqwest::Client;\nuse serde::{Deserialize, Serialize};\n\n#[derive(Serialize)]\nstruct ChatRequest {\n    model:    String,\n    messages: Vec<Message>,\n}\n\n#[derive(Serialize, Deserialize)]\nstruct Message { role: String, content: String }\n\n#[derive(Deserialize)]\nstruct ChatResponse { choices: Vec<Choice> }\n\n#[derive(Deserialize)]\nstruct Choice { message: Message }\n\nasync fn chat(prompt: &str) -> anyhow::Result<String> {\n    let client = Client::new();\n    let res: ChatResponse = client\n        .post(\"https://api.openai.com/v1/chat/completions\")\n        .bearer_auth(std::env::var(\"OPENAI_API_KEY\")?)\n        .json(&ChatRequest {\n            model:    \"gpt-4o\".into(),\n            messages: vec![Message { role: \"user\".into(), content: prompt.into() }],\n        })\n        .send().await?\n        .json().await?;\n    Ok(res.choices[0].message.content.clone())\n}",
        },
        {
            "title": "流式响应：SSE + Axum",
            "subtitle": "让用户看到逐字生成",
            "speech": "流式响应是 AI 应用最重要的用户体验——让用户看到文字逐字生成，而不是等全部完成才显示。Axum 内置 SSE 支持，配合 Tokio 的 mpsc channel，可以优雅实现。后台任务调用 LLM 流式接口，解析每个 chunk，通过 channel 发送给 SSE 端点，SSE 端点把 channel 转成事件流推给客户端。整个过程完全异步，不阻塞任何线程。",
            "code": "use axum::response::{IntoResponse, Sse};\nuse axum::response::sse::{Event, KeepAlive};\nuse tokio::sync::mpsc;\n\npub async fn stream_chat(\n    Json(input): Json<ChatInput>,\n) -> impl IntoResponse {\n    let (tx, rx) = mpsc::channel::<Result<Event, Infallible>>(32);\n\n    tokio::spawn(async move {\n        let client = Client::new();\n        let mut stream = client\n            .post(\"https://api.openai.com/v1/chat/completions\")\n            .bearer_auth(std::env::var(\"OPENAI_API_KEY\").unwrap())\n            .json(&json!({\n                \"model\": \"gpt-4o\", \"stream\": true,\n                \"messages\": [{ \"role\": \"user\", \"content\": input.message }]\n            }))\n            .send().await.unwrap().bytes_stream();\n\n        while let Some(Ok(bytes)) = stream.next().await {\n            // 解析 SSE data 行，提取 delta content\n            // 发送给 channel\n        }\n    });\n\n    Sse::new(ReceiverStream::new(rx)).keep_alive(KeepAlive::default())\n}",
        },
        {
            "title": "向量数据库与 RAG",
            "subtitle": "让 AI 回答你代码库的问题",
            "speech": "检索增强生成，简称 RAG，让 AI 能回答关于你自己代码库的专属问题。流程是：把文档向量化存入数据库，用户提问时向量化查询，找到最相关的文档片段，把这些片段加入 prompt，让 LLM 基于这些上下文回答。用 pgvector 给 PostgreSQL 加向量搜索能力，用 async-openai 生成嵌入向量，余弦相似度操作符 <=> 找最近邻。",
            "code": "-- 启用 pgvector 扩展\nCREATE EXTENSION IF NOT EXISTS vector;\n\nCREATE TABLE documents (\n    id        SERIAL PRIMARY KEY,\n    content   TEXT NOT NULL,\n    metadata  JSONB,\n    embedding vector(1536)  -- OpenAI text-embedding-3-small 维度\n);\nCREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops);\n\n// Rust RAG 查询\npub async fn search(&self, query: &str, limit: i64) -> Vec<String> {\n    let query_emb = self.embed(query).await;\n    sqlx::query!(\n        \"SELECT content FROM documents\n         ORDER BY embedding <=> $1 LIMIT $2\",\n        query_emb as Vector, limit,\n    )\n    .fetch_all(&self.pool).await.unwrap()\n    .into_iter().map(|r| r.content).collect()\n}",
        },
        {
            "title": "AI Agent：Function Calling",
            "subtitle": "让 AI 自主决定调用哪个工具",
            "speech": "AI Agent 的核心是工具调用，也叫 Function Calling。你定义一组工具，每个工具有名字、描述、参数 schema。LLM 根据用户请求决定调用哪个工具、传什么参数。你执行工具，把结果返回给 LLM，LLM 继续决策，直到任务完成。这个循环就是 Agent 的基本工作模式。用 Rust 实现 Agent，类型系统确保工具调用的参数和结果都是正确的类型。",
            "code": "pub async fn run_agent(user_request: &str) -> anyhow::Result<String> {\n    let client = reqwest::Client::new();\n    let mut messages = vec![json!({ \"role\": \"user\", \"content\": user_request })];\n\n    loop {\n        let response = client\n            .post(\"https://api.openai.com/v1/chat/completions\")\n            .bearer_auth(std::env::var(\"OPENAI_API_KEY\")?)\n            .json(&json!({\n                \"model\": \"gpt-4o\",\n                \"messages\": messages,\n                \"tools\": TOOLS,\n            }))\n            .send().await?.json::<Value>().await?;\n\n        let choice = &response[\"choices\"][0];\n        if choice[\"finish_reason\"] == \"stop\" {\n            return Ok(choice[\"message\"][\"content\"].as_str().unwrap_or(\"\").to_string());\n        }\n        // 执行工具调用，把结果追加到 messages\n        // 继续循环\n    }\n}",
        },
        {
            "title": "本地 LLM：Ollama 集成",
            "subtitle": "无需 API Key，开发免费",
            "speech": "Ollama 让你在本地运行开源 LLM，不需要 API Key，完全免费。最妙的是，Ollama 的 API 完全兼容 OpenAI 格式，只需要改 base_url，Rust 代码完全不用改。开发阶段用本地 Ollama，测试通过后切换到 Claude 或 GPT-4o，一个环境变量搞定。这是非常实用的成本优化策略。",
            "code": "# 安装 Ollama\nbrew install ollama\nollama pull llama3.2      # 通用模型\nollama pull codellama     # 代码专用模型\n\n// Rust 代码只需改 base_url\nlet client = async_openai::Client::with_config(\n    async_openai::config::OpenAIConfig::new()\n        .with_api_base(\"http://localhost:11434/v1\")\n        .with_api_key(\"ollama\"),  // 本地不需要真实 key\n);\n// 之后和调用 OpenAI 完全一样\n// 切换到 GPT-4o 只需改环境变量 OPENAI_API_KEY 和 base_url",
        },
        {
            "title": "课程完结",
            "subtitle": "你已系统掌握 Rust 全栈",
            "speech": "恭喜你完成 RustForge 全部八章！你已经系统掌握了 Rust 基础与类型系统，所有权与借用这个最核心的概念，Tokio 异步并发，Axum Web 后端开发，SQLx 数据库持久化，Next.js 加 Axum 全栈架构，Docker 和 CI/CD 的 DevOps 实践，以及 LLM API、SSE 流式响应、RAG 和 Agent 的 AI 集成。下一步：加入 Rust 中文社区，贡献开源项目，把这些技能用到真实工作中。感谢你完成 RustForge 全部课程！",
            "code": None,
        },
    ],
}

# ══════════════════════════════════════════════════════════════════════════
# 视频帧渲染
# ══════════════════════════════════════════════════════════════════════════

def load_fonts():
    sizes = {}
    for size in [16, 18, 20, 24, 28, 32, 36, 48, 56]:
        try:
            sizes[f"cn_{size}"]   = ImageFont.truetype(FONT_CN,   size)
            sizes[f"mono_{size}"] = ImageFont.truetype(FONT_MONO, size)
        except:
            sizes[f"cn_{size}"]   = ImageFont.load_default()
            sizes[f"mono_{size}"] = ImageFont.load_default()
    return sizes

FONTS = load_fonts()

def wrap_text(text, font, max_width, draw):
    """按像素宽度自动换行"""
    lines = []
    for paragraph in text.split("\n"):
        if not paragraph.strip():
            lines.append("")
            continue
        words = list(paragraph)
        current = ""
        for ch in words:
            test = current + ch
            bbox = draw.textbbox((0, 0), test, font=font)
            if bbox[2] - bbox[0] > max_width and current:
                lines.append(current)
                current = ch
            else:
                current = test
        if current:
            lines.append(current)
    return lines

def render_frame(chapter_info, seg, subtitle_line, progress):
    """渲染单帧图像"""
    img  = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # ── 顶部 bar ──
    draw.rectangle([0, 0, W, 6], fill=ACCENT)

    # ── 章节 & 标题 ──
    ch_label = f"第 {chapter_info['chapter']} 章  ·  {chapter_info['title']}"
    draw.text((60, 30), ch_label,
              font=FONTS["cn_20"], fill=TEXT_DIM)

    seg_title = seg.get("title", "")
    if seg_title:
        draw.text((60, 60), seg_title,
                  font=FONTS["cn_36"], fill=TEXT_H)

    seg_sub = seg.get("subtitle", "")
    if seg_sub:
        draw.text((60, 106), seg_sub,
                  font=FONTS["cn_20"], fill=ACCENT)

    # ── 分隔线 ──
    draw.line([(60, 140), (W - 60, 140)], fill=(50, 50, 80), width=1)

    # ── 代码块（如有） ──
    code = seg.get("code")
    if code:
        code_x, code_y = 60, 160
        code_w = W - 120
        code_lines = code.split("\n")
        max_vis = 22
        if len(code_lines) > max_vis:
            code_lines = code_lines[:max_vis] + ["..."]

        # 代码背景
        line_h = 26
        code_h = len(code_lines) * line_h + 24
        draw.rounded_rectangle(
            [code_x, code_y, code_x + code_w, code_y + code_h],
            radius=8, fill=CODE_BG
        )
        # 顶部 traffic lights
        for i, dot_color in enumerate([(220, 80, 70), (220, 180, 60), (100, 200, 80)]):
            draw.ellipse([code_x + 14 + i*20, code_y + 8,
                          code_x + 24 + i*20, code_y + 18], fill=dot_color)

        for i, line in enumerate(code_lines):
            y_pos = code_y + 24 + i * line_h
            # 简单语法高亮
            color = CODE_FG
            stripped = line.lstrip()
            if stripped.startswith("//") or stripped.startswith("#"):
                color = CODE_CMT
            elif any(stripped.startswith(kw) for kw in
                     ["fn ", "let ", "pub ", "use ", "async ", "await",
                      "struct ", "enum ", "impl ", "match ", "if ", "for ",
                      "while ", "return ", "mod ", "type ", "const "]):
                color = CODE_KW
            elif stripped.startswith(("\"", "'", "r#")):
                color = CODE_STR

            draw.text((code_x + 14, y_pos), line,
                      font=FONTS["mono_18"], fill=color)

    # ── 字幕条 ──
    if subtitle_line:
        sub_h = 70
        sub_y = H - sub_h - 20
        sub_bg = Image.new("RGBA", (W - 120, sub_h), (0, 0, 0, 190))
        img.paste(sub_bg, (60, sub_y), sub_bg)

        # 字幕文字居中
        font = FONTS["cn_28"]
        bbox = draw.textbbox((0, 0), subtitle_line, font=font)
        tw = bbox[2] - bbox[0]
        tx = (W - tw) // 2
        # 描边
        for dx, dy in [(-1,-1),(1,-1),(-1,1),(1,1)]:
            draw.text((tx+dx, sub_y+18+dy), subtitle_line, font=font, fill=(0,0,0))
        draw.text((tx, sub_y + 18), subtitle_line, font=font, fill=(255, 255, 255))

    # ── 进度条 ──
    bar_y = H - 8
    draw.rectangle([0, bar_y, W, H], fill=(30, 30, 50))
    draw.rectangle([0, bar_y, int(W * progress), H], fill=ACCENT)

    # ── Logo watermark ──
    draw.text((W - 160, H - 40), "RustForge 🦀",
              font=FONTS["cn_18"], fill=(80, 80, 100))

    return img

# ══════════════════════════════════════════════════════════════════════════
# VTT 字幕生成
# ══════════════════════════════════════════════════════════════════════════

def format_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}"

def make_vtt(cues, out_path):
    lines = ["WEBVTT", ""]
    for i, (start, end, text) in enumerate(cues, 1):
        lines.append(str(i))
        lines.append(f"{format_time(start)} --> {format_time(end)}")
        # 长文本按 25 字换行
        words = list(text)
        cur = ""
        sub_lines = []
        for ch in words:
            cur += ch
            if len(cur) >= 25:
                sub_lines.append(cur)
                cur = ""
        if cur:
            sub_lines.append(cur)
        lines.append("\n".join(sub_lines))
        lines.append("")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  字幕已保存：{out_path}")

# ══════════════════════════════════════════════════════════════════════════
# 音频生成（ChatTTS）
# ══════════════════════════════════════════════════════════════════════════

_chat = None
_rand_spk = None

def get_chat():
    global _chat, _rand_spk
    if _chat is None:
        import ChatTTS
        import torch
        _chat = ChatTTS.Chat()
        _chat.load(compile=False)
        torch.manual_seed(2024)
        _rand_spk = _chat.sample_random_speaker()
    return _chat, _rand_spk

def tts(text):
    import ChatTTS
    chat, spk = get_chat()
    params = ChatTTS.Chat.InferCodeParams(
        spk_emb=spk,
        temperature=0.3,
        top_P=0.7,
        top_K=20,
    )
    wavs = chat.infer([text], params_infer_code=params)
    return wavs[0].astype(np.float32)

# ══════════════════════════════════════════════════════════════════════════
# 主流程：为某章生成视频
# ══════════════════════════════════════════════════════════════════════════

def generate_chapter(ch_num):
    ch = CHAPTERS[ch_num]
    ch_info = {
        "chapter": ch_num,
        "title":   ch["title"],
    }
    slug = ch["slug"]
    print(f"\n=== 第 {ch_num} 章：{ch['title']} ===")

    segments   = ch["segments"]
    n_segs     = len(segments)

    # 1. 生成每段音频，记录时间戳
    audio_parts   = []
    cues          = []   # [(start, end, text), ...]
    current_time  = 0.0
    SILENCE_SHORT = np.zeros(int(SAMPLE * 0.4), dtype=np.float32)
    SILENCE_LONG  = np.zeros(int(SAMPLE * 0.8), dtype=np.float32)

    for i, seg in enumerate(segments):
        speech = seg["speech"].strip()
        print(f"  [{i+1}/{n_segs}] {seg['title']}: 生成音频...")

        # 按句子切分（句号、问号、感叹号）
        import re
        sentences = re.split(r'(?<=[。！？\n])', speech)
        sentences = [s.strip() for s in sentences if s.strip()]

        seg_waves = []
        seg_start = current_time

        for sent in sentences:
            if len(sent) < 2:
                continue
            wave = tts(sent)
            duration = len(wave) / SAMPLE
            # 这句话的字幕区间
            cues.append((current_time, current_time + duration, sent))
            seg_waves.append(wave)
            seg_waves.append(SILENCE_SHORT)
            current_time += duration + len(SILENCE_SHORT) / SAMPLE

        seg_end = current_time
        audio_parts.extend(seg_waves)
        audio_parts.append(SILENCE_LONG)
        current_time += len(SILENCE_LONG) / SAMPLE

        print(f"     {seg_start:.1f}s - {seg_end:.1f}s")

    # 2. 合并音频
    print("  合并音频...")
    full_audio = np.concatenate(audio_parts)
    total_dur  = len(full_audio) / SAMPLE
    audio_path = os.path.join(WORK_DIR, f"{slug}.wav")
    sf.write(audio_path, full_audio, SAMPLE)
    print(f"  音频时长：{total_dur:.1f}s ({total_dur/60:.1f} 分钟)")

    # 3. 生成 VTT 字幕
    vtt_path = os.path.join(SUB_OUT, f"{slug}.vtt")
    make_vtt(cues, vtt_path)

    # 4. 生成视频帧（关键帧策略：每段开始生成一帧，中间帧复用）
    print("  生成视频帧...")
    frames_dir = os.path.join(WORK_DIR, f"{slug}_frames")
    os.makedirs(frames_dir, exist_ok=True)

    # 计算每段对应的时间范围
    seg_times = []
    t = 0.0
    for i, seg in enumerate(segments):
        start = t
        n_sents = len([s for s in re.split(r'(?<=[。！？\n])', seg["speech"].strip()) if s.strip()])
        avg_sent_dur = 3.5
        seg_dur = max(n_sents * avg_sent_dur, 8.0)
        end = min(t + seg_dur, total_dur)
        seg_times.append((start, end))
        t = end

    # 生成帧：每帧找到对应的段，找到对应的字幕
    frame_count = int(total_dur * FPS)
    print(f"  总帧数：{frame_count}（{total_dur:.0f}s × {FPS}fps）")

    # 找每帧对应的段
    def get_seg_for_time(t):
        for i, (s, e) in enumerate(seg_times):
            if s <= t < e:
                return i
        return len(segments) - 1

    # 找每帧对应的字幕
    def get_subtitle_for_time(t):
        for start, end, text in cues:
            if start <= t < end:
                return text
        return ""

    # 只生成关键帧（每段第一帧），其他帧直接复用
    # 使用 ffmpeg 的 -loop 功能，配合图片序列
    # 策略：每 FPS 帧生成一张图片（每秒一张），ffmpeg 插值
    KEYFRAME_INTERVAL = FPS  # 每秒一帧

    frame_idx = 0
    for f in range(0, frame_count, KEYFRAME_INTERVAL):
        t = f / FPS
        seg_i = get_seg_for_time(t)
        seg   = segments[seg_i]
        sub   = get_subtitle_for_time(t)
        prog  = t / total_dur if total_dur > 0 else 0

        frame = render_frame(ch_info, seg, sub, prog)
        frame_path = os.path.join(frames_dir, f"frame_{frame_idx:06d}.png")
        frame.save(frame_path)
        frame_idx += 1

        if frame_idx % 30 == 0:
            print(f"     帧 {frame_idx}/{frame_count // KEYFRAME_INTERVAL}...")

    print(f"  生成了 {frame_idx} 张关键帧")

    # 5. ffmpeg 合成视频
    video_path = os.path.join(VIDEO_OUT, f"{slug}.mp4")
    print(f"  合成视频：{video_path}")

    # 关键帧 → 视频（每张图片展示 1 秒）
    frames_pattern = os.path.join(frames_dir, "frame_%06d.png")
    tmp_video = os.path.join(WORK_DIR, f"{slug}_video_only.mp4")

    cmd_video = [
        "ffmpeg", "-y",
        "-framerate", "1",            # 输入帧率：每秒 1 张图片
        "-i", frames_pattern,
        "-vf", f"fps={FPS}",          # 输出帧率：插值到 24fps
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-pix_fmt", "yuv420p",
        tmp_video
    ]
    subprocess.run(cmd_video, check=True, capture_output=True)

    # 合并音频
    cmd_merge = [
        "ffmpeg", "-y",
        "-i", tmp_video,
        "-i", audio_path,
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "128k",
        "-shortest",
        video_path
    ]
    subprocess.run(cmd_merge, check=True, capture_output=True)

    print(f"  完成！视频：{video_path}")
    print(f"  时长：{total_dur/60:.1f} 分钟")

    # 清理临时帧
    import shutil
    shutil.rmtree(frames_dir, ignore_errors=True)
    os.remove(tmp_video)

    return video_path

# ══════════════════════════════════════════════════════════════════════════
# 入口
# ══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "all"

    if arg == "all":
        for ch_num in sorted(CHAPTERS.keys()):
            generate_chapter(ch_num)
    else:
        try:
            ch_num = int(arg)
            if ch_num not in CHAPTERS:
                print(f"章节 {ch_num} 不存在，可选：{sorted(CHAPTERS.keys())}")
                sys.exit(1)
            generate_chapter(ch_num)
        except ValueError:
            print(f"用法：python3 gen_videos.py [1-8|all]")
            sys.exit(1)

    print("\n全部完成！")
