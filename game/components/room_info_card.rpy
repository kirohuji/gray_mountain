# ============================================================
# 房间信息卡片组件 — 右上角滑入，显示当前房间名称与描述
# 用法:
#   use room_info_card
# ============================================================

## 配置常量
define ROOM_CARD_WIDTH = 400
define ROOM_CARD_HEIGHT = 200
define ROOM_CARD_TOP_MARGIN = 60      # 距顶部的间距
define ROOM_CARD_SLIDE_TIME = 0.5     # 滑入动画时长


transform room_card_slidein:
    subpixel True

    # 以右上角为锚点
    xanchor 1.0
    yanchor 0.0

    # 起始：卡片完全在屏幕右侧外
    xpos config.screen_width + ROOM_CARD_WIDTH
    ypos ROOM_CARD_TOP_MARGIN

    # 滑入：右侧贴紧屏幕右边
    easein ROOM_CARD_SLIDE_TIME xpos config.screen_width


screen room_info_card():
    zorder 90

    default room_data = store.nav.get_current_room()

    frame:
        at room_card_slidein

        xsize ROOM_CARD_WIDTH
        ysize ROOM_CARD_HEIGHT
        background "#000000"
        padding (20, 20)

        vbox:
            spacing 10

            if room_data:
                text room_data["name"]:
                    size 30
                    color "#ffffff"
                    font gui.text_font

                text store.nav.get_room_description():
                    size 20
                    color "#888888"
                    font gui.text_font
