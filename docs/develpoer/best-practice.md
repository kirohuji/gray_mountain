# Ren'Py 项目最佳实践指南

> 本文档基于 Ren'Py 8.x 编写，部分特性在 7.x 中可能有差异。建议始终参考 [官方文档](https://www.renpy.org/doc/html/) 获取最新信息。

## 1. 项目目录结构

```
game/
├── script.rpy          # 主入口，负责跳转各章节
├── options.rpy         # 全局配置（由 Ren'Py 自动生成，保持整洁）
├── gui.rpy             # GUI 配置
├── screens.rpy         # 自定义屏幕
├── definitions.rpy     # 全局变量、角色定义、图像别名
├── chapters/
│   ├── chapter01.rpy
│   ├── chapter02.rpy
│   └── ...
├── images/
│   ├── bg/             # 背景图
│   ├── cg/             # CG 图
│   ├── sprites/        # 角色立绘
│   │   └── eileen/
│   └── ui/             # UI 相关图片
├── audio/
│   ├── bgm/            # 背景音乐
│   ├── sfx/            # 音效
│   └── voice/          # 语音（可选）
└── fonts/              # 自定义字体
```

### 组织原则

- 按功能而非按文件类型组织 `.rpy` 文件，便于多人协作。
- 图像按类型分子目录存放，Ren'Py 会递归扫描 `game/` 下所有图片，因此分目录不影响引用。
- 避免所有内容写在单个 `script.rpy` 中，超过 1000 行就应拆分。

## 2. 脚本编写规范

### 命名规范

```renpy
# ✅ 推荐：下划线命名，语义清晰
label chapter01_start:
label bad_ending_route_a:

# ❌ 避免：含糊的名称
label start2:
label aaa:
```

### Label 管理

```renpy
# 主入口保持简洁，仅做跳转
label start:
    jump chapter01_opening

# 每个章节有明确的起始和结束 label
label chapter01_opening:
    scene bg_town_day
    ...
    jump chapter01_cafe

label chapter01_cafe:
    ...
    jump chapter02_start
```

### 缩进与代码风格

- 使用 4 个空格缩进（Ren'Py 官方推荐，避免制表符）。
- 每个 `menu` 选项后立即写对应的处理逻辑，不要把所有分支堆到文件末尾。
- 为复杂的 `if`/`elif`/`else` 分支添加注释，说明触发条件。

```renpy
menu:
    # 玩家好感度 >= 5 时才出现该选项
    "一起去散步吧" if affection >= 5:
        $ affection += 1
        jump route_good
    "我有些事要忙":
        jump route_neutral
```

### Python 代码块

```renpy
# 简单赋值用 $ 单行
$ score += 10

# 复杂逻辑用 python: 块
python:
    import datetime
    current_hour = datetime.datetime.now().hour
    if current_hour < 12:
        time_of_day = "morning"
    else:
        time_of_day = "afternoon"
```

## 3. 角色与对话系统

### 角色定义集中管理

将所有角色定义放在 `definitions.rpy` 中：

```renpy
# definitions.rpy

define e = Character("Eileen",
    color="#c8ffc8",
    what_prefix='"',
    what_suffix='"'
)

define n = Character("Narrator",
    kind=narrator
)

define s = Character("Sophie",
    color="#ffc8c8",
    voice_tag="sophie"  # 配音标签
)
```

### 对话编写技巧

```renpy
# ✅ 使用角色对象，保持一致性
e "今天天气真好！"
s "是啊，要不要去公园？"

# ✅ 利用 extend 续写长对话
e "这件事说来话长……"
extend " 从很久很久以前说起。"

# ✅ 动态内容使用字符串插值
$ player_name = "玩家"
e "你好，[player_name]！很高兴认识你。"

# ❌ 避免裸字符串对话（失去角色格式）
"今天天气真好！"
```

### NVL 模式（全屏小说风格）

```renpy
# 切换为 NVL 模式适合大段叙事
define e_nvl = Character("Eileen", kind=nvl)

label story_flashback:
    nvl clear
    e_nvl "那是一个寒冷的冬夜……"
    e_nvl "风雪交加，她独自站在桥头。"
    nvl clear
```

