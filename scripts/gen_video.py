#!/usr/bin/env python3
"""
RustForge 视频生成脚本 v3
- 要点逐条显示（有淡入切换）
- 底部实时音频波形（全宽）
- 幻灯片内容进度条
- 每章 20+ 分钟，内容丰富

用法:
  python3 scripts/gen_video.py 1       # 生成第1章
  python3 scripts/gen_video.py all     # 生成全部 16 章
"""

import os, sys, subprocess, textwrap, re
from PIL import Image, ImageDraw, ImageFont

REPO      = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
AUDIO_DIR = os.path.join(REPO, "apps/web/public/videos")
VIDEO_DIR = os.path.join(REPO, "apps/web/public/videos")
SUB_DIR   = os.path.join(REPO, "apps/web/public/subtitles")
WORK_DIR  = os.path.join(REPO, "scripts/_work")
os.makedirs(WORK_DIR, exist_ok=True)

W, H = 1920, 1080
FPS  = 24
WAVE_H = 0     # 不保留波形区，底部改为字幕

# ffmpeg-full 包含 libass（支持 subtitles filter）
FFMPEG  = "/opt/homebrew/opt/ffmpeg-full/bin/ffmpeg"
FFPROBE = "/opt/homebrew/opt/ffmpeg-full/bin/ffprobe"

# ── 颜色 ─────────────────────────────────────────────────────────────────
BG      = (10,  10,  20)
BG2     = (16,  16,  32)
ACCENT  = (220, 110,  50)
ACCENT2 = (160,  70,  25)
WHITE   = (240, 240, 255)
GRAY    = (160, 160, 190)
DIM     = (90,  90, 120)
GRID_C  = (20,  20,  38)

# ── 字体 ─────────────────────────────────────────────────────────────────
CN_FONT   = "/System/Library/Fonts/STHeiti Medium.ttc"
MONO_FONT = "/System/Library/Fonts/Menlo.ttc"

# ── 章节元数据 ────────────────────────────────────────────────────────────
CHAPTERS = {
    1:  ("basics",         "CH.01", "入门：安装与 Cargo",         "模块一 · Rust 核心基础"),
    2:  ("variables",      "CH.02", "变量、类型与函数",            "模块一 · Rust 核心基础"),
    3:  ("ownership",      "CH.03", "所有权与借用",               "模块一 · Rust 核心基础"),
    4:  ("structs",        "CH.04", "结构体、枚举与模式匹配",      "模块一 · Rust 核心基础"),
    5:  ("errors",         "CH.05", "错误处理",                   "模块二 · Rust 进阶"),
    6:  ("generics",       "CH.06", "泛型、Trait 与迭代器",       "模块二 · Rust 进阶"),
    7:  ("smart-pointers", "CH.07", "智能指针",                   "模块二 · Rust 进阶"),
    8:  ("async",          "CH.08", "并发与异步编程",              "模块二 · Rust 进阶"),
    9:  ("web-backend",    "CH.09", "Web 后端：Axum",             "模块三 · 全栈工程"),
    10: ("database",       "CH.10", "数据库：SQLx",               "模块三 · 全栈工程"),
    11: ("fullstack",      "CH.11", "全栈实战",                   "模块三 · 全栈工程"),
    12: ("testing",        "CH.12", "测试与工具链",                "模块三 · 全栈工程"),
    13: ("devops",         "CH.13", "DevOps 与部署",              "模块四 · 生产实践"),
    14: ("performance",    "CH.14", "性能优化与 unsafe",           "模块四 · 生产实践"),
    15: ("wasm",           "CH.15", "命令行工具与 WebAssembly",    "模块四 · 生产实践"),
    16: ("ai",             "CH.16", "Rust + AI 集成",             "模块四 · 生产实践"),
}

