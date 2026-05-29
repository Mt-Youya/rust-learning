#!/usr/bin/env python3
"""
RustForge 课程音频生成脚本
使用 edge-tts 生成所有章节讲解音频

用法:
  pip install edge-tts
  python gen_audio.py [章节号]   # 生成指定章节，如 python gen_audio.py 1
  python gen_audio.py all        # 生成全部章节

输出: ./audio/ch01.mp3, ch02.mp3 ...
"""

import subprocess
import os
import sys

VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "-5%"

SCRIPTS = {}

SCRIPTS[1] = """
大家好，欢迎来到 RustForge。我是你的讲师，这套课程专门为有两到五年 JavaScript 和 React 经验的前端工程师设计，带你从前端视角出发，系统地学习 Rust，一路走到全栈开发、运维部署，以及 AI 应用集成。

这一章是第一章：入门。内容分四个部分——安装 Rust 工具链并理解 rustup，掌握 Cargo 这个核心工具，理解 Rust 程序的基本结构，以及完成一个实战练习。

我们先从动机聊起：你为什么要学 Rust？

你可能已经是一个很有经验的 JavaScript 或 TypeScript 工程师。你了解异步编程，熟悉 React 的生态，能用 Node.js 写后端服务。这些都是真正有价值的技能，不会因为学 Rust 而白费。

但你可能遇到过这些让你头疼的场景。

第一个场景：Node 服务内存占用越跑越高，找不到泄漏的原因，最后只能靠定时重启服务器来解决。第二个场景：高并发接口在压测时抖动严重，因为 JavaScript 是单线程的，CPU 密集型操作会阻塞整个事件循环。第三个场景：你想把一个常用操作做成命令行工具，用 Node.js 打包，结果发现 Hello World 都要带着几十 MB 的 runtime，分发给同事很麻烦。第四个场景：想把一段计算逻辑部署到 Cloudflare Workers 这样的边缘节点，但 Node.js 的冷启动时间和内存限制让你望而却步。

Rust 是所有这些问题的答案。

打个比方：TypeScript 把 JavaScript 的类型错误从运行时提前到了编译期——你不用运行代码就能知道类型不对。Rust 更进一步，它把内存错误、数据竞争、空指针这些问题，也全部提前到了编译期。而且这一切是零运行时开销的。

什么叫零运行时开销？就是说 Rust 没有垃圾回收器，没有虚拟机，没有 JIT 编译，直接就是跑在 CPU 上的机器码。和 C 一样快，但是编译器帮你保证内存安全。

好，我们来安装 Rust。

第一步，安装 rustup。在 macOS 或 Linux 上，打开终端运行这条命令：curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs，然后管道给 sh 执行。

这个命令安装的是 rustup——Rust 的版本管理器。把它理解成 Rust 世界里的 nvm。

安装过程中会问你选择安装方式，默认的就很好，直接回车。安装完成后，需要重新打开终端或者执行 source ~/.cargo/env 让环境变量生效。

安装完成后，rustup 帮你装好了这三样东西：rustc 是 Rust 编译器；cargo 是包管理和构建工具；rust-std 是标准库。

运行 rustc --version 验证，你会看到类似 rustc 1.78.0 的输出。

在 Windows 上，去 rustup.rs 下载安装程序，过程是一样的，不需要额外安装 MinGW 或者 MSVC，rustup 会自动处理。

rustup 有几个常用命令值得记一下：

rustup update 更新到最新稳定版，这和 nvm 的 nvm install --lts 类似，随时可以运行。

rustup toolchain list 列出所有已安装的工具链版本。Rust 有三个渠道：stable 稳定版，每六周发布一次；beta 测试版；nightly 每日构建，包含最新的实验特性。大部分时候用 stable 就够了。

rustup component add clippy 安装额外的工具组件。Clippy 是 Rust 的代码检查工具，比编译器更严格，会提示很多最佳实践。rustup component add rustfmt 安装代码格式化工具。这两个我建议安装，我们后面会用到。

rustup target add wasm32-unknown-unknown 添加 WebAssembly 编译目标——我们在第十五章会用到这个来把 Rust 代码编译成在浏览器里运行的 WASM 模块。

rustup doc 打开本地文档，即使没有网络也能查阅 Rust 标准库文档。这比上网查要快得多。

好，现在我们来深入了解 Cargo。

Cargo 是 Rust 的构建系统和包管理器，它同时做了 npm、webpack、babel、jest、Makefile 这些工具的工作——管理依赖、构建项目、运行测试、生成文档、发布包。

用 Cargo 创建项目：cargo new hello-rust，然后 cd hello-rust。

Cargo 会生成这样的目录结构：根目录有 Cargo.toml 和 .gitignore，src 文件夹里有 main.rs。注意 Cargo new 默认就初始化了 git 仓库，如果你不想要可以加 --vcs none 参数。

Cargo.toml 就是 Rust 版的 package.json，但格式是 TOML 而不是 JSON。TOML 是一种比 JSON 更适合配置文件的格式，支持注释，不用到处写引号。

打开 Cargo.toml，你会看到：

[package] 段，里面有 name 字段是项目名，version 是版本，edition 是 Rust 版本。edition 很重要，它指定使用哪个语言规范。目前常用的是 2021，最新的是 2024。Rust 的 edition 机制让语言可以在不破坏向后兼容性的情况下引入变化——不同 edition 的 crate 可以在同一个项目里共存。这和 TypeScript 的严格模式有点像，但更系统。

[dependencies] 段是你的依赖，现在是空的。依赖格式是 包名 = "版本号"，比如 rand = "0.8"，版本号支持 semver 语义化版本规范，和 npm 一样。

来对比一下 npm 和 Cargo 命令：

npm install 对应什么？Cargo 不需要单独的 install 命令。你在 Cargo.toml 里写上依赖，然后运行任何 cargo 命令（build/run/test），Cargo 会自动下载缺失的依赖，并把它们缓存在 ~/.cargo/registry 目录里。这类似于 npm install 是隐式的。如果你想显式添加，cargo add serde 会自动把 serde 的最新版本写入 Cargo.toml，类似 npm install serde。

npm run build 对应 cargo build，开发时用，编译带调试信息，速度快但文件大、运行慢；生产时用 cargo build --release，会花更多时间优化，生成的二进制文件体积小、运行快，速度差距可以是 10 倍以上。

npm test 对应 cargo test，运行所有测试，Rust 内置测试框架，不需要 Jest 这类第三方工具。

npm run dev 通常对应 cargo run，编译并立即运行。cargo run -- 参数 可以传参数给程序。cargo watch -x run 可以实现类似热重载的效果，不过 cargo-watch 需要单独安装：cargo install cargo-watch。

npm publish 对应 cargo publish，把你的 crate 发布到 crates.io，也就是 Rust 的包注册中心。

npx some-tool 对应 cargo run --bin some-tool，或者全局安装一个工具然后直接用：cargo install some-tool，然后在终端直接运行 some-tool。很多 Rust 开发工具都是这样分发的，比如 sqlx-cli、wasm-pack、cargo-generate 等等。

让我们动手。运行 cargo run，Cargo 先编译，再运行，你看到输出：Hello, world!

注意这里有个 Compiling 的步骤，每次你修改代码，Cargo 都会重新编译修改的部分。得益于增量编译，大部分修改只需要几秒钟就能重新编译运行。

Cargo.lock 文件会自动生成，这就是 package-lock.json 的对应物，锁定所有依赖的精确版本。规则和 npm 一样：应用程序（binary crate）应该提交 Cargo.lock；库（library crate）不应该提交。

target 文件夹里放的是编译产物。target/debug 是调试构建的产物，target/release 是发布构建。这个文件夹可能有好几 GB 大，是 .gitignore 的标准内容，Cargo new 会自动添加。cargo clean 清理这个目录。

注意 Rust 的编译产物和 node_modules 不同——不需要类似 npm install 的步骤。只要有 Cargo.lock，任何时候运行 cargo build，Cargo 会自动下载和编译所有依赖。

现在我们来理解 Rust 程序的结构层次。

Rust 有三个层次的概念：Package、Crate 和 Module。

Package 是最顶层，对应一个 Cargo.toml 文件管理的项目，可以包含一个或多个 crate。

Crate 是编译单元。分两种：binary crate 是可执行程序，有 main 函数，src/main.rs 是它的根文件；library crate 是库，没有 main 函数，src/lib.rs 是它的根文件。一个 Package 可以同时有这两种 crate，共享代码，互相引用。

Module 是代码组织单元，用 mod 关键字定义，类似 ES Module，但有明确的可见性控制。Rust 默认一切都是私有的，用 pub 关键字声明公开。

这个体系对应 JavaScript 的理解：package 就是一个 npm 包，crate 就是入口文件，module 就是 ES module。

打开 src/main.rs，里面是：

屏幕上可以看到 main 函数，它是程序的入口点。里面调用了 println! 这个宏来打印内容。注意 println! 后面有个感叹号，这是宏的标志，表示它在编译期展开，可以接受可变数量的参数，提供了比普通函数更灵活的代码生成能力。

注意两件事。第一，println! 后面的感叹号——这代表它是一个宏，不是普通函数。Rust 的宏在编译期展开，提供了比函数更灵活的代码生成能力。我们后面会遇到很多宏，比如 vec!、format!、assert_eq! 等等。宏和函数的最大区别是宏可以接受可变数量的参数，而且可以在编译期做更复杂的代码变换。第二，fn main() 是程序入口，不同于 Node.js 脚本从顶层代码开始执行，Rust 程序必须有一个 main 函数作为入口点。

现在我们来看变量。

在 Rust 里，let x = 5 创建的变量默认是不可变的（immutable），你不能再给 x 赋值。如果你尝试写 x = 6，编译器会报错：cannot assign twice to immutable variable。

如果要可变，必须显式写 let mut x = 5，多了一个 mut 关键字。

这和 JavaScript 的规则完全反过来了。JavaScript 用 let 创建可变变量，用 const 创建不可变绑定。Rust 用 let 创建不可变绑定，用 let mut 创建可变变量。Rust 的默认是安全的那个——不可变。

这个设计背后有深刻原因：大多数 bug 来自意外的状态修改。Rust 把"我打算修改这个变量"变成显式声明的行为，让代码意图更清晰，也让编译器能做更多静态分析。当你把一个变量传给别的函数，如果它是不可变的，你就知道那个函数不可能修改它，这极大地简化了代码推理。

Rust 还有一个特性叫变量遮蔽（shadowing）。和 JavaScript 的作用域遮蔽不一样，Rust 的遮蔽是用同名的 let 重新绑定一个变量，甚至可以改变它的类型。

比如：屏幕上展示了这个连续遮蔽的例子，用同名变量依次绑定不同的值。

现在来看基本数据类型，这里我们快速过一遍，第二章会深入讲。

Rust 是强类型语言，每个变量在编译时都必须有确定的类型，但编译器经常能自动推断，不需要你显式标注。

整数：i32 是最常用的有符号 32 位整数，u64 是无符号 64 位整数，usize 是机器字长大小的无符号整数，专门用于数组索引。数字字面量可以写下划线分隔：1_000_000 比 1000000 更易读。

浮点数：f64 是 64 位双精度浮点，是默认值。f32 是 32 位单精度。

布尔值：bool，值是 true 或 false。

字符：char，Unicode 标量值，用单引号，比如 'A'、'中'、'🦀'。注意是 Unicode 字符，不是 ASCII 字节。

字符串先给你一个初步印象：&str 是字符串切片，像引用一块只读的字符串数据；String 是堆上分配的可增长字符串。函数参数尽量用 &str，需要存储或修改时用 String。第二章会详细展开。

来看函数。

fn 关键字定义函数，参数类型必须显式标注，返回类型用箭头标注。屏幕上可以看到函数签名的格式。

这个函数接受两个整数参数，返回它们的和。注意最后一行没有分号，这就是 Rust 的表达式返回值机制。

如果你写了分号：a + b; 就变成了语句，没有返回值，函数隐式返回 unit 类型，也就是 ()，空元组。这时候如果函数签名写了返回 i32，编译器会报错说类型不匹配。这是初学者经常碰到的 bug。

控制流：if 不需要括号，直接写条件。let x = 5; if x > 3 （见屏幕代码）。

Rust 的 if 是表达式，可以用在赋值里：let result = if x > 0 （见屏幕代码）。注意两个分支必须是相同类型，不然编译器报错。

loop 是无限循环，可以用 break 携带值退出：let result = loop 在屏幕上展示的代码里。

while 条件循环，while x < 10 在屏幕上展示的代码里。

for 循环最常用，配合范围表达式或者迭代器：for i in 1..=5 在屏幕上展示的代码里。1..=5 是闭区间，1..5 是左闭右开。

现在来做实战练习，把今天学的都用上。

我们来写一个命令行温度转换器，能把摄氏度转换成华氏度和开尔文。这是一个典型的 CLI 工具。

运行 cargo new temp-converter，cd temp-converter，打开 src/main.rs。

先写两个转换函数：

这是摄氏转华氏的实现，公式是乘以 9 再除以 5 最后加 32，这就是经典的物理换算公式。

这是摄氏转开尔文的实现，只需要加上绝对零度的偏移量 273.15 即可。

注意数字字面量写 9.0 而不是 9，因为参数是 f64，Rust 不会自动把整数 9 当作 f64 使用，混用整数和浮点会编译报错。

然后 main 函数：先用 std::env::args 读取命令行参数，用 nth(1) 获取第一个参数，用 .expect() 处理没有参数的情况，用 .parse::<f64>() 把字符串解析成 f64，用 .expect() 处理解析失败的情况。

然后调用两个转换函数，用 println! 格式化输出三行结果。

运行 cargo run -- 100，两个横杠分隔 Cargo 参数和程序参数，你会看到：

摄氏 100.0 度 = 华氏 212.0 度 = 开尔文 373.15

运行 cargo run -- 0，你会看到冰点：摄氏 0.0 度 = 华氏 32.0 度 = 开尔文 273.15。

运行 cargo run -- -40，负 40 度摄氏和华氏的有趣巧合：都是 -40。

如果你不带参数直接 cargo run，会看到 expect 里的错误信息然后 panic 退出。这不优雅，第五章错误处理那一章我们会用 Result 类型做得更好。

现在让我们用 cargo build --release 构建发布版，然后 ls -lh target/release/temp-converter 查看文件大小。你会看到一个大约 300KB 到 1MB 的单一二进制文件，没有任何依赖。可以直接复制到任何机器上运行。这就是 Rust CLI 工具的魅力——零依赖部署。

让我们也感受一下 Rust 文档系统。运行 cargo doc --open，Cargo 会为你的项目和所有依赖生成 HTML 文档，然后在浏览器里打开。

在文档里你可以看到 f64 类型的所有方法：sqrt 开平方根，abs 绝对值，powi 整数幂，powf 浮点幂，floor 向下取整，ceil 向上取整，round 四舍五入，clamp 限制在范围内，以及大量数学函数。这是 Rust 的完整 API 文档，比上网搜要快，而且完全离线可用。

最后来看一下 Cargo 工作区（Workspace）的概念。我们这个课程的前端项目用的就是 monorepo 结构，Cargo 原生支持 workspace。

在根目录的 Cargo.toml 里写 [workspace] 段，members 列出所有子项目的路径。各个子项目有自己的 Cargo.toml，但共享同一个 Cargo.lock 和同一个 target 目录。这类似 npm workspace，但 Cargo 的 workspace 更原生，不需要 --workspace 标志就能从根目录构建所有项目。

cargo build --workspace 构建所有成员，cargo test --workspace 测试所有成员，cargo run --bin server 在 workspace 里运行特定的 binary。

好，第一章讲完了，我们做一个总结：

rustup 是工具链管理器，管理 Rust 版本、组件和目标平台，对应 nvm。cargo 是包管理加构建工具，对应 npm 加 webpack。Cargo.toml 是项目配置，对应 package.json；Cargo.lock 是依赖锁文件，对应 package-lock.json；target 目录是构建产物，对应 node_modules。变量默认不可变，加 mut 才可变，这和 JavaScript 正好相反。fn 定义函数，最后一个表达式是返回值，不需要 return 和分号。Rust 有丰富的数字类型，选择合适的类型是明确表达意图的方式。字符串有 &str 和 String 两种形式，参数用 &str，存储用 String。for 循环配合范围表达式是遍历的惯用方式。Rust CLI 工具编译成单一二进制文件，零依赖部署。

下一章，我们深入 Rust 的类型系统，包括所有整数类型、浮点数、字符串的完整图谱，以及 match 模式匹配这个 Rust 里最优雅的控制流结构。我们下章见。
"""

SCRIPTS[2] = """
欢迎回来，这里是 RustForge 第二章：变量、类型与函数的深入讲解。

上一章我们写了第一个 Rust 程序，了解了 Cargo 工具链，实现了温度转换 CLI。这一章我们要深入 Rust 的类型系统和函数设计。

先说一个重要的认知：Rust 的类型系统和 TypeScript 有一个根本区别。TypeScript 的类型在编译后消失，运行时还是 JavaScript。而 Rust 的类型是语言的核心，类型决定内存布局、决定可以调用哪些方法、决定数据如何传递。类型不只是文档，是程序行为的约束。

好，我们从整数类型开始，这是最基础但也最重要的。

Rust 的整数类型有十种：i8、i16、i32、i64、i128，分别是 8 到 128 位的有符号整数；u8、u16、u32、u64、u128，分别是无符号整数。另外还有两个特殊的：isize 和 usize，大小等于当前平台的机器字长，64 位系统就是 64 位。

JavaScript 里只有一种数字类型，就是 64 位浮点数。Rust 里你要选择合适的整数类型，这看起来麻烦，但实际上有清晰的规则。

什么时候用哪种类型？

i32 是最常用的，当你不确定用什么时，就用 i32。它是 CPU 最自然的运算单位，在大多数平台上运算速度最快。

u8 专门用于字节数据，比如文件内容、网络数据包、RGB 颜色值。值范围 0 到 255，正好是一个字节能表示的范围。

usize 专门用于数组索引和集合长度，因为这些值必须和平台的内存地址大小一致。你写 v.len() 返回的就是 usize，v[i] 里的 i 也必须是 usize。

i64 用于需要大数值的场景，比如时间戳（Unix 时间戳用微秒计的话可能超出 i32 的范围）、文件大小。

整数字面量的写法：十进制普通写，比如 1000；用下划线分隔大数字，1_000_000 等于一百万，比 1000000 更易读；0x 前缀写十六进制，0xFF 是 255；0o 写八进制，0o77 是 63；0b 写二进制，0b1010 是 10；u8 可以在数字后加类型标注，比如 255u8，告诉编译器这个字面量的类型。

整数溢出是一个重要话题。JavaScript 里整数溢出不会崩溃，只是精度丢失，比如 Number.MAX_SAFE_INTEGER + 1 等于 Number.MAX_SAFE_INTEGER，悄悄出错。Rust 不会让这种事情发生。

在 debug 构建（cargo build 不加 release）里，整数溢出会 panic，程序崩溃并打印错误。这能帮你在开发阶段发现 bug。

在 release 构建（cargo build --release）里，整数溢出会回绕，比如 i8 的 127 加 1 等于 -128。这是有意为之的行为，性能最高。

如果你明确需要溢出回绕行为，用 wrapping_add、wrapping_sub 等方法；如果需要检测溢出，用 checked_add，返回 Option，溢出时返回 None；如果需要饱和加法（溢出时返回最大值），用 saturating_add。

这些方法比 JavaScript 的隐式处理更明确，让你的意图清晰可见。

接下来是浮点数。Rust 有 f32 和 f64 两种，f64 是 64 位双精度，f32 是 32 位单精度。默认推荐用 f64，精度更高，现代 CPU 处理 f64 和 f32 一样快。

浮点数运算的陷阱和 JavaScript 一样，因为都是 IEEE 754 标准。0.1 + 0.2 不等于 0.3，这不是 Rust 的 bug，是浮点数学的本质。比较浮点数不要用 ==，要用差值小于 epsilon 的方式。

Rust 提供了 f64::EPSILON 常量，这是机器精度。通常判断两个浮点数相等的方式是：(a - b).abs() < f64::EPSILON。

布尔类型 bool，值是 true 或 false，大小 1 字节。Rust 和 JavaScript 不同的是，Rust 没有"真值"（truthy）和"假值"（falsy）的概念。if 条件必须是 bool 类型，不能是整数 0 或者空字符串，你必须显式比较：if count != 0 而不是 if count。

字符类型 char 是 Unicode 标量值，占 4 字节。这和 JavaScript 字符串里的"字符"不一样。JavaScript 用 UTF-16 编码，emoji 和很多中文字符需要两个码元。Rust 的 char 保证是完整的 Unicode 字符，'😀' 是一个 char，不是两个。

好，现在我们来系统讲字符串。这是前端工程师转 Rust 最容易卡住的地方，我要花比较多时间讲清楚。

Rust 有两种字符串类型，&str 和 String。这两种类型的根本区别在于内存所有权，这和下一章要讲的所有权系统紧密相关，我们先从直觉上理解。

&str 是字符串切片，是一个指向某段 UTF-8 字节数据的引用，加上数据的长度。它本身不拥有数据，只是"借用"地查看某段数据。字符串字面量 "hello world" 的类型就是 &str，数据存在程序的只读内存段，整个程序运行期间都有效。

String 是堆分配的可增长字符串。它拥有数据，负责在合适的时候释放内存。你可以向 String 追加内容，修改它，移动它，当它离开作用域时内存自动释放。

用 JavaScript 类比：String 就像一个 Array.from('hello') 得到的可变字符数组，&str 就像一个 string.substring() 得到的只读视图。当然这个类比不完全准确，但方向对的。

如何创建 String？

String::from("hello") 或者 "hello".to_string() 都可以，从字符串字面量创建 String。

let mut s = String::new() 创建空 String，然后用 s.push_str("hello") 追加字符串，s.push('!') 追加单个字符。

format!("Hello, {}!", name) 格式化创建，类似 JavaScript 的模板字符串。这是最常用的构建 String 的方式。

如何判断用 &str 还是 String？

函数参数：如果函数只需要读取字符串，用 &str，这更灵活，既能接受字符串字面量，也能接受 String 的引用。如果函数需要存储字符串到结构体或者返回拥有所有权的字符串，用 String。

在结构体里存储字符串：必须用 String，不能用 &str，因为 &str 是借用，需要明确生命周期，初学阶段避免这种复杂性。

字符串的常用操作：

len() 返回字节长度（不是字符数），对于纯 ASCII 字符串等同于字符数，但包含中文时会不同。

chars() 返回 Unicode 字符的迭代器。要数字符数用 s.chars().count()，要取第 n 个字符用 s.chars().nth(n)。

contains("world") 检查是否包含子串，starts_with、ends_with 检查前缀后缀。

replace("old", "new") 替换所有匹配，返回新 String。

split_whitespace() 按空白分割，返回迭代器。

trim() 去掉首尾空白，trim_start 和 trim_end 分别去掉开头和结尾。

to_uppercase()、to_lowercase() 大小写转换。

parse::<i32>() 把字符串解析成其他类型，返回 Result，需要处理解析失败的情况。

字符串索引的注意点：Rust 不允许 s[0] 这样的字符索引，因为字符串是 UTF-8 编码，一个字符可能占 1 到 4 个字节。如果你写 &s[0..4]，这是字节切片，如果不巧切到了多字节字符的中间，会 panic。安全的方式是用 chars() 迭代器或者 split_at 方法，确保在有效的字符边界上切。

好，现在讲元组。

元组是固定长度的、可以包含不同类型的集合。这是 Rust 里的轻量级数据结构，不需要定义结构体名字就能把多个值组合在一起。

let point = (3.0_f64, 4.0_f64); 这是一个包含两个 f64 的元组，代表二维坐标。

访问元组元素用点语法加索引：point.0 是 3.0，point.1 是 4.0。

解构赋值：let (x, y) = point; 之后 x 是 3.0，y 是 4.0。解构是 Rust 里非常常用的模式，函数返回多个值时经常用元组。

函数返回多个值的例子：fn min_max(v: &[i32]) -> (i32, i32) 在屏幕上展示的代码里。调用时：let (min, max) = min_max(&v);

类型标注：let point: (f64, f64) = (3.0, 4.0)，或者让编译器推断。

unit 类型 () 是空元组，是没有数据的类型。函数不显式返回值时返回的就是 ()，类似其他语言的 void，但在 Rust 里它是真实的类型，可以存储在变量里。

接下来是数组和 Vec 的对比。

Rust 的数组是固定长度的同类型集合，存在栈上。定义方式：let a: [i32; 5] = [1, 2, 3, 4, 5]，中括号里先是类型再是长度，用分号分隔。数组的长度是类型的一部分，[i32; 5] 和 [i32; 6] 是完全不同的类型，不能互换。

初始化相同值的数组：let zeros = [0; 100] 创建 100 个 0 的数组。

访问元素：a[0] 是 1。越界访问在运行时 panic（debug 模式）或者是未定义行为（unsafe 代码），但对于安全 Rust 代码，越界会 panic，不会像 C 那样悄悄读到随机内存。

数组的方法：a.len() 返回长度，a.iter() 创建迭代器，a.contains(&3) 检查是否包含，a.sort() 注意这要求数组元素实现了 Ord。

数组适合固定大小的数据，比如哈希值（通常是 [u8; 32]），矩阵行，固定数量的配置项。

Vec 是动态大小的同类型集合，存在堆上，类似 JavaScript 的 Array。

创建：vec![1, 2, 3] 宏创建有初始值的 Vec；Vec::new() 创建空 Vec；Vec::with_capacity(100) 创建预分配了 100 个元素空间的 Vec，避免多次重新分配内存。

添加元素：v.push(4) 在末尾添加；v.insert(1, 10) 在索引 1 处插入 10，后面的元素后移。

删除元素：v.pop() 删除最后一个元素并返回 Option<T>；v.remove(1) 删除索引 1 的元素并返回它，后面的元素前移。

访问元素：v[0] 越界 panic；v.get(0) 返回 Option<&T>，越界返回 None，这是更安全的方式。

检查：v.len() 元素数量，v.is_empty() 是否为空，v.contains(&3) 是否包含。

遍历：for item in &v 不可变遍历；for item in &mut v 可变遍历；for item in v 消耗 Vec，把所有权移入循环。

Vec 排序：v.sort() 原地排序，v.sort_by(|a, b| a.cmp(b)) 自定义比较，v.sort_by_key(|x| x.name) 按字段排序。

好，现在来深入讲函数设计。

我们之前见过简单的函数，这里来讲几个重要的细节。

表达式 vs 语句的区别非常重要，我再强调一次。

Rust 里，表达式有值，语句没有值。大多数东西都是表达式：数字字面量 5 是表达式，值是 5；函数调用是表达式；if-else 是表达式；代码块 {} 是表达式，值是最后一个表达式的值；match 表达式是表达式。

语句是做某件事但不产生值的代码：let 绑定是语句，let x = 5 不返回值；表达式加上分号变成语句，5; 是语句，值丢弃了。

函数的最后一个表达式是返回值。如果你写了分号，就变成语句，函数返回 ()，如果签名要求有返回值会报类型不匹配的错误。

提前返回用 return：当你在函数中间需要提前结束时，用 return value 显式返回。和 JavaScript 一样。

函数参数可以有默认值吗？Rust 原生不支持函数参数默认值，不像 Python 或者 JavaScript 的 function foo(x = 5)。替代方案是用 Option 参数，然后在函数里处理 None 的情况；或者用 builder 模式，为复杂配置创建一个结构体然后实现 Default。

多返回值用元组，我们刚才讲过了。

递归函数 Rust 也支持，语法和其他语言一样：fn factorial(n: u64) -> u64 在屏幕上展示的代码里。

注意 Rust 没有尾递归优化保证，所以深度递归可能导致栈溢出。如果需要深度递归，考虑用迭代加显式栈来替代。

闭包是 Rust 的匿名函数，语法用竖线括住参数，比如 |x| x * 2，对应 JavaScript 的 x => x * 2。闭包可以捕获外部变量。

let threshold = 10;
let is_big = |x| x > threshold; // 捕获了 threshold
println!("{}", is_big(15)); // true

注意 JavaScript 的箭头函数总是捕获外部变量的引用，Rust 的闭包默认也尝试用引用捕获，但在某些情况下需要用 move 关键字把值移入闭包：

let name = String::from("Alice");
let greet = move || println!("你好，{}", name); // name 所有权移入闭包
greet(); // 输出：你好，Alice
// println!("{}", name); // 报错：name 已经移入了闭包

闭包的完整讲解会在第六章泛型和 Trait 那一章，因为闭包和 Fn、FnMut、FnOnce 这些 Trait 密切相关。

好，我们来做本章的综合实战练习：实现一个命令行成绩计算器。

功能：从命令行读取学生名字和多门课的分数，计算平均分，用 match 映射成绩等级，然后格式化输出报告。

首先创建项目：cargo new grade-calc，cd grade-calc。

设计程序结构：需要一个 Student 结构体，先不用，用基础类型就够；需要 score_to_grade 函数把分数映射成字母等级；需要 calculate_average 函数计算平均分；需要 main 函数读取输入并输出报告。

先写 score_to_grade 函数：

这个函数把数值分数映射到字母等级，用 if-else 链实现分段判断。

注意浮点数的范围匹配在 Rust 里有一些限制，对于简单的成绩映射，用 if-else if 链更直接：

这个函数把数值分数映射到字母等级，用 if-else 链实现分段判断。
if score >= 90.0 （见屏幕代码）
else if score >= 80.0 （见屏幕代码）
else if score >= 70.0 （见屏幕代码）
else if score >= 60.0 （见屏幕代码）
else （见屏幕代码）

这里利用了 if-else 是表达式的特性，整个 if-else 链的值就是函数返回值。

calculate_average 函数接受一个浮点数切片，返回其平均值，处理了空切片返回零的边界情况。

实现方式：scores.iter().sum::<f64>() / scores.len() as f64。注意 sum 需要类型标注，因为编译器需要知道求和的目标类型；scores.len() 是 usize，除法前要转成 f64。

main 函数：用 std::env::args() 读取命令行参数，跳过程序名，收集剩余参数，然后依次解析成 f64 数组。

完整代码大概是这样的：

第一部分，引入标准库和定义两个辅助函数。

第二部分，main 函数：

let args: Vec<String> = std::env::args().skip(1).collect(); 跳过第一个参数（程序名），收集剩余参数到 Vec<String>。

如果 args 为空，打印用法然后 return 退出。

let scores: Vec<f64> = args.iter().filter_map(|s| s.parse().ok()).collect(); 尝试把每个字符串解析成 f64，filter_map 会自动过滤掉解析失败的值（ok() 把 Result::Err 变成 None，filter_map 过滤掉 None）。

如果 scores 为空，说明所有输入都不是有效数字，打印错误信息退出。

计算平均分和等级，然后格式化输出。

输出格式：分数列表、平均分、等级，可以加上最高分和最低分。

运行 cargo run -- 95 82 76 88 91，你会看到：

输入分数：95.0, 82.0, 76.0, 88.0, 91.0
平均分：86.4
等级：B
最高分：95.0 / 最低分：76.0

这个练习综合运用了：Vec 收集和处理，迭代器的 filter_map 方法，字符串到浮点数的 parse，if-else 表达式，函数抽象，以及基础的格式化输出。

好，第二章总结：

整数类型选 i32 作为默认，usize 用于索引，u8 用于字节数据；整数溢出在 debug 模式 panic；浮点数用 f64，比较用差值法；字符串有 &str（视图/引用）和 String（所有者）两种形式，函数参数用 &str；元组用于临时组合多个值，解构赋值非常方便；数组是固定长度栈上存储，Vec 是动态长度堆上存储；函数最后一个无分号表达式是返回值；闭包语法是竖线括参数加表达式。

下一章是这个课程最重要的章节：所有权与借用。这是 Rust 独有的核心概念，理解了它，你就理解了 Rust 为什么安全。我们下章见。
"""

