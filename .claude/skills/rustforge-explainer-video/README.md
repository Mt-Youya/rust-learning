# RustForge Course Video Skill

这是一个专门给 RustForge 项目使用的 Agent Skill。

它可以帮助你把课程文本、README、技术笔记、代码草稿转换成：

- RustForge 风格的 MDX 章节
- 中文长篇讲解稿
- CosyVoice / edge-tts 友好的 TTS 文本
- `gen_audio.py` 的 `SCRIPTS[n]`
- `gen_video.py` / `gen_video_3min.py` 的 `CHAPTERS[n]` 和 `SLIDES[n]`
- WebVTT 字幕
- 3D 可视化动画方案
- Three.js / React Three Fiber 组件思路
- 每章实战练习

## 推荐放置位置

```txt
~/.claude/skills/rustforge-course-video-skill/
```

或者你的 Agent 支持的 skills 目录。

## 使用方式

```txt
Use the rustforge-course-video skill.

根据下面文本生成 RustForge 第 8 章 Web 后端的完整章节包：
- MDX
- 长篇视频讲稿
- SLIDES
- CHAPTERS
- 字幕
- 3D 可视化方案
- 实战项目
```

## 课程目录

Skill 已内置 README 中的 16 章目录，默认按 README 的章节顺序生成。

如果你的旧 `gen_video.py` 脚本章节顺序与 README 不同，Skill 会默认以 README 为准；你也可以明确要求“兼容旧脚本顺序”。

## 关键项目路径

```txt
apps/web/src/content/chapters/{slug}.mdx
apps/web/src/data/curriculum.ts
apps/web/src/components/animations/
scripts/gen_audio.py
scripts/gen_video.py
scripts/gen_video_3min.py
scripts/cosyvoice_tts.py
apps/web/public/videos/
apps/web/public/subtitles/
```
