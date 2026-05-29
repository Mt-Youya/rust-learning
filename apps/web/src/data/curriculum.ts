export type ChapterStatus = "available" | "locked" | "coming-soon";

export interface Chapter {
  id: string;
  number: number;
  title: string;
  subtitle: string;
  description: string;
  status: ChapterStatus;
  duration: string;
  concepts: string[];
  project: string;
  slug: string;
}

export const chapters: Chapter[] = [
  // ─── 第一阶段：语言核心（Ch1-6）────────────────────────────────────
  {
    id: "ch1",
    number: 1,
    title: "入门：安装与 Cargo",
    subtitle: "从 npm 视角理解 Rust 工具链",
    description: "rustup 安装、Cargo 工作流、第一个程序——用 npm/Node.js 视角建立 Rust 工具链认知。",
    status: "available",
    duration: "3 小时",
    concepts: ["rustup 工具链管理", "Cargo vs npm", "Cargo.toml 详解", "变量与 let mut"],
    project: "温度转换 CLI",
    slug: "basics",
  },
  {
    id: "ch2",
    number: 2,
    title: "变量、类型与函数",
    subtitle: "Rust 类型系统深度解析",
    description: "整数类型、字符串两种形式、元组数组、函数表达式——建立比 TypeScript 更严格的类型认知。",
    status: "available",
    duration: "3 小时",
    concepts: ["整数与浮点数类型", "&str vs String", "元组与数组 vs Vec", "表达式 vs 语句"],
    project: "成绩计算器 CLI",
    slug: "variables",
  },
  {
    id: "ch3",
    number: 3,
    title: "所有权与借用",
    subtitle: "Rust 最核心的内存管理机制",
    description: "Move 语义、借用规则、生命周期——理解 Rust 如何在没有 GC 的情况下保证内存安全。",
    status: "available",
    duration: "4 小时",
    concepts: ["所有权三条规则", "Move vs Copy", "借用与引用 &", "生命周期入门"],
    project: "字符串处理器",
    slug: "ownership",
  },
  {
    id: "ch4",
    number: 4,
    title: "结构体、枚举与模式匹配",
    subtitle: "Rust 的数据建模利器",
    description: "struct 定义数据、enum 携带数据、match 穷举匹配——用 Option 替代 null。",
    status: "available",
    duration: "4 小时",
    concepts: ["struct 与 impl 方法", "enum 代数类型", "Option<T> 替代 null", "match 穷举"],
    project: "图形面积计算器",
    slug: "structs",
  },
  {
    id: "ch5",
    number: 5,
    title: "错误处理",
    subtitle: "Result、? 操作符与自定义错误",
    description: "Result<T,E>、? 操作符、thiserror、anyhow——告别 try-catch 的不确定性。",
    status: "available",
    duration: "3 小时",
    concepts: ["Result<T,E> 强制处理", "? 操作符传播", "thiserror 自定义错误", "anyhow 应用错误"],
    project: "CSV 解析器",
    slug: "errors",
  },
  {
    id: "ch6",
    number: 6,
    title: "泛型、Trait 与生命周期",
    subtitle: "零成本抽象与引用安全的秘密",
    description: "泛型消除重复、Trait 定义共享行为、生命周期标注验证引用安全——Rust 编译器零运行时成本的安全保证。",
    status: "available",
    duration: "4 小时",
    concepts: ["泛型与单态化", "Trait 与接口对比", "生命周期标注 'a", "#[derive] 自动实现"],
    project: "词频统计器",
    slug: "generics",
  },
  // ─── 第二阶段：系统编程（Ch7-9）────────────────────────────────────
  {
    id: "ch7",
    number: 7,
    title: "集合与函数式编程",
    subtitle: "Vec · HashMap · 闭包 · 迭代器链",
    description: "Vec 动态数组、HashMap 键值存储、闭包捕获环境、迭代器惰性链式操作——函数式思维写出简洁高效的 Rust 代码。",
    status: "available",
    duration: "3 小时",
    concepts: ["Vec 与 HashMap 操作", "闭包三种 Fn Trait", "迭代器惰性求值", "entry API 模式"],
    project: "日志分析器",
    slug: "collections",
  },
  {
    id: "ch8",
    number: 8,
    title: "并发编程",
    subtitle: "线程 · 智能指针 · async/await · Tokio",
    description: "OS 线程与消息传递、Arc/Mutex 共享状态、async/await 异步模型、Tokio 运行时——无数据竞争的高并发。",
    status: "available",
    duration: "5 小时",
    concepts: ["Arc/Mutex 线程安全", "mpsc channel 通信", "async/await + Tokio", "Rayon 数据并行"],
    project: "并发爬虫工具",
    slug: "concurrency",
  },
  {
    id: "ch9",
    number: 9,
    title: "模块系统与 Cargo 生态",
    subtitle: "代码组织 · 包管理 · Workspace",
    description: "mod 组织代码、pub 控制可见性、Cargo workspace 管理 monorepo、Crates.io 发布——像管理 npm 包一样管理 Rust。",
    status: "available",
    duration: "2 小时",
    concepts: ["mod 与 pub 可见性", "use 路径与重导出", "Cargo workspace", "发布到 Crates.io"],
    project: "发布一个 Crates.io 工具库",
    slug: "modules",
  },
  // ─── 第三阶段：工程化（Ch10-11）────────────────────────────────────
  {
    id: "ch10",
    number: 10,
    title: "测试与代码质量",
    subtitle: "单元测试 · 集成测试 · 性能基准",
    description: "Rust 内置测试、异步测试、属性测试（proptest）、criterion 基准测试、clippy/fmt——代码质量完整工具链。",
    status: "available",
    duration: "3 小时",
    concepts: ["#[test] 单元测试", "criterion 基准测试", "proptest 属性测试", "clippy + fmt CI"],
    project: "为 Axum API 构建完整测试套件",
    slug: "testing",
  },
  {
    id: "ch11",
    number: 11,
    title: "CLI 工具与 WebAssembly",
    subtitle: "clap · wasm-pack · 跨平台编译",
    description: "clap 构建专业 CLI 工具、wasm-pack 编译 WebAssembly——让同一份 Rust 代码跑在终端和浏览器里。",
    status: "available",
    duration: "3 小时",
    concepts: ["clap derive CLI", "wasm-bindgen 导出", "wasm-pack 构建", "Next.js 集成 WASM"],
    project: "Markdown 解析器（CLI + WASM 双发布）",
    slug: "cli",
  },
  // ─── 第四阶段：Web 服务（Ch12-14）──────────────────────────────────
  {
    id: "ch12",
    number: 12,
    title: "Web 后端：Axum",
    subtitle: "用 Axum 构建生产级 REST API",
    description: "Router、提取器、中间件——类型系统驱动的 Web 框架让错误在编译期暴露。",
    status: "available",
    duration: "5 小时",
    concepts: ["Axum 路由与提取器", "自定义中间件", "统一错误响应", "Tower 服务抽象"],
    project: "博客 REST API",
    slug: "web-backend",
  },
  {
    id: "ch13",
    number: 13,
    title: "数据库：SQLx",
    subtitle: "编译时 SQL 验证 + PostgreSQL",
    description: "sqlx query! 宏、迁移管理、连接池、事务——编译期验证 SQL 正确性，告别 ORM 魔法。",
    status: "available",
    duration: "4 小时",
    concepts: ["query! 编译时验证", "sqlx migrate 迁移", "连接池与事务", "#[sqlx::test] 测试"],
    project: "数据访问层实战",
    slug: "database",
  },
  {
    id: "ch14",
    number: 14,
    title: "认证与安全",
    subtitle: "JWT · OAuth2 · RBAC · 安全中间件",
    description: "Argon2 密码哈希、JWT 令牌、RBAC 权限控制、速率限制——用类型系统把安全漏洞消灭在编译期。",
    status: "available",
    duration: "3 小时",
    concepts: ["Argon2 密码哈希", "JWT 签发与验证", "RBAC 权限控制", "速率限制中间件"],
    project: "完整用户认证服务",
    slug: "auth",
  },
  // ─── 实战项目一（Ch15）─────────────────────────────────────────────
  {
    id: "ch15",
    number: 15,
    title: "实战项目一：全栈任务管理系统",
    subtitle: "Next.js + Axum + PostgreSQL + WebSocket",
    description: "综合前四阶段所有技能，构建带实时协作的生产级全栈应用——Rust 后端 + Next.js 前端 + Docker 部署。",
    status: "available",
    duration: "8 小时",
    concepts: ["Axum WebSocket 广播", "ts-rs 类型同步", "Docker Compose 本地开发", "全栈架构设计"],
    project: "TaskForge — 实时协作任务管理系统",
    slug: "project-fullstack",
  },
  // ─── 第五阶段：运维（Ch16-17）──────────────────────────────────────
  {
    id: "ch16",
    number: 16,
    title: "运维基础：容器化与 CI/CD",
    subtitle: "Docker · GitHub Actions · 自动化部署",
    description: "Docker 多阶段构建压缩镜像体积、GitHub Actions 自动化测试与发布、环境变量安全管理。",
    status: "available",
    duration: "5 小时",
    concepts: ["Docker 多阶段构建", "cargo-chef 层缓存", "GitHub Actions CI/CD", "Secrets 安全管理"],
    project: "完整 CI/CD 流水线",
    slug: "devops",
  },
  {
    id: "ch17",
    number: 17,
    title: "云原生运维",
    subtitle: "Kubernetes · 可观测性 · SRE 实践",
    description: "Helm 部署、Prometheus + Grafana 监控、OpenTelemetry 链路追踪、HPA 自动扩缩容——生产级 K8s 运维。",
    status: "available",
    duration: "5 小时",
    concepts: ["K8s Deployment/HPA", "Prometheus 指标暴露", "OpenTelemetry 追踪", "蓝绿/滚动发布"],
    project: "生产级云原生部署架构",
    slug: "cloud-ops",
  },
  // ─── 第六阶段：AI（Ch18-19）────────────────────────────────────────
  {
    id: "ch18",
    number: 18,
    title: "AI 应用集成",
    subtitle: "LLM API · RAG · 流式响应 · Agent",
    description: "调用 OpenAI/Claude API、流式响应、构建 RAG 检索增强生成、向量数据库——高性能 AI 应用。",
    status: "available",
    duration: "5 小时",
    concepts: ["async-openai API 调用", "SSE 流式响应", "pgvector RAG 管道", "AI Agent Function Calling"],
    project: "AI 代码审查助手",
    slug: "ai",
  },
  {
    id: "ch19",
    number: 19,
    title: "AI 运维：模型服务与 MLOps",
    subtitle: "推理服务 · GPU 调度 · 成本优化",
    description: "Rust AI 推理网关、多模型智能路由、Token 成本追踪、vLLM 集成、GPU K8s 调度——让 AI 服务跑得快、算得省。",
    status: "available",
    duration: "4 小时",
    concepts: ["LLM 推理网关", "多模型路由策略", "Token 成本追踪", "GPU K8s 调度"],
    project: "生产级 LLM 推理网关",
    slug: "ai-ops",
  },
  // ─── 终章实战（Ch20）───────────────────────────────────────────────
  {
    id: "ch20",
    number: 20,
    title: "最终实战：AI 驱动的全栈服务",
    subtitle: "综合 Web · DB · 运维 · AI 的毕业项目",
    description: "综合 20 章所有技能：RAG 智能代码审查、WebSocket 实时通知、GitHub Actions CI/CD、K8s 部署、Grafana 监控。",
    status: "available",
    duration: "10 小时",
    concepts: ["RAG 代码审查引擎", "全链路可观测性", "生产部署检查清单", "AI 成本优化实践"],
    project: "CodeForge — AI 代码审查平台",
    slug: "capstone",
  },
];

