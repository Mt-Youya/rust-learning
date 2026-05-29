请按照你的完整输出规范处理以下章节，生成完整的视频制作包。

---

## 章节元数据

```json
{
  "project": "RustForge",
  "chapter_id": "{{chapter_id}}",
  "title": "{{title}}",
  "source_type": "{{source_type}}",
  "target_audience": "前端工程师 / Rust 初学者",
  "video_style": "1+3+代码演示",
  "language": "zh-CN",
  "duration_target_minutes": {{duration_minutes}},
  "tone": "清晰、专业、带一点 B站节奏感",
  "extra_notes": [
    "优先使用前端工程师视角（npm/React/TypeScript）做类比",
    "类比时注意加'不完全等价'提示，避免误导",
    "视频作为网站 MDX 章节的配套内容，不需要重复文字内容",
    "代码演示要真实可运行，不要编造输出"
  ]
}
```

---

## 章节原文

{{source_content}}

---

请输出完整的视频制作包，包含：一、章节理解，二、教学设计，三、完整旁白脚本（含 TTS 纯文本版），四、分镜 storyboard（JSON），五、动画规划 manim_plan（JSON），六、代码录制计划 recording_plan（JSON），七、合成与发布 render_manifest + publish_payload（JSON），八、短视频切片建议，九、网站嵌入点建议。
