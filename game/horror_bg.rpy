# ============================================================
# 恐怖背景滤镜系统
# 用途：将照片背景处理为灰阶恐怖风格
# 用法：
#   show screen horror_bg("bg_apartment_foyer_evening")
#   scene bg_apartment_foyer_evening at horror_photo_bg
# ============================================================

# ---- 核心变换：照片 → 黑白恐怖背景 ----

transform horror_photo_bg:
    xysize (1920, 1080)
    blur 1.4
    matrixcolor SaturationMatrix(0.0) * ContrastMatrix(0.60) * BrightnessMatrix(-0.12)

# ---- 完整叠加 Screen：滤镜 + 暗角 + 底部黑雾 ----

screen horror_bg(photo):
    # 原始照片 + 黑白滤镜
    add photo at horror_photo_bg

    # 轻微冷灰/紫灰覆盖，让黑白不那么死
    add Solid("#1b1a22"):
        alpha 0.18
        xysize (1920, 1080)

    # 顶部轻微压暗
    add Solid("#000000"):
        alpha 0.18
        xpos 0
        ypos 0
        xysize (1920, 180)

    # 左右暗角
    add Solid("#000000"):
        alpha 0.28
        xpos 0
        ypos 0
        xysize (180, 1080)

    add Solid("#000000"):
        alpha 0.28
        xpos 1740
        ypos 0
        xysize (180, 1080)

    # 底部黑雾遮罩：多层黑条模拟渐变
    add Solid("#000000"):
        alpha 0.10
        xpos 0
        ypos 520
        xysize (1920, 120)

    add Solid("#000000"):
        alpha 0.22
        xpos 0
        ypos 620
        xysize (1920, 120)

    add Solid("#000000"):
        alpha 0.38
        xpos 0
        ypos 720
        xysize (1920, 140)

    add Solid("#000000"):
        alpha 0.58
        xpos 0
        ypos 830
        xysize (1920, 160)

    add Solid("#000000"):
        alpha 0.78
        xpos 0
        ypos 940
        xysize (1920, 140)


# ---- 扩展变换：不同强度的恐怖氛围 ----

# 轻度：不需要太黑的场景
transform horror_photo_bg_light:
    xysize (1920, 1080)
    blur 1.0
    matrixcolor SaturationMatrix(0.15) * ContrastMatrix(0.65) * BrightnessMatrix(-0.05)

# 重度：噩梦 / 幻觉 / 高异常值
transform horror_photo_bg_heavy:
    xysize (1920, 1080)
    blur 2.2
    matrixcolor SaturationMatrix(0.0) * ContrastMatrix(0.45) * BrightnessMatrix(-0.20)

# 动态：从模糊到清晰（醒来效果）
transform wake_up:
    xysize (1920, 1080)
    blur 12.0
    matrixcolor SaturationMatrix(0.0) * ContrastMatrix(0.40) * BrightnessMatrix(-0.25)
    linear 4.0 blur 0.0
    linear 4.0 matrixcolor SaturationMatrix(1.0) * ContrastMatrix(1.0) * BrightnessMatrix(0.0)
