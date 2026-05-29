# RustForge

专为前端工程师设计的 Rust 全栈学习平台。用 3D 动画将抽象概念可视化，以前端思维类比讲解 Rust，覆盖从基础到 Web 服务、数据库、DevOps、AI 集成的完整路径。

## 目标用户

有 2–5 年经验的前端工程师（React / Vue / TypeScript），想转型 Rust 全栈开发。

## 功能特性

- **3D 可视化动画** — Three.js 粒子场景直观演示所有权、借用等抽象概念
- **前端类比教学** — 每个 Rust 概念均从 JavaScript/TypeScript 视角出发对比讲解
- **MDX 章节系统** — Markdown + React 组件混编，支持 Callout、代码对比、实战卡片
- **视频讲解** — CosyVoice TTS + 自动化视频生成脚本，每章节附讲解视频
- **实战项目** — 每章附带可运行的 CLI / Web 项目练习

## 课程章节

| # | 章节 | 内容 |
|---|------|------|
| 1 | 入门 | rustup、Cargo 工作流，对比 npm/Node.js |
| 2 | 变量与类型 | 变量绑定、基础类型、模式匹配 |
| 3 | 所有权 | 所有权规则、移动/拷贝、借用、切片 |
| 4 | 结构体与枚举 | struct、enum、impl、trait |
| 5 | 错误处理 | Result、Option、`?` 运算符 |
| 6 | 泛型与 Trait | 泛型、trait bounds、生命周期入门 |
| 7 | 异步编程 | async/await、Tokio，对比 Promise |
| 8 | Web 后端 | Axum、REST API、中间件 |
| 9 | 数据库 | SQLx、连接池、迁移 |
| 10 | 全栈 | Leptos / Next.js + Rust API 集成 |
| 11 | DevOps | Docker、CI/CD、部署 |
| 12 | AI 集成 | 调用 LLM API、RAG 实现 |
| 13 | 智能指针 | Box、Rc、RefCell |
| 14 | 性能优化 | Profiling、零拷贝、SIMD |
| 15 | 测试 | 单元测试、集成测试、基准测试 |
| 16 | WebAssembly | wasm-bindgen、在浏览器中运行 Rust |

## 技术栈

**前端**

- Next.js 16 (canary) · App Router · Turbopack
- React 19 · TypeScript · Tailwind CSS v4
- Three.js · @react-three/fiber · GSAP
- MDX (@next/mdx · rehype-pretty-code · Shiki)

**内容生成脚本**（`scripts/`）

- `gen_audio.py` — 调用 edge-tts / CosyVoice 生成章节讲解音频
- `gen_video.py` / `gen_video_3min.py` — 合成讲解视频（幻灯片 + 音频波形）
- `cosyvoice_tts.py` — CosyVoice 本地 TTS 封装

**Monorepo**

- pnpm workspace（`apps/web`）

## 快速开始

```bash
# 安装依赖
pnpm install

# 启动开发服务器
pnpm dev
```

访问 [http://localhost:3000](http://localhost:3000)

## 项目结构

```
rust-learning/
├── apps/web/                    # Next.js 应用
│   ├── src/
│   │   ├── app/                 # App Router 路由
│   │   │   ├── page.tsx         # 首页
│   │   │   └── chapter/[slug]/  # 章节动态路由
│   │   ├── components/
│   │   │   ├── animations/      # Three.js 场景组件
│   │   │   ├── chapters/        # MDX 章节组件
│   │   │   └── sections/        # 首页版块
│   │   ├── content/chapters/    # MDX 章节内容
│   │   ├── data/curriculum.ts   # 课程目录数据
│   │   └── lib/mdx.ts           # MDX 工具函数
│   └── mdx-components.tsx       # 全局 MDX 组件映射
├── scripts/                     # 音视频生成脚本
└── asset/                       # CosyVoice 模型文件
```

## 添加新章节

1. 在 `apps/web/src/content/chapters/` 新建 `{slug}.mdx`
2. 导出 `frontmatter` 对象（title、chapter、slug、status 等字段）
3. 在 `apps/web/src/data/curriculum.ts` 中注册章节元数据

无需新建 TSX 路由文件，`generateStaticParams` 自动识别。

## 许可证

MIT
