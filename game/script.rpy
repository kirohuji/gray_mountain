# 灰山 - 主入口脚本

## 图片定义
image bg apartment_foyer = "images/scene1.png"

## 角色定义
define jim = Character("吉姆", kind = adv, ctc = "ctc")
define narrator = Character(kind = adv, ctc = "ctc", what_xalign = 0.5, what_italic = True, what_size = 30)

## 默认变量
default flags = {}

## 游戏入口
label start:
    jump ch01_start