SCRIPTS[3] = """
欢迎来到第三章，这一章是整个 Rust 课程最重要的一章：所有权、借用与生命周期。

这也是大多数人学习 Rust 最感到困惑的地方。所以我会花大量时间，用多种角度来帮你建立直觉。

先说结论：所有权系统是 Rust 在没有垃圾回收器的情况下保证内存安全的核心机制。理解了它，你就理解了 Rust 为什么能做到 C 的性能加上 Java 的安全性。

我们先从内存讲起。

程序运行时的内存分两个主要区域：栈（Stack）和堆（Heap）。

栈是后进先出的内存区域，像一叠盘子。大小在编译时就确定的数据放在栈上，比如整数、浮点数、布尔值、固定大小的数组。栈的访问非常快，因为只需要移动栈顶指针。函数调用时，局部变量被压入栈帧；函数返回时，栈帧被弹出，内存自动归还。

堆是动态分配的内存区域，像一个大房间，你可以随时申请任意大小的空间，但你要负责用完后释放。字符串、向量 Vec、以及任何动态大小的数据都放在堆上。

在 JavaScript 和 Java 这类有垃圾回收器的语言里，你不用担心堆内存的释放，GC 会自动扫描哪些内存没有引用了，然后释放。但这有代价：GC 会在不可预测的时间暂停程序，增加内存占用。Node.js 服务内存越跑越高，有时候就是 GC 没能及时回收导致的。

在 C 和 C++ 里，你手动调用 malloc 申请堆内存，用完了要调用 free 释放。但程序员会犯错：忘记释放（内存泄漏），释放后还在用（悬空指针），释放两次（double free），这些都是严重的安全漏洞。

Rust 的方案是所有权系统。

所有权系统的核心是三条规则：

第一，Rust 里的每个值都有一个变量叫做它的"所有者"。第二，一个值在任何时刻只能有一个所有者。第三，当所有者离开作用域，这个值就会被丢弃，内存自动释放。

听起来简单，让我们用代码来理解。

let s1 = String::from("hello")。这里 s1 是字符串 "hello" 的所有者，实际上 s1 在栈上存储了三样东西：指向堆上字符串数据的指针、字符串的长度、以及已分配的容量。真正的字符数据 "hello" 在堆上。

当 s1 离开作用域，比如函数结束，Rust 自动调用 s1 的 drop 函数，释放堆上的内存。你不需要手动写 free，Rust 在编译期就知道什么时候该释放。

第二条规则引出了 Rust 最让初学者困惑的行为：移动（Move）。

let s1 = String::from("hello");
let s2 = s1;

在 JavaScript 里，s2 = s1 是复制了字符串的值，s1 和 s2 都持有 "hello"。但在 Rust 里，这行代码之后，s1 就失效了，不能再使用！

为什么？因为字符串是堆上的数据，如果 s1 和 s2 都指向同一块堆内存，当它们各自离开作用域时，会尝试 free 同一块内存两次，这是 double free 错误。所以 Rust 的规定是：赋值操作把所有权"移动"给 s2，同时让 s1 失效。

这就是"移动语义"。和 JavaScript 最大的心智差异，就在这里。

如果你真的需要两个独立的字符串，用 clone：let s2 = s1.clone()，这会深拷贝堆上的数据，两个变量都是完整独立的。但 clone 是有开销的，Rust 要求你显式声明"我知道这是深拷贝"。

注意：只有堆上的数据才有移动语义。像整数这类存在栈上的类型，赋值操作是复制，不是移动：屏幕上展示了这个连续遮蔽的例子，用同名变量依次绑定不同的值。

哪些类型是 Copy 的？所有整数类型，浮点数，布尔值，字符类型，以及包含 Copy 类型的元组。哪些不是？String、Vec、以及任何包含堆分配数据的类型。

理解了移动，我们来看函数和所有权的交互，这是第一个容易踩的坑。

let s = String::from("hello");
这个函数接受字符串的所有权，函数结束后字符串被释放，调用点的原变量失效。
takes_ownership(s);
// 这里不能再用 s 了！s 的所有权被移进了函数

这是什么意思？当你把 String 传给函数时，所有权被移入函数，函数结束时内存释放。调用点的原变量失效。

如果函数需要用完还给你，可以返回所有权：

这个函数接受字符串的所有权并返回它，把所有权从函数内部移到调用方。

let s1 = gives_back(String::from("hello"))，这时 s1 是所有者。

但这样每次都要"借还"很麻烦。于是 Rust 有了"借用"（Borrowing）的概念。

借用的语法是 & 符号，表示"我借用这个值，但不获取所有权"。

这个函数通过引用借用字符串，计算其长度后返回，原字符串的所有权不变。

let s1 = String::from("hello");
let len = calculate_length(&s1);
println!("{} 的长度是 {}", s1, len); // s1 仍然有效！

这里 &s1 创建了一个对 s1 的引用，函数借用了这个引用，函数结束时引用消失，但 s1 的所有权没有移动，仍然有效。

这就是借用的核心：创建引用，不获取所有权，函数结束引用消失，原变量仍有效。

但默认的借用是不可变的。如果你想通过引用修改数据，需要可变引用：&mut。

这个函数接受可变引用，可以通过引用修改字符串内容，调用时需要传入可变引用。

let mut s = String::from("hello"); // 变量也要是 mut
change(&mut s);

可变引用有一个重要限制：在同一作用域内，一个值只能有一个可变引用。同时也不能既有可变引用又有不可变引用。

这为什么？这是 Rust 防止数据竞争的机制。在并发环境下，如果多个地方同时可变引用同一数据，就可能出现数据竞争。Rust 把这个检查提前到编译期：如果你的代码通过了编译，就不会有数据竞争。

具体规则：可以有任意多个不可变引用；或者只有一个可变引用；这两种情况不能同时存在。

初学者常见的几个编译错误和解决方法，我来逐一说一下。

第一个错误：use of moved value。你把一个 String 移入了函数或者另一个变量之后，还在用它。解决方法是要么用 clone() 做深拷贝，要么改成传引用 &String 而不是传值。

第二个错误：cannot borrow as mutable because it is also borrowed as immutable。你同时持有不可变引用和可变引用。解决方法是让不可变引用先结束生命周期，然后再创建可变引用。Rust 2018 引入了 NLL（Non-Lexical Lifetimes）之后，编译器更聪明了，很多这类问题会自动解决。

第三个错误：cannot borrow as mutable more than once at a time。你同时创建了两个可变引用。解决方法是在一个可变引用的作用域结束之后才创建另一个。

let mut s = String::from("hello");
let r1 = &mut s;
let r2 = &mut s; // 错误！r1 还在作用域里
// 解决：让 r1 先结束
{
    let r1 = &mut s;
    r1.push_str(" world");
} // r1 在这里结束
let r2 = &mut s; // 现在可以了

第四个错误：returns a reference to local variable。函数里创建了局部变量，然后返回这个变量的引用，但函数结束时局部变量被销毁，引用就变成了悬空引用。解决方法是返回值本身（转移所有权）而不是返回引用。

接下来讲切片类型，这是借用的一个特别用法。

切片让你引用集合中的一部分，而不是整个集合。字符串切片的类型是 &str，这就是我们上章说的字符串字面量的类型。

let s = String::from("hello world");
let hello = &s[0..5]; // "hello"
let world = &s[6..11]; // "world"

这里 hello 和 world 都是 &str，它们是对 s 里某段数据的借用引用，没有复制数据。

切片的一个强大用法是写接受字符串参数的函数：参数类型用 &str 而不是 &String，这样既能接受字符串字面量，也能接受 String 的引用，更灵活。这叫做 deref coercion，字符串的引用会自动降级成切片。

数组切片也是类似的：&[i32] 是整数数组的切片，fn sum_slice(s: &[i32]) -> i32 可以接受 &[1,2,3] 也可以接受 Vec<i32> 的引用，非常灵活。

好，我们来讲生命周期（Lifetimes），这是很多人觉得最神秘的部分。

生命周期的存在是为了防止悬空引用——也就是引用指向的数据已经被释放了，但引用还在被使用。

大多数时候，生命周期是由编译器自动推断的，你不需要写任何东西。但当编译器无法自动推断时，你需要手动标注生命周期。

生命周期标注的语法是单引号加名称，比如 'a。

比如这个函数，屏幕上可以看到具体的字段定义和类型标注。

这里的 'a 告诉编译器：返回的引用的生命周期和两个参数中较短的那个一样长。没有这个标注，编译器不知道返回的引用指向 x 还是 y，也就无法确保安全。

让我们看一个更具体的例子来理解为什么需要生命周期标注：

fn longest<'a>(x: &'a str, y: &'a str) -> &'a str，调用时传入了 s1 和 s2，其中 s1 生命周期更长，s2 生命周期更短。编译器根据 'a 的标注知道返回值的生命周期是两者中较短的，也就是 s2 的生命周期。这确保了调用者在使用返回值时，s2 还没有被释放。

在实际代码里，大部分函数不需要显式生命周期标注，因为 Rust 有一套省略规则（lifetime elision rules）会自动推断。编译器遵守三条规则：输入引用各自有独立的生命周期参数；如果只有一个输入生命周期参数，它被赋给所有输出引用；如果有多个输入生命周期参数但其中有 &self 或 &mut self，那么 self 的生命周期被赋给所有输出引用。

当编译器报生命周期错误时，再去理解具体的场景，先看错误信息，编译器通常会给出明确的提示。

好，这章的内容非常密集，我们来做一个实战练习巩固。

实现一个简单的文本分析工具：输入一段文字，输出单词数量、最长单词、以及每个单词出现的次数。

这个练习会用到：字符串切片 &str、Vec 和 HashMap 集合类型、借用和引用、迭代器方法。

屏幕上可以看到 word_count 函数的定义，返回 HashMap<&str，参数类型都有明确标注。

屏幕上可以看到 longest_word 函数的定义，返回 &str，参数类型都有明确标注。

main 函数里组合使用这两个函数，然后格式化输出。

这里有个值得注意的地方：word_count 函数返回的 HashMap 的键类型是 &str 而不是 String。这些键都是对 text 的借用引用，不需要复制字符串数据。只要 text 存在，这些引用就有效。这是 Rust 借用系统的实际好处：零复制的字符串处理。

运行 cargo run，你会看到详细的文本分析结果。


让我们再多谈一下所有权系统在实际工程中的应用，这对你今后写 Rust 代码非常关键。

所有权系统初学时最让人头疼的是"借用检查器"（Borrow Checker）报错。很多初学者把借用检查器当成敌人，觉得它在故意刁难你。但正确的心态是：借用检查器是在帮你发现 bug。每一个它拒绝的代码，在 C++ 里都可能是运行时崩溃或者内存安全漏洞。

来看几个现实中常见的模式，帮你建立更深的直觉。

第一个模式：循环中修改集合。

这是从 JavaScript 转来时很常见的困惑：

let mut v = vec![1, 2, 3, 4, 5];
for x in &v {
    v.push(*x * 2); // 错误！不能在有不可变引用时修改 v
}

在 JavaScript 里，for...of 循环过程中修改数组是允许的（虽然通常是 bug）。在 Rust 里，这是编译错误，因为 &v 是不可变引用，.push() 需要可变引用，两者不能同时存在。

正确的做法：先用迭代器收集需要添加的元素，循环结束后再 extend：

let additions: Vec<i32> = v.iter().map(|x| x * 2).collect();
v.extend(additions);

或者用索引而不是引用：

let len = v.len();
for i in 0..len {
    let new_val = v[i] * 2;
    v.push(new_val);
}

第二个模式：返回局部变量的引用。

fn get_greeting(name: &str) -> &str {
    let greeting = format!("你好，{}！", name); // greeting 是局部变量
    &greeting // 错误！greeting 在函数返回后被销毁
}

这在 C 里是悬空指针的经典来源，在 Rust 里编译器直接拒绝。解决方法是返回 String 而不是 &str：

fn get_greeting(name: &str) -> String {
    format!("你好，{}！", name)
}

或者如果你确实需要引用，返回的引用必须来自参数，不能来自局部变量。

第三个模式：结构体里的引用字段。

如果结构体里有引用字段，需要生命周期标注：

struct Important<'a> {
    part: &'a str, // 'a 标注了 part 和创建此结构体的字符串的生命周期关系
}

let novel = String::from("Call me Ishmael...");
let first_sentence = novel.split('.').next().unwrap();
let announcement = Important { part: first_sentence };
// announcement 的生命周期不能超过 novel

初学阶段遇到这种情况，最简单的解决方法是把 &str 改成 String，让结构体拥有字符串而不是借用它，这样就不需要生命周期标注了。

第四个模式：多个可变借用的分散技巧。

有时候你需要同时可变引用同一个结构体的两个字段，编译器可能会报错（因为它无法确认你引用的是不同字段）：

struct Matrix {
    rows: Vec<Vec<f64>>,
    cols: Vec<Vec<f64>>,
}

// 这会报错，因为编译器认为 rows 和 cols 属于同一个 Matrix
// let (rows, cols) = (&mut m.rows, &mut m.cols);

解决方法之一是用 split_at_mut 这样的方法，或者重构数据结构。Rust 2024 edition 对这类问题有了更智能的处理（disjoint capture），编译器能够识别不相交的字段访问。

第五个模式：所有权与迭代器。

for item in collection 会消耗 collection，之后不能再用它。如果不想消耗，用 &collection 或者 collection.iter()：

let v = vec![1, 2, 3];
for item in &v { println!("{}", item); } // v 仍然有效
for item in v { println!("{}", item); }  // v 被消耗，之后不能用

这和 JavaScript 完全不同——JavaScript 的 for...of 不会"消耗"数组，数组始终可以继续用。Rust 的 for item in v 在语义上是把 v 的每个元素逐个移动出来，所以 v 之后就空了。

一个实用的技巧：当你不确定是否需要 clone，先试着用 &，如果编译器报错，再考虑是否需要 clone。通常借用就够了，不需要 clone。过度使用 clone 的代码虽然能编译，但会有不必要的内存分配和复制开销。

另外值得一提的是 std::mem::take 函数：let taken = std::mem::take(&mut some_option)。这会取走 some_option 的值，把它替换成默认值（Option 的默认值是 None）。在循环里修改复杂的嵌套数据结构时，这个函数很有用，可以避免临时的可变引用冲突。

这章最重要的三个概念：

所有权：每个值只有一个所有者，离开作用域自动释放。移动语义让堆数据的赋值是所有权转移。Copy 类型的赋值是值复制。

借用：用 & 借用引用，不获取所有权。可以有多个不可变引用，或者一个可变引用，不能同时存在。引用不能比它指向的数据活得更长。

生命周期：确保引用不会比它指向的数据活得更长。大多数情况编译器自动推断，特殊情况需要手动标注。标注 'a 是在告诉编译器不同引用之间的生命周期关系，不是在延长或者缩短生命周期。

这三个概念是 Rust 内存安全的基石，也是你在接下来所有 Rust 代码里会反复遇到的东西。

建议你在脑子里保持一个画面：每个变量都有一个"所有权标签"，借用就是临时摘掉标签看一看，移动就是把标签贴到新变量上，生命周期保证你不会引用一个已经扔掉的东西。

下一章，我们讲结构体和枚举——Rust 的核心数据建模工具，以及和它们配合的模式匹配。这是 Rust 里最让人愉快的部分之一。下章见。
"""

SCRIPTS[4] = """
欢迎来到第四章：结构体、枚举与模式匹配。

上一章我们经历了 Rust 最难的概念所有权系统。这章会轻松一些——我们来学 Rust 的数据建模工具，以及配合它们使用的模式匹配。这也是 Rust 里最让人愉快的部分之一。

前端工程师对数据建模不陌生。在 JavaScript 里你用对象 object 和类 class 来组织数据，用 TypeScript 的 interface 和 type 来描述数据结构。Rust 用结构体 struct 和枚举 enum 来做类似的事情，但它们更强大、更安全。

我们先从结构体开始。

结构体是命名的字段的集合，类似 JavaScript 的对象或者 TypeScript 的 interface。但 Rust 的结构体是有行为的——可以给它定义方法。

用 struct 关键字定义：

屏幕上可以看到 User 结构体的定义，每个字段都有明确的类型标注，这是 Rust 强类型系统的体现。

对应的 TypeScript 接口是：interface User { username: string; email: string; age: number; active: boolean; }。但 Rust 的 struct 不只是类型描述，它是真实的数据布局，编译器会根据字段类型计算内存布局，每个字段在内存里的位置在编译时就确定了。

创建实例：let user1 = User 在屏幕上展示的代码里。修改字段需要整个变量是 mut：let mut user1 = User...，然后 user1.email = String::from("new@example.com")。

注意 Rust 不允许只让某些字段可变，必须整个结构体实例是 mut。这和 JavaScript 不同，JavaScript 的 const 对象里的属性还是可以修改的。

Rust 的结构体更新语法很方便，从另一个实例创建新实例，只修改部分字段：

let user2 = User 在屏幕上展示的代码里。这和 JavaScript 的展开运算符 ...user1 很像。

但注意：如果 user1 里有 String 类型的字段被移入了 user2，user1 就不能再用那些字段了。如果只移动了 Copy 类型的字段，user1 仍然有效。

Rust 有三种结构体：

普通结构体，每个字段都有名字，如上面的 User。

元组结构体，字段没有名字，只有类型：struct Color(i32, i32, i32)，用 Color(255, 0, 0) 创建。访问用 .0、.1、.2，比如 let black = Color(0, 0, 0); black.0 是红色分量。元组结构体相比元组的优势是有类型名字，比如 Color 和 Point 虽然都是 (i32, i32)，但它们是不同的类型，不能混用，编译器会帮你发现传参顺序搞错的问题。

单元结构体，没有任何字段：struct AlwaysEqual。主要用于实现 trait，作为类型标记。

给结构体添加方法，使用 impl 块：

屏幕上可以看到 User 的实现块，里面定义了各个方法和关联函数。

这个 is_active 函数的实现在屏幕上可以看到，逻辑清晰直观。

这个 greet 函数的实现在屏幕上可以看到，逻辑清晰直观。

这个 new 函数的实现在屏幕上可以看到，逻辑清晰直观。

Rust 没有类（class），但 struct 加上 impl 就是等价物。区别是 Rust 明确区分数据（struct）和行为（impl），而不是混在一起。而且一个结构体可以有多个 impl 块，这在泛型编程里很有用。

方法可以消耗 self：fn into_something(self) -> Something 会移走 self 的所有权。调用之后 self 就失效了。这用于转换操作，比如 builder 模式最后的 build() 方法。

Builder 模式在 Rust 里非常常见，尤其是有很多可选配置项的场景：

屏幕上可以看到 RequestBuilder 结构体的定义，每个字段都有明确的类型标注，这是 Rust 强类型系统的体现。

屏幕上可以看到 RequestBuilder 的实现块，里面定义了各个方法和关联函数。
屏幕上可以看到 new 函数的定义，返回 Self，参数类型都有明确标注。
屏幕上可以看到 timeout 函数的定义，返回 Self，参数类型都有明确标注。
屏幕上可以看到 header 函数的定义，返回 Self，参数类型都有明确标注。
屏幕上可以看到 build 函数的定义，返回 Request，参数类型都有明确标注。

使用：RequestBuilder::new(url).timeout(5000).header("Accept", "application/json").build()。

注意 timeout 和 header 方法接受 mut self（消耗并返回新的 self），不是 &mut self（可变引用）。这让链式调用成为可能，每次调用都是移动操作，没有引用的复杂性。

好，接下来讲枚举，这是 Rust 里我个人最喜欢的特性之一。

Rust 的枚举远比大多数语言的枚举强大——它的每个变体都可以携带数据，这让它变成了一个代数数据类型（Algebraic Data Type）工具。

最简单的枚举：

屏幕上可以看到 Direction 枚举的定义，包含了所有可能的变体，每个变体都可以携带不同类型的数据。

let dir = Direction::North;

每个变体可以携带不同类型的数据：

屏幕上可以看到 Shape 枚举的定义，包含了所有可能的变体，每个变体都可以携带不同类型的数据。
Circle(f64) 表示半径，
Rectangle(f64, f64) 表示宽和高，
Triangle 在屏幕上展示的代码里。

创建：let c = Shape::Circle(3.0)，let r = Shape::Rectangle(4.0, 5.0)，let t = Shape::Triangle { base: 3.0, height: 4.0 }。

配合 match 计算面积：

屏幕上可以看到 Shape 的实现块，里面定义了各个方法和关联函数。
屏幕上可以看到 area 函数的定义，返回 f64，参数类型都有明确标注。
屏幕上的 match 表达式对每种可能的情况分别处理，编译器强制要求覆盖所有可能的模式，这是 Rust 穷举性检查的体现。
Shape::Circle(r) 箭头 std::f64::consts::PI * r * r，
Shape::Rectangle(w, h) 箭头 w * h，
Shape::Triangle { base, height } 箭头 base * height / 2.0。

注意 match 里的解构语法，直接从枚举变体里取出内部数据。这比 JavaScript 的 switch 强大太多了。JavaScript 的 switch 只能匹配值，Rust 的 match 可以匹配结构。

Rust 的枚举里有两个最重要的枚举：Option 和 Result，它们是 Rust 标准库的基础。

Option 枚举表示一个值可能存在也可能不存在，替代了其他语言的 null：

enum Option<T> 在屏幕上展示的代码里。

在 JavaScript 里，你可能写：

function findUser(id) { ... return user || null; }
const user = findUser(1);
if (user) { console.log(user.name); } // 要检查 null

在 Rust 里：

这个 find_user 函数的实现在屏幕上可以看到，逻辑清晰直观。

let maybe_user = find_user(1);
屏幕上的 match 表达式对每种可能的情况分别处理，编译器强制要求覆盖所有可能的模式，这是 Rust 穷举性检查的体现。
Some(user) 箭头 println!("{}", user.username)，
None 箭头 println!("用户不存在")。

或者用 if let 更简洁：
if let Some(user) = find_user(1) 在屏幕上展示的代码里。

Option 强制你处理"没有值"的情况，不像 null 可以在任何地方悄悄传播然后运行时报错。这是 Rust 比 JavaScript 更安全的原因之一。

Option 有很多有用的方法：

unwrap() 取出 Some 里的值，如果是 None 就 panic。只在你确定不是 None 时用，或者测试代码里。

unwrap_or(default) 如果是 None 则返回默认值。这类似 JavaScript 的 ?? 操作符：value ?? 'default'。

map(|v| ...) 如果是 Some，对值做转换，返回新的 Option。类似 JavaScript 的 optional chaining：user?.name。

and_then(|v| ...) 用于链式操作，类似 flatMap。

? 操作符可以在函数里简化 Option 的处理，下一章错误处理里会详细讲。

Result 枚举表示操作可能成功也可能失败：

enum Result<T, E> 在屏幕上展示的代码里。

这个 read_number 函数的实现在屏幕上可以看到，逻辑清晰直观。

屏幕上的 match 表达式对每种可能的情况分别处理，编译器强制要求覆盖所有可能的模式，这是 Rust 穷举性检查的体现。
Ok(n) 箭头 println!("数字是 {}", n)，
Err(e) 箭头 println!("解析失败：{}", e)。

Result 和 Option 的处理方式非常类似，很多方法也是对应的。

现在让我们深入看模式匹配，这是 Rust 里最优雅的特性之一。

match 表达式我们已经见过很多次，但它的能力远不止匹配枚举变体。

匹配字面量：match x 在屏幕上展示的代码里。

匹配多种情况：用竖线 | 分隔：3 | 7 | 11 箭头。

绑定变量：match msg 在屏幕上展示的代码里。

匹配守卫（guard）：在分支后加 if 条件：Some(x) if x > 0 箭头 println!("正数 {}", x)。

@ 绑定：既测试范围又绑定变量：n @ 1..=10 箭头 println!("1到10里的 {}", n)。

解构结构体：

struct Point （见屏幕代码）。
let p = Point { x: 3, y: 7 };
屏幕上的 match 表达式对每种可能的情况分别处理，编译器强制要求覆盖所有可能的模式，这是 Rust 穷举性检查的体现。

或者在 let 里直接解构：let Point { x, y } = p。这和 JavaScript 的对象解构 const { x, y } = p 语法非常相似。

解构嵌套：match 在屏幕上展示的代码里。

..忽略其余字段：match user 在屏幕上展示的代码里。

while let 模式：while let Some(value) = stack.pop() 在屏幕上展示的代码里。这比用 loop 加 if let break 更简洁。

Rust 的模式匹配是穷举的（exhaustive），你必须处理所有可能的模式，否则编译不通过。这是一个非常强的保证——当你添加了新的枚举变体，所有的 match 表达式都会报编译错误，提醒你处理新情况。这在 TypeScript 的 switch 里做不到，除非用特殊技巧。

好，我们来做这一章的实战练习：实现一个简单的几何图形面积计算器，支持命令行交互。

定义 Shape 枚举包含圆形、矩形、三角形。实现 area() 和 perimeter() 方法。从命令行参数读取图形类型和尺寸，解析并计算。

这个练习综合了：枚举定义和方法实现、match 模式匹配和解构、字符串解析、错误处理基础（parse 的 Result）、命令行参数读取。

cargo new geometry，实现上面的功能，然后 cargo run -- circle 5 应该输出圆形半径 5 的面积和周长。

常见的初学者错误：在 impl Shape 里写 match shape 而不是 match self，这会导致所有权问题；枚举变体名字要用完整路径 Shape::Circle 而不只是 Circle，除非用 use Shape::*。


让我们深入讲一下枚举和模式匹配的几个进阶用法，这在实际项目里非常常见。

首先是用枚举建模状态机。前端工程师应该熟悉状态机——React 的 useReducer 就是一种状态机。Rust 的枚举非常适合这种场景。

以一个订单的生命周期为例：

#[derive(Debug, PartialEq)]
enum OrderStatus {
    Pending,
    Paid { amount: f64, paid_at: String },
    Shipped { tracking_number: String },
    Delivered { delivered_at: String },
    Cancelled { reason: String },
}

struct Order {
    id: u64,
    items: Vec<String>,
    status: OrderStatus,
}

impl Order {
    fn pay(&mut self, amount: f64, timestamp: String) -> Result<(), &'static str> {
        match &self.status {
            OrderStatus::Pending => {
                self.status = OrderStatus::Paid { amount, paid_at: timestamp };
                Ok(())
            }
            _ => Err("只有待支付的订单才能支付"),
        }
    }

    fn ship(&mut self, tracking: String) -> Result<(), &'static str> {
        match &self.status {
            OrderStatus::Paid { .. } => {
                self.status = OrderStatus::Shipped { tracking_number: tracking };
                Ok(())
            }
            _ => Err("只有已支付的订单才能发货"),
        }
    }
}

这个设计的优势是：订单的所有可能状态都在一个枚举里清楚地列出；状态转换逻辑在方法里强制执行；如果你尝试在错误状态下执行操作，会得到明确的错误，而不是静默失败。

在 TypeScript 里，你可能会用 type OrderStatus = 'pending' | 'paid' | 'shipped' | ... 加上额外的可选字段来表达这个，但 Rust 的枚举让每个状态携带它专属的数据，类型更严格。

另一个重要的进阶话题是 newtype 模式。

Newtype 是用元组结构体包裹现有类型，创建一个新的语义上不同的类型：

struct UserId(u64);
struct PostId(u64);
struct Meters(f64);
struct Feet(f64);

这样 UserId 和 PostId 虽然内部都是 u64，但是不同的类型，不能混用。如果你有一个函数 fn find_post(user_id: UserId, post_id: PostId)，就不可能把参数顺序搞反——编译器会报错。

这在 JavaScript/TypeScript 里很难做到同等安全。TypeScript 有 branded types 技巧，但需要额外的手动 cast，不如 Rust 原生支持。

Newtype 的零成本：struct UserId(u64) 在运行时和 u64 完全一样，没有任何额外开销。这是 Rust 类型安全的又一个体现——安全性不需要运行时代价。

访问 newtype 内部值：UserId(42).0 得到 42。可以给 newtype 实现 Deref trait 来更方便地访问内部值，或者提供专门的 getter 方法。

接下来讲一下 match 的一些特殊语法，这在阅读真实 Rust 代码时会遇到。

ref 和 ref mut：在模式里用 ref 绑定引用而不是移动值：

let name = String::from("Alice");
match name {
    ref s => println!("Hello, {}", s), // s 是 &String，name 没有被移动
}
println!("{}", name); // name 仍然有效

在现代 Rust 里，通常用 &name 或者 name.as_str() 等方式代替 ref，更自然。但在阅读老代码时会遇到 ref。

解构函数参数：模式匹配可以直接在函数参数里：

struct Point { x: f64, y: f64 }

fn print_point(&Point { x, y }: &Point) {
    println!("({}, {})", x, y);
}

这在 JavaScript 里也支持：function printPoint({ x, y }) { ... }。

let else：Rust 1.65 引入的语法，let 解构失败时执行 else 分支（else 分支必须 return 或 panic 或 continue/break）：

fn parse_header(s: &str) -> Option<(&str, &str)> {
    let (key, value) = s.split_once(':').expect("格式错误");
    Some((key.trim(), value.trim()))
}

fn process_line(line: &str) {
    let Some((key, value)) = parse_header(line) else {
        return; // 解构失败就提前返回
    };
    println!("键: {}, 值: {}", key, value);
}

这比 if let ... { ... } else { return; } 更简洁，尤其是在需要连续解构多个 Option 的场景。

常量和枚举的组合：枚举变体在模式里可以当常量用：

const MAX_RETRIES: u32 = 3;

match retry_count {
    0 => println!("首次尝试"),
    1..=MAX_RETRIES => println!("重试中"),
    _ => println!("已达最大重试次数"),
}

这章小结：

结构体 struct 定义命名字段的数据类型。impl 块给结构体添加方法，没有 self 参数的是关联函数，相当于静态方法。Builder 模式用方法链创建复杂配置。枚举 enum 的变体可以携带数据，是代数数据类型。Option 枚举替代 null，强制处理"无值"情况。Result 枚举表示可能失败的操作，强制处理错误。模式匹配 match 是穷举的，当枚举新增变体时所有匹配都会提醒你更新。if let 和 while let 是 match 的简化形式，只关心一种情况时使用。

下一章，我们会全面讲解 Rust 的错误处理——Result、?操作符、自定义错误类型，以及何时使用 panic。这一章学完，你就能写出真正健壮的 Rust 代码。下章见。
"""