export const jsRustComparisons = [
  {
    concept: "变量声明",
    js: `// JavaScript: 默认可变
let name = "Alice";
name = "Bob"; // ✓ 随时修改

const arr = [1, 2, 3];
arr.push(4); // ✓ 内容可变`,
    rust: `// Rust: 默认不可变
let name = "Alice";
// name = "Bob"; // ✗ 编译错误！

let mut arr = vec![1, 2, 3];
arr.push(4); // ✓ 需要 mut 声明`,
    insight: "Rust 的不可变默认值迫使你明确意图，消灭了大量运行时 bug。",
  },
  {
    concept: "错误处理",
    js: `// JavaScript: try/catch + undefined
async function getUser(id) {
  try {
    const res = await fetch(\`/api/\${id}\`);
    return res.json();
  } catch (e) {
    console.error(e); // 忘记处理？
    // 函数隐式返回 undefined
  }
}`,
    rust: `// Rust: Result<T, E> 强制处理
async fn get_user(id: u32)
  -> Result<User, AppError>
{
  let res = fetch_user(id).await?;
  // ? 操作符：错误自动传播
  // 编译器保证你不能忽略错误
  Ok(res)
}`,
    insight: "Result 类型让错误成为类型系统的一部分。忘记处理 = 编译失败。",
  },
  {
    concept: "并发模型",
    js: `// JavaScript: 单线程 + 事件循环
// 所有异步都在同一个线程
const [a, b] = await Promise.all([
  fetchA(), fetchB()
]);
// 不存在数据竞争，但也
// 无法利用多核 CPU`,
    rust: `// Rust: 真正的多线程并发
// 编译器保证无数据竞争
let (a, b) = tokio::join!(
  fetch_a(),
  fetch_b()
);
// 可跨多核并行
// Send + Sync trait 保证线程安全`,
    insight: "Rust 在编译期消除数据竞争，让多线程像单线程一样安全。",
  },
];
