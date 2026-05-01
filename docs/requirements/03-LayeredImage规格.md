# LayeredImage 实现规格 — 《灰山》

> 版本：v1.0 | 对应 Ren'Py `layeredimage` 语句

---

## 一、通用规范

### 文件结构

```
game/images/sprites/
├── tom/
│   ├── body_normal.webp
│   ├── head_normal.webp
│   ├── eyes_tired.webp
│   ├── eyes_sharp.webp
│   ├── eyes_tearful.webp
│   ├── eyes_soft.webp
│   ├── eyes_exhausted.webp
│   ├── mouth_anxious.webp
│   ├── mouth_sad.webp
│   ├── mouth_determined.webp
│   ├── mouth_scared.webp
│   ├── mouth_tender.webp
│   ├── extra_stubble.webp
│   ├── extra_sweat.webp
│   └── extra_darkcircles.webp
├── elena/
│   ├── body_normal.webp
│   ├── ...
├── jim/
├── west/
├── father/
├── harding/
├── nurse/
└── patient_m/
```

### 图像要求

- 所有分层的**画布尺寸必须一致**：832 × 2176 px
- 各层**位置对齐**：头部在相同坐标，眼睛/嘴在相同坐标
- 透明背景（WebP lossless 支持 alpha 通道）
- 墨线勾勒统一粗细和风格

---

## 二、汤姆·卡特 LayeredImage 定义

```renpy
layeredimage tom:

    always:
        "images/sprites/tom/body_normal.webp"

    group head:
        attribute normal default:
            "images/sprites/tom/head_normal.webp"

    group eyes:
        attribute tired default:
            "images/sprites/tom/eyes_tired.webp"
        attribute sharp:
            "images/sprites/tom/eyes_sharp.webp"
        attribute tearful:
            "images/sprites/tom/eyes_tearful.webp"
        attribute soft:
            "images/sprites/tom/eyes_soft.webp"
        attribute exhausted:
            "images/sprites/tom/eyes_exhausted.webp"

    group mouth:
        attribute anxious default:
            "images/sprites/tom/mouth_anxious.webp"
        attribute sad:
            "images/sprites/tom/mouth_sad.webp"
        attribute determined:
            "images/sprites/tom/mouth_determined.webp"
        attribute scared:
            "images/sprites/tom/mouth_scared.webp"
        attribute tender:
            "images/sprites/tom/mouth_tender.webp"

    group extra:
        attribute stubble:
            "images/sprites/tom/extra_stubble.webp"
        attribute sweat:
            "images/sprites/tom/extra_sweat.webp"
        attribute darkcircles:
            "images/sprites/tom/extra_darkcircles.webp"
```

**使用示例**：
```renpy
show tom at left                    # 默认（tired eyes + anxious mouth）
show tom sharp determined at left   # 锐利眼神 + 坚定
show tom tearful sad at left        # 含泪 + 悲伤
show tom exhausted scared sweat at center  # 极度恐惧 + 冷汗
```

---

## 三、艾琳娜·卡特 LayeredImage 定义

```renpy
layeredimage elena:

    always:
        "images/sprites/elena/body_normal.webp"

    group head:
        attribute normal default:
            "images/sprites/elena/head_normal.webp"

    group eyes:
        attribute gentle default:
            "images/sprites/elena/eyes_gentle.webp"
        attribute tired:
            "images/sprites/elena/eyes_tired.webp"
        attribute tearful:
            "images/sprites/elena/eyes_tearful.webp"
        attribute closed:
            "images/sprites/elena/eyes_closed.webp"
        attribute brave:
            "images/sprites/elena/eyes_brave.webp"

    group mouth:
        attribute smiling default:
            "images/sprites/elena/mouth_smiling.webp"
        attribute coughing:
            "images/sprites/elena/mouth_coughing.webp"
        attribute worried:
            "images/sprites/elena/mouth_worried.webp"
        attribute encouraging:
            "images/sprites/elena/mouth_encouraging.webp"
        attribute pain:
            "images/sprites/elena/mouth_pain.webp"

    group extra:
        attribute bluelips:
            "images/sprites/elena/extra_bluelips.webp"
        attribute flush:
            "images/sprites/elena/extra_flush.webp"
        attribute handkerchief:
            "images/sprites/elena/extra_handkerchief.webp"
```

---

## 四、简化角色 LayeredImage 定义

### 吉姆

```renpy
layeredimage jim:
    always: "images/sprites/jim/body_normal.webp"
    group head: attribute normal default: "images/sprites/jim/head_normal.webp"
    group eyes:
        attribute calm default: "images/sprites/jim/eyes_calm.webp"
        attribute concerned: "images/sprites/jim/eyes_concerned.webp"
        attribute serious: "images/sprites/jim/eyes_serious.webp"
    group mouth:
        attribute calm default: "images/sprites/jim/mouth_calm.webp"
        attribute concerned: "images/sprites/jim/mouth_concerned.webp"
        attribute serious: "images/sprites/jim/mouth_serious.webp"
```

### 韦斯特医生

```renpy
layeredimage west:
    always: "images/sprites/west/body_normal.webp"
    group head: attribute normal default: "images/sprites/west/head_normal.webp"
    group eyes:
        attribute professional default: "images/sprites/west/eyes_professional.webp"
        attribute cold: "images/sprites/west/eyes_cold.webp"
    group mouth:
        attribute professional default: "images/sprites/west/mouth_professional.webp"
        attribute cold: "images/sprites/west/mouth_cold.webp"
```

### 神父

```renpy
layeredimage father:
    always: "images/sprites/father/body_normal.webp"
    group head: attribute normal default: "images/sprites/father/head_normal.webp"
    group eyes:
        attribute gazing default: "images/sprites/father/eyes_gazing.webp"
        attribute merciful: "images/sprites/father/eyes_merciful.webp"
    group mouth:
        attribute gazing default: "images/sprites/father/mouth_gazing.webp"
        attribute merciful: "images/sprites/father/mouth_merciful.webp"
    group extra:
        attribute lantern: "images/sprites/father/extra_lantern.webp"
```

---

## 五、图像对齐参考

所有 LayeredImage 资产需在以下坐标对齐：

```
原点 (0,0) ────────────────────────────── (832, 0)
    │                                          │
    │    头部区域 (y: 0~400)                    │
    │    眼睛 y: ~220                          │
    │    嘴   y: ~290                          │
    │                                          │
    │    身体区域 (y: 400~2176)                 │
    │                                          │
    │                                          │
    │    脚   y: ~2100                         │
    │                                          │
(0, 2176) ─────────────────────────── (832, 2176)
```

生成立绘时，确保所有图层的头/眼/嘴位置一致，以便 `layeredimage` 正确叠加。