SCRIPTS[5] = """
欢迎来到第五章：错误处理。

在 JavaScript 里，错误处理主要靠 try-catch，但有个大问题：你不知道一个函数会不会抛出异常，除非你读文档或者踩坑。一个函数签名 function doSomething(x) 完全没告诉你它是否可能失败。TypeScript 也没有解决这个问题，即使加了类型标注，函数签名里依然无法体现"可能抛出异常"这一事实。

Rust 的哲学完全不同：可能失败的操作，必须在类型签名里体现出来。函数返回 Result<T, E> 就告诉你：这个操作可能成功返回 T，也可能失败返回错误 E。你必须处理这两种情况，否则编译器会提醒你。

这一章我们深入讲 Rust 的错误处理体系：panic、Result、?操作符、自定义错误类型，以及 thiserror 和 anyhow 这两个常用的第三方库。

先说 panic。

panic 是 Rust 里的"不可恢复错误"。当出现程序员的错误，比如数组越界、整数溢出（debug 模式）、调用 unwrap() 在 None 上，Rust 会 panic。

panic 会打印错误信息和调用栈，然后退出程序（或者展开调用栈，取决于配置）。

什么时候应该 panic？当你遇到的情况表明程序处于无法继续的不一致状态，或者违反了不应该发生的不变量（invariant）时。比如配置文件格式错误，或者内部数据结构损坏。在原型代码里也可以大量使用 unwrap 和 expect，快速验证逻辑，稳定后再改成正确的错误处理。

什么时候不应该 panic？任何可能由外部输入或者预期情况导致的失败，都应该用 Result 而不是 panic。比如解析用户输入，文件不存在，网络请求失败。库代码尤其要避免 panic，因为库的调用方有权选择如何处理错误，如果库直接 panic，调用方完全没有机会。

来看 Result 枚举的深度使用。

Result<T, E> 有两个变体：Ok(T) 表示成功，Err(E) 表示失败，E 是错误类型。

标准库里很多函数返回 Result：

use std::fs::File;
屏幕上的 match 表达式对每种可能的情况分别处理，编译器强制要求覆盖所有可能的模式，这是 Rust 穷举性检查的体现。
Ok(file) 箭头 处理文件，
Err(e) 箭头 处理错误，比如文件不存在或者权限不够。

我们可以进一步细化错误处理，匹配不同的错误种类：

use std::io::ErrorKind;
屏幕上的 match 表达式对每种可能的情况分别处理，编译器强制要求覆盖所有可能的模式，这是 Rust 穷举性检查的体现。
Ok(file) 箭头处理文件，
Err(e) 在屏幕上展示的代码里
ErrorKind::NotFound 箭头尝试创建文件，
其他 箭头 panic。

这很详细，但写起来比较啰嗦。Rust 提供了更简洁的方式。

unwrap 和 expect 是快速原型阶段常用的：File::open("hello.txt").unwrap() 在成功时返回文件，失败时 panic。File::open("hello.txt").expect("无法打开文件") 类似但允许自定义 panic 信息。

在生产代码里，真正优雅的错误处理用 ? 操作符。

? 操作符是 Rust 最常用的错误处理语法糖。在一个返回 Result 的函数里，expr? 的意思是：如果 expr 是 Ok(value)，继续执行并用 value；如果是 Err(e)，立刻从当前函数返回 Err(e)。

比如读取文件内容：

use std::io;
use std::io::Read;
use std::fs::File;

这个 read_username 函数的实现在屏幕上可以看到，逻辑清晰直观。
let mut f = File::open("username.txt")?; // 失败则返回 Err
let mut s = String::new();
f.read_to_string(&mut s)?; // 失败则返回 Err
Ok(s)

注意最后要把成功值包在 Ok 里返回。

这和 JavaScript 的 async/await 错误处理很像：await 会把 Promise 拒绝变成异常，? 会把 Err 变成提前返回。思路是一样的，都是把错误传播自动化。

? 操作符还有一个强大之处：自动类型转换。如果底层函数返回的错误类型和外层函数不同，? 会自动尝试用 From trait 进行转换。只要你为你的错误类型实现了 From<底层错误类型>，? 就能自动转换。这是 Rust 错误处理体系的精妙之处。

? 还可以用于 Option：在返回 Option 的函数里，expr? 如果是 None 则返回 None，如果是 Some(v) 则继续用 v。

接下来讲自定义错误类型，这是写库时必需的技能。

实际项目里通常有多种不同的错误，你需要把它们统一成一种自定义错误类型。

手动实现的方式：

use std::fmt;

#[derive(Debug)]
屏幕上可以看到 AppError 枚举的定义，包含了所有可能的变体，每个变体都可以携带不同类型的数据。

然后实现 fmt::Display trait：
impl fmt，屏幕上可以看到具体的字段定义和类型标注。
屏幕上可以看到 fmt 函数的定义，返回 fmt，参数类型都有明确标注。
屏幕上的 match 表达式对每种可能的情况分别处理，编译器强制要求覆盖所有可能的模式，这是 Rust 穷举性检查的体现。

还需要实现 std::error::Error trait，通常是空实现：
impl std::error::Error for AppError {}

为了让 ? 操作符能自动转换，还需要为每种底层错误类型实现 From trait：
impl From<std，屏幕上可以看到具体的字段定义和类型标注。
屏幕上可以看到 from 函数的定义，返回 Self，参数类型都有明确标注。

这样在函数里用 ? 时，如果底层返回了 io::Error，会自动转换成 AppError::IoError。

但这很繁琐。好消息是有 thiserror 库帮你省掉大量样板代码：

Cargo.toml 里加 thiserror = "1"，然后：

use thiserror::Error;

#[derive(Error, Debug)]
屏幕上可以看到 AppError 枚举的定义，包含了所有可能的变体，每个变体都可以携带不同类型的数据。
#[error("IO 错误：{0}")] 和 IoError(#[from] std::io::Error)，
#[error("解析错误：{0}")] 和 ParseError(#[from] std::num::ParseIntError)，
#[error("资源不存在：{0}")] 和 NotFound(String)。

#[derive(Error)] 宏自动实现了 Display、Error、以及带 #[from] 的 From 转换。代码量减少了一大半。

#[error("...")] 里的 {0} 表示枚举变体的第一个字段，{resource} 表示命名字段，对应结构体变体的字段名。这让错误信息可以包含动态内容。

而 anyhow 库提供了另一种思路，适合应用程序（不是库）的快速错误处理：

Cargo.toml 里加 anyhow = "1"，然后函数返回类型改成 anyhow::Result<T>，这是 Result<T, anyhow::Error> 的别名，anyhow::Error 能包含任何错误类型，你甚至可以直接用字符串作为错误：

use anyhow::{Context, Result, bail, ensure};

这个 parse_config 函数的实现在屏幕上可以看到，逻辑清晰直观。
let content = fs::read_to_string("config.json")
    .context("无法读取配置文件")?; // context 给错误加上更多上下文信息
let config = serde_json::from_str(&content)
    .context("配置文件 JSON 格式错误")?;

// bail! 宏用于提前返回错误
if config.port == 0 {
    bail!("端口号不能为 0");
}

// ensure! 宏用于断言，失败时返回错误
ensure!(config.port < 65535, "端口号必须小于 65535");

Ok(config)

anyhow 特别适合写应用程序的 main 函数和高层业务逻辑，因为你不需要定义精确的错误类型，只需要传播错误并加上有意义的上下文。

错误链的调试——用 anyhow 时，错误信息会包含整个错误链：

Error: 解析用户配置失败
Caused by:
  0: 无法读取配置文件 /home/user/.config/app/config.json
  1: No such file or directory (os error 2)

这让调试非常方便，每一层错误都有上下文。

最佳实践总结：

库代码用 thiserror 定义精确的错误类型，调用方可以 match 不同的错误情况；应用程序代码用 anyhow 快速传播错误，在 main 函数层打印有意义的错误信息；只在你确定永远不会是 None 或者 Err 的地方用 unwrap，或者只在测试代码里用；用 ? 而不是 match 来传播错误，代码更简洁；给错误加上 context 信息，让错误信息更容易调试；错误类型要实现 Debug 和 Display，Debug 给开发者看，Display 给最终用户看。

在 JavaScript 里，错误处理的最大问题是"错误吞噬"——catch 到错误后什么都不做，或者只是 console.error 就继续运行，导致程序在错误状态下继续执行。Rust 的 Result 类型在语言层面要求你处理每一个错误，不能忽略。如果你真的想忽略，也要显式写 let _ = some_fallible_op()，表明你知道它可能失败，只是选择不处理。

来看实战练习：写一个命令行 CSV 解析器，读取 CSV 文件，解析每行数据，处理所有可能的错误情况。

cargo new csv-parser，Cargo.toml 加上 anyhow = "1" 和 thiserror = "1"。

定义 ParseError 枚举，用 thiserror 实现，包括：文件读取错误、行格式错误（不够字段、字段为空）、数字解析错误。

定义 Record 结构体，有名字、年龄、分数三个字段。

屏幕上可以看到 parse_record 函数的定义，返回 Result<Record，参数类型都有明确标注。

屏幕上可以看到 parse_csv 函数的定义，返回 anyhow，参数类型都有明确标注。

main 函数调用 parse_csv，打印结果，用 anyhow 处理顶层错误。测试时可以创建一个有格式错误的 CSV 文件，看看错误信息是否清晰。


让我们深入讲一下错误处理的几个实战模式，这在写真实的 Rust 应用时非常重要。

首先是错误类型的设计原则。

好的错误类型应该满足几个条件：可以区分不同的错误原因（方便调用方做不同处理）；包含足够的上下文信息（方便调试）；实现 Display 用于用户友好的消息，实现 Debug 用于开发调试。

一个常见的反模式是用 String 作为错误类型：

fn do_something() -> Result<(), String> {
    Err("出错了".to_string())
}

这的确能工作，但调用方无法区分不同类型的错误，只能靠解析字符串，非常脆弱。正确做法是用有意义的枚举。

错误处理的分层架构在大项目里非常重要。典型的架构是：

底层库函数返回精确的 thiserror 错误类型，比如 SqlError、IoError；
业务逻辑层把底层错误包装成业务错误，加上业务上下文；
API 层把业务错误转换成 HTTP 响应；
main 函数用 anyhow 处理所有顶层错误。

这个分层架构让错误信息在每个层次都有意义，同时各层次可以独立演化。

来看一个实际的例子：用户注册功能的错误链：

用户提交注册表单，数据验证失败，应该返回 ValidationError 包含具体哪个字段不合法；
如果数据库唯一约束冲突（邮箱已注册），应该返回 EmailAlreadyExists；
如果数据库连接失败，应该返回 DatabaseError。

用 thiserror 定义：

#[derive(Error, Debug)]
pub enum RegisterError {
    #[error("字段验证失败：{field} - {message}")]
    Validation { field: String, message: String },

    #[error("该邮箱已被注册：{email}")]
    EmailAlreadyExists { email: String },

    #[error("数据库错误")]
    Database(#[from] sqlx::Error),
}

每种错误都有清晰的语义，API 层可以根据错误类型返回不同的 HTTP 状态码：Validation 对应 400，EmailAlreadyExists 对应 409，Database 对应 500。

错误的 source 链：实现 Error trait 的 source() 方法可以暴露底层错误，让错误链更完整：

impl std::error::Error for AppError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            AppError::Io(e) => Some(e),
            _ => None,
        }
    }
}

anyhow 自动处理 source 链，打印 Caused by: 段落。

在实际开发中，一个实用的调试技巧是 RUST_BACKTRACE=1 cargo run，这会打印完整的 panic 调用栈，帮助定位问题。对于非 panic 的错误，anyhow 的 .context() 形成的错误链已经足够追踪问题根源。

接下来讲 ? 操作符的更多使用技巧。

问号操作符不只能用在函数里，在某些情况下还可以用在 main 函数里。Rust 的 main 函数可以返回 Result：

fn main() -> anyhow::Result<()> {
    let config = std::fs::read_to_string("config.toml")?;
    let settings: Settings = toml::from_str(&config)?;
    run_app(settings)?;
    Ok(())
}

这样 main 函数里的 ? 可以直接传播错误，程序退出时打印错误信息和 Debug 格式。比手动 match 或者 unwrap 更优雅。

一个常见的需要注意的问题是：? 会调用 From 来转换错误类型，但有时候你可能有多种底层错误类型都能转换成同一种 AppError，Rust 的类型推断可能无法确定用哪个 From 实现。这时候需要显式转换：

let result = some_fallible_fn().map_err(AppError::from)?;
// 或者
let result = some_fallible_fn().map_err(|e| AppError::Io(e))?;

unwrap_or_else 与 ? 的配合：有时候你想在某个错误情况下用默认值，而不是传播错误：

let config = read_config().unwrap_or_else(|_| Config::default());

这在应用程序的配置读取里很常见——配置文件不存在时用默认配置，而不是直接退出。

错误的日志记录最佳实践：不要在每个 ? 的地方都打印日志，只在最顶层（或者每个模块的边界）打印。否则同一个错误会被打印多次，日志会非常嘈杂。

fn process_file(path: &str) -> Result<(), AppError> {
    let content = read_file(path)?; // 不打印日志，让错误传播
    let parsed = parse_content(&content)?; // 不打印日志
    save_result(parsed)?; // 不打印日志
    Ok(())
}

fn main() -> anyhow::Result<()> {
    match process_file("data.txt") {
        Ok(()) => println!("处理成功"),
        Err(e) => {
            eprintln!("处理失败：{:#}", e); // 只在这里打印，#格式打印完整错误链
        }
    }
    Ok(())
}

好，这章总结：panic 用于不可恢复的程序逻辑错误；Result<T, E> 是处理可恢复错误的标准方式；? 操作符简化错误传播，在函数里自动转换和传播 Err；thiserror 用于定义精确的错误类型，适合库；anyhow 用于快速错误传播，适合应用程序；用 .context() 给错误加上上下文，让调试更容易；错误信息要面向开发者和用户，提供足够的上下文信息。

下一章我们讲 Rust 的高阶特性：泛型、Trait 和迭代器。这是 Rust 实现零成本抽象的核心机制，也是让 Rust 既安全又高性能的关键。下章见。
"""

SCRIPTS[6] = """
欢迎来到第六章：泛型、Trait 与迭代器。

这一章是 Rust 实现"零成本抽象"的核心。我们要讲三个紧密联系的概念：泛型让你写一次代码处理多种类型；Trait 定义类型之间共享的行为；迭代器提供对集合的高性能抽象操作。

对前端工程师来说，这一章和 TypeScript 的泛型、接口以及函数式编程的 map、filter、reduce 有很多相似之处，但 Rust 的实现更深入底层，也更强大。

我们先从泛型开始。

泛型让你编写可以处理多种类型的代码，而不需要为每种类型重复写一遍。

最简单的例子：找到数组中最大的值。

没有泛型时，你得写两个函数：fn largest_i32，专门处理 i32 数组；fn largest_f64，专门处理 f64 数组。代码完全一样，只有类型不同，这违反了 DRY 原则。

用泛型写法，这个函数接受任意可比较类型的切片参数，返回该类型的最大值。但这还不够，你需要告诉编译器这个类型 T 支持比较操作，所以要加 Trait 约束，表示 T 必须实现了可以比较大小的特征。屏幕上可以看到完整的泛型函数签名。

完整写法，屏幕上可以看到完整的函数定义和实现。

在结构体里用泛型：

struct Point，尖括号里 T，在屏幕上展示的代码里。创建 Point { x: 5, y: 10 } 是 Point<i32>，Point { x: 1.5, y: 4.0 } 是 Point<f64>。

也可以用多个类型参数，屏幕上可以看到完整的函数定义和实现。

泛型在 impl 块里的使用：

impl，尖括号里 T，然后 Point，尖括号里 T，在屏幕上展示的代码里。如果想只为特定类型实现方法，可以用具体类型：impl Point，尖括号里 f64，在屏幕上展示的代码里。

泛型不会影响运行时性能！Rust 在编译时做单态化（monomorphization）——编译器为每种实际使用的类型生成专用代码。所以 largest::<i32> 和 largest::<f64> 在运行时是完全独立的函数，没有虚函数调用的开销。这就是"零成本抽象"。

类型推断通常让你不需要显式标注类型参数：let result = largest(&[1, 2, 3, 4, 5])，编译器自动推断 T 是 i32。只有在有歧义时才需要写 largest::<i32>(&array) 这样的形式。

现在来讲 Trait。

Trait 是 Rust 里定义共享行为的机制，类似 TypeScript 的 interface 或者其他语言的接口。但 Rust 的 Trait 更强大，可以有默认实现，可以作为函数参数的约束，还有 Trait 对象可以实现运行时多态。

定义 Trait：

trait Summary 在屏幕上展示的代码里
屏幕上可以看到 summarize_author 函数的定义，返回 String，参数类型都有明确标注。
这个方法返回内容的摘要字符串，Trait 默认实现会调用 summarize_author 方法。

为类型实现 Trait：

屏幕上可以看到 NewsArticle 结构体的定义，每个字段都有明确的类型标注，这是 Rust 强类型系统的体现。

屏幕上可以看到 NewsArticle 的实现块，里面定义了各个方法和关联函数。
fn summarize_author，返回 self.title.clone()；
可以选择覆盖 summarize 或者用默认实现。

屏幕上可以看到 Tweet 结构体的定义，每个字段都有明确的类型标注，这是 Rust 强类型系统的体现。

屏幕上可以看到 Tweet 的实现块，里面定义了各个方法和关联函数。
fn summarize_author，返回 format!("@{}", self.username)；
fn summarize，覆盖默认实现，返回更详细的格式。

Trait 有一个重要限制：孤儿规则（Orphan Rule）。你只能为你自己定义的类型实现你自己定义的 Trait，或者为外部类型实现你自己的 Trait，但不能为外部类型实现外部 Trait。比如你不能为标准库的 Vec<T> 实现标准库的 Display Trait——因为这两个都不是你的代码。这个规则防止了不同库之间的冲突。

Trait 作为参数约束，有两种写法：

方法一，impl Trait 语法，屏幕上可以看到完整的函数定义和实现。

方法二，where 子句，屏幕上可以看到完整的函数定义和实现。

多个 Trait 约束用加号连接：T: Display + Summary。

返回位置的 impl Trait：fn make_summary() -> impl Summary 表示返回某个实现了 Summary 的类型，调用方不需要知道具体是什么类型。这在返回闭包或者迭代器时很常用，因为这些类型的名字很长（甚至写不出来），用 impl Trait 更简洁。

常用的标准库 Trait 有哪些？

Display 和 Debug：控制如何打印类型。println!("{}") 要求 Display，println!("{:?}") 要求 Debug。Debug 通常用 #[derive(Debug)] 自动实现，Display 需要手动实现因为你要控制用户看到的格式。

Clone 和 Copy：Clone 提供 .clone() 深拷贝，Copy 让赋值时自动复制而不是移动。Copy 只能用于栈上的类型。

PartialEq 和 Eq：让类型支持 == 和 != 比较。PartialEq 用于浮点数（因为 NaN != NaN），Eq 用于严格全序比较。

PartialOrd 和 Ord：让类型支持 <、>、<= 等比较。

Default：提供 Default::default() 创建默认值。对于结构体 #[derive(Default)] 要求所有字段都实现 Default。

From 和 Into：类型转换。实现 From<T> for U 后，Into<U> for T 自动实现。

Iterator：实现迭代器协议，这我们马上讲。

大多数 Trait 可以用 #[derive] 宏自动实现，比如 #[derive(Debug, Clone, PartialEq, Default)] 就自动给你的结构体实现了这四个 Trait，减少大量样板代码。

关联类型是 Trait 里另一个重要概念。有些 Trait 里有类型占位符：

trait Iterator 在屏幕上展示的代码里。

这里的 Item 就是关联类型，实现 Iterator 时你要指定 Item 是什么，比如 type Item = i32。关联类型和泛型参数的区别是：一个类型只能实现一次带有关联类型的 Trait（比如你的类型只能有一种 Iterator::Item），但可以用不同的泛型参数多次实现泛型 Trait（比如 From<i32> 和 From<String> 可以同时实现）。

Trait 对象：当你需要在运行时处理多种不同类型时，用 dyn Trait。比如：

let shapes: Vec<Box<dyn Draw>> = vec![
    Box::new(Circle { radius: 5.0 }),
    Box::new(Rectangle { width: 10.0, height: 3.0 }),
];

for shape in &shapes {
    shape.draw();
}

Box<dyn Draw> 是一个 Trait 对象，可以持有任何实现了 Draw Trait 的类型。这是运行时多态，有一点虚函数调用的开销，但非常灵活。

对比：泛型是编译时多态（性能更好），Trait 对象是运行时多态（更灵活）。泛型要求在编译时知道所有类型，Trait 对象允许在运行时动态分发。在前端类比里，泛型像是 TypeScript 泛型，Trait 对象像是 TypeScript 的接口类型变量 let item: SomeInterface = ...。

现在来讲迭代器，这是 Rust 最优雅的特性之一。

所有实现了 Iterator Trait 的类型都可以用迭代器方法。Iterator Trait 的核心只有一个方法：fn next，返回 Option<Self::Item>。每次调用返回下一个元素，没有元素时返回 None。

创建迭代器：对 Vec 调用 .iter() 获得不可变引用的迭代器，.iter_mut() 获得可变引用的迭代器，.into_iter() 获得拥有所有权的迭代器（会消耗原集合）。

迭代器方法分两类：适配器方法返回新迭代器（惰性求值），消费器方法消费迭代器返回结果。

常用适配器：

map 转换每个元素：v.iter().map(|x| x * 2) 得到每个元素乘以 2 的迭代器。

filter 过滤元素：v.iter().filter(|x| **x > 3) 得到大于 3 的元素的迭代器。注意双重解引用，因为迭代器给你的是 &&i32（引用的引用），**x 解两层引用得到 i32。更常见的写法是用 filter(|&&x| x > 3)，或者写 filter(|x| **x > 3)。

zip 合并两个迭代器：iter1.zip(iter2) 得到元组对的迭代器。

take 取前 n 个：iter.take(5)。

skip 跳过前 n 个：iter.skip(3)。

chain 拼接两个迭代器：iter1.chain(iter2)。

flat_map 先 map 后 flat：iter.flat_map(|x| vec![x, x * 2])。

enumerate 给每个元素加上索引：iter.enumerate() 得到 (index, value) 对。

常用消费器：

collect 把迭代器收集成集合：let v: Vec<_> = iter.collect()。

sum 求和：iter.sum::<i32>()。

count 计数：iter.count()。

any 检查是否有元素满足条件：iter.any(|x| x > 3)。

all 检查是否所有元素满足条件：iter.all(|x| x > 0)。

fold 折叠，相当于 reduce：iter.fold(0, |acc, x| acc + x)。

max、min、max_by_key、min_by_key 查找极值。

for_each 对每个元素执行操作，替代 for 循环：iter.for_each(|x| println!("{}", x))。

链式操作：

let result: Vec<i32> = (1..=10)
    .filter(|x| x % 2 == 0)  // 取偶数
    .map(|x| x * x)            // 平方
    .take(3)                    // 取前3个
    .collect();                 // 收集

result 是 [4, 16, 36]。

这个代码在 JavaScript 里是：[1,2,...,10].filter(x => x%2===0).map(x => x*x).slice(0,3)。

Rust 的迭代器是惰性的——filter 和 map 不会立即执行，只有当 collect 消费时才真正遍历，而且是一次遍历，不是三次。这比 JavaScript 的链式调用更高效。

自定义迭代器：实现 Iterator Trait：

屏幕上可以看到 Counter 结构体的定义，每个字段都有明确的类型标注，这是 Rust 强类型系统的体现。

impl Iterator for Counter 在屏幕上展示的代码里
type Item = u32;
屏幕上可以看到 next 函数的定义，返回 Option<u32>，参数类型都有明确标注。
self.count += 1;
if self.count < 6 （见屏幕代码）。

然后 Counter::new() 就可以用所有迭代器方法了。你可以 counter.zip(counter.skip(1)) 来得到相邻元素对，用 counter.map(...).filter(...) 等等，完全不需要重新实现这些方法，只要实现了 next，其他 70+ 个迭代器方法都自动可用。

实战练习：用迭代器实现一个词频统计，输入文本，输出每个词出现次数排序后的前 10 个。

用 split_whitespace 分词，用 map 把每个词转小写（to_lowercase），用 fold 统计频率到 HashMap，然后把 HashMap 转成 Vec，用 sort_by 排序，最后 take(10)。

一链到底，不用一行 for 循环。


让我们更深入地讲一下 Trait 的一些高级用法和设计模式，这在真实的 Rust 项目里非常常见。

首先是 Trait 的扩展方法（Extension Traits）模式。

当你想给外部类型添加方法，但孤儿规则不允许时，可以定义一个新的扩展 Trait：

// 你想给 &[u8] 添加一个 hex_encode 方法
// 但 &[u8] 不是你的类型，std::fmt::UpperHex 也不是你的 Trait
// 所以不能 impl UpperHex for &[u8]

// 方案：定义自己的扩展 Trait
pub trait BytesExt {
    fn hex_encode(&self) -> String;
    fn to_utf8_lossy(&self) -> String;
}

impl BytesExt for [u8] {
    fn hex_encode(&self) -> String {
        self.iter().map(|b| format!("{:02x}", b)).collect()
    }

    fn to_utf8_lossy(&self) -> String {
        String::from_utf8_lossy(self).into_owned()
    }
}

// 使用
let bytes = b"hello world";
println!("{}", bytes.hex_encode()); // 68656c6c6f20776f726c64

这个模式让你可以给任何类型"添加方法"，而不违反孤儿规则。只要在使用时 use your_crate::BytesExt 引入 Trait 就行。

第二个是 Builder 模式与 Trait 的结合，这在写配置 API 时非常优雅：

pub trait ConfigBuilder: Sized {
    fn with_timeout(self, ms: u64) -> Self;
    fn with_retries(self, n: u32) -> Self;
    fn build(self) -> Config;
}

通过给 Trait 方法提供默认实现，你可以构建出"可组合的 DSL"：方法链直觉上和 JavaScript 的 fluent API 一模一样，但类型安全更强。

第三个是 Newtype 加 Deref 的完美搭档：

use std::ops::Deref;

struct Meters(f64);

impl Deref for Meters {
    type Target = f64;
    fn deref(&self) -> &f64 { &self.0 }
}

impl Meters {
    fn to_feet(&self) -> f64 { self.0 * 3.28084 }
}

// 使用
let distance = Meters(100.0);
println!("{}", *distance);          // 通过 Deref 访问内部 f64
println!("{}", distance.to_feet()); // 访问 Meters 特有的方法
println!("{}", distance.abs());     // 通过 Deref 访问 f64 的所有方法！

实现 Deref 后，Meters 自动继承了 f64 的所有方法（通过 Deref coercion），同时拥有自己的方法。这比 TypeScript 的 extend 更灵活，因为你不需要修改原类型。

关于迭代器的更多进阶技巧：

scan 方法类似 fold 但返回迭代器，可以观察累积过程：

let running_sum: Vec<i32> = (1..=5)
    .scan(0, |acc, x| { *acc += x; Some(*acc) })
    .collect();
// [1, 3, 6, 10, 15]

peekable 让你可以"偷看"下一个元素而不消耗它：

let mut iter = [1, 2, 3].iter().peekable();
if let Some(&&1) = iter.peek() {
    println!("下一个是 1");
}
println!("{:?}", iter.next()); // Some(1) — peek 没有消耗

windows 和 chunks 是数组的特殊迭代器：

let data = [1, 2, 3, 4, 5];
for window in data.windows(3) {
    println!("{:?}", window); // [1,2,3] [2,3,4] [3,4,5]
}
for chunk in data.chunks(2) {
    println!("{:?}", chunk); // [1,2] [3,4] [5]
}

这在处理时间序列数据（滑动窗口平均）或者分批处理数据时非常有用。

step_by 设置步长，相当于 for i in (0..10).step_by(3)，得到 0, 3, 6, 9。

partition 把迭代器分成满足条件和不满足条件两个 Vec：

let (evens, odds): (Vec<i32>, Vec<i32>) = (0..10).partition(|x| x % 2 == 0);
// evens: [0, 2, 4, 6, 8], odds: [1, 3, 5, 7, 9]

unzip 把元组迭代器拆成两个 Vec：

let pairs = vec![(1, 'a'), (2, 'b'), (3, 'c')];
let (nums, chars): (Vec<i32>, Vec<char>) = pairs.into_iter().unzip();

最后说一下迭代器和闭包的性能：

Rust 的迭代器链编译后通常和手写的 for 循环一样快，因为 LLVM 能够将迭代器链完全内联和展开。实际上，由于迭代器让编译器看到更多信息（比如 filter 后 map 的模式），有时候反而比等价的 for 循环更容易被向量化（SIMD 优化）。

这一点和 JavaScript 完全不同。JavaScript 的 Array.map().filter() 每步都产生新数组，有内存分配开销。Rust 的迭代器链是完全惰性的，只在消费时才产生一次遍历，零中间分配。

这章总结：泛型让代码处理多种类型，编译时单态化保证零运行时开销；Trait 定义共享行为，类似接口；孤儿规则防止外部 Trait 的冲突实现；#[derive] 宏自动实现常用 Trait；关联类型让 Trait 里的类型占位符更简洁；Trait 对象 dyn Trait 实现运行时多态；迭代器提供高性能惰性集合操作；适配器方法惰性求值，消费器方法触发执行；链式迭代器通常只遍历一次，比多次 for 循环更高效。

下一章讲智能指针——Box、Rc、RefCell，以及它们解决的问题。下章见。
"""

