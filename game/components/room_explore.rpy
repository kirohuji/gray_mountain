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

    # ---- 顶部：房间信息栏 ----
    frame:
        xalign 0.5
        yalign 0.0
        xsize 900
        background "#000000cc"
        padding (20, 10)

        vbox:
            xalign 0.5
            spacing 4

            if room_data:
                text room_data["name"]:
                    size 30
                    color "#ffffff"
                    font gui.text_font
                    xalign 0.5

                # $ desc = store.nav.get_room_description(current_room)
                # if desc:
                #     text desc:
                #         size 15
                #         color "#999999"
                #         font gui.text_font
                #         xalign 0.5

    # ---- 右侧面板：调查 + 导航 ----
    python:
        activities = get_available_activities(current_room)
        connections = get_room_connections(current_room)

    if activities or connections:
        frame:
            xalign 1.0
            yalign 0.5
            xsize 260
            background "#000000bb"
            padding (15, 15)

            vbox:
                spacing 5

                if activities:
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
                            text_style "panel_button_text"

                if connections:
                    if activities:
                        text "":
                            size 6

                    for rid, rname in connections:
                        textbutton "→ [rname]":
                            xsize 230
                            action Jump("move_to_room")
                            hovered SetVariable("_hovered_dest", rid)
                            unhovered SetVariable("_hovered_dest", "")
                            text_style "panel_button_text"

    # 悬浮变量通过 SetVariable 自动写入 store 层级，此处无需 screen-local 默认值


# 样式
style panel_button_text:
    size 22
    color "#cccccc"
    hover_color "#ffffff"
    font gui.text_font