# ── 幻灯片内容（与第二版相同） ─────────────────────────────────────────────
SLIDES = {}
SLIDES[1] = [
    ("为什么前端工程师学 Rust？",
     ["Node 服务内存泄漏、高并发抖动、CLI 工具体积大",
      "TypeScript 把类型错误提前到编译期",
      "Rust 更进一步：内存错误 + 并发 bug 也提前到编译期",
      "零运行时开销：无 GC、无 VM，直接机器码"],
     600),
    ("安装 Rust 工具链",
     ["rustup：Rust 的版本管理器，对应 nvm",
      "macOS/Linux: curl --proto '=https' ... | sh",
      "安装结果：rustc 编译器 + cargo 构建工具 + rust-std",
      "rustup update / rustup toolchain list"],
     500),
    ("rustup 组件管理",
     ["rustup component add clippy  →  代码检查工具",
      "rustup component add rustfmt  →  代码格式化",
      "rustup target add wasm32-unknown-unknown  →  WASM 目标",
      "rustup doc  →  离线文档，无需网络"],
     450),
    ("Cargo：包管理 + 构建工具",
     ["cargo new hello-rust  →  创建项目（自动 git init）",
      "Cargo.toml  ≈  package.json（TOML 格式，支持注释）",
      "target/ 目录  ≈  node_modules（加入 .gitignore）",
      "Cargo.lock  ≈  package-lock.json（应用提交，库不提交）"],
     600),
    ("npm vs Cargo 命令对比",
     ["npm install  →  cargo add / 编辑 Cargo.toml",
      "npm run build  →  cargo build（--release 生产版）",
      "npm test  →  cargo test（内置测试框架）",
      "npm publish  →  cargo publish（发布到 crates.io）"],
     550),
    ("Rust 程序结构",
     ["Package → Crate → Module 三层体系",
      "src/main.rs 是 binary crate 入口（有 main 函数）",
      "src/lib.rs 是 library crate 入口（供他人调用）",
      "fn main() 是程序入口，println! 后有 ! 表示这是宏"],
     500),
    ("变量默认不可变",
     ["let x = 5  →  不可变（类似 const）",
      "let mut x = 5  →  显式声明可变",
      "变量遮蔽（shadowing）：同名 let 可改变类型",
      "设计理念：显式表达「我要修改这个变量」的意图"],
     500),
    ("基础数据类型",
     ["整数：i32（默认）、u8（字节）、usize（索引）",
      "浮点数：f64（默认）、f32",
      "字符串：&str 是引用视图，String 是堆上所有者",
      "函数参数用 &str，存储/修改用 String"],
     550),
    ("函数与控制流",
     ["fn add(a: i32, b: i32) -> i32  →  参数和返回类型必须标注",
      "最后一个表达式（无分号）就是返回值，不需要 return",
      "if 是表达式：let result = if x > 0 { \"正\" } else { \"负\" }",
      "for i in 1..=5 配合范围表达式遍历"],
     550),
    ("实战：温度转换 CLI",
     ["cargo new temp-converter",
      "函数：celsius_to_fahrenheit、celsius_to_kelvin",
      "命令行参数：std::env::args().nth(1)",
      "cargo run -- 100  →  传参数给程序"],
     400),
    ("本章总结",
     ["rustup 管工具链 / Cargo 管项目和依赖",
      "变量默认不可变，mut 显式声明可变",
      "表达式无分号 = 返回值，语句有分号 = 无值",
      "下一章：变量类型系统深度解析"],
     300),
]

# 其余章节使用简化版要点（用于视频，详细内容在 MDX 里）
for ch_num in range(2, 17):
    SLIDES[ch_num] = SLIDES[1][:]   # 占位，实际运行时会使用真实数据

# 为 ch2-16 补充真实要点
SLIDES[2] = [
    ("类型系统：为什么比 TypeScript 更严格",
     ["TypeScript 类型编译后消失，运行时还是 JS",
      "Rust 类型影响内存布局、函数约定、性能特征",
      "类型错误不只是逻辑错误，往往是内存安全问题的信号",
      "静态强类型 + 编译器类型推断 = 两全其美"],
     500),
    ("整数类型体系",
     ["i8/i16/i32/i64/i128  →  有符号整数",
      "u8/u16/u32/u64/u128  →  无符号整数",
      "isize / usize  →  机器字长，专用于数组索引",
      "1_000_000 下划线分隔 / 0xFF 十六进制 / 0b1010 二进制"],
     550),
    ("字符串两种形式",
     ["&str：字符串切片，引用只读数据，不拥有内存",
      "String：堆分配可增长字符串，拥有数据",
      "&str 是「视图」，String 是「所有者」",
      "String::from(\"hello\") / \"hello\".to_string() 互转"],
     500),
    ("元组与 Vec",
     ["元组：固定长度，不同类型  →  let p = (3.0, 4.0)",
      "点语法访问：p.0 / p.1；解构：let (x, y) = p",
      "Vec：动态长度堆存储，类比 JavaScript Array",
      "vec![1, 2, 3] 宏创建 / push/pop/get 操作"],
     500),
    ("函数与表达式",
     ["表达式有值，语句没有值——这是 Rust 的核心设计",
      "最后一行无分号 = 表达式 = 返回值",
      "最后一行有分号 = 语句 = 返回 unit ()",
      "if-else 本身是表达式，可用于赋值"],
     500),
]