SCRIPTS[7] = """
欢迎来到第七章：智能指针与内存管理进阶。

上一章我们学了泛型和 Trait，知道了 Rust 如何实现零成本抽象。这一章我们深入内存管理，讲 Rust 的智能指针。

智能指针是拥有数据并具有额外能力的指针类型。普通引用 & 只是指向数据，不拥有它；智能指针拥有数据，并且在 Drop 时执行特定操作（通常是释放内存）。

理解智能指针，我们要先理解两个 Trait：Deref 和 Drop。

Deref Trait 让智能指针可以像普通引用一样使用。实现 Deref 的类型可以用 * 操作符解引用，也会触发 Deref coercion——自动的引用转换。比如 Box<String> 可以自动转成 &String，&String 又可以自动转成 &str。这让你可以把 Box<String> 直接传给需要 &str 参数的函数，不需要手动转换。

Drop Trait 定义了当值离开作用域时的清理逻辑。Rust 会自动调用每个值的 Drop::drop 方法，按照创建时的逆序。你可以为自己的类型实现 Drop 来做自定义清理，比如释放文件句柄、关闭网络连接、通知其他系统。

智能指针实际上是实现了 Deref 和 Drop 的结构体。Rust 标准库里的 String、Vec<T> 本质上也是智能指针——它们管理堆上的数据，离开作用域时自动释放。

Rust 最常用的智能指针有：Box<T>、Rc<T>、Arc<T>、RefCell<T>、以及 Cell<T>。

我们先从最简单的 Box<T> 开始。

Box<T> 是最基础的智能指针，它把数据放在堆上，本身在栈上。三种主要使用场景：

第一，编译时不知道大小的类型。Rust 要求在编译时知道所有类型的大小，这样才能为栈上的变量分配空间。但有些类型的大小无法确定，比如递归类型。

屏幕上可以看到 List 枚举的定义，包含了所有可能的变体，每个变体都可以携带不同类型的数据。

解决方法是用 Box：enum List 在屏幕上展示的代码里。Box<List> 的大小是固定的（一个指针的大小），所以整个 List 的大小就确定了。

第二，需要拥有堆上数据但不想复制。当你想把一个大型数据从一个地方移动到另一个地方，同时不复制数据时，可以把它放在 Box 里，移动的只是指针。

第三，Trait 对象。你已经见过 Box<dyn Trait> 了，这是 Trait 对象最常见的形式。

Box 没有运行时开销，解引用时直接访问堆上数据。在内存使用上，Box<T> 在栈上只占一个指针大小（8 字节在 64 位系统），数据在堆上。

Box 和 JavaScript 的关系类比：JavaScript 里所有对象都在堆上，引用在栈上。Rust 里默认数据在栈上，Box 让你显式把它放到堆上。这是明确控制内存布局的能力。

接下来是 Rc<T>，引用计数指针。

有时候一个数据需要有多个所有者。Rust 的所有权规则说每个值只有一个所有者，但现实中确实有需要共享所有权的场景，比如图数据结构里一个节点可能被多条边引用，或者在 GUI 应用里一个数据模型可能被多个视图引用。

Rc<T>（Reference Counted）实现了引用计数：每次克隆（Rc::clone(&rc)）都增加计数，每当一个 Rc 被 drop 时计数减一，计数降为零时数据才真正释放。

let a = Rc::new(5);
let b = Rc::clone(&a);
let c = Rc::clone(&a);
println!("引用计数：{}", Rc::strong_count(&a)); // 输出 3

注意：Rc::clone 只复制指针并增加计数，非常廉价，不像 .clone() 是深拷贝。这是 Rc 特有的约定，当你看到代码里有 Rc::clone，你知道这不是深拷贝，只是增加引用计数。

Rc<T> 只能用于单线程。如果你在多线程代码里用 Rc<T>，编译器会报错，因为 Rc<T> 没有实现 Send。多线程场景用 Arc<T>（Atomic Reference Counted），接口完全一样但内部计数操作是原子的（thread-safe），略有性能开销。

Rc<T> 和 Arc<T> 的共同限制：只能通过不可变引用访问数据。如果你想通过共享的 Rc 修改数据，需要 RefCell<T>。

Rc<T> 在实际代码里的典型用途：树结构和图结构的节点共享，观察者模式里多个观察者持有同一个主题，缓存系统里多个地方共享同一份数据。

RefCell<T> 实现了内部可变性（Interior Mutability）。

通常 Rust 的可变性规则是：可变引用只能有一个，而且在编译期检查。但有时候你需要在编译器"以为"是不可变的情况下修改数据。这听起来违反了规则，但实际上是有合理使用场景的——只要你能保证运行时只有一个可变借用，就是安全的。

RefCell<T> 把借用规则的检查推迟到运行时：调用 .borrow() 获取不可变引用，调用 .borrow_mut() 获取可变引用。内部维护一个计数器，每次 borrow 时增加，drop 时减少。如果你违反了借用规则（比如同时有可变和不可变借用），不是编译错误，而是运行时 panic。

RefCell 适合什么场景？最典型的是实现某些 Trait 时，Trait 的方法签名只给你 &self（不可变引用），但你需要在方法里修改内部状态。比如实现 Mock 对象记录方法调用次数，外部看到的是 &self，内部用 RefCell 包裹计数器，可以在不可变方法里递增。

组合使用：Rc<RefCell<T>> 实现了可以被多个所有者共享且可以修改的数据：

let shared = Rc::new(RefCell::new(vec![1, 2, 3]));
let clone1 = Rc::clone(&shared);
let clone2 = Rc::clone(&shared);

clone1.borrow_mut().push(4); // 通过 clone1 修改
println!("{:?}", clone2.borrow()); // 通过 clone2 读取，看到了修改

这个模式在 Rust 里很常见，比如图数据结构、事件系统、状态机。

对应到 JavaScript：JavaScript 里 const obj = { value: 1 } 是可以修改 obj.value 的，因为 const 只保证 obj 引用不变，不保证内容不变。Rust 的 Rc<RefCell<T>> 提供了类似的能力，但显式地标明了"这里有共享可变性"，让代码更清晰。

多线程版本：Arc<Mutex<T>> 是线程安全版本，Mutex 取代 RefCell，提供互斥锁。我们会在下一章详细讲。

Cell<T> 是更简单的内部可变性，适合实现 Copy 的类型（比如整数、布尔），不需要借用，直接 get 和 set：

let cell = Cell::new(5);
cell.set(10);
println!("{}", cell.get()); // 10

Cell 没有运行时的借用追踪，性能比 RefCell 更好，但只能用于 Copy 类型。典型用途：在不可变结构体里缓存计算结果，比如存储一个懒加载的哈希值。

Cow<T>（Clone on Write）是一个枚举，表示"有时候借用、有时候拥有"的场景：

enum Cow<'a, B> 在屏幕上展示的代码里。Cow 只在需要修改时才克隆，避免不必要的复制。

常用于字符串处理：fn process_text(input: &str) -> Cow<str>，如果输入不需要修改就返回 Borrowed(input)，否则返回 Owned(modified_string)。调用方不需要关心返回的是引用还是拥有数据，直接用就好。

Cow<str> 的优势：接受一段文本，大多数情况不需要修改就直接返回，零分配；只在少数情况需要修改时才分配内存。对于高频调用的文本处理函数，这个优化很重要。

Weak<T> 是 Rc<T> 的弱引用版本，不增加强引用计数：

Rc<T> 有一个风险：如果两个 Rc 互相持有对方的引用，引用计数永远不会降为零，内存泄漏。

解决方法是 Weak<T>：通过 Rc::downgrade 创建弱引用，不增加强引用计数，可以被回收。用 weak.upgrade() 可以尝试获取强引用，如果数据已经被释放则返回 None。

典型场景：父节点持有子节点的强引用 Rc，子节点持有父节点的弱引用 Weak，打破循环。在前端类比里，这类似父组件持有子组件，子组件通过 callback 引用父组件，如果用强引用就循环了，弱引用相当于回调不持有父组件的所有权。

让我们通过一个实战例子把这些概念综合起来。

我们来实现一个简单的依赖注入容器——在 Web 框架里很常见，用来管理服务的实例。

每个服务可能被多个组件使用（Rc 共享所有权），服务可能需要修改内部状态（RefCell 内部可变性），服务之间可能有依赖但不能循环引用（Weak 打破循环）。

use std::rc::{Rc, Weak};
use std::cell::RefCell;

屏幕上可以看到 Logger 结构体的定义，每个字段都有明确的类型标注，这是 Rust 强类型系统的体现。

屏幕上可以看到 Logger 的实现块，里面定义了各个方法和关联函数。
屏幕上可以看到 log 函数的定义，参数类型都有明确标注。
self.logs.borrow_mut().push(message.to_string())。
屏幕上可以看到 get_logs 函数的定义，返回 Vec<String>，参数类型都有明确标注。
self.logs.borrow().clone()。

屏幕上可以看到 Service 结构体的定义，每个字段都有明确的类型标注，这是 Rust 强类型系统的体现。

屏幕上可以看到 Service 的实现块，里面定义了各个方法和关联函数。
屏幕上可以看到 new 函数的定义，返回 Service，参数类型都有明确标注。
屏幕上可以看到 do_work 函数的定义，参数类型都有明确标注。
self.logger.log(&format!("服务 {} 正在处理", self.name))。

这个 main 函数的实现在屏幕上可以看到，逻辑清晰直观。
let logger = Rc::new(Logger { logs: RefCell::new(vec![]) });
let svc1 = Service::new("用户服务", Rc::clone(&logger));
let svc2 = Service::new("订单服务", Rc::clone(&logger));

svc1.do_work();
svc2.do_work();

println!("{:?}", logger.get_logs());
// 输出: ["服务 用户服务 正在处理", "服务 订单服务 正在处理"]

这个例子展示了 Rc<RefCell<T>> 的实际使用：Logger 被多个 Service 共享（Rc），Logger 内部需要修改（RefCell）。

什么时候选择哪种智能指针？

只需要堆上分配：用 Box<T>。
单线程共享所有权，不需要修改：用 Rc<T>。
单线程共享所有权，需要修改：用 Rc<RefCell<T>>。
多线程共享所有权，不需要修改：用 Arc<T>。
多线程共享所有权，需要修改：用 Arc<Mutex<T>>。
避免循环引用：打破循环的那一方用 Weak<T>。

这个决策树在实际编程里非常有用，当你不知道用什么指针时，按这个顺序考虑。


让我们再深入讲几个智能指针的实际应用场景，以及一些容易踩坑的地方。

首先说一下 Box 的 DST（Dynamically Sized Types）使用场景。

Rust 里有些类型的大小在编译时无法确定，叫做 DST。最常见的 DST 是 str（注意不是 &str）和 [T]（注意不是 &[T]）。你不能直接存储 str 或者 [T]，只能通过引用 &str、&[T]，或者通过 Box<str>、Box<[T]> 来拥有它们。

Box<str> 是一个有趣的类型：它拥有字符串内容，大小固定（两个 usize：指针和长度），比 String 更简单（没有 capacity 字段）。在字符串不需要增长时，Box<str> 比 String 更节省内存（一个 usize 的差别）。

Box<[T]> 类似：它是一个固定大小的、拥有所有权的数组，没有 Vec 的额外容量字段。当你有一个固定大小的数据集合时，Box<[T]> 比 Vec<T> 略微节省内存。

从 Vec 转换成 Box<[T]>：vec.into_boxed_slice()。从 Box<[T]> 转回 Vec：boxed_slice.into_vec()（如果你之后需要增长）。

接下来讲一个 RefCell 的典型使用场景：Mock 对象。

在测试里，你经常需要记录函数被调用了多少次，或者用什么参数调用的。但 Trait 方法通常只给你 &self，你不能在 &self 方法里修改字段。这正是 RefCell 的用武之地：

use std::cell::RefCell;

struct MockLogger {
    calls: RefCell<Vec<String>>,
}

impl MockLogger {
    fn new() -> Self {
        MockLogger { calls: RefCell::new(vec![]) }
    }

    fn get_call_count(&self) -> usize {
        self.calls.borrow().len()
    }
}

impl Logger for MockLogger {
    fn log(&self, message: &str) { // 注意 &self 不是 &mut self
        self.calls.borrow_mut().push(message.to_string());
    }
}

#[test]
fn test_service_logs_on_error() {
    let logger = MockLogger::new();
    let service = MyService::new(&logger);
    service.do_something_that_errors();
    assert_eq!(logger.get_call_count(), 1);
}

这个模式在测试代码里非常实用。注意 Logger Trait 的 log 方法签名是 &self，因为调用方通常不需要知道 Logger 是否需要内部可变性——这是实现细节。

现在来讲一下 Arc 和 Mutex 组合的一个重要优化技巧：避免锁竞争。

当多个线程频繁地 lock 同一个 Mutex 时，会有锁竞争，降低并发性能。解决方案之一是分片锁（Sharding）：

struct ShardedMap {
    shards: Vec<Mutex<HashMap<String, String>>>,
}

impl ShardedMap {
    fn new(shard_count: usize) -> Self {
        let shards = (0..shard_count)
            .map(|_| Mutex::new(HashMap::new()))
            .collect();
        ShardedMap { shards }
    }

    fn get_shard(&self, key: &str) -> &Mutex<HashMap<String, String>> {
        // 根据 key 的哈希决定使用哪个分片
        let shard_idx = hash(key) % self.shards.len();
        &self.shards[shard_idx]
    }

    fn insert(&self, key: String, value: String) {
        self.get_shard(&key).lock().unwrap().insert(key, value);
    }
}

不同 key 的操作落到不同分片，大幅减少锁竞争。这是 DashMap 这类高性能并发 HashMap 库的核心思路。

还有一个重要的 Rust 特性：内部可变性和线程安全的关系。

RefCell<T> 不是 Sync，不能在多线程间共享。Mutex<T> 是 Sync，可以安全地在多线程间共享。RwLock<T> 也是 Sync，读多写少时用它代替 Mutex。Atomics（AtomicBool、AtomicI32 等）是最轻量的共享可变状态，适合简单的计数器、标志位等场景，没有 Mutex 的加锁开销。

use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::Arc;

let counter = Arc::new(AtomicUsize::new(0));

for _ in 0..10 {
    let counter = Arc::clone(&counter);
    std::thread::spawn(move || {
        counter.fetch_add(1, Ordering::SeqCst); // 原子加法，无锁
    });
}

原子操作的 Ordering 参数控制内存序，对大多数应用用 SeqCst（顺序一致性）是最安全的选择，虽然性能不是最优，但保证最强的一致性。

最后说一下 Pin<T> 这个比较特殊的智能指针。

Pin<T> 保证 T 不会被移动（在内存中保持固定位置）。为什么需要这个？因为 async/await 的底层实现生成的 Future 结构体里可能有自引用（指向自身字段的指针），如果这个结构体被移动，内部指针就失效了。

Pin<T> 是 Rust 异步编程基础设施的一部分，大多数时候你不需要直接使用它，tokio 和 async-std 帮你处理了。但当你手动实现 Future Trait 时，需要理解 Pin 的语义。

这章总结：Deref trait 让智能指针可以像引用一样使用，触发 Deref coercion 自动转换；Drop trait 定义清理逻辑，Rust 自动调用；Box<T> 把数据放堆上，用于递归类型、大型数据移动、Trait 对象；Rc<T> 和 Arc<T> 实现共享所有权，Arc 是线程安全版本；RefCell<T> 把借用检查推迟到运行时，实现内部可变性；Rc<RefCell<T>> 是可共享可修改数据的常用组合；Cell<T> 是 Copy 类型的轻量级内部可变性；Cow<T> 避免不必要的克隆；Weak<T> 避免循环引用导致的内存泄漏。

下一章：并发——线程、消息传递、共享状态，以及 Rust 如何让并发编程更安全。下章见。
"""

SCRIPTS[8] = """
欢迎来到第八章：并发与异步编程。

这一章是整个课程里最实用的章节之一。前端工程师对异步编程不陌生——JavaScript 的 Promise 和 async/await 就是处理异步的工具。但 Rust 的并发和异步有很多独特之处，也避免了 JavaScript 并发模型里一些固有的问题。

我们先讲线程并发，再讲 async/await 和 Tokio。

JavaScript 是单线程的，所以你不会遇到真正的数据竞争——两个代码同时修改同一变量的情况不会发生（除了 SharedArrayBuffer + Worker 的特殊情形）。Node.js 通过事件循环处理并发，I/O 操作异步进行，但 CPU 密集型操作会阻塞整个事件循环。

Rust 支持真正的多线程并发，多个线程可以同时在多个 CPU 核心上运行。这带来了更高的性能，也带来了数据竞争的风险。Rust 的类型系统在编译期消灭了数据竞争。

Rust 的线程模型叫做"无畏并发"（Fearless Concurrency）。Rust 的类型系统和所有权系统在编译期防止了大量并发 bug：数据竞争（data race）在 Rust 里是编译错误。

创建线程：

use std::thread;

let handle = thread::spawn(|| {
    for i in 1..=5 {
        println!("子线程 {}", i);
        thread::sleep(std::time::Duration::from_millis(100));
    }
});

handle.join().unwrap(); // 等待子线程完成

thread::spawn 接受一个闭包，在新线程里执行。返回 JoinHandle，调用 .join() 等待线程完成。如果你不保存 handle 并 join，主线程结束时子线程会被强制终止。

线程和所有权：如果你想在新线程里使用主线程的数据，有两种方式。

第一种，使用 move 闭包，把所有权移入线程：

let data = vec![1, 2, 3];
let handle = thread::spawn(move || {
    println!("{:?}", data); // data 被移入了这个线程
});

第二种，使用 Arc<T>（原子引用计数）让多个线程共享数据：

let data = Arc::new(vec![1, 2, 3]);
let data_clone = Arc::clone(&data);
let handle = thread::spawn(move || {
    println!("{:?}", data_clone);
});

线程间通信：消息传递（Message Passing）。

Rust 推荐"不要通过共享内存来通信，而要通过通信来共享内存"——这也是 Go 语言的核心理念。

使用 channel：

use std::sync::mpsc; // multiple producer, single consumer

let (tx, rx) = mpsc::channel();

thread::spawn(move || {
    let messages = vec!["你好", "来自", "子线程"];
    for msg in messages {
        tx.send(msg).unwrap();
        thread::sleep(std::time::Duration::from_millis(100));
    }
});

for received in rx { // 遍历 rx 直到所有发送方关闭
    println!("{}", received);
}

可以有多个发送者：let tx2 = tx.clone()。rx 上可以调用 recv()（阻塞）或 try_recv()（非阻塞），或者像上面一样用 for 循环遍历直到 channel 关闭。

发送端 tx 被 drop 时，channel 关闭，接收端的循环自然结束。这个模式在生产者-消费者场景里非常优雅：生产者线程完成后自然关闭 channel，消费者知道工作结束了。

共享状态并发：Mutex<T>。

当多个线程需要修改同一块数据时，用 Mutex（互斥锁）：

use std::sync::{Arc, Mutex};

let counter = Arc::new(Mutex::new(0));
let mut handles = vec![];

for _ in 0..10 {
    let counter = Arc::clone(&counter);
    let handle = thread::spawn(move || {
        let mut num = counter.lock().unwrap(); // 加锁
        *num += 1;
    }); // lock 在这里自动释放（MutexGuard 被 drop）
    handles.push(handle);
}

for handle in handles {
    handle.join().unwrap();
}

println!("结果：{}", *counter.lock().unwrap()); // 10

Arc 提供共享所有权，Mutex 提供互斥访问。Rust 要求你用 Arc 包裹 Mutex 才能在多线程间共享。.lock() 返回 MutexGuard，实现了 Deref，可以像引用一样使用，MutexGuard 在超出作用域时自动释放锁。

死锁的防范：Rust 不能在编译期防止死锁（因为死锁是运行时行为），但可以用良好的编程习惯避免：按固定顺序获取多个锁；尽量缩短持有锁的时间；考虑用 try_lock() 而不是阻塞的 lock()，超时后放弃。

RwLock<T> 是读写锁，允许多个读者或一个写者：let rw = RwLock::new(data)；读取用 rw.read().unwrap()；写入用 rw.write().unwrap()。在读多写少的场景下，RwLock 比 Mutex 更高效。

Rust 的并发安全来自两个 Marker Trait：

Send 表示类型可以安全地在线程间传递所有权。大多数类型是 Send 的，但 Rc<T> 不是（因为它的引用计数不是线程安全的）。

Sync 表示类型的引用可以在多个线程间共享。大多数类型是 Sync 的，但 RefCell<T> 不是（因为它的运行时借用检查不是线程安全的）。

如果你尝试把非 Send 类型发送到另一个线程，或者把非 Sync 类型通过引用跨线程访问，编译器会报错。这就是 Rust 并发安全的保证。

好，现在进入这章的重头戏：async/await 和 Tokio。

JavaScript 工程师对 async/await 很熟悉，但 Rust 的异步模型有几个关键区别，我们一一来讲。

首先，Rust 的 async/await 不是语言自带的运行时，你需要选择一个异步运行时。最流行的是 Tokio，其次是 async-std。

在 Cargo.toml 里加：tokio = { version = "1", features = ["full"] }

Rust 的 async 函数返回的是 Future，而不是 Promise。Future 是惰性的——它在被 poll 之前不做任何事情。这和 JavaScript Promise 不同，Promise 一创建就开始执行。

这意味着：Rust 里的 Future 非常轻量，你可以创建很多 Future 而不立即产生任何工作，只有在运行时 poll 它时才执行。

用 async/await 写异步函数：

use tokio;

#[tokio::main] // 这个宏把 main 函数变成异步运行时的入口
async fn main() {
    let result = fetch_data("https://example.com").await;
    println!("{}", result);
}

async fn fetch_data(url: &str) -> String {
    // 真实场景用 reqwest
    tokio::time::sleep(std::time::Duration::from_secs(1)).await;
    format!("来自 {} 的数据", url)
}

.await 暂停当前异步任务，让出控制权，等结果就绪后继续执行。这和 JavaScript 的 await 语义完全一样。

并发执行多个异步任务：

use tokio::join; // 类似 Promise.all

let (r1, r2, r3) = tokio::join!(
    fetch_data("url1"),
    fetch_data("url2"),
    fetch_data("url3")
);

join! 宏等待所有 Future 完成，类似 JavaScript 的 Promise.all，但更高效——三个请求真正并发，总时间接近最慢那个请求的时间，而不是三个请求时间之和。

或者用 tokio::spawn 创建独立的异步任务（类似 JavaScript 里不 await 一个 Promise，让它在后台运行）：

let handle1 = tokio::spawn(fetch_data("url1"));
let handle2 = tokio::spawn(fetch_data("url2"));

let r1 = handle1.await.unwrap();
let r2 = handle2.await.unwrap();

tokio::spawn 创建的任务是独立的，即使你不 await 它，它也会在后台运行。注意 join! 和两次 spawn 后 await 的区别：join! 不允许任务在两者之间执行其他代码，spawn 允许。

select! 宏等待多个 Future 中最先完成的那个，类似 Promise.race：

use tokio::select;

select! {
    result = fetch_data("url1") => println!("url1 先完成：{}", result),
    result = fetch_data("url2") => println!("url2 先完成：{}", result),
}

select! 还有更多高级用法，比如带取消的超时：

use tokio::time::timeout;

select! {
    result = expensive_operation() => handle(result),
    _ = tokio::time::sleep(Duration::from_secs(5)) => {
        println!("超时了，放弃");
    }
}

这类似 JavaScript 的 Promise.race([operation, timeout])，但语法更简洁。

错误处理在异步代码里：async 函数可以返回 Result，用 ? 传播错误：

async fn fetch_and_parse(url: &str) -> anyhow::Result<serde_json::Value> {
    let body = reqwest::get(url).await?.text().await?;
    let json = serde_json::from_str(&body)?;
    Ok(json)
}

这和同步代码的 ? 完全一样，写法非常自然。

异步代码的生命周期注意事项：async 函数里的引用类型有特殊的生命周期要求。如果你在 async 函数里存了引用，这个引用必须在整个 async 函数的生命周期内有效，因为 Future 可能在 await 点被挂起，引用需要在挂起期间保持有效。常见的解决方法是 clone 数据而不是传引用，或者用 Arc 包裹数据。

Stream 是 Rust 的异步迭代器，类似 JavaScript 的 AsyncIterable：

use tokio_stream::StreamExt; // 提供 next() 方法

async fn process_stream() {
    let mut stream = some_stream();
    while let Some(item) = stream.next().await {
        process(item);
    }
}

tokio 提供了很多内置 Stream：文件按行读取（LinesStream），时间间隔（tokio::time::interval），channel 的接收端（ReceiverStream）。

实战练习：用 Tokio 实现一个并发 HTTP 请求工具，接受多个 URL，并发发送请求，收集所有结果，按完成时间排序输出。

Cargo.toml 加上 tokio、reqwest（features: json）、anyhow、futures。

定义 fetch_url 异步函数，返回 (url, 耗时, 状态码) 的元组。用 tokio::spawn 并发所有请求，然后 join 收集结果，按耗时排序输出。

这个练习模拟了真实的 API 聚合场景，比如 BFF（Backend For Frontend）层汇聚多个微服务的数据。


让我们更深入地讲一下 Tokio 运行时的工作原理和一些实战技巧，这对写高性能异步代码非常重要。

Tokio 使用工作线程池来执行异步任务。默认情况下，工作线程数等于 CPU 核心数。每个工作线程都有一个任务队列，当某个线程空闲时，它可以从其他线程"偷"任务来执行（工作窃取算法），保证 CPU 核心始终忙碌。

这和 JavaScript 的单线程事件循环根本不同。JavaScript 里所有代码在一个线程上执行，CPU 密集型操作会阻塞所有其他任务。Tokio 里，CPU 密集型操作会阻塞一个工作线程，但其他线程继续处理其他任务。

但注意：如果你在 async 代码里做 CPU 密集型操作（比如复杂计算、正则匹配大文本），会阻塞整个工作线程，导致该线程上的其他异步任务延迟。解决方法是用 tokio::task::spawn_blocking 把 CPU 密集型工作放到专用的阻塞线程池：

let result = tokio::task::spawn_blocking(|| {
    // 这里可以做 CPU 密集型操作
    compute_expensive_hash(data)
}).await.unwrap();

spawn_blocking 会把任务提交到一个独立的阻塞线程池（默认最多 512 个线程），不影响异步工作线程。

异步任务的取消在 Rust 里有独特的语义。在 JavaScript 里，取消 Promise 需要额外的 AbortController 机制。在 Rust/Tokio 里，drop 一个 Future 就是取消它——当你 drop 一个 tokio::spawn 返回的 JoinHandle，对应的任务就被请求取消了（不是立即取消，而是在下一个 await 点被通知取消）。

这是 Rust 异步的一个优雅之处：取消是通过所有权系统自然实现的，不需要额外的取消令牌。但也要注意：如果任务在执行到一半时被取消，可能导致状态不一致，所以关键的清理逻辑要放在 Drop 的实现里，而不是 await 后面。

tokio::time::timeout 包装一个 Future，超时后返回 Err(Elapsed)：

use tokio::time::{timeout, Duration};

match timeout(Duration::from_secs(5), expensive_operation()).await {
    Ok(result) => handle_result(result),
    Err(_elapsed) => println!("操作超时"),
}

这比 select! 更简洁，适合单个操作的超时控制。

异步锁与同步锁的区别是 Rust 异步编程的一个重要细节。

std::sync::Mutex 是同步锁，在 lock() 期间会阻塞线程，不能在 .await 期间持有。如果你持有 std::sync::Mutex 锁的时候 await 一个 Future，你会阻塞整个工作线程，其他异步任务无法运行，严重降低并发性。

tokio::sync::Mutex 是异步锁，lock().await 在等待锁时会让出线程，允许其他任务运行。但它比 std::sync::Mutex 更重，应该只在真正需要跨 await 持有锁时才用。

原则：如果锁在持有期间不需要 await，用 std::sync::Mutex（更轻量）；如果锁需要跨 await 持有，用 tokio::sync::Mutex。

实际场景：读取配置（不需要跨 await）用 std::sync::RwLock；更新共享状态后通知其他任务（需要跨 await）用 tokio::sync::Mutex 或者 tokio::sync::RwLock。

Tokio 还提供了很多有用的同步原语：

tokio::sync::Notify：通知机制，类似 JavaScript 的 EventEmitter，一个任务 notify()，等待的任务被唤醒。

tokio::sync::Semaphore：信号量，限制并发数。比如同时最多 10 个 HTTP 请求：

let semaphore = Arc::new(Semaphore::new(10));
let permit = semaphore.acquire().await.unwrap();
// 在 permit drop 之前最多有 10 个任务持有 permit
let result = make_http_request().await;
drop(permit); // 释放名额

tokio::sync::oneshot：单次发送的 channel，类似 Promise：

let (tx, rx) = tokio::sync::oneshot::channel();

tokio::spawn(async move {
    let result = compute_something().await;
    let _ = tx.send(result); // 发送结果
});

let result = rx.await.unwrap(); // 等待结果

这在需要在两个异步任务之间传递单个值时很有用。

关于异步代码的测试，Tokio 提供了 tokio::test 宏：

#[tokio::test]
async fn test_my_async_function() {
    let result = my_async_function().await;
    assert_eq!(result, expected);
}

也可以用 tokio::time::pause() 让时间快进，测试超时行为：

#[tokio::test]
async fn test_timeout_behavior() {
    tokio::time::pause(); // 暂停真实时间
    let handle = tokio::spawn(async {
        tokio::time::sleep(Duration::from_secs(60)).await;
    });
    tokio::time::advance(Duration::from_secs(60)).await; // 快进 60 秒
    handle.await.unwrap();
}

这让时间相关的测试可以在毫秒内完成，不需要真正等待 60 秒。

最后，关于 Tokio 的运行时配置，在生产环境里值得关注：

#[tokio::main(flavor = "multi_thread", worker_threads = 4)]
async fn main() { ... }

默认是 "multi_thread" flavor（多线程），也有 "current_thread" flavor（单线程，适合资源受限的嵌入式环境）。worker_threads 默认等于 CPU 核心数，可以根据工作负载特性调整。

这章总结：Rust 线程通过所有权系统保证内存安全，Send 和 Sync trait 在编译期检查线程安全；mpsc channel 实现线程间通信，推荐用消息传递而不是共享内存；Arc<Mutex<T>> 实现线程安全的共享状态；RwLock 在读多写少时比 Mutex 更高效；Rust 的异步需要运行时，Tokio 是最流行的选择；async 函数返回惰性的 Future，.await 驱动执行；tokio::join! 类似 Promise.all，select! 类似 Promise.race，tokio::spawn 类似不 await 的 Promise；用 Stream 处理异步序列，类似 AsyncIterable。

下一章我们开始进入全栈实战模块：用 Axum 构建 REST API 后端。下章见。
"""

