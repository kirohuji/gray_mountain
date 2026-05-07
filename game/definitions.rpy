## 图像定义
image bg apartment_foyer = Transform("images/bg/scene1.png", fit="cover")

## 角色定义
define jim = Character("吉姆", kind = adv, ctc = "ctc")
define narrator = Character(kind = adv, ctc = "ctc", what_xalign = 0.5, what_italic = True, what_size = 30)

## 存档变量
default flags = {}