SLIDES[3] = [
    ("内存基础：栈 vs 堆",
     ["栈：后进先出，大小编译时确定，访问极快",
      "堆：动态分配，灵活但需要管理，存放 String/Vec 等",
      "JavaScript：GC 自动管理；C：手动 malloc/free",
      "Rust：所有权系统，编译器自动插入释放代码"],
     550),
    ("所有权三条规则",
     ["规则一：每个值都有一个变量作为它的「所有者」",
      "规则二：一个值在任何时刻只有一个所有者",
      "规则三：所有者离开作用域，值自动被释放",
      "违反规则 → 编译错误，不会进入运行时"],
     500),
    ("Move 语义：所有权转移",
     ["let s2 = s1  →  String 的所有权从 s1 转移到 s2",
      "转移后 s1 失效，不能再使用——编译期就阻止",
      "防止 double free：不让两个变量同时拥有同一数据",
      "整数等 Copy 类型赋值是复制，不是移动"],
     550),
    ("借用（Borrowing）",
     ["&s1 创建对 s1 的引用，函数「借用」而不获取所有权",
      "借用规则：可以有多个 &T 不可变引用",
      "同一时刻只能有一个 &mut T 可变引用",
      "这些规则在编译期检查，防止数据竞争"],
     500),
    ("生命周期",
     ["引用不能比它指向的数据活得更长",
      "编译器自动推断大多数情况的生命周期",
      "复杂场景需要显式标注：&'a str",
      "'a 标注告诉编译器引用之间的生命周期关系"],
     500),
]

SLIDES[4] = [
    ("结构体：数据 + 行为",
     ["struct User { username: String, email: String }",
      "impl User { fn new(...) / fn greet(&self) }",
      "关联函数（无 self）= 静态方法，用 User::new() 调用",
      "方法（有 &self）= 实例方法，用 user.greet() 调用"],
     550),
    ("枚举：代数数据类型",
     ["enum Shape { Circle(f64), Rectangle(f64, f64) }",
      "每个变体可以携带不同类型的数据",
      "比其他语言的 enum 强大得多——不只是标签",
      "配合 match 实现类型安全的多态分发"],
     500),
    ("Option：消灭 null",
     ["Option<T> = Some(T) | None",
      "Rust 没有 null，所有「可能无值」的情况用 Option",
      "编译器强制你处理 None——不能像 null 悄悄传播",
      "if let Some(v) = opt { ... }  简洁处理有值情况"],
     500),
    ("match 穷举模式匹配",
     ["必须覆盖所有情况，否则编译错误",
      "支持范围、多值（|）、绑定变量、守卫（if）",
      "解构：match point { Point{x, y} => ... }",
      "新增枚举变体时，所有 match 都会提醒你处理"],
     500),
]

SLIDES[5] = [
    ("错误处理哲学",
     ["JavaScript：函数是否抛出异常？只能看文档或踩坑",
      "Rust：返回 Result<T,E> = 明确告诉你可能失败",
      "不处理 Result，编译器报警告——无法忽略错误",
      "panic vs Result：程序 bug 用 panic，预期失败用 Result"],
     550),
    ("? 操作符：优雅传播错误",
     ["expr?  =  Ok(v) 则继续用 v；Err(e) 则立即返回 Err",
      "类比 await：await 让 Promise 拒绝变异常",
      "? 让错误沿调用链自动往上冒泡",
      "只能在返回 Result 或 Option 的函数里用 ?"],
     500),
    ("thiserror：精确错误类型",
     ["#[derive(Error, Debug)]  →  自动实现 Display 和 Error",
      "#[error(\"IO 错误：{0}\")]  →  自定义错误信息模板",
      "#[from] io::Error  →  自动 From 转换（? 需要）",
      "适合库代码：调用方可以 match 不同的错误情况"],
     500),
    ("anyhow：应用级快速错误",
     ["anyhow::Result<T>  =  Result<T, anyhow::Error>",
      "可以装入任意错误类型，无需手动定义错误枚举",
      ".context(\"无法读取配置文件\")  加上有意义的上下文",
      "适合应用代码：关注错误信息，不关注具体类型"],
     500),
]

SLIDES[6] = [
    ("泛型：写一次，处理多种类型",
     ["fn largest<T: PartialOrd>(list: &[T]) -> &T",
      "T 是类型参数，: PartialOrd 是 Trait 约束",
      "编译时单态化：为每种实际类型生成专用代码",
      "零运行时开销——不是 Java 泛型那种装箱"],
     500),
    ("Trait：定义共享行为",
     ["trait Summary { fn summarize(&self) -> String; }",
      "impl Summary for Article { ... }  →  为类型实现 Trait",
      "Trait 可以有默认实现，子类可以选择覆盖",
      "类似 TypeScript interface，但可以有方法体"],
     500),
    ("迭代器：惰性高效链式操作",
     ["Iterator Trait 核心：fn next() -> Option<Self::Item>",
      "适配器（惰性）：map / filter / zip / take",
      "消费器（触发执行）：collect / sum / count / fold",
      "链式操作一次遍历，比多次 for 循环更高效"],
     500),
    ("JS 数组 vs Rust 迭代器",
     ["JavaScript：filter().map() 三次遍历、三次中间数组",
      "Rust：.filter().map().collect() 一次遍历",
      "迭代器是惰性的，到 collect 才真正执行",
      "LLVM 通常能自动 SIMD 向量化迭代器循环"],
     500),
]