SCRIPTS[9] = """
欢迎来到第九章：Web 后端开发——Axum 框架深度解析。

这章开始我们进入全栈实战模块。你之前学的所有 Rust 知识——所有权、泛型、Trait、异步——都会在这里用上。我们要用 Axum 框架构建一个完整的 REST API。

Axum 是 Tokio 团队出品的 Web 框架，设计理念是：充分利用 Rust 的类型系统，让错误尽早暴露在编译期。它和 Express.js 的思路很像，但类型安全程度远超 TypeScript + Express。

先做项目初始化。Cargo.toml 需要加这些依赖：axum 版本 0.8，tokio 完整 features，serde 带 derive feature，serde_json，tower-http 带 cors 和 trace features，uuid 带 v4 feature，jsonwebtoken，tracing，tracing-subscriber。

我们来构建一个完整的博客 API，包含文章的增删改查和用户认证。

先看路由系统。Axum 的路由非常直观：

use axum::{routing::{get, post, put, delete}, Router};

let app = Router::new()
    .route("/", get(root_handler))
    .route("/posts", get(list_posts).post(create_post))
    .route("/posts/:id", get(get_post).put(update_post).delete(delete_post))
    .route("/auth/login", post(login))
    .route("/auth/register", post(register));

每个 route 方法对应 HTTP 方法，处理函数是普通的 async 函数，类型推断让你不需要显式标注路由类型。

Handler 函数——这是 Axum 最强大的地方。Axum 使用"提取器"（Extractor）模式，函数的参数声明就是你想从请求里取什么。

基本的 handler：

async fn list_posts() -> Json<Vec<Post>> {
    Json(vec![]) // 返回 JSON
}

带路径参数的 handler：

async fn get_post(Path(id): Path<Uuid>) -> Result<Json<Post>, StatusCode> {
    // 从路径里提取 UUID
}

带请求体的 handler：

async fn create_post(
    Json(payload): Json<CreatePostRequest>
) -> (StatusCode, Json<Post>) {
    // payload 是自动反序列化的 Rust 结构体
}

带查询参数：

#[derive(Deserialize)]
struct ListQuery {
    page: Option<u32>,
    per_page: Option<u32>,
}

async fn list_posts(Query(params): Query<ListQuery>) -> Json<Vec<Post>> {
    let page = params.page.unwrap_or(1);
}

带 State（共享状态）：

#[derive(Clone)]
struct AppState {
    db: PgPool,
    jwt_secret: String,
}

async fn create_post(
    State(state): State<AppState>,
    Json(payload): Json<CreatePostRequest>,
) -> Result<Json<Post>, AppError> {
    // 使用 state.db 查询数据库
}

注意 AppState 必须实现 Clone，因为每个请求都会 clone 一次 State。如果 State 里有重型资源（比如数据库连接池），用 Arc 包裹或者选择 Clone 是廉价的类型。

中间件是 Axum 里另一个重要概念，它基于 Tower 生态，可以用 layer 方法添加：

use tower_http::cors::{CorsLayer, Any};
use tower_http::trace::TraceLayer;

let app = Router::new()
    .route(...)
    .layer(TraceLayer::new_for_http()) // 请求日志
    .layer(CorsLayer::new().allow_origin(Any).allow_methods(Any)); // CORS

JWT 认证中间件。在 Axum 里，认证通常用自定义提取器实现，而不是中间件：

struct AuthUser {
    user_id: Uuid,
    role: String,
}

#[async_trait]
impl<S> FromRequestParts<S> for AuthUser
where S: Send + Sync
{
    type Rejection = AppError;
    
    async fn from_request_parts(parts: &mut Parts, _: &S) -> Result<Self, Self::Rejection> {
        // 从 Authorization header 提取和验证 JWT
        let token = parts.headers
            .get("Authorization")
            .and_then(|v| v.to_str().ok())
            .and_then(|v| v.strip_prefix("Bearer "))
            .ok_or(AppError::Unauthorized)?;
        
        let claims = verify_jwt(token)?;
        Ok(AuthUser { user_id: claims.sub, role: claims.role })
    }
}

然后在需要认证的路由里直接用 AuthUser 做参数：

async fn create_post(
    auth: AuthUser, // 自动从请求里提取，不是认证就报 401
    State(state): State<AppState>,
    Json(payload): Json<CreatePostRequest>,
) -> Result<Json<Post>, AppError> { ... }

错误处理——统一的错误响应。定义 AppError 枚举，实现 IntoResponse trait：

#[derive(Debug)]
enum AppError {
    NotFound(String),
    Unauthorized,
    Forbidden,
    BadRequest(String),
    Internal(anyhow::Error),
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, message) = match self {
            AppError::NotFound(msg) => (StatusCode::NOT_FOUND, msg),
            AppError::Unauthorized => (StatusCode::UNAUTHORIZED, "未授权".into()),
            // ...
        };
        
        let body = Json(json!({ "error": message }));
        (status, body).into_response()
    }
}

这样所有 handler 返回 Result<T, AppError>，错误自动转成正确的 HTTP 响应。

完整的 main 函数：

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    tracing_subscriber::init();
    
    dotenvy::dotenv().ok();
    let db = PgPool::connect(&std::env::var("DATABASE_URL")?).await?;
    sqlx::migrate!().run(&db).await?;
    
    let state = AppState { db };
    
    let app = Router::new()
        .nest("/api", api_routes())
        .with_state(state)
        .layer(TraceLayer::new_for_http());
    
    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await?;
    tracing::info!("服务器启动在 http://localhost:3000");
    axum::serve(listener, app).await?;
    
    Ok(())
}

实战项目：完整的博客后端 API，包含：用户注册和登录（JWT）、文章 CRUD（需要认证）、分类和标签、评论系统、分页和搜索。

运行 cargo new blog-api，然后按上面的模式一步步构建。


让我们深入讲一下 Axum 的几个高级特性，这在构建真实 API 时非常重要。

首先是中间件的编写和应用。Axum 的中间件基于 Tower 生态系统，非常灵活。除了使用现成的中间件，你也可以编写自己的。

一个常见需求是请求 ID 中间件，为每个请求生成唯一 ID，方便日志追踪：

use axum::{
    http::{Request, Response},
    middleware::Next,
    body::Body,
};
use uuid::Uuid;

pub async fn request_id_middleware(
    mut request: Request<Body>,
    next: Next,
) -> Response<Body> {
    let request_id = Uuid::new_v4().to_string();
    request.headers_mut().insert(
        "x-request-id",
        request_id.parse().unwrap()
    );

    let mut response = next.run(request).await;
    response.headers_mut().insert(
        "x-request-id",
        request_id.parse().unwrap()
    );
    response
}

然后在路由里 .layer(axum::middleware::from_fn(request_id_middleware)) 应用这个中间件。

限流中间件——用 tower_governor 库：

use tower_governor::{governor::GovernorConfigBuilder, GovernorLayer};

let governor_conf = Arc::new(
    GovernorConfigBuilder::default()
        .per_second(2)     // 每秒 2 个请求
        .burst_size(5)     // 突发最多 5 个
        .finish()
        .unwrap()
);

let app = Router::new()
    .route("/api/expensive", get(expensive_handler))
    .layer(GovernorLayer { config: governor_conf });

这会给 /api/expensive 路由加上限流，超过限制返回 429 Too Many Requests。

接下来讲 Axum 的类型安全路由验证。

Axum 会在运行时验证路径参数能否解析到指定类型，但你可以用自定义提取器做更精细的验证：

use validator::Validate;

#[derive(Deserialize, Validate)]
struct CreateUserRequest {
    #[validate(email)]
    email: String,

    #[validate(length(min = 3, max = 50))]
    username: String,

    #[validate(length(min = 8))]
    password: String,
}

// 自定义提取器：先解析 JSON，再验证
struct ValidatedJson<T>(T);

#[async_trait]
impl<S, T> FromRequest<S> for ValidatedJson<T>
where
    T: DeserializeOwned + Validate,
    S: Send + Sync,
{
    type Rejection = (StatusCode, Json<serde_json::Value>);

    async fn from_request(req: Request, state: &S) -> Result<Self, Self::Rejection> {
        let Json(value) = Json::<T>::from_request(req, state)
            .await
            .map_err(|e| (
                StatusCode::BAD_REQUEST,
                Json(json!({ "error": e.body_text() }))
            ))?;

        value.validate().map_err(|errors| (
            StatusCode::UNPROCESSABLE_ENTITY,
            Json(json!({ "errors": errors }))
        ))?;

        Ok(ValidatedJson(value))
    }
}

然后 handler 里直接用 ValidatedJson<CreateUserRequest>，所有验证自动处理，不需要在每个 handler 里重复验证逻辑。

分页和排序的标准模式：

#[derive(Deserialize)]
struct PaginationParams {
    page: Option<u32>,
    per_page: Option<u32>,
    sort_by: Option<String>,
    sort_dir: Option<SortDirection>,
}

#[derive(Deserialize)]
enum SortDirection { Asc, Desc }

impl PaginationParams {
    fn offset(&self) -> i64 {
        let page = self.page.unwrap_or(1) as i64;
        let per_page = self.per_page() as i64;
        (page - 1) * per_page
    }

    fn per_page(&self) -> u32 {
        self.per_page.unwrap_or(20).min(100) // 最多 100 条
    }
}

这样所有列表接口都能一致地支持分页，不需要在每个接口里重复写 offset/limit 计算。

文件上传处理：Axum 通过 multipart 提取器支持文件上传：

use axum_multipart::Multipart;

async fn upload_avatar(
    State(state): State<AppState>,
    auth: AuthUser,
    mut multipart: Multipart,
) -> Result<Json<serde_json::Value>, AppError> {
    while let Some(field) = multipart.next_field().await? {
        let name = field.name().unwrap_or("").to_string();
        if name == "avatar" {
            let data = field.bytes().await?;
            let filename = format!("avatars/{}.jpg", auth.user_id);
            tokio::fs::write(&filename, &data).await?;
            return Ok(Json(json!({ "url": format!("/static/{}", filename) })));
        }
    }
    Err(AppError::BadRequest("未找到 avatar 字段".into()))
}

Server-Sent Events（SSE）推送——用于实时通知：

use axum::response::sse::{Event, Sse};
use tokio_stream::StreamExt;

async fn sse_notifications(
    auth: AuthUser,
    State(state): State<AppState>,
) -> Sse<impl Stream<Item = Result<Event, Infallible>>> {
    let mut rx = state.notifications.subscribe();

    let stream = async_stream::stream! {
        loop {
            match rx.recv().await {
                Ok(notification) if notification.user_id == auth.user_id => {
                    let data = serde_json::to_string(&notification).unwrap();
                    yield Ok(Event::default().data(data));
                }
                Err(_) => break,
                _ => {}
            }
        }
    };

    Sse::new(stream).keep_alive(
        axum::response::sse::KeepAlive::new()
            .interval(Duration::from_secs(15))
            .text("ping")
    )
}

前端 JavaScript 接收 SSE：const eventSource = new EventSource('/api/notifications')，然后 eventSource.onmessage = (e) => handleNotification(JSON.parse(e.data))。SSE 比 WebSocket 更简单，适合服务器向客户端的单向推送。

OpenAPI 文档自动生成：用 utoipa 库可以从 Axum handler 自动生成 OpenAPI 3.0 文档：

use utoipa::{OpenApi, ToSchema};

#[derive(ToSchema, Serialize)]
struct Post {
    id: Uuid,
    title: String,
}

#[utoipa::path(
    get,
    path = "/posts",
    responses(
        (status = 200, description = "文章列表", body = Vec<Post>),
        (status = 401, description = "未授权"),
    )
)]
async fn list_posts() -> Json<Vec<Post>> { ... }

#[derive(OpenApi)]
#[openapi(paths(list_posts), components(schemas(Post)))]
struct ApiDoc;

然后在路由里加 .merge(SwaggerUi::new("/swagger-ui").url("/api-docs/openapi.json", ApiDoc::openapi()))，就有了完整的 Swagger UI。这消除了手写 API 文档的需要，文档永远和代码同步。


我们来深入聊一聊 Axum 框架的设计理念和工程实践经验，这对你在真实项目里用好 Axum 非常重要。

Axum 的核心设计哲学是"类型即文档"。在 Node.js 和 Express 里，你的路由处理函数通常长这样：函数接受 req 和 res 两个参数，所有东西都在这两个对象里。这种方式非常灵活，但也很难一眼看出这个路由需要什么数据、会返回什么。

Axum 的做法完全不同。你的 handler 函数参数声明，就直接告诉了你和编译器：这个接口需要什么。比如函数参数里有 Path(id): Path<Uuid>，就说明这个路由有一个路径参数 id，而且必须是有效的 UUID 格式；参数里有 State(state): State<AppState>，说明这个路由会用到应用状态；参数里有 Json(body): Json<CreatePostInput>，说明这个接口期望 JSON 请求体，而且要符合 CreatePostInput 的结构。

这种声明式的接口定义让代码自文档化，即使不读代码注释，只看函数签名就知道这个接口的行为。

从 Express/Koa 迁移到 Axum，心态上最大的转变是从"一切都是 req/res"到"类型系统是你的朋友"。在 Express 里你会大量用 req.params.id、req.body.username、req.headers.authorization 这样的字符串键访问，拼错字段名到运行时才知道。在 Axum 里，这些全都是编译期检查的类型。

关于 Axum 的错误处理，我想多说几句，因为这是前端工程师转过来最容易迷失的地方。

在 TypeScript 的 Express 里，你可能这样处理错误：在中间件里 try-catch，然后 res.status(500).json({ error: e.message })。这种方式有个问题：如果你忘了 catch，错误就悄悄地变成了未处理的 Promise 拒绝。

Axum 里，每个 handler 返回的是 Result<T, E>，E 需要实现 IntoResponse trait。这意味着：你不可能"忘记处理错误"——如果函数返回 Result，Rust 编译器会要求你明确处理 Ok 和 Err 两种情况。在 handler 里用 ? 传播错误，最终由实现了 IntoResponse 的错误类型转成 HTTP 响应。这个机制让错误处理成为类型系统的一部分，不是可选的约定。

Axum 的状态管理和 React 的状态管理有有趣的相似之处。React 里你用 Context 传递共享状态，Axum 里你用 State 提取器传递共享状态。两者都是"依赖注入"的思路——把共享数据传给需要它的地方，而不是用全局变量。

不同的是 Axum 的 State 是线程安全的，必须实现 Clone 和 Send + Sync。这保证了多个请求同时处理时不会有数据竞争。而 React 的 Context 是单线程的，不需要考虑这些。

一个实用的架构建议：不要把所有东西都塞进 AppState。随着项目增长，AppState 会变得越来越大，难以维护。更好的做法是把不同的关注点分开，比如用 Extension 类型或者多层 State。

关于 Axum 路由的性能，这是前端工程师可能会关心的问题。Axum 的路由匹配基于 matchit 库，使用紧凑型 radix tree，理论复杂度是对数级别，不是线性扫描。对于几百个路由的应用，路由匹配的开销基本可以忽略不计。

真正影响 API 性能的通常是数据库查询、外部服务调用、JSON 序列化/反序列化。在这些方面，Rust 的优势非常明显：serde 的 JSON 处理速度是 Node.js 的 5-10 倍，SQLx 的零复制数据库行映射让数据库操作极其高效。

一个典型的 Axum API 服务，每个核心可以处理 50000 到 100000 个请求每秒（在 I/O 绑定场景下）。相比之下，Node.js 的 Express 通常在 10000 到 30000 之间。这不只是数字游戏——在实际的高并发场景，这个差距意味着你需要更少的服务器实例，更低的云成本。

最后我想说一下 Axum 生态和 Node.js 生态的对比。Node.js 的 npm 有 200 万个包，Rust 的 crates.io 有 15 万个。数量差距很大，但质量很高。Rust 生态里的库通常：有详细的文档和示例，有完善的测试，有严格的语义化版本，很少出现"维护者放弃"的情况（因为 Rust 写的库通常工作量更大，发布前会更认真）。

对于 Web 后端开发，你需要的核心库基本都有：Axum 或者 Actix-web 做 HTTP 框架，SQLx 或者 Diesel 做数据库，serde 做序列化，tokio 做异步运行时，reqwest 做 HTTP 客户端，redis-rs 做 Redis，lettre 发邮件，tracing 做日志。该有的都有，而且质量很高。

这章总结：Axum 用 Router 定义路由；提取器模式让 handler 函数参数声明即提取逻辑；State 传递共享状态，必须 Clone；中间件用 layer 添加；自定义提取器实现认证；实现 IntoResponse 统一错误处理；全程类型安全，大量错误在编译期暴露。

下一章：数据库集成——SQLx 和 PostgreSQL 的深度使用，包括复杂查询、事务、迁移管理。下章见。
"""

SCRIPTS[10] = """
欢迎来到第十章：数据库——SQLx 深度集成。

上一章我们搭好了 Axum 后端框架，这章来接数据库。Rust 生态里最流行的数据库库是 SQLx，它的特点是：在编译时验证 SQL 语句的正确性。

SQLx 最震撼的能力：如果你的 SQL 语句有语法错误、引用了不存在的列、或者查询结果类型和 Rust 结构体不匹配，编译不通过。这在 TypeScript 加 Prisma 里是做不到的，Prisma 的类型安全是在生成的代码层面，不是在原始 SQL 层面。

先配置好项目环境。

安装 SQLx CLI：cargo install sqlx-cli --features postgres。

创建 .env 文件：DATABASE_URL=postgres://用户名:密码@localhost/数据库名。

安装 PostgreSQL（推荐用 Docker）：docker run --name postgres -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres:16。

创建数据库：sqlx database create。

设计数据库 schema。我们继续博客项目，设计表结构：

创建用户表的迁移文件：sqlx migrate add create_users。

在生成的 SQL 文件里写：

CREATE TABLE users (
    id           UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    email        TEXT        NOT NULL UNIQUE,
    username     TEXT        NOT NULL UNIQUE,
    password_hash TEXT       NOT NULL,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE posts (
    id           UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    author_id    UUID        NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title        TEXT        NOT NULL,
    slug         TEXT        NOT NULL UNIQUE,
    content      TEXT        NOT NULL DEFAULT '',
    published    BOOLEAN     NOT NULL DEFAULT FALSE,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX posts_author_idx ON posts(author_id);
CREATE INDEX posts_published_idx ON posts(published);
CREATE INDEX posts_slug_idx ON posts(slug);

运行迁移：sqlx migrate run。

定义 Rust 数据模型：

#[derive(Debug, Serialize, Deserialize, sqlx::FromRow)]
struct User {
    pub id: Uuid,
    pub email: String,
    pub username: String,
    #[serde(skip_serializing)] // 不在 JSON 里暴露密码哈希
    pub password_hash: String,
    pub created_at: OffsetDateTime,
    pub updated_at: OffsetDateTime,
}

#[derive(Debug, Serialize, Deserialize, sqlx::FromRow)]
struct Post {
    pub id: Uuid,
    pub author_id: Uuid,
    pub title: String,
    pub slug: String,
    pub content: String,
    pub published: bool,
    pub created_at: OffsetDateTime,
    pub updated_at: OffsetDateTime,
}

编写查询。SQLx 有两种查询方式：

query! 宏：在编译时验证 SQL，需要连接真实数据库（通过 .env 里的 DATABASE_URL）。适合开发和生产代码。

query 函数：不做编译时验证，更灵活。适合动态构建的查询。

基本 CRUD：

// 创建用户
async fn create_user(pool: &PgPool, email: &str, username: &str, hash: &str) 
    -> sqlx::Result<User> 
{
    sqlx::query_as!(
        User,
        r#"
        INSERT INTO users (email, username, password_hash)
        VALUES ($1, $2, $3)
        RETURNING *
        "#,
        email, username, hash
    )
    .fetch_one(pool)
    .await
}

// 按 email 查用户
async fn find_user_by_email(pool: &PgPool, email: &str) -> sqlx::Result<Option<User>> {
    sqlx::query_as!(User, "SELECT * FROM users WHERE email = $1", email)
        .fetch_optional(pool)
        .await
}

// 分页查询文章列表
async fn list_posts(pool: &PgPool, page: i64, per_page: i64) 
    -> sqlx::Result<Vec<Post>> 
{
    let offset = (page - 1) * per_page;
    sqlx::query_as!(
        Post,
        "SELECT * FROM posts WHERE published = true ORDER BY created_at DESC LIMIT $1 OFFSET $2",
        per_page,
        offset
    )
    .fetch_all(pool)
    .await
}

JOIN 查询——注意 SQLx 需要你明确处理 JOIN 的结果类型：

#[derive(Debug, Serialize, sqlx::FromRow)]
struct PostWithAuthor {
    pub id: Uuid,
    pub title: String,
    pub content: String,
    pub author_username: String,
    pub created_at: OffsetDateTime,
}

async fn list_posts_with_authors(pool: &PgPool) -> sqlx::Result<Vec<PostWithAuthor>> {
    sqlx::query_as!(
        PostWithAuthor,
        r#"
        SELECT 
            p.id, p.title, p.content, p.created_at,
            u.username AS author_username
        FROM posts p
        JOIN users u ON p.author_id = u.id
        WHERE p.published = true
        ORDER BY p.created_at DESC
        "#
    )
    .fetch_all(pool)
    .await
}

事务处理：

async fn transfer_post_ownership(
    pool: &PgPool, 
    post_id: Uuid, 
    new_author_id: Uuid
) -> sqlx::Result<()> {
    let mut tx = pool.begin().await?;
    
    // 检查新作者是否存在
    let user_exists = sqlx::query_scalar!(
        "SELECT EXISTS(SELECT 1 FROM users WHERE id = $1)",
        new_author_id
    )
    .fetch_one(&mut *tx)
    .await?
    .unwrap_or(false);
    
    if !user_exists {
        tx.rollback().await?; // 显式回滚
        return Err(sqlx::Error::RowNotFound);
    }
    
    sqlx::query!(
        "UPDATE posts SET author_id = $1 WHERE id = $2",
        new_author_id,
        post_id
    )
    .execute(&mut *tx)
    .await?;
    
    tx.commit().await?; // 提交事务
    Ok(())
}

编写测试——SQLx 支持测试用的数据库事务回滚：

#[sqlx::test]
async fn test_create_user(pool: PgPool) {
    // pool 是测试专用的，每个测试函数用独立事务，测试后自动回滚
    let user = create_user(&pool, "test@example.com", "testuser", "hashed")
        .await
        .unwrap();
    
    assert_eq!(user.email, "test@example.com");
}

#[sqlx::test] 宏自动提供一个干净的数据库连接，每个测试结束后自动回滚，不会影响其他测试。

全文搜索——PostgreSQL 内置了基本的全文搜索：

async fn search_posts(pool: &PgPool, query: &str) -> sqlx::Result<Vec<Post>> {
    sqlx::query_as!(
        Post,
        r#"
        SELECT * FROM posts
        WHERE 
            to_tsvector('english', title || ' ' || content) 
            @@ plainto_tsquery('english', $1)
            AND published = true
        ORDER BY 
            ts_rank(to_tsvector('english', title || ' ' || content), 
                    plainto_tsquery('english', $1)) DESC
        LIMIT 20
        "#,
        query
    )
    .fetch_all(pool)
    .await
}


让我们深入讲一下 SQLx 的几个高级用法，这些在真实项目里会反复用到。

首先是查询宏的编译时验证细节。

SQLx 的 query! 宏在编译时连接数据库验证 SQL。这意味着 CI/CD 流程里需要有数据库访问，或者使用 sqlx prepare 命令生成离线缓存：

sqlx prepare --database-url "$DATABASE_URL"

这会生成 .sqlx 目录，存储查询的元信息。之后在没有数据库的 CI 环境里，设置 SQLX_OFFLINE=true 就能用缓存验证。

复杂查询的类型映射——SQLx 会把 PostgreSQL 类型映射到 Rust 类型，一些需要特别注意：

PostgreSQL 的 NULL 列映射到 Option<T>，非 NULL 列映射到 T。如果查询结果包含可能为 NULL 的 JOIN 列，要用 Option。

PostgreSQL 的 TIMESTAMPTZ 映射到 time::OffsetDateTime（需要开启 time feature）或者 chrono::DateTime<Utc>（需要开启 chrono feature）。

PostgreSQL 的 JSONB 类型映射到 serde_json::Value，可以直接序列化/反序列化你的 Rust 结构体。

PostgreSQL 的数组类型映射到 Vec<T>：比如 TEXT[] 映射到 Vec<String>。

高级查询模式——RETURNING 子句：

async fn update_post_and_return(
    pool: &PgPool,
    id: Uuid,
    title: &str
) -> sqlx::Result<Post> {
    sqlx::query_as!(
        Post,
        "UPDATE posts SET title = $1, updated_at = NOW() WHERE id = $2 RETURNING *",
        title,
        id
    )
    .fetch_one(pool)
    .await
}

RETURNING * 让你不需要额外的 SELECT 查询就能得到更新后的数据，减少一次数据库往返。

批量插入——用 unnest：

async fn bulk_insert_posts(pool: &PgPool, posts: &[(String, String, Uuid)])
    -> sqlx::Result<Vec<Post>>
{
    let titles: Vec<&str> = posts.iter().map(|(t, _, _)| t.as_str()).collect();
    let slugs: Vec<&str> = posts.iter().map(|(_, s, _)| s.as_str()).collect();
    let author_ids: Vec<Uuid> = posts.iter().map(|(_, _, id)| *id).collect();

    sqlx::query_as!(
        Post,
        r#"
        INSERT INTO posts (title, slug, author_id)
        SELECT * FROM UNNEST($1::text[], $2::text[], $3::uuid[])
        RETURNING *
        "#,
        &titles as &[&str],
        &slugs as &[&str],
        &author_ids as &[Uuid]
    )
    .fetch_all(pool)
    .await
}

这一次 SQL 调用插入所有数据，比循环调用 INSERT 快得多。

游标分页（Cursor-based Pagination）比 OFFSET 分页更高效：

async fn list_posts_cursor(
    pool: &PgPool,
    cursor: Option<(OffsetDateTime, Uuid)>, // (created_at, id) 作为游标
    limit: i64,
) -> sqlx::Result<Vec<Post>> {
    match cursor {
        None => {
            sqlx::query_as!(
                Post,
                "SELECT * FROM posts ORDER BY created_at DESC, id DESC LIMIT $1",
                limit
            )
            .fetch_all(pool)
            .await
        }
        Some((cursor_time, cursor_id)) => {
            sqlx::query_as!(
                Post,
                r#"
                SELECT * FROM posts
                WHERE (created_at, id) < ($1, $2)
                ORDER BY created_at DESC, id DESC
                LIMIT $3
                "#,
                cursor_time,
                cursor_id,
                limit
            )
            .fetch_all(pool)
            .await
        }
    }
}

游标分页避免了 OFFSET 的性能问题（OFFSET 需要扫描跳过的所有行），特别适合大数据集的分页。

数据库连接池调优，这在生产环境很重要：

let pool = PgPoolOptions::new()
    .max_connections(20)           // 最大连接数，根据数据库配置调整
    .min_connections(5)            // 最小空闲连接数
    .acquire_timeout(Duration::from_secs(3))  // 获取连接超时
    .idle_timeout(Duration::from_secs(600))   // 空闲连接超时关闭
    .max_lifetime(Duration::from_secs(1800))  // 连接最大存活时间
    .connect(&database_url)
    .await?;

最大连接数要根据 PostgreSQL 的 max_connections 配置来设置，默认是 100，留一些给管理连接，应用连接池不要超过总限制的 80%。

监控查询性能——开启 sqlx 的查询日志：

RUST_LOG=sqlx=debug cargo run

这会打印每条 SQL 的执行时间。慢查询（超过 100ms）通常需要加索引。用 EXPLAIN ANALYZE 分析查询计划是 PostgreSQL 调优的基本方法。


我们来深入聊一聊数据库集成在实际项目里的工程经验，以及 SQLx 和其他 ORM 方案的对比。

对于从 JavaScript/TypeScript 生态转过来的工程师，最常见的疑问是：为什么要用 SQLx 写原生 SQL，而不是用 ORM？Rust 有 Diesel 和 SeaORM，为什么推荐 SQLx？

这个问题没有绝对的答案，但让我说说我的理解。

先说 ORM 的优势：你可以用代码的方式描述查询，不需要记 SQL 语法；重构字段名时 ORM 会帮你更新查询；某些 ORM 支持多种数据库，方便切换；对于简单的 CRUD，ORM 写起来非常快。

ORM 的代价：复杂查询很难用 ORM 表达（连多个 JOIN、子查询、窗口函数、PostgreSQL 特有的操作符）；ORM 生成的 SQL 有时候不是最优的，而你看不到也控制不了；学习 ORM 本身需要时间，有时候比直接学 SQL 花的时间还多；调试困难，当查询出了问题，你要先把 ORM 翻译成 SQL 再去分析。

SQLx 的定位是：直接写 SQL，但在编译期验证 SQL 的正确性。你写 SQL，编译器帮你检查，运行时零额外开销。这让你同时拥有了 SQL 的灵活性和 Rust 的安全性。

当然 SQLx 也有代价：你需要懂 SQL；每次添加新查询，本地必须有数据库（或者 sqlx prepare 生成离线缓存）；不同数据库的方言有差异，切换数据库需要修改 SQL。

在真实项目里，我建议的策略是：简单的 CRUD 用 SeaORM 或者 SQLx 的简单接口；复杂查询、性能敏感的查询用 SQLx 写原生 SQL；报表查询可以单独管理，甚至存储为 .sql 文件，通过 include_str! 宏载入。

关于 PostgreSQL 的选择，我想多说一句。很多前端工程师习惯了 MongoDB，因为 JavaScript 和 JSON 天然兼容，灵活的 Schema 让原型开发很快。但对于生产级应用，关系型数据库的优势非常明显。

PostgreSQL 不只是一个传统的关系型数据库，它支持 JSONB 类型（可以存储 JSON 文档，而且可以在 JSON 字段上建索引）、数组类型（比如 tags TEXT[] 比单独一张关系表更高效）、全文搜索（内置向量相似度、tsvector）、地理数据（PostGIS 扩展）、时间序列（TimescaleDB 扩展）。

你可以把 PostgreSQL 理解为：关系型数据库的严格性加上文档数据库的灵活性。不需要在早期就为"将来可能改 Schema"担心，PostgreSQL 的 ALTER TABLE 操作在大多数情况下很高效。

数据库迁移管理是另一个重要话题。SQLx CLI 的迁移功能和 Rails 的 migrations、Flyway、Liquibase 的理念一样：每次 Schema 变更写一个迁移文件，迁移文件一旦创建就不能修改，只能新增回滚迁移。这让数据库 Schema 的变更历史完整可追溯，可以在任意版本间前进或回退。

在团队协作时，迁移文件提交到 Git 仓库，所有人的数据库都保持同步。CI/CD 里自动运行迁移，部署前确保数据库是最新状态。

关于数据库连接池的监控，生产环境里需要关注这些指标：连接池大小是否合适（太小会有等待，太大会让数据库不堪重负）；平均查询时间（用 tracing 记录每个查询的耗时）；慢查询（超过 100ms 的查询要加索引或者优化）；连接泄漏（连接数持续增长但请求数正常）。

SQLx 本身不提供这些监控，但你可以用 tracing 记录查询日志，结合 Prometheus 和 Grafana 搭建完整的监控体系。

最后聊一下 PostgreSQL 的高可用方案，虽然这超出了 SQLx 的范畴，但作为全栈工程师需要了解。基础方案是主从复制：一个主节点处理读写，多个从节点只读。SQLx 支持多个数据库 URL，你可以配置写操作走主节点，读操作走从节点：

写连接池用 DATABASE_WRITE_URL，读连接池用 DATABASE_READ_URL。对于读多写少的应用（博客、内容平台），这个简单的读写分离就能把读取压力分担到从节点，大幅提升吞吐量。

这章总结：SQLx 提供编译时 SQL 验证，需要 DATABASE_URL 指向真实数据库；query_as! 宏把查询结果映射到 Rust 结构体；sqlx::FromRow derive 自动实现行到结构体的映射；事务用 pool.begin()，commit() 或 rollback()；#[sqlx::test] 提供带自动回滚的测试数据库；PostgreSQL 支持 UUID、JSONB、全文搜索等高级特性，SQLx 都能用。

下一章：全栈实战——Next.js 前端加 Rust 后端的完整架构，包括类型同步、WebSocket 实时功能、JWT 认证。下章见。
"""

