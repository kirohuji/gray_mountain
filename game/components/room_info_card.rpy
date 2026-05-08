# ============================================================
# 任务提示卡片组件 — 右上角滑入，显示当前任务阶段提示
# 用法:
#   use quest_hint_card
# ============================================================

## 配置常量
define QUEST_CARD_WIDTH = 400
define QUEST_CARD_HEIGHT = 200
define QUEST_CARD_TOP_MARGIN = 60       # 距顶部的间距
define QUEST_CARD_SLIDE_TIME = 0.5      # 滑入动画时长


transform quest_card_slidein:
    # 以右上角为锚点
    xanchor 1.0
    yanchor 0.0

    # 起始：卡片完全在屏幕右侧外
    xpos config.screen_width + QUEST_CARD_WIDTH
    ypos QUEST_CARD_TOP_MARGIN

    # 滑入：右侧贴紧屏幕右边
    easein QUEST_CARD_SLIDE_TIME xpos config.screen_width


screen quest_hint_card():
    zorder 90

    default hint = store.quest.get_stage_hint()

    if hint:
        frame:
            at quest_card_slidein

            xsize QUEST_CARD_WIDTH
            ysize QUEST_CARD_HEIGHT
            background "#000000"
            padding (20, 20)

            vbox:
                spacing 10

                text "任务":
                    size 30
                    color "#ffffff"
                    font gui.text_font

                text hint:
                    size 22
                    color "#cccccc"
                    font gui.text_font