SLIDES[7] = [
    ("为什么需要智能指针",
     ["所有权规则：每值只有一个所有者",
      "但有时需要多个所有者、堆上分配、内部可变",
      "智能指针：拥有数据 + Drop 时自动释放 + 额外能力",
      "Box / Rc / Arc / RefCell 解决不同场景"],
     500),
    ("Box<T>：堆分配",
     ["Box::new(value) 把值分配到堆，本身在栈上",
      "用途1：递归类型（编译时大小未知）",
      "enum List { Cons(i32, Box<List>), Nil }",
      "用途2：Trait 对象  Box<dyn Shape>"],
     450),
    ("Rc<T>：引用计数，共享所有权",
     ["Rc::new(value) 创建引用计数智能指针",
      "Rc::clone(&rc) 只增加引用计数，非常廉价",
      "所有 Rc 都 drop 后，计数降为0，数据释放",
      "单线程用 Rc，多线程用 Arc（原子计数）"],
     500),
    ("RefCell<T>：内部可变性",
     ["编译时检查变为运行时检查（违规则 panic）",
      "Rc<RefCell<T>>：可共享 + 可修改的数据",
      ".borrow() 获取不可变引用 / .borrow_mut() 可变引用",
      "常用于图数据结构、事件系统、状态机"],
     500),
]

SLIDES[8] = [
    ("线程与「无畏并发」",
     ["thread::spawn(|| { ... }) 创建新线程",
      "Send trait：类型可以安全跨线程传递",
      "Sync trait：类型的引用可以多线程共享",
      "违反 Send/Sync → 编译错误，防止数据竞争"],
     500),
    ("线程间通信：消息传递",
     ["mpsc::channel() 创建发送者/接收者对",
      "tx.send(value) 发送；rx.recv() 阻塞等待",
      "Arc::new(Mutex::new(0)) 线程安全的共享状态",
      "「不要通过共享内存通信，通过通信共享内存」"],
     500),
    ("async/await 与 Tokio",
     ["Rust 的异步需要运行时，最流行的是 Tokio",
      "async fn 返回惰性的 Future，.await 驱动执行",
      "tokio::join!(task1, task2)  ≈  Promise.all",
      "语义和 JavaScript await 完全一致"],
     500),
    ("Stream：异步迭代器",
     ["Stream ≈ JavaScript 的 AsyncIterable",
      "while let Some(item) = stream.next().await",
      "常用于处理 SSE、WebSocket 消息、数据库游标",
      "tokio-stream crate 提供 StreamExt 扩展方法"],
     450),
]

SLIDES[9] = [
    ("Axum：类型安全的 Web 框架",
     ["类似 Express.js，但类型安全程度远超 TS+Express",
      "Router::new().route(\"/posts\", get(list).post(create))",
      "方法对应 HTTP 动词，链式 API 简洁直观",
      "充分利用 Rust 类型系统，错误尽早在编译期暴露"],
     500),
    ("提取器（Extractor）模式",
     ["函数参数声明 = 从请求里取什么",
      "Path(id): Path<Uuid>  →  从路径提取 UUID",
      "Json(body): Json<CreatePost>  →  反序列化请求体",
      "State(state): State<AppState>  →  共享状态"],
     500),
    ("JWT 认证：自定义提取器",
     ["impl FromRequestParts<S> for AuthUser { ... }",
      "从 Authorization: Bearer TOKEN 提取并验证",
      "handler 参数加 auth: AuthUser → 自动验证",
      "未认证自动返回 401，无需在每个 handler 手动检查"],
     450),
    ("统一错误处理",
     ["enum AppError { NotFound, Unauthorized, Internal }",
      "impl IntoResponse for AppError → 自动转 HTTP 状态码",
      "所有 handler 返回 Result<T, AppError>",
      "错误信息统一返回 JSON 格式"],
     500),
]

SLIDES[10] = [
    ("SQLx：编译时验证 SQL",
     ["sqlx::query! 宏在编译时连接数据库验证 SQL",
      "SQL 语法错误 / 列不存在 / 类型不匹配 → 编译失败",
      "比 Prisma 更透明：你写真正的 SQL，不是 ORM 方言",
      "支持 PostgreSQL / MySQL / SQLite"],
     500),
    ("数据库迁移",
     ["cargo install sqlx-cli  →  安装命令行工具",
      "sqlx migrate add create_users  →  创建迁移文件",
      "sqlx migrate run  →  执行所有待执行迁移",
      "sqlx::migrate!().run(&pool) 启动时自动迁移"],
     450),
    ("连接池与查询",
     ["PgPool::connect(&url).await  →  创建连接池",
      "sqlx::query_as!(User, \"SELECT * FROM users WHERE id=$1\", id)",
      "fetch_one / fetch_optional / fetch_all / execute",
      "类型安全：编译期验证查询结果类型"],
     500),
    ("事务处理",
     ["let mut tx = pool.begin().await?",
      "query.execute(&mut *tx).await?  →  在事务内执行",
      "tx.commit().await?  →  提交",
      "tx drop 时如未提交自动回滚（RAII 语义）"],
     450),
]