SCRIPTS[11] = """
欢迎来到第十一章：全栈实战——Next.js 加 Rust 的完整架构。

这是一个整合章节，把前面学到的 Axum、SQLx、异步编程，和前端的 Next.js 结合起来，构建一个生产级别的全栈应用：实时协作任务板。

应用功能：多用户注册登录，创建和管理任务（Kanban 看板），任务更新实时同步到所有在线用户，拖拽改变任务状态。

项目结构：Monorepo 组织，根目录有 backend 和 frontend 两个文件夹，以及一个共享类型的 shared-types 目录。

前后端类型共享是全栈 Rust 最大的优势之一。ts-rs crate 可以把 Rust 类型自动生成对应的 TypeScript 定义。

在 Cargo.toml 里加 ts-rs = "10"。

然后在 Rust 模型里加注解：

use ts_rs::TS;

#[derive(Debug, Serialize, Deserialize, TS)]
#[ts(export, export_to = "../frontend/src/types/")]
pub struct Task {
    pub id: Uuid,
    pub title: String,
    pub description: Option<String>,
    pub status: TaskStatus,
    pub assignee_id: Option<Uuid>,
    pub created_at: String,
}

#[derive(Debug, Serialize, Deserialize, TS)]
#[ts(export, export_to = "../frontend/src/types/")]
pub enum TaskStatus {
    Todo,
    InProgress,
    Done,
}

运行 cargo test export_bindings，Rust 会自动在前端目录生成对应的 TypeScript 类型文件：

// frontend/src/types/Task.ts（自动生成，不要手动修改）
export type TaskStatus = "Todo" | "InProgress" | "Done";

export interface Task {
    id: string;
    title: string;
    description: string | null;
    status: TaskStatus;
    assignee_id: string | null;
    created_at: string;
}

这意味着：Rust 后端修改了字段类型，前端的 TypeScript 定义会自动更新，TypeScript 编译器会报告所有需要修改的地方。彻底消灭手动同步类型的需要。

WebSocket 实时功能。Axum 内置了 WebSocket 支持：

use axum::extract::ws::{Message, WebSocket, WebSocketUpgrade};
use std::sync::Arc;
use tokio::sync::broadcast;

type BoardChannel = Arc<broadcast::Sender<BoardEvent>>;

#[derive(Clone, Serialize, Deserialize)]
#[serde(tag = "type", content = "data")]
enum BoardEvent {
    TaskCreated(Task),
    TaskUpdated(Task),
    TaskDeleted { id: Uuid },
    UserJoined { user_id: Uuid, username: String },
}

async fn ws_handler(
    ws: WebSocketUpgrade,
    State(state): State<AppState>,
) -> impl IntoResponse {
    ws.on_upgrade(|socket| handle_socket(socket, state))
}

async fn handle_socket(mut socket: WebSocket, state: AppState) {
    let mut rx = state.board_channel.subscribe();
    
    loop {
        tokio::select! {
            Ok(event) = rx.recv() => {
                let msg = serde_json::to_string(&event).unwrap();
                if socket.send(Message::Text(msg)).await.is_err() {
                    break;
                }
            }
            Some(Ok(msg)) = socket.recv() => {
                // 处理来自客户端的消息
                if let Message::Text(text) = msg {
                    // 解析并广播
                }
            }
            else => break,
        }
    }
}

AppState 里加上 board_channel：

#[derive(Clone)]
struct AppState {
    db: PgPool,
    board_channel: Arc<broadcast::Sender<BoardEvent>>,
}

在 main 函数里初始化：

let (tx, _) = broadcast::channel::<BoardEvent>(100);
let state = AppState {
    db: pool,
    board_channel: Arc::new(tx),
};

在 REST API 里创建任务后广播事件：

async fn create_task(...) -> Result<Json<Task>, AppError> {
    let task = db::create_task(&state.db, ...).await?;
    
    // 广播给所有 WebSocket 连接
    let _ = state.board_channel.send(BoardEvent::TaskCreated(task.clone()));
    
    Ok(Json(task))
}

前端用 React Hook 接收 WebSocket 事件：

export function useBoard(boardId: string) {
    const [tasks, setTasks] = useState<Task[]>([]);
    
    useEffect(() => {
        const ws = new WebSocket(`${WS_URL}/ws/board/${boardId}`);
        
        ws.onmessage = (e) => {
            const event: BoardEvent = JSON.parse(e.data);
            
            setTasks(prev => {
                switch (event.type) {
                    case "TaskCreated":
                        return [...prev, event.data];
                    case "TaskUpdated":
                        return prev.map(t => t.id === event.data.id ? event.data : t);
                    case "TaskDeleted":
                        return prev.filter(t => t.id !== event.data.id);
                    default:
                        return prev;
                }
            });
        };
        
        return () => ws.close();
    }, [boardId]);
    
    return { tasks };
}

Next.js Server Components 可以直接调用 Rust API，不需要客户端 fetch：

export default async function BoardPage({ params }: { params: { id: string } }) {
    const token = cookies().get("auth_token")?.value;
    if (!token) redirect("/login");
    
    // 这行代码在服务器上运行，直接调用 Rust API
    const tasks = await api.tasks.list(token);
    
    return (
        <main>
            <TaskBoard initialTasks={tasks} boardId={params.id} />
        </main>
    );
}

TaskBoard 是 Client Component，接受服务端数据作为初始状态，之后通过 WebSocket 接收实时更新。这样首次渲染有 SSR 优势（SEO 友好、快速 TTFB），之后的更新用实时 WebSocket。

JWT Cookie 认证流程：

后端登录接口在成功时设置 HttpOnly Cookie：

async fn login(...) -> Result<impl IntoResponse, AppError> {
    let token = generate_jwt(user.id)?;
    
    let cookie = format!(
        "auth_token={}; HttpOnly; Secure; SameSite=Strict; Path=/; Max-Age=604800",
        token
    );
    
    Ok((
        StatusCode::OK,
        [("Set-Cookie", cookie)],
        Json(json!({ "user": user }))
    ))
}

Next.js 前端的自定义提取器从 Cookie 头里读 JWT，Server Component 用 next/headers 的 cookies() 读取。


让我们更深入地讲一下全栈实战中的几个关键技术细节，这些在实际项目里会遇到。

首先是前后端接口设计的最佳实践。

API 版本管理：随着业务发展，API 会演化，需要保持向后兼容。常见策略是 URL 版本化（/api/v1/posts）或者 Header 版本化（Accept: application/vnd.app.v2+json）。在 Axum 里用路由嵌套支持多版本：

let v1_routes = Router::new()
    .route("/posts", get(v1::list_posts))
    .route("/users", get(v1::list_users));

let v2_routes = Router::new()
    .route("/posts", get(v2::list_posts)) // 新版本实现
    .route("/users", get(v2::list_users));

let app = Router::new()
    .nest("/api/v1", v1_routes)
    .nest("/api/v2", v2_routes);

在 Next.js 前端，用常量定义 API 版本：const API_VERSION = 'v2'，方便统一切换。

接口幂等性设计，这在网络不稳定时很重要。客户端重试时，同一个请求不应该产生重复效果。做法是：

为 POST 请求接受 Idempotency-Key Header，后端记录每个 key 对应的响应；如果相同的 key 再次请求，直接返回之前缓存的响应，不重复执行业务逻辑。

Rust 实现幂等性中间件：在 Redis 里存储 idempotency_key => response_body，TTL 设为 24 小时。请求来了先查 Redis，命中则直接返回；未命中则执行业务逻辑，结果存入 Redis。

TypeScript 类型生成的进阶用法——ts-rs 不只能生成接口，还能生成枚举的字符串字面量联合类型：

Rust 枚举：
#[derive(TS)]
pub enum ApiError {
    NotFound,
    Unauthorized,
    RateLimited { retry_after: u32 },
}

生成的 TypeScript：
export type ApiError =
    | "NotFound"
    | "Unauthorized"
    | { RateLimited: { retry_after: number } };

前端可以对这个类型做穷举的 if-else 或者 switch，TypeScript 会提示你处理每种情况。这和 Rust 的 match 穷举性相呼应，类型安全延伸到了前后端边界。

Next.js 的 Server Actions 与 Rust API 的结合：

// app/actions/posts.ts
'use server'

export async function createPost(formData: FormData) {
    const token = cookies().get('auth_token')?.value;

    const response = await fetch(`${API_URL}/api/posts`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
            title: formData.get('title'),
            content: formData.get('content'),
        }),
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error);
    }

    revalidatePath('/posts');
    return response.json();
}

Server Actions 在服务端执行，天然有 CORS 白名单访问后端 API，比前端直接调用 API 更安全（不暴露 Token 给客户端）。

真实时场景的 WebSocket 协议设计：

生产级 WebSocket 协议需要处理以下情况：消息确认（客户端确认收到）；重连机制（断开后自动重连，重放未确认消息）；心跳检测（检测僵尸连接）；消息序列号（排序和去重）。

一个简单的协议设计：

#[derive(Serialize, Deserialize, TS)]
#[serde(tag = "type")]
pub enum WsMessage {
    // 服务器 -> 客户端
    Event { id: u64, payload: BoardEvent },
    Ack { message_id: u64 },
    Ping,

    // 客户端 -> 服务器
    AckEvent { event_id: u64 },
    ClientMessage { id: u64, payload: ClientAction },
    Pong,
}

每个事件有序列号，客户端 Ack 后服务端才删除缓存，确保消息不丢失。

关于 CORS 配置的最佳实践：

在 Axum 里用 tower_http 的 CorsLayer 配置精确的 CORS 规则：

let cors = CorsLayer::new()
    .allow_origin(["https://yourdomain.com".parse::<HeaderValue>().unwrap()])
    .allow_methods([Method::GET, Method::POST, Method::PUT, Method::DELETE])
    .allow_headers([
        header::AUTHORIZATION,
        header::CONTENT_TYPE,
        header::ACCEPT,
    ])
    .allow_credentials(true); // 允许带 Cookie 的跨域请求

注意 allow_credentials(true) 时，allow_origin 不能是 Any，必须指定具体域名。这是浏览器的安全限制。开发环境单独配置 allow_origin(Any) 或者 allow_origin("http://localhost:3000")，不要在生产环境用 Any。


让我们更深入地聊一聊全栈架构的设计思路和最佳实践，这对你构建真实项目非常重要。

Next.js 加 Rust 后端的这个技术栈选择，背后有几个重要的设计理念，值得仔细思考。

首先是"关注点分离"。前端的核心职责是用户界面和体验，后端的核心职责是数据和业务逻辑。Next.js 擅长 UI 渲染、路由、SEO 优化、前端缓存；Rust 后端擅长高并发处理、复杂计算、数据安全、与数据库的交互。把两者清晰地分开，每一层只做最擅长的事情。

其次是"类型系统的延伸"。TypeScript 给了前端代码类型安全，Rust 给了后端代码类型安全，ts-rs 让这两个类型系统产生连接。这意味着从数据库模型到前端组件，整个链路都有类型检查，真正做到了端到端的类型安全。这在大型团队里尤其有价值，减少了大量因为接口文档过时或者理解偏差导致的 bug。

第三是"性能和成本的平衡"。Next.js 的 Server Components 在服务器上渲染，减少了客户端 JavaScript 的执行；Rust 后端的高性能让相同的硬件可以处理更多请求。两者结合，对于中等规模的应用，你可能只需要很少的服务器实例就能支撑相当大的流量。

现在我想聊一聊这个技术栈在实际团队协作中的经验。

对于一个小团队（2-5 人），这个技术栈有一个权衡：Rust 的学习曲线会让新成员上手慢。如果你的团队里只有你一个人懂 Rust，当你不在时维护会很困难。所以这个技术栈更适合以下场景：你有时间培训团队，大家都在学习；对性能有明确需求（比如需要处理高并发、CPU 密集型操作）；你在构建一个长期维护的产品，而不是一个快速试验的原型。

对于原型或者快速迭代的产品，Node.js 后端加 Next.js 前端可能更合适——更多的开发者会用，更多的库可用，迭代速度更快。但当产品稳定下来，考虑把性能瓶颈的部分用 Rust 重写。

关于 Monorepo 的工具链选择，这个项目用了 Cargo workspace 管理 Rust 代码，前端可以用 npm workspace 或者 Turborepo。

Turborepo 是 Vercel 出品的 Monorepo 构建工具，对 Next.js 支持非常好：增量构建（只重新构建有变更的包）、并行任务执行、远程缓存（团队共享构建缓存）。结合 Cargo workspace 的智能增量编译，整个 Monorepo 的构建速度会比单独的 repo 快很多。

推荐的目录结构是：根目录有 apps 目录（放各个应用，比如 web 是 Next.js，api 是 Rust 后端）、packages 目录（放共享的代码，比如 types 放 ts-rs 生成的类型）、Cargo.toml（workspace 配置）、package.json（npm workspace 配置）。

代码质量工具：前端用 ESLint 加 Prettier 做代码检查和格式化，Rust 后端用 cargo clippy 加 rustfmt。在 Git hooks（用 husky）里配置 pre-commit 同时运行两套检查，提交时自动保证代码质量。

关于部署策略，这个全栈项目有几种常见的部署方案。

方案一，同域部署：Next.js 和 Rust API 部署在同一个域名下，比如 / 走 Next.js，/api/* 走 Rust 后端。用 Nginx 做反向代理分流。好处是没有跨域问题，Cookie 可以直接共享；坏处是两个服务要一起部署，滚动更新需要协调。

方案二，不同子域：Next.js 在 app.example.com，Rust API 在 api.example.com。好处是独立部署，可以分别扩缩容；坏处是需要 CORS 配置，Cookie 需要设置 domain = .example.com。

方案三，Vercel 加后端云：Next.js 部署到 Vercel（极度优化的 Next.js 部署平台），Rust API 部署到 Fly.io 或者 Railway。好处是各自用最适合的平台；坏处是要管理两个平台，账单更复杂。

对于大多数中小型项目，方案一是最简单的起点。当你有了明确的扩缩容需求时再考虑分拆。

关于实时功能的可靠性设计，WebSocket 连接在真实网络环境里会断开：网络切换（WiFi 到 4G）、服务器重启、负载均衡器超时。你的前端必须实现自动重连机制，而且重连后要恢复到正确的状态。

推荐的模式是：维护一个"事件序列号"，每个服务器发出的事件都有递增的序列号；客户端记录最后收到的序列号；重连时带上序列号，服务器从该序列号之后的事件开始重放。这保证了断线重连期间的事件不会丢失。

这个模式和 Kafka 的消费者偏移量概念非常相似，实质上就是一个简化版的消息队列。对于真正高可靠的实时系统，可以引入 Redis Pub/Sub 作为消息中间件，解耦发布者和订阅者。

另一个值得讨论的话题是：前后端代码的同构性。在 JavaScript 生态里，同构是一个常见的架构目标——同一段代码可以在浏览器和 Node.js 上运行。Next.js 的 Server Components 和 Client Components 之间的边界就是一种同构的体现。

在 Rust 加 Next.js 的架构里，"同构"体现在类型层面：Rust 类型通过 ts-rs 生成 TypeScript 类型，两端"说同一种语言"。这不是代码共享，而是类型契约共享，更严格也更可维护。

这章总结：ts-rs 自动从 Rust 类型生成 TypeScript 定义，消灭手动同步；Axum 的 WebSocket 配合 broadcast channel 实现实时广播；tokio::select! 同时等待多个异步事件；Server Component 在服务端调用 Rust API 用于 SSR；Client Component 用 WebSocket 接收实时更新；HttpOnly Cookie 是 JWT 存储的推荐方式。

下一章：测试和工具链——如何写好 Rust 测试，如何用 CI/CD 保证质量。下章见。
"""

SCRIPTS[12] = """
欢迎来到第十二章：测试、工具链与项目发布。

写好代码是一方面，保证代码正确是另一方面。这章我们讲 Rust 的测试体系，然后讲如何发布你的 crate 到 crates.io，以及一些提升开发体验的工具。

Rust 有非常完善的内置测试支持，不需要额外安装测试框架。

单元测试——直接写在源文件里：

// src/lib.rs 或任何源文件里

pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

// 测试模块的约定：#[cfg(test)] 表示只在测试时编译
#[cfg(test)]
mod tests {
    use super::*; // 导入外部模块的所有内容
    
    #[test] // 这个属性标记测试函数
    fn test_add() {
        assert_eq!(add(2, 3), 5);
    }
    
    #[test]
    fn test_add_negative() {
        assert_eq!(add(-1, -2), -3);
    }
    
    #[test]
    #[should_panic(expected = "division by zero")] // 期望 panic
    fn test_divide_by_zero() {
        divide(10, 0);
    }
    
    #[test]
    fn test_option_handling() {
        let result = find_user(1);
        assert!(result.is_some());
        
        let missing = find_user(999);
        assert!(missing.is_none());
    }
}

运行测试：cargo test，运行所有测试。cargo test test_add，运行名字包含 test_add 的测试。cargo test -- --nocapture，显示 println! 输出（默认测试时会捕获输出）。

断言宏：assert! 检查是否为 true，assert_eq! 检查两值相等，assert_ne! 检查两值不等，这些都支持自定义错误信息：assert_eq!(result, expected, "失败原因：{}", extra_info)。

集成测试——放在 tests 目录里，测试的是公开 API：

// tests/integration_test.rs
use my_crate; // 作为外部用户使用库

#[test]
fn test_full_workflow() {
    let app = my_crate::App::new();
    let result = app.process("input");
    assert_eq!(result, "expected output");
}

集成测试文件的每个文件都是独立的 crate，模拟真实用户使用库的体验。

异步测试：使用 tokio::test 宏：

#[tokio::test]
async fn test_fetch_data() {
    let result = fetch_from_api("https://example.com").await;
    assert!(result.is_ok());
}

属性测试（Property Testing）——用 proptest 库自动生成大量测试用例：

Cargo.toml 加 proptest = { version = "1", default-features = false, features = ["std"] }。

use proptest::prelude::*;

proptest! {
    #[test]
    fn test_reverse_twice_is_identity(s in "\\w{0,20}") {
        // 对任意最多 20 个字符的字符串，反转两次等于原字符串
        let reversed = reverse_string(&reverse_string(&s));
        prop_assert_eq!(reversed, s);
    }
}

基准测试——测量性能：

// benches/benchmark.rs
use criterion::{criterion_group, criterion_main, Criterion};

fn bench_my_function(c: &mut Criterion) {
    c.bench_function("my_function", |b| {
        b.iter(|| my_expensive_function(100))
    });
}

criterion_group!(benches, bench_my_function);
criterion_main!(benches);

运行 cargo bench 生成性能报告。

文档测试——Rust 里的文档示例代码可以作为测试运行：

/// 把两个数相加。
///
/// # 示例
///
/// ```
/// let result = my_crate::add(2, 3);
/// assert_eq!(result, 5);
/// ```
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

运行 cargo test 时，文档里的代码块也会被执行。这保证了文档示例永远是正确的。

开发工具介绍：

cargo clippy——Rust 的代码检查工具，比编译器更严格，提供很多改进建议：cargo clippy -- -D warnings 把所有警告当错误。

cargo fmt——代码格式化工具，统一代码风格：cargo fmt，自动格式化；cargo fmt --check，只检查不修改，用于 CI。

cargo doc——生成文档：cargo doc --open 生成并在浏览器打开文档。

rust-analyzer——VS Code 等编辑器的 Rust 语言服务器，提供代码补全、跳转定义、错误提示。

cargo audit——安全漏洞检查：cargo install cargo-audit，然后 cargo audit 检查依赖是否有已知漏洞。

cargo watch——文件变化时自动运行命令：cargo install cargo-watch，然后 cargo watch -x test 自动运行测试。

发布 crate 到 crates.io：

注册 crates.io 账号，然后 cargo login 登录。

完善 Cargo.toml：

[package]
name = "my-awesome-crate"
version = "0.1.0"
edition = "2021"
description = "做某件很棒的事情"
license = "MIT OR Apache-2.0"
repository = "https://github.com/yourname/my-awesome-crate"
keywords = ["keyword1", "keyword2"]
categories = ["web-programming"]
readme = "README.md"

运行 cargo publish 发布。使用语义化版本：修复 bug 改 patch 版本，新功能改 minor 版本，破坏性变更改 major 版本。


让我们系统地讲一下 Rust 测试的更多进阶内容和开发工具的深度使用。

测试组织结构的最佳实践：

一个完整的 Rust 项目通常有三层测试：

第一层，单元测试：在 src/ 目录的每个文件里，用 #[cfg(test)] mod tests 组织。测试私有函数，验证最小单元的正确性。

第二层，集成测试：在 tests/ 目录里，每个文件是独立的 crate，只测试公开 API。模拟真实用户使用场景。

第三层，端到端测试：对于 Web 服务，用 reqwest 或者 httpc-test 对启动的服务发 HTTP 请求。测试完整的请求-响应链路，包括中间件、数据库、认证。

端到端测试的 Axum 示例：

#[tokio::test]
async fn test_create_post_api() {
    // 启动测试服务器
    let listener = TcpListener::bind("127.0.0.1:0").await.unwrap();
    let addr = listener.local_addr().unwrap();

    let pool = create_test_db().await;
    let app = create_app(pool.clone());

    tokio::spawn(async move {
        axum::serve(listener, app).await.unwrap();
    });

    // 先登录获取 token
    let client = reqwest::Client::new();
    let login_res = client
        .post(format!("http://{}/api/auth/login", addr))
        .json(&json!({ "email": "test@example.com", "password": "password" }))
        .send()
        .await
        .unwrap();

    let token = login_res.json::<serde_json::Value>().await.unwrap()
        ["token"].as_str().unwrap().to_string();

    // 创建文章
    let create_res = client
        .post(format!("http://{}/api/posts", addr))
        .bearer_auth(&token)
        .json(&json!({ "title": "测试文章", "content": "内容" }))
        .send()
        .await
        .unwrap();

    assert_eq!(create_res.status(), 201);
    let post: serde_json::Value = create_res.json().await.unwrap();
    assert_eq!(post["title"], "测试文章");
}

测试覆盖率——用 cargo-llvm-cov：

cargo install cargo-llvm-cov
cargo llvm-cov --html --open

生成 HTML 格式的覆盖率报告，清楚地看到哪些代码还没被测试到。目标是核心业务逻辑的覆盖率 80% 以上。

测试辅助工具——fixtures 和 factories：

重复创建测试数据很繁琐，可以创建 Factory 函数：

// tests/helpers/factories.rs
pub async fn create_test_user(pool: &PgPool) -> User {
    let email = format!("test_{}@example.com", Uuid::new_v4());
    create_user(pool, &email, "testuser", "hashed_password")
        .await
        .unwrap()
}

pub async fn create_test_post(pool: &PgPool, author: &User) -> Post {
    create_post(pool, author.id, "测试文章", "内容")
        .await
        .unwrap()
}

测试里用 let user = create_test_user(&pool).await，简洁地创建测试数据，不需要在每个测试里重复写所有字段。

Snapshot 测试——用 insta 库：

cargo add --dev insta

#[test]
fn test_format_error_message() {
    let error = AppError::NotFound("用户 123".into());
    let message = format!("{}", error);
    insta::assert_snapshot!(message); // 第一次运行时会创建 snapshot 文件
}

第一次运行生成 snapshot 文件，之后每次运行和 snapshot 对比。如果输出变化，测试失败，你需要手动 cargo insta review 来决定是接受新的 snapshot 还是修复 bug。适合测试复杂的格式化输出。

Cargo 的更多有用命令和工具：

cargo tree 查看依赖树，帮助理解哪些传递依赖被引入了：cargo tree --duplicates 找出被多个版本引入的重复依赖。

cargo deny 检查许可证合规和安全问题：deny.toml 里配置哪些许可证允许，哪些不允许，在 CI 里保证所有依赖的许可证都是可接受的。

cargo-expand 展开宏，帮助理解宏生成了什么代码：cargo expand --bin my-app，看到 #[derive(Serialize)] 展开后的代码，对调试宏相关问题很有帮助。

cargo-udeps 找出未使用的依赖：cargo +nightly udeps，帮你清理 Cargo.toml 里不再使用的依赖，减小编译时间和二进制大小。

rust-analyzer 的高级功能：除了基本的代码补全，rust-analyzer 还提供内联类型提示（在变量名旁边显示推断的类型）、引用计数（每个函数被调用了多少次）、快速修复（自动实现 Trait、自动 import）、代码动作（提取函数、内联变量、添加缺失的 match arm）。

CI/CD 中的测试最佳实践：

并行运行测试——cargo test 默认就并行运行测试，但 SQLx 的数据库测试需要隔离，用 #[sqlx::test] 的自动隔离机制。

测试超时——默认 cargo test 的单个测试没有超时，容易因为网络问题卡住。可以设置全局超时：

[profile.test]
# 没有内置超时支持，用 tokio::time::timeout 包裹
# 或者用 cargo-nextest（下面讲）

cargo-nextest 是 cargo test 的替代品，提供更丰富的功能：更快的并行执行，更好的输出格式，内置超时支持，重试失败的测试，测试结果的 JUnit XML 输出（用于 CI 报告）：

cargo install cargo-nextest
cargo nextest run --test-threads 8 --retries 2 --timeout 30

在 GitHub Actions 里用 nextest 替代 cargo test，CI 输出更清晰，失败更容易定位。


最后补充一些工具链的实用技巧，这些在日常开发中非常有价值。

cargo workspace 的高效管理：

在 monorepo 里，Cargo workspace 让多个 crate 共享 Cargo.lock 和编译缓存。workspace 级别的 Cargo.toml 可以设置共享的依赖版本：

# 根目录 Cargo.toml
[workspace.dependencies]
tokio = { version = "1", features = ["full"] }
serde = { version = "1", features = ["derive"] }
axum = "0.8"

# 各子 crate 的 Cargo.toml
[dependencies]
tokio.workspace = true  # 使用 workspace 里定义的版本
serde.workspace = true

这确保所有子 crate 用完全相同版本的依赖，避免同一个库的多个版本被编译进最终二进制。

条件编译的实际应用：

#[cfg(feature = "postgres")]
pub mod postgres_backend;

#[cfg(feature = "sqlite")]
pub mod sqlite_backend;

#[cfg(target_os = "linux")]
fn get_system_info() -> String {
    // Linux 专有实现
    std::fs::read_to_string("/proc/version").unwrap_or_default()
}

#[cfg(target_os = "macos")]
fn get_system_info() -> String {
    // macOS 专有实现
    "macOS".to_string()
}

条件编译让同一份代码可以支持不同数据库后端、不同操作系统，在编译时选择正确的实现，运行时没有任何多余代码。


让我再聊一聊 Rust 测试文化和前端测试文化的异同，这对你建立正确的测试习惯很有帮助。

前端工程师通常有这样的测试观念：单元测试测组件逻辑，集成测试测页面流程，E2E 测试（用 Playwright 或者 Cypress）测真实用户操作。Rust 的测试分层和这个很类似，但重心不太一样。

在 Rust 生态里，单元测试的比重更大，因为 Rust 的纯函数非常适合单元测试。一个接受输入、返回输出、没有副作用的纯函数，单元测试最简单最可靠。Rust 的不可变默认、所有权系统等特性天然倾向于写出更多纯函数，让单元测试更容易。

测试驱动开发（TDD）在 Rust 里也很流行，而且比在 JavaScript 里更舒适，因为：编译器已经帮你排查了很多错误，测试专注于业务逻辑的正确性；测试失败时错误信息非常清晰，assert_eq! 会显示左右两边的值；代码重构时，类型系统帮你发现受影响的地方，测试验证行为没变。

关于测试的运行速度，Rust 的测试编译后是原生代码，运行非常快。即使你有几千个单元测试，通常几秒钟就能跑完。这和 Jest 在 Node.js 上运行几千个测试需要几分钟形成鲜明对比。

但要注意：Rust 的测试编译本身可能需要一段时间（首次编译最慢，之后有增量编译）。cargo-nextest 的一个优势是更好地利用增量编译，减少不必要的重编译。

一个关于 Rust 测试的建议：测试函数的命名要清晰地描述测试的场景，而不只是被测函数的名字。比如 test_parse_valid_email 不如 test_valid_email_format_accepted，test_auth_failure 不如 test_expired_jwt_returns_401。好的测试名字本身就是文档。

关于 CI/CD 中的测试策略，我推荐以下实践：

在 PR 阶段，运行所有单元测试和集成测试。速度要快，如果超过 5 分钟开发者会失去耐心。可以并行化：编译不同的测试二进制，分开运行。

在合并到主分支后，运行更完整的测试套件，包括 E2E 测试和性能基准测试。这些测试可以慢一点，但要全面。

数据库测试的隔离策略：每个测试用独立的事务（sqlx::test 的默认行为），测试结束后自动回滚；或者每个测试用独立的数据库（重型隔离，更慢但更彻底）。对于大多数场景，事务隔离就足够了。

关于测试的可读性，一个有用的模式是 Given-When-Then：

每个测试分三个部分：Given（准备测试数据和环境）、When（执行被测代码）、Then（断言结果）。用空行或者注释分开这三个部分，让测试的意图一目了然。

比如测试"文章创建"功能：Given，先创建一个用户，创建一个认证令牌；When，用这个令牌调用创建文章接口；Then，验证接口返回 201，验证数据库里有这篇文章，验证文章的作者是刚创建的用户。这样组织的测试，即使代码变化了，测试的意图也清晰可见。

这章总结：#[test] 标记测试函数，#[cfg(test)] 标记测试模块；集成测试放在 tests 目录；#[tokio::test] 测试异步代码；assert_eq!、assert! 等宏做断言；cargo test 运行测试，cargo bench 运行基准测试；文档测试保证示例代码正确；clippy 提供更严格的检查，fmt 统一代码风格；发布到 crates.io 需要完善的元数据。

下一章：DevOps——Docker 多阶段构建把 Rust 服务打包成 20MB 的镜像，GitHub Actions 自动化 CI/CD。下章见。
"""

