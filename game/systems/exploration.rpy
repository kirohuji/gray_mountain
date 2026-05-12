# ============================================================
# Exploration Engine — 通用探索循环与交互处理
#
# 所有章节共享的探索模式引擎。提供：
#   exploration_init  — 通用系统初始化（加载所有管理器数据）
#   explore_loop      — 主探索循环（叙事触发 → 显示探索UI → 等待交互）
#   move_to_room      — 房间移动处理（导航 + 场景切换 + 事件触发）
#   handle_activity   — 互动处理（加载活动定义 + 标记完成 + 跳转叙事）
#   after_activity    — 互动后处理（事件检查 + 任务推进）
#
# 使用模式：
#   label chXX_start:
#       call exploration_init
#       python:
#           state.reset()
#           nav.set_initial_room("foyer")
#           quest.start_quest("chXX")
#       # ... 章节专属开场叙事 ...
#       jump explore_loop
# ============================================================

label exploration_init:
    python:
        nav.load()
        quest.load()
        inv.load()
        events.load()
        chars.load()
    return


label explore_loop:
    python:
        narrative_jump = events.check_narrative_stage()
        if narrative_jump:
            renpy.jump(narrative_jump)

    window hide
    show screen room_explore

    python:
        hint = quest.get_stage_hint()
        last_hint = getattr(store, '_last_quest_hint', None)
        if hint and hint != last_hint:
            renpy.notify(hint)
            store._last_quest_hint = hint

    pause
    hide screen room_explore
    jump explore_loop


label move_to_room:
    hide screen room_explore

    python:
        dest = store._hovered_dest if hasattr(store, '_hovered_dest') and store._hovered_dest else "livingroom"
        success, result = nav.move_to(dest)

    if success:
        scene expression nav.get_current_room()["background"]
        with dissolve

        python:
            desc = nav.get_room_description()
            if desc:
                renpy.say(narrator, desc)

            events.check_enter_room(dest)
            events.check_periodic()

            if quest.check_stage_completion():
                quest.advance_stage()
    else:
        python:
            renpy.say(narrator, result if isinstance(result, str) else "你无法去那里。")

    jump explore_loop


label handle_activity:
    python:
        act_id = store._hovered_activity if hasattr(store, '_hovered_activity') and store._hovered_activity else None
        if not act_id:
            renpy.jump("explore_loop")

        all_acts = _load_activities_data()
        activity = all_acts.get(act_id)

        if not activity:
            renpy.jump("explore_loop")

        state.mark_activity_completed(act_id)
        state.mark_examined(act_id)
        if activity.get("flag"):
            state.set_flag(activity["flag"])

        narrative_label = activity.get("narrative", {}).get("jump")
        if narrative_label:
            renpy.jump(narrative_label)

        desc = activity.get("description", "")
        if desc:
            renpy.say(narrator, desc)

        renpy.jump("after_activity")

    jump explore_loop


label after_activity:
    python:
        if hasattr(store, '_hovered_activity') and store._hovered_activity:
            events.check_after_activity(store._hovered_activity)

        if quest.check_stage_completion():
            quest.advance_stage()

    jump explore_loop