SLIDES[11] = [
    ("全栈架构",
     ["前端：Next.js 16（App Router + Server Components）",
      "后端：Axum + Tokio + SQLx",
      "类型同步：ts-rs 自动从 Rust 生成 TypeScript 类型",
      "实时通信：Axum WebSocket + React Hook"],
     500),
    ("ts-rs：类型自动同步",
     ["#[derive(TS)] #[ts(export)] struct Task { ... }",
      "cargo test export_bindings  →  生成 .ts 文件",
      "后端改字段 → 前端 TypeScript 自动报错提醒",
      "彻底消灭前后端类型手动同步的烦恼"],
     500),
    ("WebSocket：实时广播",
     ["broadcast::channel::<Event>(100) 广播频道",
      "AppState 持有 Arc<broadcast::Sender<Event>>",
      "ws_handler：为每个连接订阅广播，转发给客户端",
      "REST 接口操作后广播事件给所有在线用户"],
     500),
    ("Server Components + Rust API",
     ["Server Component 直接调用 Rust API（服务端请求）",
      "首次渲染 SSR：快速 TTFB + SEO 友好",
      "之后更新通过 WebSocket 实时推送",
      "HttpOnly Cookie 存 JWT：安全 + 自动随请求携带"],
     450),
]

SLIDES[12] = [
    ("Rust 内置测试框架",
     ["#[test] 标记测试函数，cargo test 自动发现",
      "#[cfg(test)] mod tests { ... } 只在测试时编译",
      "assert_eq! / assert! / assert_ne! 断言宏",
      "无需安装 Jest 等第三方框架，开箱即用"],
     500),
    ("异步测试与数据库测试",
     ["#[tokio::test] async fn test_api() { ... }",
      "#[sqlx::test] → 自动提供干净的数据库连接",
      "每个测试用独立事务，结束自动回滚",
      "测试真实 SQL，不用 mock，更可靠"],
     450),
    ("代码质量工具",
     ["cargo clippy -- -D warnings  →  代码检查",
      "cargo fmt / cargo fmt --check  →  格式化",
      "cargo doc --open  →  生成并查看文档",
      "cargo audit  →  检查依赖安全漏洞"],
     450),
    ("CI 配置",
     ["cargo fmt --check && cargo clippy -- -D warnings",
      "cargo test  →  运行所有测试",
      "Swatinem/rust-cache@v2  →  缓存编译产物",
      "dtolnay/rust-toolchain@stable  →  安装指定版本"],
     450),
]

SLIDES[13] = [
    ("Rust 的 DevOps 优势",
     ["单一静态二进制，无运行时依赖",
      "Node.js 镜像：350MB+  →  Rust 镜像：10-20MB",
      "冷启动极快（毫秒级），适合边缘计算",
      "内存占用极低：64MB vs Node 的 256-512MB"],
     500),
    ("Docker 多阶段构建",
     ["阶段1（builder）：rust:slim 编译，~2GB 工具链",
      "阶段2（runtime）：debian:bookworm-slim + 单个二进制",
      "COPY --from=builder /app/target/release/app .",
      "最终镜像只有几十 MB，不含任何编译工具"],
     500),
    ("GitHub Actions CI",
     ["on: push → branches: [main]",
      "services: postgres 在 CI 里起测试数据库",
      "Swatinem/rust-cache 缓存编译产物",
      "cargo fmt --check + cargo clippy + cargo test"],
     450),
    ("Kubernetes 部署",
     ["Deployment: replicas: 3，滚动更新",
      "resources.limits.memory: \"128Mi\"（Rust 极低内存）",
      "readinessProbe: GET /health，确保服务就绪",
      "secretKeyRef: DATABASE_URL 从 K8s Secret 读取"],
     450),
]

SLIDES[14] = [
    ("性能优化原则",
     ["先测量再优化，flamegraph 找真实热点",
      "cargo flamegraph --bin app  →  生成火焰图",
      "cargo bench  →  使用 Criterion 做微基准测试",
      "cargo build --release  →  Debug 和 Release 差 10 倍"],
     500),
    ("Rayon：一行代码并行化",
     ["data.iter().map(|x| expensive(x)).sum()  →  串行",
      "data.par_iter().map(|x| expensive(x)).sum()  →  并行",
      "改一个方法名，自动用所有 CPU 核心",
      "工作窃取算法，无数据竞争，编译器保证安全"],
     450),
    ("unsafe Rust",
     ["unsafe 不是「关闭安全检查」",
      "而是「我保证这段代码的安全性，编译器信任我」",
      "extern \"C\" { fn strlen(...) }  →  FFI 调用 C 库",
      "最小化 unsafe 范围，详细注释安全理由"],
     500),
    ("Release 构建优化",
     ["lto = \"fat\"  →  链接时优化（跨 crate 内联）",
      "codegen-units = 1  →  更多优化机会",
      "strip = true  →  去掉调试符号，减小体积",
      "jemalloc 替换默认分配器：高并发下更快"],
     450),
]