SCRIPTS[13] = """
欢迎来到第十三章：DevOps——Docker 容器化与 CI/CD 自动化。

Rust 编译出的是单一静态二进制文件，没有运行时依赖。这让容器化极其简单和高效：

Node.js 镜像：基础镜像 100MB 加上 node 运行时 50MB 再加 node_modules 几百 MB，总共可能 400MB。Rust 镜像：从 scratch 基础镜像加上单个二进制文件，10 到 20MB。

这不是一点点差距，在大规模部署时意味着显著更低的云存储费用、更快的镜像拉取速度、更低的攻击面。

Docker 多阶段构建——核心技巧。

Rust 编译需要完整工具链，大约 2GB，但运行只需要编译出的二进制，大约 5-20MB。多阶段构建分离编译和运行：

# Dockerfile
# ── 阶段 1：编译 ───────────────────────────────
FROM rust:1.78-slim AS builder

WORKDIR /app

# 利用 Docker 层缓存：先复制依赖文件
# 只有 Cargo.toml 或 Cargo.lock 变化时才重新下载依赖
COPY Cargo.toml Cargo.lock ./
RUN mkdir src && echo "fn main() {}" > src/main.rs
RUN cargo build --release
RUN rm -rf src

# 再复制真正的源码
COPY src ./src
RUN touch src/main.rs && cargo build --release

# ── 阶段 2：运行时镜像 ─────────────────────────
FROM debian:bookworm-slim AS runtime

# 只安装必要的运行时依赖
RUN apt-get update &&     apt-get install -y ca-certificates &&     rm -rf /var/lib/apt/lists/*

# 安全最佳实践：非 root 用户运行
RUN useradd -m appuser
USER appuser

WORKDIR /app
COPY --from=builder /app/target/release/blog-api .

EXPOSE 3000
CMD ["./blog-api"]

这里有个重要的优化技巧：先复制 Cargo.toml 和 Cargo.lock，创建一个虚假的 main.rs，运行 cargo build 只编译依赖。这样以后只要依赖没变，这一层会命中缓存，不需要重新下载和编译依赖，大幅加快 CI 速度。

更极致的方案：使用 cargo-chef 工具，它专门优化 Docker 层缓存：

FROM lukemathwalker/cargo-chef:latest-rust-1 AS chef
WORKDIR /app

FROM chef AS planner
COPY . .
RUN cargo chef prepare --recipe-path recipe.json

FROM chef AS builder
COPY --from=planner /app/recipe.json recipe.json
RUN cargo chef cook --release --recipe-path recipe.json
COPY . .
RUN cargo build --release --bin blog-api

FROM debian:bookworm-slim AS runtime
# ...跟之前一样

cargo-chef 让 Dockerfile 更简洁，也更可靠地利用层缓存。

Docker Compose 用于本地开发：

version: "3.9"

services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: rustforge
      POSTGRES_PASSWORD: development
      POSTGRES_DB: rustforge_db
    ports: ["5432:5432"]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U rustforge"]
      interval: 5s
      retries: 5
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: ./backend
    ports: ["3001:3000"]
    environment:
      DATABASE_URL: postgres://rustforge:development@postgres:5432/rustforge_db
    depends_on:
      postgres:
        condition: service_healthy

volumes:
  postgres_data:

运行 docker compose up -d 一键启动完整开发环境。

GitHub Actions CI/CD：

name: CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env: { POSTGRES_PASSWORD: test, POSTGRES_DB: test_db }
        ports: ["5432:5432"]
        options: --health-cmd pg_isready --health-interval 10s

    steps:
      - uses: actions/checkout@v4
      
      - name: Install Rust
        uses: dtolnay/rust-toolchain@stable
        with:
          components: clippy, rustfmt
      
      # 缓存编译产物，大幅加速后续 CI
      - name: Cache
        uses: Swatinem/rust-cache@v2
      
      - name: Lint
        run: |
          cargo fmt --check
          cargo clippy -- -D warnings
      
      - name: Test
        env:
          DATABASE_URL: postgres://postgres:test@localhost/test_db
        run: cargo test

  build-and-push:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Login to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

Kubernetes 基础配置：

apiVersion: apps/v1
kind: Deployment
metadata:
  name: blog-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: blog-api
  template:
    spec:
      containers:
        - name: blog-api
          image: ghcr.io/your-org/blog-api:latest
          ports:
            - containerPort: 3000
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: db-secret
                  key: url
          resources:
            requests:
              cpu: "100m"
              memory: "64Mi"    # Rust 内存占用极低
            limits:
              cpu: "500m"
              memory: "128Mi"   # Node.js 通常需要 256-512Mi
          readinessProbe:
            httpGet:
              path: /health
              port: 3000

Rust 服务的内存限制可以设得远比 Node.js 低，在大规模集群里这意味着显著的云成本节省。

健康检查端点——生产必备：

async fn health() -> Json<serde_json::Value> {
    Json(json!({
        "status": "ok",
        "version": env!("CARGO_PKG_VERSION"),
        "timestamp": chrono::Utc::now()
    }))
}

优雅关闭——确保处理完所有请求才退出：

axum::serve(listener, app)
    .with_graceful_shutdown(shutdown_signal())
    .await?;

async fn shutdown_signal() {
    tokio::signal::ctrl_c().await.expect("安装 Ctrl+C 失败");
}

结构化日志——Kubernetes 友好：

tracing_subscriber::fmt()
    .with_env_filter("info")
    .json() // JSON 格式，适合日志聚合系统
    .init();

RUST_LOG=blog_api=debug,sqlx=warn cargo run 控制日志级别。


让我们深入讲一下容器化和 CI/CD 的更多实战细节。

首先是 Rust 的交叉编译，这在 CI/CD 里很常见。

如果你在 macOS 上开发但要部署到 Linux，或者要为多种架构（x86_64、ARM64）构建二进制，需要交叉编译。

用 cross 工具简化交叉编译：

cargo install cross
cross build --release --target aarch64-unknown-linux-gnu

cross 内部使用 Docker 容器提供交叉编译环境，不需要你手动安装目标平台的工具链。

在 GitHub Actions 里发布多架构 Docker 镜像：

- name: Set up QEMU
  uses: docker/setup-qemu-action@v3

- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v3

- name: Build and push multi-arch
  uses: docker/build-push-action@v5
  with:
    platforms: linux/amd64,linux/arm64
    push: true
    tags: ghcr.io/${{ github.repository }}:latest

这样构建出来的镜像在 x86_64 的云服务器和 ARM64 的 Apple M 系列或 AWS Graviton 上都能运行。

Distroless 镜像——比 Debian slim 更小更安全：

FROM gcr.io/distroless/cc-debian12 AS runtime
COPY --from=builder /app/target/release/blog-api /
EXPOSE 3000
CMD ["/blog-api"]

Distroless 镜像里只有运行时库，没有 shell，没有包管理器，攻击面极小。但调试更困难，建议在生产用 Distroless，开发和 staging 用 debian-slim。

最终的镜像大小：debian-slim 基础 + Rust 二进制 ≈ 80MB；Distroless 基础 + Rust 二进制 ≈ 30MB；scratch（完全静态编译）+ Rust 二进制 ≈ 10MB。

完全静态编译（scratch 镜像）需要 musl 目标：

rustup target add x86_64-unknown-linux-musl
RUSTFLAGS="-C target-feature=+crt-static" cargo build --release --target x86_64-unknown-linux-musl

FROM scratch
COPY --from=builder /app/target/x86_64-unknown-linux-musl/release/blog-api /blog-api
CMD ["/blog-api"]

注意 musl 的静态编译有一些限制：DNS 解析使用静态 resolver 而不是系统的，某些场景下有差异。如果用了动态链接的 C 库（比如某些加密库），可能无法完全静态化。

GitHub Actions 的高级优化技巧：

分布式缓存——不只是编译缓存，还要缓存 cargo registry：

- uses: Swatinem/rust-cache@v2
  with:
    cache-all-crates: true      # 缓存所有 crate 包
    save-if: ${{ github.ref == 'refs/heads/main' }} # 只在 main 分支保存缓存

缓存策略：PR 共享 main 的缓存（只读），main 构建后更新缓存。这样 PR 的构建能利用缓存加速，但不会污染主缓存。

并行化 CI 步骤——把 lint、test、build 并行：

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - run: cargo fmt --check && cargo clippy -- -D warnings

  test:
    runs-on: ubuntu-latest
    steps:
      - run: cargo test

  build:
    needs: [lint, test]    # 只有 lint 和 test 通过才构建
    runs-on: ubuntu-latest
    steps:
      - run: docker build -t myapp .

lint 和 test 并行运行，都通过后才构建镜像，减少总 CI 时间。

在 Kubernetes 里管理数据库迁移：

数据库迁移不应该在应用启动时自动运行（多副本同时迁移会有问题），应该作为独立的 Job 在部署前运行：

apiVersion: batch/v1
kind: Job
metadata:
  name: db-migrate
spec:
  template:
    spec:
      containers:
        - name: migrate
          image: ghcr.io/your-org/blog-api:latest
          command: ["sqlx", "migrate", "run"]
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: db-secret
                  key: url
      restartPolicy: Never

在 Helm chart 或者 Argo CD 里配置 pre-sync hook 运行迁移 Job，确保迁移在应用 Deployment 更新之前完成。

环境变量管理——Kubernetes Secrets vs 外部 Secret 管理：

小项目：直接用 Kubernetes Secrets，注意 base64 编码不是加密；中大项目：用 External Secrets Operator 从 AWS Secrets Manager、HashiCorp Vault、或者 GCP Secret Manager 同步到 Kubernetes Secret；生产最佳实践：Sealed Secrets 或者 SOPS 加密 Secret 后提交到 Git，安全地实现 GitOps。


让我们聊一聊 DevOps 实践的更多深度内容，以及 Rust 在部署运维方面独特的优势。

首先我想谈谈 Rust 服务在云原生环境中的资源特点，这对你规划基础设施成本非常重要。

一个典型的 Node.js Express 服务，即使是一个简单的 Hello World API，运行时的内存占用通常在 50-100MB 之间（Node.js 运行时本身就要占这么多）。当你加上业务代码、依赖库、数据库连接池，实际内存往往在 256MB 到 512MB 之间。

一个等价的 Rust Axum 服务，运行时内存通常在 20-50MB 之间，包括所有业务代码和连接池。这不是因为 Rust 代码"省内存"，而是因为 Rust 没有虚拟机运行时的开销，内存使用更精确，只为真正需要的数据分配内存。

这个差距在 Kubernetes 里意味着：每个 Pod 的内存 request 可以设得更小，同样的节点可以运行更多 Pod，节省真实的云费用。如果你有 100 个微服务，每个服务节省 200MB 内存，总共节省 20GB，在大多数云平台上这意味着可观的月度费用节省。

CPU 的情况也类似。Rust 服务在空闲时几乎不消耗 CPU（没有 GC 暂停，没有 JIT 预热）。在有请求时，CPU 效率更高（原生机器码，无解释器开销）。在 Kubernetes 里，CPU limit 可以设得更低，提高整个集群的 CPU 利用率。

启动时间也是 Rust 的一个显著优势。Node.js 服务通常需要 2-10 秒才能准备就绪（加载模块、JIT 预热）。Rust 服务通常在 100ms 以内就绪（直接是机器码，没有预热阶段）。在 Kubernetes 的滚动部署场景，快速启动意味着新版本更快上线，旧版本更快下线，整个部署过程对用户的影响更小。

在 Serverless 平台（Cloudflare Workers、AWS Lambda、Fly.io Machines）上，启动时间尤为重要。Node.js 在 Lambda 上的冷启动通常是几百毫秒到几秒；Rust 编译成 WASM 的 Cloudflare Worker 冷启动通常小于 50ms。对于需要全球低延迟的应用（比如 API 网关、认证服务），Rust 是不二选择。

说到 Cloudflare Workers，这是一个值得深入了解的部署平台。Cloudflare 有遍布全球的 300+ 个节点，你的代码会在离用户最近的节点上运行。这是真正的"边缘计算"。

Rust 通过 worker-rs crate 可以方便地开发 Cloudflare Workers：

在 wrangler.toml 里配置好项目后，cargo component build --release 编译，wrangler deploy 部署。你的 Rust 代码以 WASM 形式运行在 Cloudflare 的边缘节点上，全球延迟通常在 5-20ms 以内。

Workers 有一些限制：不支持持久化文件系统（用 KV 存储或者 R2 对象存储）；不支持传统的 TCP 数据库连接（用 Cloudflare D1 SQLite 或者 Hyperdrive 代理到 PostgreSQL）；每次请求有 CPU 时间限制（免费计划 10ms，付费计划 50ms，大多数 API 请求完全够用）。

对于全球化的应用，可以考虑混合架构：用 Cloudflare Workers 处理认证、路由、静态资源；主要的业务逻辑部署在普通的云服务器上，Workers 作为全球入口把请求代理到最近的服务器。

关于可观测性（Observability），这是现代 DevOps 的核心概念。可观测性包括三个支柱：日志（Logs）、指标（Metrics）、链路追踪（Traces）。

Rust 的 tracing 生态对这三个支柱都有很好的支持：

tracing 库提供结构化日志和 span（链路追踪的基本单元）；tracing-subscriber 把 span 和日志输出到不同的目的地；opentelemetry 和 opentelemetry-otlp 把链路追踪数据发送到 Jaeger、Zipkin、或者云厂商的追踪服务（比如 AWS X-Ray、Google Cloud Trace）；prometheus crate 导出 Prometheus 指标，结合 Grafana 做仪表盘。

一个结合了所有这些的初始化代码：在 main 函数里配置 tracing_subscriber，同时输出 JSON 日志和 OpenTelemetry traces，然后注册一个 /metrics 接口暴露 Prometheus 指标。这些配置好之后，你就有了完整的可观测性能力，出了问题可以快速定位。

关于数据库的可观测性，每条 SQL 查询都应该记录执行时间。SQLx 本身不自动记录，但你可以用 sqlx::sqlite::SqliteConnection 的 trace 方法或者自己包装一层。更简单的方案是直接在 PostgreSQL 里开启 pg_stat_statements 扩展，记录所有慢查询。

最后讲一下灾难恢复（DR）策略。备份策略：数据库每天完整备份，每小时增量备份，备份文件存到不同地理位置的对象存储（比如 S3）；定期验证备份可恢复性，"没有测试过的备份不是备份"。

回滚策略：每次部署保留上一个版本的镜像；数据库迁移必须有对应的回滚迁移；用蓝绿部署或者金丝雀发布，可以快速切换回旧版本。这些都是生产级服务必备的工程能力。

这章总结：Docker 多阶段构建让 Rust 镜像只有 10-20MB；先编译依赖再编译代码利用 Docker 层缓存；cargo-chef 进一步优化缓存；GitHub Actions 配合 Swatinem/rust-cache 大幅加速 CI；Rust 服务在 Kubernetes 里内存限制可设极低；健康检查和优雅关闭是生产必备。

下一章：性能优化和 unsafe Rust——如何用 unsafe 做真正的底层操作，以及 Rust 的性能调优技巧。下章见。
"""

SCRIPTS[14] = """
欢迎来到第十四章：性能优化与 unsafe Rust。

Rust 号称零成本抽象，但零成本不等于自动最快。这章我们讲如何真正榨出 Rust 的性能，以及在必要时如何用 unsafe 做底层操作。

先说性能分析，不测量就不要优化。

最常用的 Rust profiler 是 cargo-flamegraph：

cargo install flamegraph
cargo flamegraph --bin my-app

生成火焰图，直观看出哪里耗时最多。

也可以用 criterion 做微基准测试，我们上章讲过。

基本优化原则：

第一，选择正确的数据结构。HashMap 的查找是 O(1)，Vec 的查找是 O(n)，BTreeMap 的查找是 O(log n)。高频查找用 HashMap，需要有序用 BTreeMap，随机访问的集合用 Vec。

第二，避免不必要的克隆和分配。clone() 是昂贵的，能用引用就用引用。避免在循环里 String::new() 然后 push_str，尽量用 format! 一次构建。

第三，使用迭代器而不是索引循环。迭代器可以被编译器向量化（SIMD 指令），手写索引循环通常不能。

第四，release 构建和 debug 构建性能差异巨大。Cargo.toml 里可以调整优化级别：

[profile.release]
opt-level = 3      # 默认，最高优化
lto = "fat"        # 链接时优化（编译更慢，运行更快）
codegen-units = 1  # 单个代码生成单元（编译更慢，运行更快）

第五，使用 Rayon 并行化 CPU 密集型工作：

use rayon::prelude::*;

// 串行
let sum: i64 = data.iter().map(|x| expensive(x)).sum();

// 并行（改一个方法就行）
let sum: i64 = data.par_iter().map(|x| expensive(x)).sum();

Rayon 自动用线程池并行化迭代器操作。

现在讲 unsafe Rust。

unsafe 关键字不是说"这段代码不安全，不用管"，而是说"编译器无法验证这段代码的安全性，我作为程序员来保证它的正确性"。

unsafe 让你做五件在 safe Rust 里不能做的事：解引用裸指针，调用 unsafe 函数，访问或修改可变静态变量，实现 unsafe Trait，访问 union 字段。

裸指针——unsafe Rust 最常用的场景：

let x = 5;
let raw = &x as *const i32; // 不可变裸指针
let raw_mut = &mut 5 as *mut i32; // 可变裸指针

// 只在 unsafe 块里才能解引用
unsafe {
    println!("{}", *raw);
}

裸指针不受借用规则约束，可以同时有多个可变裸指针，可以是 null，可以指向已释放的内存。这就是为什么解引用需要 unsafe——你要自己保证安全。

实际的 unsafe 使用场景：

FFI（Foreign Function Interface）——调用 C 库：

extern "C" {
    fn abs(input: i32) -> i32; // 声明 C 函数
}

unsafe {
    println!("{}", abs(-5));
}

用 cbindgen 或 bindgen 自动生成 FFI 绑定。

内存映射文件——大文件处理的高性能方式：

use memmap2::MmapOptions;

let file = File::open("large.bin")?;
let mmap = unsafe { MmapOptions::new().map(&file)? };
// 像访问内存一样访问文件内容
println!("{}", mmap[0]);

实现零拷贝操作：unsafe 允许你在不复制数据的情况下改变类型视图，比如把 u8 数组视为 i32 数组。当然这需要非常小心字节序和对齐。

自定义分配器——对特定场景的极致优化：

use std::alloc::{GlobalAlloc, Layout, System};

// 用 jemalloc 替换默认分配器，在高并发下通常更快
#[global_allocator]
static GLOBAL: tikv_jemallocator::Jemalloc = tikv_jemallocator::Jemalloc;

unsafe 代码的最佳实践：最小化 unsafe 的范围，把 unsafe 操作封装在安全的接口后面，详细注释为什么这段 unsafe 是正确的，用 Miri 工具检测 unsafe 代码里的未定义行为（cargo +nightly miri test）。

字符串和 IO 性能优化：用 BufWriter 和 BufReader 包裹 IO，批量读写减少系统调用次数；对于大量字符串操作，考虑用 SmallVec 避免小集合的堆分配；用 Cow<str> 避免不必要的字符串克隆。

SIMD——手动向量化：对于计算密集型任务，可以用 std::arch 或者 wide crate 用 SIMD 指令：

use std::arch::x86_64::*;

unsafe {
    let a = _mm256_set_epi32(1,2,3,4,5,6,7,8);
    let b = _mm256_set_epi32(1,2,3,4,5,6,7,8);
    let sum = _mm256_add_epi32(a, b);
    // 一次操作 8 个 i32 的加法
}

但大多数情况下，写好的迭代器代码，LLVM 会自动 auto-vectorize，不需要手动 SIMD。


让我们深入讲一下性能优化的更多实战技巧，以及 unsafe 的更多应用场景。

首先是 Rust 的内存布局优化，这对缓存友好性影响很大。

现代 CPU 的 L1 缓存通常是 32KB，L2 是 256KB，L3 是几 MB。缓存行（cache line）通常是 64 字节。如果你的数据结构紧凑，访问模式顺序，CPU 缓存命中率高，程序就快。

用 #[repr(C)] 控制内存布局：

#[repr(C)]
struct Particle {
    position: [f32; 3],  // 12 字节
    velocity: [f32; 3],  // 12 字节
    mass: f32,           // 4 字节
    // 总共 28 字节，两个 Particle 能放进一个缓存行
}

vs. Rust 默认可能重排字段顺序来优化对齐，结果可能更大或者布局不符合预期。

结构体字段排序的影响：Rust 默认会对结构体字段重排以最小化填充（padding）字节。如果你需要特定的内存布局（比如和 C 代码的互操作），用 #[repr(C)]。如果不需要，让编译器自己优化。

用 std::mem::size_of 检查结构体大小：

println!("{}", std::mem::size_of::<Option<u8>>()); // 1 字节！（不是 2）
println!("{}", std::mem::size_of::<Option<Box<i32>>>()); // 8 字节（和 Box 一样）

Option<T> 在 T 有空值表示时（Non-Null Optimization，NNO）不需要额外字节。这是 Rust 枚举优化的经典例子。

枚举的内存大小是最大变体的大小加上 tag。可以用 Box 包裹大变体来减少枚举大小：

enum Response {
    Success(Box<LargeSuccessData>), // LargeSuccessData 在堆上，枚举只存指针
    Error(SmallErrorData),
}

String 和 Vec 的内存问题：每个 String 或 Vec 占 24 字节（栈上：指针 8 字节 + 长度 8 字节 + 容量 8 字节），加上堆上的实际数据。如果你有很多小字符串（比如枚举变体的字符串表示），考虑用 &'static str 或者 SmallString 库。

CPU 性能分析工具：

perf（Linux）：sudo perf record ./my-app && sudo perf report，精确到 CPU 指令级别。cargo-flamegraph 在底层就是用 perf。

Instruments（macOS）：Xcode 自带，支持 Time Profiler 和 Allocations 等分析器，比 perf 更直观。

Valgrind Callgrind：cargo install cargo-valgrind，cargo valgrind --bin my-app，统计函数调用次数和指令数。

内存分配分析——用 dhat-heap crate：

use dhat::{Dhat, DhatAlloc};

#[global_allocator]
static ALLOC: DhatAlloc = DhatAlloc;

fn main() {
    let _dhat = Dhat::start_heap_profiling();
    // ... 你的代码
}

程序结束时生成 dhat-heap.json，用 DHAT viewer 可视化所有堆分配，找出高频的小分配（这些通常可以用 arena 分配器或者对象池优化）。

SIMD 自动向量化的触发条件：LLVM 会尝试向量化满足以下条件的循环：循环体简单，没有依赖；数组大小已知或者足够大；没有别名（同一块内存不会被两个指针指向）。

你可以用 cargo rustc -- --emit=asm 查看汇编，用 vmovaps、vaddps 等 AVX 指令确认是否向量化了。或者用 cargo-asm 工具：cargo asm my_crate::my_function 查看特定函数的汇编。

LTO（Link Time Optimization）的效果：lto = "fat" 让编译器在链接时做全程序优化，可以跨 crate 边界内联函数。对于有很多小函数的代码（比如迭代器链），LTO 能进一步消除函数调用开销。但编译时间会显著增加（10-30% 左右）。

PGO（Profile-Guided Optimization）：先用 instrumentation build 运行收集 profile，再用 profile 数据指导优化：

# 1. 生成 instrumentation build
RUSTFLAGS="-Cprofile-generate=/tmp/pgo-data" cargo build --release
# 2. 运行并生成 profile 数据
./target/release/my-app
# 3. 合并 profile 数据
llvm-profdata merge -o /tmp/pgo-data/merged.profdata /tmp/pgo-data/
# 4. 用 profile 数据构建
RUSTFLAGS="-Cprofile-use=/tmp/pgo-data/merged.profdata" cargo build --release

PGO 能显著提升真实工作负载下的性能，有时候比标准 --release 快 10-20%，因为编译器知道哪些分支是热点，可以更好地优化。

关于 unsafe 的一些更具体的例子：

实现零拷贝反序列化（类似 serde 的 zero-copy feature）：

// 把 &[u8] 解释为 &[u32]，前提是字节对齐
fn bytes_to_u32s(bytes: &[u8]) -> &[u32] {
    assert!(bytes.len() % 4 == 0);
    assert!(bytes.as_ptr() as usize % 4 == 0); // 检查对齐
    unsafe {
        std::slice::from_raw_parts(
            bytes.as_ptr() as *const u32,
            bytes.len() / 4,
        )
    }
}

注意 unsafe 前的两个 assert!：在进入 unsafe 之前，尽可能用安全的检查来验证前提条件，缩小 unsafe 需要保证的范围。

手动内存管理的实际场景——实现一个对象池：

struct ObjectPool<T> {
    objects: Vec<T>,
    available: Vec<usize>, // 可用对象的索引
}

impl<T: Default> ObjectPool<T> {
    fn acquire(&mut self) -> (usize, &mut T) {
        let idx = self.available.pop().unwrap_or_else(|| {
            let idx = self.objects.len();
            self.objects.push(T::default());
            idx
        });
        (idx, &mut self.objects[idx])
    }

    fn release(&mut self, idx: usize) {
        self.available.push(idx);
    }
}

对象池避免了频繁的内存分配/释放，在高频创建销毁对象的场景（游戏实体、网络包、数据库连接）能显著提升性能。


让我们继续讲一些 Rust 性能优化和 unsafe 的高级话题，这在写系统级代码时很有价值。

字符串处理的性能优化是一个常见场景。Rust 的标准 String 操作已经很高效，但有时候可以做得更好：

Cow<str>（Clone on Write）我们在第七章提到过，它在字符串处理里特别有用。比如你有个函数需要根据条件返回原始字符串或者修改过的字符串：

use std::borrow::Cow;

fn sanitize_username(name: &str) -> Cow<str> {
    if name.chars().all(|c| c.is_alphanumeric() || c == '_') {
        // 无需修改，返回对原字符串的借用
        Cow::Borrowed(name)
    } else {
        // 需要修改，只在此时分配内存
        let cleaned: String = name.chars()
            .filter(|c| c.is_alphanumeric() || *c == '_')
            .collect();
        Cow::Owned(cleaned)
    }
}

如果用户名已经合法（大多数情况），这个函数零内存分配。只有不合法时才分配。

紧凑字符串类型——用 compact_str 或者 smol_str 库：

标准 String 占 24 字节（3 个 usize），对于短字符串（小于等于 22 字节的 UTF-8）可以用 SSO（Short String Optimization），内联存储在结构体里，不需要堆分配。

compact_str 和 smol_str 实现了这个优化：

use compact_str::CompactString;

let s: CompactString = "hello".into(); // 无堆分配
let heap: CompactString = "这是一个很长的字符串，超过了内联缓冲区".into(); // 堆分配

对于存储大量短字符串的场景（比如词典、配置键），这可以显著减少内存占用和分配次数。

正则表达式的性能——预编译正则：

正则表达式的编译是昂贵的，不要在循环里重复编译：

// 错误方式——每次调用都编译正则
fn is_email(s: &str) -> bool {
    let re = regex::Regex::new(r"^[\\w.+-]+@[\\w-]+\\.[a-z]{2,}$").unwrap();
    re.is_match(s)
}

// 正确方式——用 once_cell 懒初始化
use once_cell::sync::Lazy;

static EMAIL_RE: Lazy<regex::Regex> = Lazy::new(|| {
    regex::Regex::new(r"^[\\w.+-]+@[\\w-]+\\.[a-z]{2,}$").unwrap()
});

fn is_email(s: &str) -> bool {
    EMAIL_RE.is_match(s)
}

once_cell::sync::Lazy 只在第一次访问时初始化，之后重复使用编译好的正则，无锁访问。

哈希算法的选择也影响性能：

Rust 标准库的 HashMap 默认用 SipHash，抗 DoS 攻击（哈希洪水攻击），但不是最快的。如果你的 HashMap 键来自可信源（不接受用户输入作为键），可以用更快的哈希算法：

use ahash::AHashMap; // 或者 rustc_hash::FxHashMap

let mut map: AHashMap<String, i32> = AHashMap::new();
// 和标准 HashMap 接口完全一样，但通常快 2-5 倍

ahash 使用 AES 硬件指令实现高速哈希，在 x86_64 上几乎没有计算开销。

内存池分配器 bumpalo：

对于生命周期相同的一批对象，用 arena 分配器可以极大提升性能——分配 O(1)，释放整个 arena 也是 O(1)，不需要逐个释放：

use bumpalo::Bump;

fn process_request(request_data: &[u8]) {
    let arena = Bump::new(); // 创建 arena

    // 在这次请求处理期间的所有临时对象都从 arena 分配
    let parsed = arena.alloc(parse_request(request_data, &arena));
    let result = arena.alloc(process(parsed, &arena));
    serialize(result);

    // 函数结束时，arena 被 drop，所有对象一次性释放
    // 没有逐个调用 drop，极快
}

这在 Web 框架的请求处理、编译器、游戏的每帧处理等场景里非常有效。每次请求用一个新 arena，处理完毕整体释放，内存碎片为零。

最后说一下 Miri——检测 unsafe 代码的工具：

Miri 是 Rust 的解释器，能检测 unsafe 代码里的未定义行为，包括：使用未初始化内存，越界访问，违反 Rust 引用规则（比如从 &T 创建 &mut T），数据竞争的 happens-before 违规。

cargo +nightly miri test 运行你的测试，如果有 unsafe 相关的 UB，Miri 会精确报告出来。编写 unsafe 代码后，一定要跑 Miri，它能发现很多难以用普通测试发现的问题。

这章总结：先测量再优化，用 flamegraph 找热点；选对数据结构，避免不必要的克隆；Rayon 一行代码并行化迭代器；release 构建加 LTO 榨取极致性能；unsafe 是精确的安全边界，而不是关闭安全检查；unsafe 主要用于 FFI、裸指针操作、内存映射；最小化 unsafe 范围并用注释说明安全理由。

下一章：命令行工具与 WebAssembly——Rust 打包成 CLI 工具和跑在浏览器里的 WASM 模块。下章见。
"""