## 4. 图像与资源管理

### 图像定义规范

```renpy
# definitions.rpy 中集中定义图像

# 背景
image bg town day = "images/bg/town_day.webp"
image bg town night = "images/bg/town_night.webp"

# 立绘（使用 LayeredImage 实现多层合成）
layeredimage eileen:
    always:
        "images/sprites/eileen/body.png"
    group expression:
        attribute normal default:
            "images/sprites/eileen/face_normal.png"
        attribute happy:
            "images/sprites/eileen/face_happy.png"
        attribute sad:
            "images/sprites/eileen/face_sad.png"
    group outfit:
        attribute school default:
            "images/sprites/eileen/outfit_school.png"
        attribute casual:
            "images/sprites/eileen/outfit_casual.png"
```

### 图像格式建议

| 用途 | 推荐格式 | 说明 |
|---|---|---|
| 背景图 | WebP / JPEG | 有损压缩，文件小 |
| 带透明的立绘 | WebP (有透明通道) / PNG | WebP 体积更小 |
| UI 小图标 | PNG | 需要精确像素 |
| 动画帧 | PNG 序列 / WebM | 取决于复杂度 |

> **注意：** 从 Ren'Py 7.4 起支持 WebP，强烈推荐替换 PNG 以减小包体积。

### 图像预加载

```renpy
# 在场景切换前预加载下一章节的图像
label chapter01_end:
    # 提前加载第二章资源
    $ renpy.start_predict("bg town night", "eileen sad school")

    e "明天见……"
    jump chapter02_start
```

## 5. 音频管理

### 音频定义与调用

```renpy
# definitions.rpy
define audio.bgm_town = "audio/bgm/town_theme.ogg"
define audio.sfx_door = "audio/sfx/door_open.ogg"

# 脚本中使用
label chapter01_start:
    play music audio.bgm_town fadeout 1.0 fadein 1.0
    play sound audio.sfx_door
```

### 音频格式建议

- **BGM**：OGG Vorbis（所有平台兼容，体积小）
- **音效**：OGG 或 WAV（WAV 延迟更低，适合短促音效）
- **语音**：OGG

### 音频管理最佳实践

```renpy
# 使用 channel 区分不同音频流
play music "bgm.ogg" channel "music"
play sound "rain.ogg" channel "ambient" loop  # 环境音独立通道

# 场景切换时淡出
scene bg interior:
    with dissolve
stop music fadeout 2.0
play music "indoor_bgm.ogg" fadein 1.5
```

## 6. 存档与持久化数据

### 存档变量管理

```renpy
# 默认情况下，所有在 init 之外的变量都会被存档
# 使用 default 语句声明变量，确保存档兼容性

default affection_eileen = 0
default affection_sophie = 0
default flags = {}              # 用字典统一管理旗标
default chapter_reached = 1

# 持久化数据（跨存档共享，适合成就/解锁内容）
$ persistent.total_playtime = getattr(persistent, "total_playtime", 0)
$ persistent.endings_unlocked = getattr(persistent, "endings_unlocked", set())
```

### 存档兼容性

当更新游戏版本时，用 `default` 而非 `define` 声明变量，新增变量不会破坏旧存档：

```renpy
# ✅ 正确：新版本新增变量用 default
default new_feature_flag = False  # 旧存档读取时自动填入默认值

# ❌ 错误：用 $ 在 label 中初始化，旧存档会跳过这行
label start:
    $ new_feature_flag = False   # 旧存档加载后此行不会执行
```

## 7. 变量与状态管理

### 用字典统一管理旗标

```renpy
default flags = {}

# 设置旗标
$ flags["met_eileen"] = True
$ flags["chose_park"] = True

# 检查旗标
if flags.get("met_eileen", False):
    e "我们之前见过！"
```

### 避免全局变量污染