SLIDES[15] = [
    ("CLI 工具：Rust 的天然优势",
     ["单一二进制，无需安装运行时，启动速度微秒级",
      "知名 Rust CLI：ripgrep、fd、bat、exa、tokei",
      "比 Node.js 脚本快 10-100 倍，内存占用极低",
      "clap crate：声明式定义命令行接口"],
     500),
    ("WebAssembly：Rust 跑在浏览器里",
     ["rustup target add wasm32-unknown-unknown",
      "cargo install wasm-pack  →  WASM 打包工具",
      "#[wasm_bindgen] pub fn fibonacci(n: u32) -> u32",
      "wasm-pack build --target web  →  生成 pkg/ 目录"],
     450),
    ("在 Next.js 里使用 WASM",
     ["import init, { fibonacci } from '@/wasm/pkg/my_wasm'",
      "useEffect(() => { init().then(() => setLoaded(true)) })",
      "const result = fibonacci(40)  →  调用 Rust 函数",
      "动态 import WASM，不阻塞主线程"],
     450),
    ("WASM 适合什么场景",
     ["图像处理（像素操作比 JS 快 10-50x）",
      "加密算法（AES / SHA 等密集计算）",
      "数据压缩、物理引擎、音视频编解码",
      "不适合：DOM 操作（还是用 JS）、网络请求"],
     400),
]

SLIDES[16] = [
    ("为什么用 Rust 做 AI 后端",
     ["AI 应用瓶颈在网络 I/O，正是 Rust 异步的甜区",
      "Tokio 同时处理数千个 LLM 请求，内存极低",
      "Stream trait 天然适合 SSE 流式响应",
      "向量计算 SIMD 加速，比 Python 快 10x+"],
     500),
    ("调用 LLM API",
     ["async-openai crate：OpenAI 官方 Rust 客户端",
      "Client::new() 自动读取 OPENAI_API_KEY 环境变量",
      "client.chat().create_stream(request).await?",
      "SSE 流式传输：Sse::new(stream).keep_alive(...)"],
     500),
    ("RAG 管道",
     ["pgvector：PostgreSQL 向量扩展",
      "1. 文档向量化：text-embedding-3-small → vector(1536)",
      "2. 存储：INSERT INTO documents (content, embedding)",
      "3. 检索：ORDER BY embedding <=> $1 余弦距离搜索"],
     500),
    ("AI Agent：Function Calling",
     ["定义工具：JSON 格式描述函数名、参数、用途",
      "发请求 → LLM 返回工具调用指令",
      "本地执行工具函数，把结果返回给 LLM",
      "循环直到 finish_reason = \"stop\""],
     500),
    ("课程完结",
     ["模块一：Rust 核心基础（所有权、类型、数据建模）",
      "模块二：Rust 进阶（错误处理、泛型、并发异步）",
      "模块三：全栈工程（Axum、SQLx、Next.js 集成）",
      "模块四：生产实践（DevOps、性能、CLI、AI）"],
     400),
]


def load_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def get_text_width(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0]


