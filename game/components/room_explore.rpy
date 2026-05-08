# ============================================================
# 房间探索 Screen — 玩家在公寓中自由移动和调查
# ============================================================

init python:
    import json

    _cached_activities = None

    def _load_activities_data():
        global _cached_activities
        if _cached_activities is not None:
            return _cached_activities
        try:
            with renpy.file("data/activities.json") as f:
                _cached_activities = json.load(f).get("activities", {})
        except Exception:
            _cached_activities = {}
        return _cached_activities

    def get_available_activities(room_id):
        all_activities = _load_activities_data()
        available = []
        for act_id, act in all_activities.items():
            if act.get("room") != room_id:
                continue
            # 一次性活动检查
            if act.get("once") and store.state.is_activity_completed(act_id):
                continue
            available.append(act)
        return available

    def get_room_name(room_id):
        room = store.nav.get_room(room_id)
        return room["name"] if room else room_id

    def get_room_connections(room_id):
        room = store.nav.get_room(room_id)
        if not room:
            return []
        return [(rid, get_room_name(rid)) for rid in room.get("connections", [])]


screen room_explore():
    zorder 0

    default current_room = store.nav.current_room
    default room_data = store.nav.get_current_room()

    # 背景
    if room_data and room_data.get("background"):
        add room_data["background"]
    else:
        add "#1a1a1a"

    # ---- 顶部：任务提示栏 ----
    frame:
        xalign 0.5
        yalign 0.0
        xsize 900
        ysize 60
        background "#000000cc"
        padding (20, 5)

        hbox:
            xalign 0.5
            spacing 15

            if store.quest.get_stage_hint():
                text "▶ [store.quest.get_stage_hint()]":
                    color "#cccccc"
                    size 24
                    font gui.text_font

    # ---- 底部：房间描述 ----
    frame:
        xalign 0.5
        yalign 1.0
        xsize 1100
        ysize 160
        background "#000000dd"
        padding (30, 20)

        vbox:
            spacing 5

            if room_data:
                text "[room_data['name']]":
                    size 36
                    color "#ffffff"
                    font gui.text_font

                text store.nav.get_room_description(current_room):
                    size 24
                    color "#999999"
                    font gui.text_font

    # ---- 右侧：调查活动列表 ----
    python:
        activities = get_available_activities(current_room)

    if activities:
        frame:
            xalign 1.0
            yalign 0.5
            xsize 260
            background "#000000bb"
            padding (15, 15)

            vbox:
                spacing 8

                text "调查":
                    size 28
                    color "#ffffff"
                    font gui.text_font
                    xalign 0.0

                for act in activities:
                    $ act_id = act["id"]
                    $ act_name = act["name"]
                    textbutton act_name:
                        xsize 230
                        action Jump("handle_activity")
                        hovered SetVariable("_hovered_activity", act_id)
                        unhovered SetVariable("_hovered_activity", "")
                        text_style "activity_button_text"

    # ---- 底部：导航按钮 ----
    python:
        connections = get_room_connections(current_room)

    if connections:
        frame:
            xalign 1.0
            yalign 1.0
            yoffset -180
            xsize 200
            background None
            padding (10, 10)

            vbox:
                spacing 5
                xalign 1.0

                for rid, rname in connections:
                    textbutton "→ [rname]":
                        xsize 180
                        action Jump("move_to_room")
                        hovered SetVariable("_hovered_dest", rid)
                        unhovered SetVariable("_hovered_dest", "")
                        text_style "nav_button_text"

    # 悬浮变量通过 SetVariable 自动写入 store 层级，此处无需 screen-local 默认值


# 样式
style activity_button_text:
    size 22
    color "#cccccc"
    hover_color "#ffffff"
    font gui.text_font

style nav_button_text:
    size 22
    color "#999999"
    hover_color "#ffffff"
    font gui.text_font