```renpy
# ✅ 命名空间化，避免冲突
default ch1 = {}    # 第一章状态
default ch2 = {}    # 第二章状态

$ ch1["opened_door"] = True

# ❌ 避免大量散乱的顶层变量
default opened_door = False
default talked_to_guard = False
default found_key = False
# 几十个这样的变量会难以维护
```

### 使用 Python 类封装复杂状态

```renpy
init python:
    class CharacterStats:
        def __init__(self, name):
            self.name = name
            self.affection = 0
            self.trust = 0

        def befriend(self):
            self.affection += 1
            self.trust += 1

default eileen_stats = CharacterStats("Eileen")
default sophie_stats = CharacterStats("Sophie")

# 使用
$ eileen_stats.befriend()
e "谢谢你帮助我！"
```

## 8. 屏幕（Screen）与 UI

### Screen 基本规范

```renpy
# screens.rpy

screen custom_hud():
    # 使用 zorder 控制层级
    zorder 10

    # 固定位置元素
    frame:
        xalign 0.0
        yalign 0.0
        padding (10, 10)

        hbox:
            spacing 5
            text "好感度：" size 16
            text str(affection_eileen) size 16 color "#ff9999"

# 在脚本中显示/隐藏
label chapter01_start:
    show screen custom_hud
    ...
    hide screen custom_hud
```

### 避免在 Screen 中写业务逻辑

```renpy
# ❌ 不推荐：在 screen 的 action 里写复杂逻辑
screen bad_example():
    textbutton "确认":
        action [
            SetVariable("x", 1),
            SetVariable("y", 2),
            SetVariable("z", x + y),  # 容易出错
            Jump("next_label")
        ]

# ✅ 推荐：action 只做跳转，逻辑放在 label 里
screen good_example():
    textbutton "确认":
        action Jump("handle_confirm")

label handle_confirm:
    $ x = 1
    $ y = 2
    $ z = x + y
    jump next_label
```

### GUI 主题定制

```renpy
# gui.rpy 中统一管理颜色和字体
define gui.accent_color = '#c8a4c8'
define gui.idle_color = '#888888'
define gui.hover_color = '#ffffff'
define gui.text_font = "fonts/NotoSansCJK.otf"
define gui.text_size = 22
```

## 9. 性能优化

### ATL（动画变换语言）优化

```renpy
# ✅ 简单移动用 transform 而非每帧 python 计算
transform slide_in_left:
    xpos -200 alpha 0
    linear 0.5 xpos 0 alpha 1

show eileen normal at slide_in_left
```

### 图像缓存管理

```renpy
# 控制图像缓存大小（在 options.rpy 中）
define config.image_cache_size = 8      # 缓存图像数（移动端调小）
define config.cache_surfaces = False    # 减少内存占用

# 主动释放不再使用的图像
$ renpy.free_memory()
```

### 减少 init 阶段开销

```renpy
# ❌ 避免在 init python 中做耗时操作
init python:
    import time
    time.sleep(1)   # 拖慢启动

# ✅ 延迟到实际需要时再执行
label start:
    python:
        # 按需加载
        heavy_data = load_data()
```

### 移动端专项优化

```renpy
# options.rpy
init python:
    if renpy.android or renpy.ios:
        config.image_cache_size = 4
        config.sound_buffer_size = 8192  # 减小音频缓冲
```

## 10. 多语言支持（翻译）

### 提取翻译字符串

```bash
# 在 Ren'Py Launcher 中执行，或命令行：
renpy.sh game generate_translations zh_hans
```

### 翻译文件结构

```renpy
# game/tl/zh_hans/script.rpy（自动生成）

translate zh_hans chapter01_opening_abc12345:
    # e "Hello, world!"
    e "你好，世界！"
```

### 多语言图像替换

```renpy
# 为不同语言提供不同图像（如含文字的 CG）
translate zh_hans strings:
    old "images/cg/letter_en.png"
    new "images/cg/letter_zh.png"
```

### 语言切换

```renpy
# 在设置菜单中允许玩家切换语言
screen language_menu():
    vbox:
        textbutton "English":
            action Language(None)   # None 表示默认语言
        textbutton "简体中文":
            action Language("zh_hans")
        textbutton "日本語":
            action Language("ja")
```