SCRIPTS[15] = """
欢迎来到第十五章：命令行工具与 WebAssembly。

这章覆盖 Rust 的两个有趣方向：用 Rust 写高性能命令行工具，以及把 Rust 编译成 WebAssembly 跑在浏览器里。

先讲命令行工具。

Rust 非常适合写 CLI 工具：单一二进制文件，无需安装运行时，启动速度极快，性能远超 Node.js 脚本。很多知名 CLI 工具都是 Rust 写的：ripgrep、fd、bat、exa、tokei、hyperfine。

最流行的 CLI 库是 clap（Command Line Argument Parser）：

Cargo.toml 加 clap = { version = "4", features = ["derive"] }。

use clap::{Parser, Subcommand};

#[derive(Parser)]
#[command(name = "my-tool")]
#[command(about = "我的命令行工具", version)]
struct Cli {
    #[arg(short, long, action = clap::ArgAction::Count)]
    verbose: u8,
    
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// 搜索文件
    Search {
        /// 搜索关键词
        pattern: String,
        
        /// 搜索目录
        #[arg(default_value = ".")]
        path: std::path::PathBuf,
        
        /// 忽略大小写
        #[arg(short, long)]
        ignore_case: bool,
    },
    
    /// 统计行数
    Count {
        files: Vec<std::path::PathBuf>,
    },
}

fn main() {
    let cli = Cli::parse();
    
    match cli.command {
        Commands::Search { pattern, path, ignore_case } => {
            do_search(&pattern, &path, ignore_case);
        }
        Commands::Count { files } => {
            do_count(&files);
        }
    }
}

clap 的 derive 特性让你用结构体定义命令行接口，自动生成 --help 文档，自动解析参数和验证类型，自动生成错误信息。

用 indicatif 添加进度条：

use indicatif::{ProgressBar, ProgressStyle};

let pb = ProgressBar::new(total_files);
pb.set_style(ProgressStyle::with_template(
    "{spinner:.green} [{elapsed}] [{bar:40.cyan/blue}] {pos}/{len} {msg}"
)?);

for file in files {
    pb.set_message(file.display().to_string());
    process_file(file);
    pb.inc(1);
}
pb.finish_with_message("完成");

用 colored 添加彩色输出：

use colored::Colorize;

println!("{} {}", "错误:".red().bold(), message);
println!("{} {}", "成功:".green(), result);

配置文件处理用 config crate，或者直接用 serde 反序列化 TOML/JSON/YAML 文件。

接下来讲 WebAssembly——这是前端工程师最感兴趣的部分。

WebAssembly（WASM）让你把 Rust 代码编译成在浏览器里运行的二进制模块。这意味着：

性能密集型任务（图像处理、加密、数据分析）可以用 Rust 实现，比 JavaScript 快 10-50 倍；可以把整个 Rust 库暴露给 JavaScript 调用；Rust 的类型安全在 WASM 边界上也能体现。

安装工具：rustup target add wasm32-unknown-unknown 添加 WASM 编译目标；cargo install wasm-pack 安装 WASM 打包工具。

创建一个 WASM 库：

cargo new --lib my-wasm-lib，修改 Cargo.toml：

[lib]
crate-type = ["cdylib"] # 编译成动态库，WASM 需要

[dependencies]
wasm-bindgen = "0.2"
web-sys = { version = "0.3", features = ["console"] }
js-sys = "0.3"

src/lib.rs：

use wasm_bindgen::prelude::*;

// #[wasm_bindgen] 标记暴露给 JavaScript 的函数
#[wasm_bindgen]
pub fn fibonacci(n: u32) -> u32 {
    match n {
        0 => 0,
        1 => 1,
        _ => fibonacci(n - 1) + fibonacci(n - 2),
    }
}

#[wasm_bindgen]
pub struct ImageProcessor {
    data: Vec<u8>,
    width: u32,
    height: u32,
}

#[wasm_bindgen]
impl ImageProcessor {
    #[wasm_bindgen(constructor)]
    pub fn new(data: Vec<u8>, width: u32, height: u32) -> ImageProcessor {
        ImageProcessor { data, width, height }
    }
    
    pub fn grayscale(&mut self) {
        for i in (0..self.data.len()).step_by(4) {
            let r = self.data[i] as f32;
            let g = self.data[i + 1] as f32;
            let b = self.data[i + 2] as f32;
            let gray = (0.299 * r + 0.587 * g + 0.114 * b) as u8;
            self.data[i] = gray;
            self.data[i + 1] = gray;
            self.data[i + 2] = gray;
        }
    }
    
    pub fn get_data(&self) -> Vec<u8> {
        self.data.clone()
    }
}

编译：wasm-pack build --target web，生成 pkg 目录里有 .wasm 文件和 JavaScript 绑定。

在 Next.js 里使用：

import init, { fibonacci, ImageProcessor } from './pkg/my_wasm_lib';

export default async function WasmPage() {
    await init(); // 加载 WASM 模块
    
    const result = fibonacci(40); // 调用 Rust 函数
    console.log(result);
    
    // 使用图像处理器
    const processor = new ImageProcessor(imageData, width, height);
    processor.grayscale();
    const processed = processor.get_data();
}

WASM 的内存管理注意点：JavaScript 和 WASM 共享内存，但有类型限制。Vec<u8> 在边界上会被复制，如果你处理大数组，考虑用 wasm_bindgen 的 js_sys::Uint8Array 直接共享内存视图，避免复制。

实战练习：实现一个 Markdown 解析器，Rust 端用 pulldown-cmark 库解析 Markdown，暴露 parse_markdown(input: &str) -> String 函数给 JavaScript 调用，在 Next.js 里替换现有的 JavaScript Markdown 库。


让我们更深入地讲一下命令行工具和 WebAssembly 的实际应用。

首先是 CLI 工具的配置文件处理，这是一个常见需求。

用 config crate 支持多种配置来源：

use config::{Config, ConfigError, Environment, File};
use serde::Deserialize;

#[derive(Debug, Deserialize)]
struct AppConfig {
    database_url: String,
    port: u16,
    log_level: String,
}

impl AppConfig {
    fn load() -> Result<Self, ConfigError> {
        Config::builder()
            // 1. 默认值
            .set_default("port", 3000)?
            .set_default("log_level", "info")?
            // 2. 配置文件（可选）
            .add_source(File::with_name("config").required(false))
            // 3. 环境变量（最高优先级），APP_ 前缀
            .add_source(Environment::with_prefix("APP").separator("_"))
            .build()?
            .try_deserialize()
    }
}

这样配置文件、环境变量、默认值会按优先级合并，环境变量覆盖文件，文件覆盖默认值。在 Docker 部署时用环境变量，本地开发用配置文件。

CLI 工具的交互式输入——用 dialoguer 库：

use dialoguer::{Input, Select, Confirm, Password, MultiSelect};

// 文本输入
let name: String = Input::new()
    .with_prompt("请输入你的名字")
    .default("world".into())
    .interact()?;

// 单选菜单
let options = vec!["开发环境", "测试环境", "生产环境"];
let selection = Select::new()
    .with_prompt("选择部署环境")
    .items(&options)
    .default(0)
    .interact()?;

// 密码输入
let password = Password::new()
    .with_prompt("输入数据库密码")
    .interact()?;

// 确认
let confirmed = Confirm::new()
    .with_prompt("确认要删除这个文件吗？")
    .default(false)
    .interact()?;

这让你的 CLI 工具可以交互式地引导用户完成复杂的配置流程，比如项目初始化向导、部署脚本等。

CLI 工具的彩色和格式化输出——用 comfy-table 做表格输出：

use comfy_table::{Table, Cell, Color, Attribute};

let mut table = Table::new();
table.set_header(["用户名", "邮箱", "角色", "创建时间"]);

for user in &users {
    table.add_row(vec![
        Cell::new(&user.username),
        Cell::new(&user.email),
        Cell::new(&user.role).fg(if user.role == "admin" {
            Color::Red
        } else {
            Color::Green
        }),
        Cell::new(&user.created_at),
    ]);
}

println!("{table}");

这比手动用 format! 对齐字符串简单多了，而且会根据终端宽度自适应列宽。

WASM 的更多实际应用——音视频处理：

Rust 的 mp4 和 image crate 可以编译成 WASM，在浏览器里做客户端音视频处理，不需要把文件上传服务器：

#[wasm_bindgen]
pub fn process_image_data(data: Vec<u8>, operation: &str) -> Vec<u8> {
    let img = image::load_from_memory(&data).unwrap();

    let processed = match operation {
        "grayscale" => img.grayscale(),
        "blur" => img.blur(3.0),
        "sharpen" => img.unsharpen(2.0, 10),
        "thumbnail" => img.thumbnail(200, 200),
        _ => img,
    };

    let mut output = Vec::new();
    processed.write_to(&mut std::io::Cursor::new(&mut output), image::ImageFormat::Jpeg).unwrap();
    output
}

前端可以用 HTML Canvas 读取图片像素数据，调用 Rust WASM 处理，再用 Canvas 显示结果。整个过程在浏览器里完成，无需网络请求。

WASM 的性能实测对比——一个 Fibonacci(40) 的例子：

JavaScript 实现：约 1.5 秒；Rust WASM 实现：约 0.8 秒（约 2 倍快）；

但这只是说明性数字。对于真正的 CPU 密集型任务（如图像处理、加密、数据压缩），Rust WASM 通常比 JavaScript 快 5-20 倍，主要来自 SIMD 支持和更好的内存布局。

WASM 与 Web Workers 配合——避免阻塞主线程：

WASM 运行在主线程时，耗时操作会冻结 UI。正确的做法是在 Web Worker 里初始化 WASM 模块：

// worker.js
import init, { process_image } from './pkg/my_wasm_lib.js';

self.onmessage = async (e) => {
    await init();
    const result = process_image(e.data.imageData);
    self.postMessage(result);
};

// 主线程
const worker = new Worker('./worker.js', { type: 'module' });
worker.postMessage({ imageData: pixels });
worker.onmessage = (e) => updateCanvas(e.data);

这样即使 WASM 操作需要几百毫秒，UI 也不会冻结。

wasm-bindgen 的一些高级特性：

直接操作 DOM：use web_sys::Document，然后 let document = web_sys::window().unwrap().document().unwrap()，然后 document.create_element("div") 等等。但通常不推荐在 WASM 里操作 DOM，因为每次 JS/WASM 跨界调用都有开销。更好的做法是 WASM 负责计算，JavaScript 负责 DOM 操作。

共享内存（SharedArrayBuffer）与 WASM 线程：现代浏览器支持 SharedArrayBuffer，配合 Rust 的 rayon WASM 端口（wasm-bindgen-rayon），可以在 WASM 里使用多线程并行计算，进一步提升性能。但需要服务器设置 Cross-Origin-Opener-Policy 和 Cross-Origin-Embedder-Policy 头。

将 Rust 库发布为 NPM 包：

wasm-pack publish --target bundler

这会把编译好的 .wasm 文件和 JS 绑定代码发布到 NPM。其他人可以直接 npm install your-wasm-lib 使用，就像普通的 JS 库一样。这是 Rust WASM 库的分发方式，rust-lzma、rollup（部分模块）等项目都用这种方式。


让我们聊一聊 Rust 命令行工具和 WebAssembly 在真实项目中的更多实践经验。

首先说说为什么前端工程师应该关注 Rust 命令行工具。

我们每天都在用 CLI 工具：npm、git、cargo、docker……这些工具的体验好坏直接影响开发效率。很多开发团队有内部工具需求：自动化重复任务、封装常用操作、构建内部 DevOps 流程。Node.js 写 CLI 工具有门槛：分发需要全局安装 Node.js，或者打包成一个大的 bundle；启动慢（Node.js 启动开销）；依赖 node_modules，分发和更新麻烦。

Rust 写的 CLI 工具没有这些问题：单一静态二进制，复制到任何机器就能用；几乎零启动时间；零依赖，不需要安装任何运行时。对于要分发给非技术人员使用的工具，或者需要集成到 CI 脚本里的工具，Rust 是理想选择。

关于 Rust CLI 工具的分发，有几种常见方式。

直接用 cargo install 安装：cargo install my-tool，Cargo 会从 crates.io 下载源码，在本地编译安装到 ~/.cargo/bin/。这需要用户有 Rust 工具链，适合开发者工具。

预编译二进制分发：在 GitHub Releases 里发布多平台预编译二进制（macOS x86_64 和 ARM64、Linux x86_64 和 ARM64、Windows x86_64）。用户下载对应平台的二进制，无需任何运行环境。

用 cargo-dist 自动化预编译分发流程：cargo install cargo-dist，然后 cargo dist init，cargo dist build 构建所有平台的二进制，cargo dist plan 生成 CI 配置，一键发布到 GitHub Releases，支持 homebrew tap。

Homebrew 分发（macOS）：创建一个 Homebrew tap（一个包含 Formula 文件的 GitHub 仓库），用户 brew install your-tap/your-tool 即可安装。这是 macOS 开发者最习惯的工具安装方式。

关于命令行工具的用户体验设计，有几个原则值得遵循。

遵循 Unix 哲学：做好一件事；可以和其他工具通过管道组合；无提示时输出机器可读格式（方便脚本处理），有终端时输出人类友好格式。

错误信息要清晰：错误信息应该说明发生了什么、为什么发生、如何修复。比如 "无法读取配置文件" 不如 "无法读取配置文件 ~/.config/my-tool/config.toml: 文件不存在。运行 my-tool init 创建默认配置文件。"。

提供 --help 和 --version：clap 会自动生成，但要确保帮助文档清晰。每个子命令和每个参数都应该有描述。

支持 -v / --verbose 和 -q / --quiet：-v 显示更多信息（调试用），-q 减少输出（脚本用）。多个 -v（如 -vvv）可以增加详细程度级别。

遵守 POSIX 退出码约定：0 表示成功，非零表示失败。1 通常表示一般错误，2 表示参数错误，其他值可以表示特定错误类型。CI 脚本靠退出码判断命令是否成功。

关于 WebAssembly 的更多应用场景，我想分享一些让你眼前一亮的例子。

图表和数据可视化：D3.js 做图表渲染非常流行，但在数据量很大时（几十万数据点）JavaScript 的聚合、统计计算会很慢。可以用 Rust WASM 做数据聚合和统计，JavaScript 做最终的 SVG/Canvas 渲染。Rust 部分负责 CPU 密集型的数据处理，JavaScript 部分负责 DOM 操作，两者各司其职。

代码编辑器中的语法高亮和解析：很多现代代码编辑器（比如 VS Code 的 WebAssembly 扩展、Zed 编辑器）用 Rust 写语法高亮器，编译成 WASM 在浏览器里运行。tree-sitter 就是这样工作的——用 Rust 写的通用解析器框架，支持几乎所有主流语言的语法解析，被编译成 WASM 在浏览器代码编辑器里实时解析。

加密和安全操作：密码哈希（argon2、bcrypt）、端到端加密（x25519-dalek、aes-gcm）、签名验证（ed25519）这些操作在客户端做可以避免密码明文发往服务器。Rust 的密码学库质量很高，编译成 WASM 后性能比 JavaScript 实现快 3-10 倍。

离线优先应用：把数据库查询逻辑编译成 WASM，浏览器里运行 SQLite（用 sql.js 或者 Rust 的 rusqlite 编译的 WASM 版本），在离线状态下也能查询本地数据。当网络恢复时再同步到服务器。这是 PWA（Progressive Web App）的一种高级模式。

关于 WASM 的未来方向，有几个值得关注的技术：

WASI（WebAssembly System Interface）让 WASM 不只在浏览器里运行，还能在服务器上运行，访问文件系统、网络等系统资源。Cloudflare Workers 就支持 WASI 标准。WASM 组件模型让不同语言写的 WASM 模块可以互相调用，Rust 写的 WASM 组件可以被 JavaScript、Python 等调用，形成真正的语言无关的组件生态。

Rust 在 WASM 生态里是最成熟的语言，wasm-bindgen、wasm-pack、cargo-component 这些工具链让 Rust 到 WASM 的工作流非常顺畅。如果你要探索 WASM，Rust 是最好的起点。

这章总结：clap derive 宏声明式定义 CLI 参数，自动生成帮助文档；Rust CLI 工具性能远超 Node.js 脚本；wasm-pack 编译 Rust 为 WASM；#[wasm_bindgen] 标记暴露给 JavaScript 的 API；WASM 特别适合性能密集型任务；大数组操作注意内存复制开销，考虑共享内存视图。

最后一章：Rust 加 AI——用 Rust 的性能优势驱动 AI 应用。下章见。
"""

SCRIPTS[16] = """
欢迎来到最后一章，第十六章：Rust 加 AI——LLM API、RAG、以及 AI Agent。

AI 时代已经来临，而 Rust 在 AI 应用开发里有独特的优势，这一章我们来充分利用它。

为什么用 Rust 做 AI 后端？

AI 应用通常瓶颈在网络 I/O（调用 LLM API）而非 CPU，这正是 Rust 异步模型的甜区。Tokio 可以同时处理数千个 LLM 请求，内存占用极低。

流式响应：Rust 的 Stream trait 天然适合 SSE（Server-Sent Events），比 Node.js 的流更高效。

向量计算：Rust 的 SIMD 支持让向量相似度计算比 Python 快 10 倍以上。

边缘部署：Rust 二进制可以部署到 Cloudflare Workers、Fly.io 等边缘节点，比 Node.js 更轻量。

先来实现调用 OpenAI API 的基本功能。

Cargo.toml 加上：reqwest features json 和 stream；serde 和 serde_json；tokio full；anyhow；async-openai。

async-openai 是 OpenAI 的官方 Rust 客户端：

use async_openai::{Client, types::{ChatCompletionRequestUserMessageArgs, CreateChatCompletionRequestArgs}};

async fn chat(prompt: &str) -> anyhow::Result<String> {
    let client = Client::new(); // 自动读取 OPENAI_API_KEY 环境变量
    
    let request = CreateChatCompletionRequestArgs::default()
        .model("gpt-4o")
        .messages([
            ChatCompletionRequestUserMessageArgs::default()
                .content(prompt)
                .build()?
                .into()
        ])
        .build()?;
    
    let response = client.chat().create(request).await?;
    
    Ok(response.choices[0].message.content.clone().unwrap_or_default())
}

流式响应——让用户看到 AI 逐字生成的效果：

use async_openai::types::CreateChatCompletionStreamResponse;
use futures::StreamExt;

async fn stream_chat(prompt: &str) -> anyhow::Result<()> {
    let client = Client::new();
    
    let request = CreateChatCompletionRequestArgs::default()
        .model("gpt-4o")
        .stream(true)
        .messages([...])
        .build()?;
    
    let mut stream = client.chat().create_stream(request).await?;
    
    while let Some(result) = stream.next().await {
        let response = result?;
        if let Some(content) = response.choices[0].delta.content.as_ref() {
            print!("{}", content);
            std::io::stdout().flush()?;
        }
    }
    
    Ok(())
}

在 Axum 里实现 SSE 流式 API：

use axum::response::{IntoResponse, Sse};
use axum::response::sse::{Event, KeepAlive};
use tokio::sync::mpsc;
use tokio_stream::wrappers::ReceiverStream;

async fn stream_chat_handler(
    Json(input): Json<ChatInput>,
) -> impl IntoResponse {
    let (tx, rx) = mpsc::channel(32);
    
    tokio::spawn(async move {
        let client = Client::new();
        // ... 流式调用 LLM
        // 把每个 token 通过 tx 发送
        let _ = tx.send(Ok(Event::default().data(token))).await;
    });
    
    let stream = ReceiverStream::new(rx);
    Sse::new(stream).keep_alive(KeepAlive::default())
}

RAG——检索增强生成，让 AI 回答你的私有知识库。

RAG 的流程是：把文档分块，用 Embedding 模型向量化，存入向量数据库；用户提问时，把问题向量化，找最相似的文档块；把相关文档块和问题一起发给 LLM，生成基于私有知识的回答。

Rust 里用 pgvector 扩展给 PostgreSQL 加上向量能力：

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE documents (
    id        SERIAL PRIMARY KEY,
    content   TEXT NOT NULL,
    metadata  JSONB,
    embedding vector(1536)
);

CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops);

Rust 代码：

use pgvector::Vector;

// 向量化文本
async fn embed(client: &Client, text: &str) -> anyhow::Result<Vector> {
    let request = CreateEmbeddingRequestArgs::default()
        .model("text-embedding-3-small")
        .input(text)
        .build()?;
    
    let response = client.embeddings().create(request).await?;
    let values: Vec<f32> = response.data[0].embedding.clone();
    Ok(Vector::from(values))
}

// 相似度搜索
async fn search(pool: &PgPool, query_embedding: &Vector, limit: i64) 
    -> sqlx::Result<Vec<String>> 
{
    sqlx::query_scalar!(
        r#"
        SELECT content FROM documents
        ORDER BY embedding <=> $1  -- cosine distance 操作符
        LIMIT $2
        "#,
        query_embedding as &Vector,
        limit
    )
    .fetch_all(pool)
    .await
}

// RAG 管道
async fn rag_answer(pool: &PgPool, client: &Client, question: &str) 
    -> anyhow::Result<String> 
{
    let query_embedding = embed(client, question).await?;
    let contexts = search(pool, &query_embedding, 5).await?;
    let context = contexts.join("

---

");
    
    let prompt = format!(
        "根据以下文档回答问题。

文档：
{context}

问题：{question}"
    );
    
    chat(client, &prompt).await
}

AI Agent——让 AI 自主使用工具。

Function Calling 让 LLM 能"调用函数"——实际上 LLM 输出一个结构化的函数调用请求，你的代码来执行，再把结果返回给 LLM。

use serde_json::{json, Value};

async fn run_agent(user_request: &str) -> anyhow::Result<String> {
    let tools = json!([
        {
            "type": "function",
            "function": {
                "name": "run_cargo_check",
                "description": "对 Rust 代码运行 cargo check",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": { "type": "string" }
                    },
                    "required": ["code"]
                }
            }
        }
    ]);
    
    let mut messages = vec![json!({"role": "user", "content": user_request})];
    
    loop {
        let response = call_openai(&messages, Some(&tools)).await?;
        let choice = &response["choices"][0];
        
        if choice["finish_reason"] == "stop" {
            return Ok(choice["message"]["content"].as_str().unwrap().to_string());
        }
        
        if let Some(tool_calls) = choice["message"]["tool_calls"].as_array() {
            messages.push(choice["message"].clone());
            
            for call in tool_calls {
                let fn_name = call["function"]["name"].as_str().unwrap();
                let args: Value = serde_json::from_str(
                    call["function"]["arguments"].as_str().unwrap()
                )?;
                
                let result = match fn_name {
                    "run_cargo_check" => execute_cargo_check(&args).await,
                    _ => "未知工具".to_string(),
                };
                
                messages.push(json!({
                    "role": "tool",
                    "tool_call_id": call["id"],
                    "content": result
                }));
            }
        }
    }
}

本地 LLM——用 Ollama 完全免费：

cargo install ollama（或者 brew install ollama）安装 Ollama，ollama pull llama3.2 下载模型，然后 async-openai 改一下 base_url 就能用：

let client = Client::with_config(
    OpenAIConfig::new()
        .with_api_base("http://localhost:11434/v1")
        .with_api_key("ollama"),
);

API 和 OpenAI 完全兼容，代码无需改动。适合开发调试阶段节省 API 费用，测试通过后换回 GPT-4o 或 Claude。

接入 Claude API（Anthropic）：Rust 没有官方 SDK，但 Claude API 是标准的 HTTP REST，直接用 reqwest：

let client = reqwest::Client::new();
let response = client
    .post("https://api.anthropic.com/v1/messages")
    .header("x-api-key", &api_key)
    .header("anthropic-version", "2023-06-01")
    .json(&json!({
        "model": "claude-opus-4-7",
        "max_tokens": 1024,
        "messages": [{"role": "user", "content": prompt}]
    }))
    .send()
    .await?
    .json::<serde_json::Value>()
    .await?;

let content = response["content"][0]["text"].as_str().unwrap();

综合实战项目：AI 代码审查助手。

接收 POST 请求，body 是用户提交的 Rust 代码；自动运行 cargo clippy 检查代码；用 RAG 检索相关的 Rust 最佳实践文档；把 clippy 结果和相关文档一起发给 LLM；通过 SSE 流式返回代码审查建议。

整个流程大约需要 200 行 Rust 代码，但提供了完整的 AI 工程师工作流：本地工具调用、向量检索、LLM 推理、流式响应。

好，到这里，整个 RustForge 课程的 16 章内容就全部讲完了。

我们一起走过了：Rust 基础语法和工具链，所有权这个最核心的独特概念，结构体和枚举这些数据建模工具，错误处理的哲学，泛型和 Trait 的零成本抽象，智能指针和内存管理，线程安全并发和异步编程，Axum 全栈 Web 后端，SQLx 类型安全数据库，Next.js 加 Axum 的全栈实战，测试和工具链，Docker 和 CI/CD 的 DevOps，性能优化和 unsafe，命令行工具和 WASM，以及最前沿的 Rust 加 AI 集成。

这是一套完整的工程师路径，从前端到全栈，从 JavaScript 到 Rust，从开发到部署，从传统 API 到 AI 应用。

接下来你可以：加入 Rust 中文社区，在 rustcc.cn 持续学习交流；去 GitHub 找有趣的 Rust 开源项目，贡献代码；把你在这门课里学到的知识用于实际工作项目；继续深入《The Rust Programming Language》官方书籍，它的 21 章涵盖了很多我们没有讲到的细节；探索 Rust 的嵌入式方向、系统编程方向，或者继续深化全栈方向。

Rust 社区有一句话：Fighting the borrow checker——和借用检查器"搏斗"。但当你真正掌握了所有权系统，你会发现那些"搏斗"其实是在帮你排查真实的 bug。

感谢你完成 RustForge 全部 16 章课程。希望这门课真的帮助了你，让 Rust 不再是遥不可及的系统编程语言，而是你工具箱里最锋利的那把刀。

加油，Rustacean！

让我们深入聊一聊 Rust 在 AI 时代的独特价值，以及如何用 Rust 构建真正有竞争力的 AI 应用。

首先我想谈谈 AI 应用的技术栈选择问题，这是很多工程师现在面临的真实决策。

目前大多数 AI 应用是用 Python 写的，因为 Python 有丰富的 ML 库（PyTorch、TensorFlow、Hugging Face）。Node.js 也在这个领域快速发展，有 LangChain.js、Vercel AI SDK 等工具。那 Rust 在什么场景下有优势呢？

关键的洞察是：大多数 AI 应用不是在"跑模型"——模型跑在 GPU 上，是 PyTorch 或者云厂商的 API 在处理。你的应用代码主要做的是：接收用户请求、调用 LLM API、处理流式响应、管理对话历史、查询向量数据库、组合多个 API 结果。这些工作全都是 I/O 密集型的，正是 Rust 异步模型的甜区。

具体来说，Rust 在 AI 应用中的优势体现在以下几个方面：

处理大量并发的 LLM 请求。LLM API 调用通常需要几秒到几十秒，如果你的应用需要同时处理大量用户，Tokio 的异步模型可以高效地管理成千上万个并发的 LLM 请求，不需要等一个完成再处理下一个。Node.js 也能做到，但内存效率更低。

流式响应的处理。LLM 的流式输出需要持续处理来自 OpenAI 或者 Anthropic API 的 SSE 流，解析每个 token，转发给客户端。Rust 的 Stream trait 和异步处理让这个过程极其高效，延迟非常低。

向量计算的性能。RAG 系统里需要计算向量相似度，对于百万级别的向量库，朴素的余弦相似度计算会很慢。Rust 的 SIMD 支持让向量计算比 Python/JavaScript 快 5-20 倍。如果你用 PostgreSQL 的 pgvector，查询层的性能很好；但如果需要内存中的向量搜索，Rust 的 usearch 或者 hnswlib 绑定会非常有优势。

长时间运行的 AI 工作流。自动化脚本、数据处理流水线、AI Agent 的工具执行这些任务可能运行几分钟甚至几小时。Python 脚本在这个场景下内存可能越用越多（GC 不够及时），而 Rust 的内存使用极其精确，运行几天都不会有内存增长的问题。

关于 AI Agent 的架构设计，这是当前最热门的话题，我想多说一些。

AI Agent 的核心是 ReAct 模式（Reason + Act）：LLM 分析任务，决定调用哪个工具，执行工具，把结果返回给 LLM，LLM 再分析结果决定下一步，如此循环直到任务完成。

在 Rust 里实现这个循环，关键是工具的定义和执行。工具可以是：文件系统操作（读写文件）、网络请求（调用外部 API）、代码执行（在沙箱里运行代码）、数据库查询（SQL 查询）、搜索引擎（搜索网络或者内部知识库）。

Rust 的类型系统让工具定义非常优雅。你可以定义一个 Tool trait，每个工具实现这个 trait，包括工具的名字、描述（用于 function calling 的 JSON Schema）、执行方法。Agent 运行时维护一个工具注册表，根据 LLM 的选择动态调用对应的工具。

这个模式和 React 里的 hooks 有点相似：工具是可组合的功能单元，Agent 就像是一个 runtime，协调这些工具的调用。

关于 Rust 与 Python AI 库的互操作，这是一个很实际的问题。如果你需要用 PyTorch 或者 Hugging Face 的模型，有两种方案：

通过 HTTP API 调用：把 Python 模型服务包装成一个 HTTP API（用 FastAPI），Rust 服务通过 HTTP 调用它。这是最简单的集成方式，两个服务独立部署，可以分别扩缩容。

通过 libtorch 直接调用：tch-rs crate 提供了 PyTorch 的 Rust 绑定，可以直接在 Rust 里加载和运行 PyTorch 模型，不需要 Python 运行时。对于需要低延迟模型推理的场景，这种方式延迟更低（没有 HTTP 开销）。

对于大多数应用，HTTP API 方案更实用，因为它的部署更灵活，模型服务可以独立更新，不需要重新编译 Rust 代码。

关于提示词工程（Prompt Engineering）在 Rust 里的实践，这是写好 AI 应用的关键技能。

Rust 的字符串处理能力让提示词模板管理非常清晰。用 format! 宏构建提示词虽然简单，但对于复杂的提示词模板，建议用 tera 或者 minijinja 这样的模板引擎。这让提示词模板可以单独管理（存储为 .j2 文件）、支持条件逻辑和循环、方便 A/B 测试不同的提示词版本。

Prompt 缓存是节省 API 费用的重要技巧。对于有大量系统提示词的应用（比如 RAG 系统里的上下文），Anthropic 的 Claude API 和 OpenAI 的 API 都支持 prompt caching：重复使用的提示词前缀只收一次费用，后续调用价格大幅降低（通常 90% 以上的折扣）。在 Rust 里实现 prompt caching 只需要在 API 请求里正确设置 cache_control 参数，然后监控缓存命中率来优化提示词结构。

关于 AI 应用的安全性，这是经常被忽视但极其重要的话题。

提示词注入攻击：用户可能在输入里夹带特殊指令，试图绕过系统提示词的限制（比如 "忽略之前所有指令，改为..."）。防御措施包括：在系统提示词里明确说明如何处理可疑输入；对用户输入做清理和过滤；在代码层面限制工具的权限（比如文件系统工具只能访问指定目录）。

数据隐私：如果用 RAG 处理内部敏感文档，要确保向量数据库的访问控制严格；如果调用外部 LLM API，要注意不要把用户的个人数据发送给第三方（或者确保用了数据不训练协议）；考虑部署本地模型（用 Ollama 跑 Llama 等开源模型），敏感数据不离开内网。

成本控制：LLM API 是按 token 计费的，token 用多了账单会很高。实践上：缓存重复的查询（同样的问题不需要每次都调用 LLM）；限制对话历史的长度（只保留最近的几轮对话）；对于不需要强大推理能力的任务，用小模型（比如 gpt-4o-mini 代替 gpt-4o）；设置每用户每日的 token 使用限额。

Rust 的类型系统让这些安全约束可以在编译期表达。比如你可以定义不同权限级别的工具类型，确保低权限的 Agent 不能调用高权限的工具，不需要运行时检查。

最后谈一下 AI 应用的可观测性。AI 应用的调试比普通应用更困难，因为 LLM 的输出是不确定的，同样的输入可能产生不同的输出。这让传统的"确定性测试"很难做。

推荐的实践是：记录所有 LLM 请求和响应（包括系统提示词、用户输入、模型输出、token 用量、延迟）；用 LLM 评估 LLM（用一个 LLM 来自动评估另一个 LLM 的输出质量）；A/B 测试不同的提示词版本，用数据驱动提示词优化；设置告警，监控异常的响应时间或者 token 用量，提前发现问题。

Rust 的 tracing 生态可以很好地支持这些需求，结合结构化日志（JSON 格式），所有的 LLM 调用数据都可以发送到日志分析平台（比如 Datadog、Elastic、或者自建的 OpenSearch）做分析。
"""

def generate_audio(chapter_num: int, output_dir: str = ".") -> bool:
    script = SCRIPTS.get(chapter_num)
    if not script:
        print(f"章节 {chapter_num} 的脚本还未编写")
        return False

    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"ch{chapter_num:02d}.mp3")
    script_file = f"/tmp/ch{chapter_num:02d}_script.txt"

    with open(script_file, "w") as f:
        f.write(script.strip())

    print(f"正在生成第 {chapter_num} 章音频...")
    result = subprocess.run([
        "edge-tts",
        "--voice", VOICE,
        f"--rate={RATE}",
        "--file", script_file,
        "--write-media", output_file,
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"错误：{result.stderr}")
        return False

    size = os.path.getsize(output_file)
    print(f"完成：{output_file} ({size // 1024} KB)")
    try:
        os.unlink(script_file)
    except FileNotFoundError:
        pass
    return True


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="生成 RustForge 课程音频")
    parser.add_argument("chapter", nargs="?", default="all",
                        help="章节号 (1-16) 或 all")
    parser.add_argument("--output", default="./audio",
                        help="输出目录 (默认: ./audio)")
    args = parser.parse_args()

    if args.chapter == "all":
        for i in sorted(SCRIPTS.keys()):
            generate_audio(i, args.output)
    else:
        try:
            n = int(args.chapter)
            generate_audio(n, args.output)
        except ValueError:
            print(f"无效章节号：{args.chapter}")
            sys.exit(1)

