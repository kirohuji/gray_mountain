# 《灰山》AI 美术 Prompts 体系 — NovelAI V4.5

> 视觉风格：**混合媒材 — 水彩渲染 + 墨线勾勒 + 炭笔阴影**
> UI 主题：[ess Black & White Horror UI Theme](https://ess-vn-assets.itch.io/renpy-black-white-ui-theme)

---

## 风格定义

所有 prompt 统一使用以下混合媒材标签：

```
monochrome, sepia tone, umber, muted tones, limited palette, year 1930,
mixed media, traditional media,
watercolor wash, pigment granulation,
ink line art, dip pen lines, uneven ink flow,
charcoal shading, charcoal smudge, powdery texture,
handmade, rough watercolor paper, paper texture,
bleeding edges, water stain,
visible brushstrokes, painterly, loose brushwork,
dramatic shadows, chiaroscuro, low-key lighting,
atmospheric, fog, mist.
```

**核心反 AI 策略**：`uneven ink flow` + `organic` + `handmade` + `bleeding edges`
→ 刻意保留手工不完美，避免机械感

---

## 目录结构

```
prompts/
├── README.md
├── 00-风格定义/               ← 修改风格只改这里
│   ├── 主风格基准.txt
│   ├── 黑白恐怖风格.txt
│   ├── 质量标签集合.txt
│   └── negative_prompt.txt
│
├── 01-角色/                   ← LayeredImage 5层结构
│   ├── 汤姆-主角.txt          ✅ 已更新混合媒材
│   ├── 艾琳娜-妻子.txt        ✅ 已更新混合媒材
│   ├── 吉姆-好友.txt
│   ├── 亨利韦斯特-院长.txt
│   ├── 迈克尔神父.txt
│   └── NPC通用.txt
│
├── 02-背景场景/
│   ├── 灰山外景.txt
│   ├── 卧室.txt
│   ├── 客厅.txt
│   ├── 厨房.txt
│   ├── 会诊室.txt
│   ├── 灰山教堂.txt
│   ├── 疗养院外景.txt
│   ├── 疗养院病房.txt
│   └── 疗养院阳台.txt
│
├── 03-事件CG/
│   ├── 噩梦-灰山脚下.txt      ✅ 已更新
│   ├── 噩梦-山在呼吸.txt      ✅ 已更新
│   ├── 确诊时刻.txt           ✅ 已更新
│   ├── 上山路途.txt           ✅ 已更新
│   ├── 教堂相遇.txt           ✅ 已更新
│   └── 疗养院-希望.txt        ✅ 已更新
│
├── 04-UI元素/
│   ├── 文本框样式.txt
│   ├── 按钮与图标.txt
│   ├── 菜单背景.txt
│   └── 装饰元素.txt
│
└── 05-氛围与特效/
    ├── 雾气效果.txt
    ├── 雪花效果.txt
    ├── 噪点纹理.txt
    ├── 光影效果.txt
    └── 恐怖氛围.txt
```

---

## V4.5 推荐参数

| 参数 | 值 | 说明 |
|------|-----|------|
| 模型 | V4.5 Full | |
| Steps | 28 | |
| Prompt Guidance | 4.5 - 5.0 | 低于默认，保留水彩渗色自由 |
| Prompt Guidance Rescale | 0.40 | |
| Decrisper | OFF | 水彩不需要锐化 |
| 立绘 | 832×1216 | 生成后裁剪到 832×2176 |
| 场景/CG | 1920×1080 | |

---

## 相关文档

| 文档 | 说明 |
|------|------|
| `docs/requirements/` | 需求文档：风格规格 + 资产清单 + LayeredImage 规格 + CG 清单 |
| `docs/settings/` | 设定文档：世界观 + 角色 + 时间线 + 故事片段 |
| `.cursor/rules/` | 开发规则：编码规范 + 美术管线 + 章节结构 + Prompt 使用 |

---

## 版本

- v4.0 — 混合媒材风格重定义 + LayeredImage 分层 + 完整需求文档
- v3.0 — 对齐 ess UI Theme
- v2.0 — V4.5 适配
- v1.0 — 初始版本
