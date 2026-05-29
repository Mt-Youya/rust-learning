# ch01 MDX 视频组件插入补丁
# 使用方法：将下面各段插入 apps/web/src/content/chapters/basics.mdx 对应位置
#
# ─── 步骤 1：在文件顶部 import 区块追加 ────────────────────────────

```mdx
import { ThreeScene } from '@/components/animations/ThreeScene'
import { QuizCard } from '@/components/chapters/QuizCard'
import { PracticeCard } from '@/components/chapters/PracticeCard'
import { CodeCompare } from '@/components/chapters/CodeCompare'
```

# ─── 步骤 2：在 <ChapterHero> 下方插入（Hook 场景）────────────────

```mdx
<ThreeScene
  id="memory-leak-burst"
  caption="Node.js 内存泄漏 200MB→2GB——Rust 从根源解决这个问题"
/>
```

# ─── 步骤 3：在「第一个 Rust 程序」段落前插入 ────────────────────

```mdx
<ThreeScene
  id="rust-shield-trio"
  caption="零运行时开销 · 内存安全 · 并发安全——三个保证，全部在编译期验证"
/>

| 保证 | 含义 | 类比 TypeScript |
|------|------|----------------|
| **零运行时开销** | 没有 GC，没有 VM，直接编译为机器码 | TS 仍然在 V8 上运行 |
| **内存安全** | 悬垂指针、重复释放，编译器拦截 | TS 没有这层保证 |
| **并发安全** | 数据竞争在编译期消灭 | TS 没有这层保证 |
```

# ─── 步骤 4：在安装命令块前插入（rustup vs nvm 对比）────────────

```mdx
<ThreeScene
  id="toolchain-3d-compare"
  caption="rustup vs nvm：版本管理是共同点，但 rustup 还多了组件和编译目标管理"
/>
```

# ─── 步骤 5：在「cargo 就是 Rust 的 npm」句子前插入 ──────────────

```mdx
<ThreeScene
  id="cargo-particle-merge"
  caption="npm + webpack + jest 三合一——粒子聚合成 Cargo"
/>
```

在 cargo new / cargo run 代码块后插入：

```mdx
<QuizCard
  trigger_timestamp="03:52"
  question="cargo new 自动创建了哪两个核心文件？"
  options={[
    "index.js 和 package.json",
    "Cargo.toml 和 src/main.rs",
    "main.rs 和 Cargo.lock",
    "src/lib.rs 和 Cargo.toml"
  ]}
  answer={1}
  explanation="Cargo.toml 是项目配置（类比 package.json），src/main.rs 是程序入口（类比 src/index.js）。Cargo.lock 在第一次 build 时自动生成。"
/>
```

# ─── 步骤 6：在 cargo 命令对比附近插入 ─────────────────────────────

```mdx
<ThreeScene
  id="cargo-vs-npm"
  caption="npm ↔ cargo 命令映射——记住这几条，日常 80% 够用"
/>

<ThreeScene
  id="cargo-pipeline-3d"
  caption="cargo run 背后：Cargo → 读 Cargo.toml → 调用 rustc → 生成可执行文件 → 运行"
/>
```

# ─── 步骤 7：在「变量与不可变性」章节 CompareBlock 前插入 ─────────

```mdx
<ThreeScene
  id="immutable-lock"
  caption="let = 编译器锁住 · let mut = 显式解锁——强制你明确每一个「变化」"
/>
```

在 shadowing 代码块后插入：

```mdx
<QuizCard
  trigger_timestamp="05:28"
  question="下面这段代码会发生什么？"
  code={`let mut x = 10;\nprintln!("{}", x);`}
  options={[
    "编译错误：x 没有被修改，mut 是多余的",
    "编译成功，输出 10，但编译器给出 warning",
    "编译错误：println! 不接受整数",
    "编译成功，且没有任何警告"
  ]}
  answer={1}
  explanation="声明了 mut 但从未修改，编译器给出 warning（不是错误）：'variable does not need to be mutable'。这是 Rust 强制意图明确的体现。"
/>
```

# ─── 步骤 8：替换现有 <VideoPlaceholder> ──────────────────────────

将：
```mdx
<VideoPlaceholder
  title="Rust 基础：变量、类型、函数、match"
  duration="1 分钟精讲"
  description="从 JS 视角出发，演示 Rust 基础语法。"
  src="/videos/ch01-basics.mp4"
  subtitles="/subtitles/ch01-basics.vtt"
/>
```

替换为：
```mdx
<VideoPlaceholder
  title="Getting Started · Rust 工具链与第一个项目"
  duration="7 分钟"
  description="从 npm 视角出发，演示 rustup 安装、Cargo 工作流、变量不可变性。"
  src="/videos/ch01.mp4"
  subtitles="/subtitles/ch01.vtt"
  chapters={[
    { time: "00:00", title: "开场：为什么前端工程师学 Rust" },
    { time: "00:45", title: "Rust 三大优势" },
    { time: "01:35", title: "安装 rustup" },
    { time: "02:40", title: "Cargo 是什么" },
    { time: "03:15", title: "cargo new 创建项目" },
    { time: "04:05", title: "Cargo.toml 详解" },
    { time: "05:10", title: "变量不可变演示" },
    { time: "06:15", title: "小结与练习引导" }
  ]}
/>
```

# ─── 步骤 9：在本章小结前插入 PracticeCard ──────────────────────

```mdx
<PracticeCard
  title="温度转换器"
  command="cargo new temp-converter"
  objectives={[
    "实现 celsius_to_fahrenheit(c: f64) -> f64 函数",
    "实现 fahrenheit_to_celsius(f: f64) -> f64 函数",
    "在 main() 中调用并用 println! 打印结果",
    "（进阶）用 std::env::args() 读取命令行参数"
  ]}
/>
```

# ─── 新增组件开发清单 ────────────────────────────────────────────
#
# 以下组件需要新建（对应 ch01_scenes.yaml 中的 component_name）：
#
# apps/web/src/components/animations/
# ├── MemoryLeakBurstScene.tsx     ← memory-leak-burst
# ├── RustShieldTrioScene.tsx      ← rust-shield-trio
# ├── ToolchainCompareScene.tsx    ← toolchain-3d-compare
# ├── CargoParticleMergeScene.tsx  ← cargo-particle-merge
# ├── CargoPipeline3DScene.tsx     ← cargo-pipeline-3d
# ├── CargoVsNpmBubblesScene.tsx   ← cargo-vs-npm
# └── ImmutableLockScene.tsx       ← immutable-lock
#
# 每个组件接口：
# interface ThreeSceneProps {
#   id: string           // scene_id，供 ThreeScene wrapper 路由
#   autoplay?: boolean   // 默认 false，进入视口时自动播放
#   loop?: boolean       // 默认 false
# }
