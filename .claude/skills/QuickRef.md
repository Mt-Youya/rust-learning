# RustForge Video Skill — 快速参考

## 单章触发词

以下任意短语触发此 Skill：

- "把第 N 章做成视频"
- "生成第 N 章的视频内容包"
- "SCRIPTS[N] 转视频脚本"
- "帮我处理所有权那章的视频"
- "给第三章生成旁白和字幕"

## 各轨道可单独触发

| 用户说 | 只生成 |
|--------|--------|
| "只要旁白脚本" | 轨道 A |
| "只要 SRT 字幕" | 轨道 B |
| "给我 Three.js 的场景配置" | 轨道 C |
| "写 MDX 文件" | 轨道 D |
| "给 gen_video.py 的配置" | 轨道 E |
| "全部都要" | 轨道 A+B+C+D+E |

## 批量处理（多章）

```
把第 1、2、3 章都处理一遍，只要旁白脚本和 SRT，
按 ch1_narration.txt、ch1_subtitles.srt 这样的格式输出。
```

Agent 会串行处理，每章解析完先确认再继续。

## 覆写参数

在触发词后可追加：

| 参数 | 示例 |
|------|------|
| TTS 语速 | "语速 1.15" → `tts.speed: 1.15` |
| 声音 | "用女声" → `voice: zh-CN-XiaoxiaoNeural` |
| 跳过 Three.js | "不需要动画场景" → 跳过轨道 C |
| 只要代码对比 | "只生成 CodeCompare 组件" → 轨道 D 仅输出 CodeCompare |

## 项目路径速查

```
旁白脚本  →  rust-learning/scripts/ch{N}_narration.txt
字幕文件  →  rust-learning/scripts/ch{N}_subtitles.srt
场景规格  →  rust-learning/scripts/ch{N}_scenes.yaml
视频配置  →  rust-learning/scripts/ch{N}_video_config.py
MDX 草稿  →  rust-learning/apps/web/src/content/chapters/{slug}.mdx
```

## 章节 Slug 对照表

| 章节 | slug |
|------|------|
| Ch01 | getting-started |
| Ch02 | variables-and-types |
| Ch03 | ownership-borrowing-lifetimes |
| Ch04 | structs-enums-pattern-matching |
| Ch05 | error-handling |
| Ch06 | generics-traits-iterators |
| Ch07 | smart-pointers |
| Ch08 | concurrency-async |
| Ch09 | web-backend-axum |
| Ch10 | database-sqlx |
| Ch11 | fullstack |
| Ch12 | devops |
| Ch13 | testing-toolchain |
| Ch14 | performance-unsafe |
| Ch15 | cli-and-wasm |
| Ch16 | rust-and-ai |

## 旁白中模糊提示的处理规则

讲稿原文经常出现「见屏幕代码」「屏幕上可以看到」等模糊提示。
处理规则：

1. 如果上下文能推断出具体代码 → 替换为 `[CODE:rust:{描述}]`
2. 如果是终端命令 → 替换为 `[TERM:{命令}]`
3. 如果是对比 → 替换为 `[COMPARE:JS vs Rust]`
4. 如果是抽象概念示意 → 替换为 `[THREE:{scene_id}]`
5. 无法推断 → 保留占位符 `[VISUAL:TODO:{原文描述}]` 并在质检中标出

## CosyVoice 特殊字符处理

| 原文写法 | TTS 朗读指导 |
|---------|------------|
| `&str` | → 在旁白里写「字符串切片」，括注`(&str)` |
| `Vec<T>` | → 「向量 T」，括注`(Vec<T>)` |
| `Result<T, E>` | → 「结果 T E」 |
| `->` | → 「返回」或「箭头」 |
| `::` | → 「双冒号」，路径时念完整名称 |
| `//` | → 跳过不念，或说「注释」 |
| 数字下标 `1_000_000` | → 「一百万」 |