# 图片卡片组件
# 从右下侧滑出（高于对话框，带间距），停留后渐变消失
# 用法:
#   $ show_image_card("images/box.png")
#   $ show_image_card("images/box.png", distance=200)            # 自定义滑入距离
#   $ show_image_card("images/box.png", card_w=400, card_h=300)  # 自定义卡片尺寸
#   show screen show_card("images/box.png")

## 配置常量
define IMAGE_CARD_SLIDE_DISTANCE = 280    # 从右边缘向左滑入的像素距离
define IMAGE_CARD_STAY_TIME = 2.0         # 卡片停留时间（秒）
define IMAGE_CARD_SLIDE_IN_TIME = 0.6     # 滑入动画时长
define IMAGE_CARD_FADE_OUT_TIME = 0.8     # 渐变消失时长
define IMAGE_CARD_BOTTOM_MARGIN = 350     # 卡片底部距屏幕底部像素（高于对话框）
define IMAGE_CARD_DEFAULT_WIDTH = 400     # 卡片默认宽度
define IMAGE_CARD_DEFAULT_HEIGHT = 300    # 卡片默认高度


transform card_slidein(distance=IMAGE_CARD_SLIDE_DISTANCE):
    """
    滑入 + 停留 + 渐变消失的复合变换
    distance: 从右边缘向左滑入的像素距离
    """
    subpixel True

    # 以卡片底部为锚点，定位在对话框上方
    yanchor 1.0
    ypos config.screen_height - IMAGE_CARD_BOTTOM_MARGIN

    # 起始：画面右侧外
    xpos config.screen_width

    # 第一阶段：向左滑入
    easein IMAGE_CARD_SLIDE_IN_TIME xpos config.screen_width - distance

    # 第二阶段：停留
    pause IMAGE_CARD_STAY_TIME

    # 第三阶段：渐变消失
    easeout IMAGE_CARD_FADE_OUT_TIME alpha 0.0


screen show_card(img, distance=IMAGE_CARD_SLIDE_DISTANCE, card_w=IMAGE_CARD_DEFAULT_WIDTH, card_h=IMAGE_CARD_DEFAULT_HEIGHT):
    """
    图片卡片 Screen
    参数:
        img:      图片路径或已定义的 image 名称
        distance: 从右边缘向左滑入距离（px）
        card_w:   卡片宽度（px）
        card_h:   卡片高度（px）
    """
    tag show_card
    zorder 150

    frame:
        background "#0a0a0a"
        xpadding 3
        ypadding 3

        at card_slidein(distance)

        add Transform(img, xsize=card_w, ysize=card_h, fit="contain")

    timer (IMAGE_CARD_SLIDE_IN_TIME + IMAGE_CARD_STAY_TIME + IMAGE_CARD_FADE_OUT_TIME) action Hide("show_card")


## 脚本内快捷调用
init python:
    def show_image_card(img, distance=IMAGE_CARD_SLIDE_DISTANCE, card_w=IMAGE_CARD_DEFAULT_WIDTH, card_h=IMAGE_CARD_DEFAULT_HEIGHT):
        """
        显示图片卡片，从右下侧滑出，停留后渐变消失。
        脚本内会等待动画结束再继续。

        参数:
            img:      图片路径或已定义的 image 名称
            distance: 从右边缘向左滑入距离（px）
            card_w:   卡片宽度（px）
            card_h:   卡片高度（px）
        """
        renpy.show_screen("show_card", img=img, distance=distance, card_w=card_w, card_h=card_h)
        total_time = IMAGE_CARD_SLIDE_IN_TIME + IMAGE_CARD_STAY_TIME + IMAGE_CARD_FADE_OUT_TIME
        renpy.pause(total_time, hard=False)