## 11. 版本控制

### .gitignore 推荐配置

```
# Ren'Py 生成文件
game/cache/
game/saves/
game/log.txt
game/errors.txt
*.rpyc
*.rpymc

# 构建产物
build/
dist/

# 编辑器配置
.vscode/
.idea/
```

### 多人协作建议

- 按章节或功能拆分 `.rpy` 文件，减少合并冲突。
- 美术/音频资源使用 Git LFS 管理，避免仓库臃肿。
- 建立 Commit 规范，例如 `[script] ch02: 添加咖啡馆场景` 或 `[art] eileen: 新增哭泣表情`。

## 12. 测试与调试

### 开发模式工具

```renpy
# 在 options.rpy 中开启开发模式
define config.developer = True  # 启用 Shift+D 调试菜单、Shift+R 重载

# 快速跳转测试（开发时使用）
label start:
    if config.developer:
        jump chapter03_ending_test
```

### 使用 Lint 检查脚本

在 Ren'Py Launcher 中执行 "Check Script (Lint)"，可检测：

- 未定义的图像引用
- 跳转到不存在的 label
- 变量类型错误

### 编写测试用例

```renpy
# 利用 Ren'Py 的 Screen 测试功能
init python:
    def test_affection_system():
        assert affection_eileen >= 0, "好感度不能为负数"
        assert affection_eileen <= 100, "好感度不能超过上限"
```

### 常见错误排查

| 错误现象 | 可能原因 | 解决方案 |
|---|---|---|
| 图像不显示 | 路径/文件名大小写错误 | 检查 images/ 目录，注意大小写 |
| 存档无法加载 | 新版本删除了变量 | 用 default 补充默认值 |
| 转场卡顿 | 图像过大未压缩 | 转换为 WebP，降低分辨率 |
| 音频延迟 | WAV 文件过大 | 短音效用 OGG，或减小 buffer |
| 翻译未生效 | .rpyc 缓存 | 删除 game/cache/ 后重启 |

## 13. 发布与打包

### 构建配置（options.rpy）

```renpy
define build.name = "MyVisualNovel"
define build.version = "1.0.0"

# 排除不需要打包的文件
build.classify('**/*.psd', None)       # 排除 PSD 源文件
build.classify('**/.DS_Store', None)   # 排除 macOS 文件
build.classify('game/dev/**', None)    # 排除开发专用脚本
```

### 多平台注意事项

| 平台 | 注意事项 |
|---|---|
| Windows | 路径分隔符问题；注意 .exe 图标设置 |
| macOS | 需要代码签名才能顺利运行；.app 包结构 |
| Linux | 确保字体文件随包分发 |
| Android | 屏幕分辨率适配；config.screen_width/height 设置 |
| iOS | 需要 Apple 开发者账号；资源大小有限制 |
| Web (HTML5) | 音频自动播放受浏览器限制；存档用 IndexedDB |

### 发布前检查清单

- [ ] 运行 Lint 无错误
- [ ] 删除所有调试代码，关闭 developer 模式
- [ ] 确认版权信息（字体、音乐授权）
- [ ] 测试全平台存档读写
- [ ] 压缩图像和音频至合理大小
- [ ] 确认 .gitignore 和构建排除规则正确
- [ ] 测试从头到尾的完整流程（至少一遍）

## 附录：常用代码速查

```renpy
# 显示/隐藏图像
show eileen happy school at left with dissolve
hide eileen with dissolve

# 场景切换
scene bg town day with fade

# 变量操作
$ score += 1
default score = 0

# 条件跳转
if score >= 10:
    jump good_ending
else:
    jump bad_ending

# 菜单选择
menu:
    "选项 A":
        pass
    "选项 B":
        pass

# 播放音频
play music "bgm.ogg" fadein 1.0
play sound "sfx.ogg"
stop music fadeout 2.0

# 调用子程序
call subroutine_label
return

# 延时等待
pause 2.0  # 等待 2 秒
```