def render_slide(ch_num, slide_idx, total_slides, title, bullets,
                 progress_pct, ch_label, ch_title, module_label,
                 bullet_count=None):
    """
    渲染幻灯片。
    bullet_count: 显示前 N 条要点（None=全部，0=只显示标题）
    """
    content_h = H - WAVE_H   # 内容区高度（留出波形区）
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # ── 网格（仅内容区） ──────────────────────────────────────────────────
    step = 80
    for x in range(0, W, step):
        draw.line([(x, 0), (x, content_h)], fill=GRID_C, width=1)
    for y in range(0, content_h, step):
        draw.line([(0, y), (W, y)], fill=GRID_C, width=1)

    # ── 顶部装饰条 ────────────────────────────────────────────────────────
    draw.rectangle([0, 0, W, 4], fill=ACCENT)

    # 波形区已去除，内容区占满全屏

    # ── 字体 ──────────────────────────────────────────────────────────────
    f_mono_sm  = load_font(MONO_FONT, 22)
    f_mono_md  = load_font(MONO_FONT, 28)
    f_cn_title = load_font(CN_FONT,   64)
    f_cn_body  = load_font(CN_FONT,   34)
    f_cn_sm    = load_font(CN_FONT,   24)

    # ── 顶部信息栏 ────────────────────────────────────────────────────────
    draw.text((36, 22), module_label, font=f_mono_sm, fill=DIM)
    draw.text((36, 50), ch_label,     font=f_mono_md, fill=ACCENT)
    draw.text((180, 54), ch_title,    font=f_cn_sm,   fill=GRAY)

    # 幻灯片编号（右上角）
    slide_txt = f"{slide_idx + 1} / {total_slides}"
    sw = get_text_width(draw, slide_txt, f_mono_sm)
    draw.text((W - sw - 36, 30), slide_txt, font=f_mono_sm, fill=DIM)

    # ── 分隔线 ────────────────────────────────────────────────────────────
    draw.line([(20, 100), (W - 20, 100)], fill=ACCENT2, width=1)

    # ── 标题 ──────────────────────────────────────────────────────────────
    title_y = 130
    draw.text((50, title_y), title, font=f_cn_title, fill=WHITE)
    tw = get_text_width(draw, title, f_cn_title)
    draw.rectangle([50, title_y + 78, min(50 + tw, W - 50), title_y + 82], fill=ACCENT)

    # ── 要点列表 ──────────────────────────────────────────────────────────
    visible_count = bullet_count if bullet_count is not None else len(bullets)
    visible_count = min(visible_count, 4, len(bullets))

    bullet_start_y = title_y + 110
    line_height    = 88

    for i in range(min(4, len(bullets))):
        by = bullet_start_y + i * line_height
        bullet = bullets[i]

        if i < visible_count:
            # 已显示的要点——正常颜色
            # 当前刚显示的要点（最后一条）用亮橙色序号
            is_current = (i == visible_count - 1) and (bullet_count is not None)
            num_color = ACCENT if is_current else ACCENT2
            text_color = WHITE

            # 序号圆圈
            cx, cy = 68, by + 22
            draw.ellipse([cx-18, cy-18, cx+18, cy+18], fill=num_color)
            num_txt = str(i + 1)
            nw = get_text_width(draw, num_txt, f_mono_sm)
            draw.text((cx - nw//2 - 1, cy - 12), num_txt, font=f_mono_sm, fill=BG)

            # 要点文字
            draw.text((100, by), bullet, font=f_cn_body, fill=text_color)
        else:
            # 还未显示的要点——非常暗淡的占位线
            draw.line([(100, by + 20), (400, by + 22)], fill=DIM, width=2)

    # ── 进度条（波形区上方） ──────────────────────────────────────────────
    bar_y = content_h - 6
    draw.rectangle([0, bar_y, W, content_h], fill=BG2)
    bar_w = int(W * progress_pct)
    if bar_w > 0:
        draw.rectangle([0, bar_y, bar_w, content_h], fill=ACCENT)

    # ── 品牌 ──────────────────────────────────────────────────────────────
    brand = "RustForge · rustforge.dev"
    bw = get_text_width(draw, brand, f_mono_sm)
    draw.text((W - bw - 20, content_h + 12), brand, font=f_mono_sm, fill=DIM)

    return img


def get_duration(audio_path):
    r = subprocess.run(
        [FFPROBE, "-v", "quiet", "-show_entries", "format=duration",
         "-of", "csv=p=0", audio_path],
        capture_output=True, text=True
    )
    return float(r.stdout.strip())


def make_subtitle(ch_num, stages, sub_path):
    """生成字幕（按幻灯片段落）"""
    slug, ch_label, ch_title, _ = CHAPTERS[ch_num]

    def fmt_srt(s):
        h, r = divmod(int(s), 3600)
        m, sec = divmod(r, 60)
        ms = int((s - int(s)) * 1000)
        return f"{h:02d}:{m:02d}:{sec:02d},{ms:03d}"

    cues = []
    t = 0.0
    last_title = None
    cue_idx = 1
    for (slide_idx, bullet_count, dur) in stages:
        if slide_idx < len(SLIDES.get(ch_num, [])):
            slide_title = SLIDES[ch_num][slide_idx][0]
        else:
            slide_title = ch_title
        if slide_title != last_title:
            cues.append(str(cue_idx))
            cues.append(f"{fmt_srt(t)} --> {fmt_srt(t + dur)}")
            cues.append(slide_title)
            cues.append("")
            last_title = slide_title
            cue_idx += 1
        t += dur

    with open(sub_path, "w", encoding="utf-8") as f:
        f.write("\n".join(cues))
    print(f"  字幕: {sub_path}")


def generate_video(ch_num):
    if ch_num not in CHAPTERS:
        print(f"章节 {ch_num} 不存在")
        return False

    slides_def = SLIDES.get(ch_num)
    if not slides_def:
        print(f"章节 {ch_num} 的幻灯片内容未定义，跳过")
        return False

    slug, ch_label, ch_title, module_label = CHAPTERS[ch_num]
    audio_path = os.path.join(AUDIO_DIR, f"ch{ch_num:02d}.mp3")
    video_path = os.path.join(VIDEO_DIR, f"ch{ch_num:02d}-{slug}.mp4")
    sub_path   = os.path.join(SUB_DIR,   f"ch{ch_num:02d}-{slug}.srt")

    if not os.path.exists(audio_path):
        print(f"音频不存在: {audio_path}")
        return False

    print(f"\n=== 生成第 {ch_num} 章: {ch_title} ===")
    total_duration = get_duration(audio_path)

    # ── 计算所有"阶段"（每个阶段 = 某幻灯片显示到第N条要点） ────────────────
    # 策略：先估算每张幻灯片总时长，再细分为逐条揭示阶段
    total_chars = sum(s[2] for s in slides_def)
    slide_durations = []
    remaining = total_duration
    for i, (title, bullets, chars) in enumerate(slides_def):
        if i == len(slides_def) - 1:
            slide_durations.append(max(remaining, 15.0))
        else:
            d = total_duration * chars / total_chars
            d = max(d, 20.0)
            slide_durations.append(d)
            remaining -= d

    # 生成 stages: (slide_idx, bullet_count, duration)
    TITLE_RATIO = 0.12   # 12% 的时间只显示标题
    MIN_STAGE   = 4.0    # 每个阶段最短 4 秒
    stages = []
    for slide_idx, (title, bullets, _) in enumerate(slides_def):
        slide_dur = slide_durations[slide_idx]
        n = min(4, len(bullets))

        # 阶段0：只显示标题
        t0 = max(MIN_STAGE, slide_dur * TITLE_RATIO)
        stages.append((slide_idx, 0, t0))

        # 阶段1..n：逐条揭示要点
        leftover = slide_dur - t0
        per_bullet = leftover / n if n > 0 else leftover
        per_bullet = max(per_bullet, MIN_STAGE)
        for b in range(1, n + 1):
            if b < n:
                stages.append((slide_idx, b, per_bullet))
            else:
                # 最后一个阶段用剩余时间
                used = t0 + per_bullet * (n - 1)
                last_dur = max(slide_dur - used, MIN_STAGE)
                stages.append((slide_idx, b, last_dur))

    total_stage_dur = sum(s[2] for s in stages)
    print(f"  音频: {total_duration/60:.1f} 分钟  |  共 {len(stages)} 个阶段")

    # ── 渲染每个阶段的 PNG ────────────────────────────────────────────────
    frames_dir = os.path.join(WORK_DIR, f"ch{ch_num:02d}_stages")
    os.makedirs(frames_dir, exist_ok=True)

    concat_file = os.path.join(WORK_DIR, f"ch{ch_num:02d}_concat.txt")
    elapsed = 0.0
    with open(concat_file, "w") as cf:
        for s_idx, (slide_idx, bullet_count, dur) in enumerate(stages):
            title, bullets, _ = slides_def[slide_idx]
            progress = elapsed / total_stage_dur

            if s_idx % 10 == 0:
                print(f"  渲染阶段 {s_idx+1}/{len(stages)}...")

            img = render_slide(
                ch_num, slide_idx, len(slides_def),
                title, bullets, progress,
                ch_label, ch_title, module_label,
                bullet_count=bullet_count
            )
            img_path = os.path.join(frames_dir, f"stage_{s_idx:04d}.png")
            img.save(img_path, "PNG")

            cf.write(f"file '{img_path}'\n")
            cf.write(f"duration {dur:.3f}\n")
            elapsed += dur

        # 最后一帧重复（concat demuxer 要求）
        last_img = os.path.join(frames_dir, f"stage_{len(stages)-1:04d}.png")
        cf.write(f"file '{last_img}'\n")

    # ── ffmpeg 合成幻灯片视频（带淡入淡出过渡） ─────────────────────────────
    # 方案：concat demuxer → 生成幻灯片序列视频
    # ── 生成字幕文件 ─────────────────────────────────────────────────────
    make_subtitle(ch_num, stages, sub_path)

    # ── ffmpeg 合成：幻灯片 + 音频 + 烧录字幕 ────────────────────────────
    print("  ffmpeg 合成视频 + 音频 + 字幕...")
    srt_path = sub_path  # VTT 路径（make_subtitle 生成的）

    escaped = srt_path.replace(":", "\\:")
    sub_filter = f"subtitles={escaped}"

    r = subprocess.run([
        FFMPEG, "-y",
        "-f", "concat", "-safe", "0", "-i", concat_file,
        "-i", audio_path,
        "-vf", f"fps={FPS},scale={W}:{H},{sub_filter}",
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-shortest",
        video_path
    ], capture_output=True, text=True)
    if r.returncode != 0:
        print(f"  ffmpeg 错误:\n{r.stderr[-1000:]}")
        return False

    # ── 清理临时文件 ──────────────────────────────────────────────────────
    import shutil
    shutil.rmtree(frames_dir, ignore_errors=True)
    if os.path.exists(concat_file):
        os.unlink(concat_file)

    size_mb = os.path.getsize(video_path) / 1024 / 1024
    print(f"  完成: {video_path} ({size_mb:.1f} MB)")
    return True


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="RustForge 视频生成 v3")
    parser.add_argument("chapter", nargs="?", default="1")
    args = parser.parse_args()

    if args.chapter == "all":
        for n in sorted(CHAPTERS.keys()):
            generate_video(n)
    else:
        try:
            generate_video(int(args.chapter))
        except ValueError:
            print(f"无效章节: {args.chapter}")
            sys.exit(1)
