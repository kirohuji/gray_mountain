# ============================================================
# EventManager — 条件判断与剧情触发系统
# 其他系统只记录状态，EventManager 统一判断发生什么
# ============================================================

init python:
    import json

    class EventManager:

        def __init__(self):
            self.events = []      # 所有事件定义列表
            self._loaded = False

        # ---- 加载 ----

        def load(self):
            if self._loaded:
                return

            try:
                with renpy.file("data/events.json") as f:
                    data = json.load(f)
                # 转换为 list 方便遍历
                self.events = list(data.get("events", {}).values())
                self._loaded = True
            except Exception as e:
                renpy.notify("无法加载 events.json: {}".format(e))

        # ---- 条件评估 ----

        def _check_condition(self, condition, event_id=""):
            for key, value in condition.items():
                if key == "room":
                    if store.nav.current_room != value:
                        return False

                elif key == "quest_stage":
                    current_stage = store.quest.current_stage
                    if isinstance(value, list):
                        # 任意匹配
                        if current_stage not in value:
                            return False
                    else:
                        if current_stage != value:
                            return False

                elif key == "flag":
                    if not store.state.has_flag(value):
                        return False

                elif key == "not_flag":
                    if store.state.has_flag(value):
                        return False

                elif key == "time":
                    if store.state.get_time() != value:
                        return False

                elif key == "reality_below":
                    if store.state.get_reality() >= value:
                        return False

                elif key == "reality_above":
                    if store.state.get_reality() <= value:
                        return False

                elif key == "has_item":
                    if not store.inv.has_item(value):
                        return False

                elif key == "anomaly_at_least":
                    if store.state.get_anomaly_count() < value:
                        return False

            return True

        # ---- 动作执行 ----

        def _execute_action(self, action):
            atype = action.get("type", "")

            if atype == "set_room_description":
                # 已在 NavigationManager 中处理
                pass

            elif atype == "advance_quest":
                stage = action.get("stage")
                if stage:
                    store.quest.set_stage(stage)

            elif atype == "show_message":
                text = action.get("text", "")
                if text:
                    renpy.notify(text)

            elif atype == "increment_anomaly":
                amount = action.get("amount", 1)
                store.state.increment_anomaly(amount)

            elif atype == "adjust_reality":
                delta = action.get("delta", 0)
                store.state.adjust_reality(delta)

            elif atype == "add_item":
                item_id = action.get("item_id", "")
                store.inv.add_item(item_id)

            elif atype == "set_flag":
                flag = action.get("flag", "")
                store.state.set_flag(flag, True)

        # ---- 公开接口 ----

        def check_enter_room(self, room_id):
            results = []
            for event in self.events:
                if event.get("trigger") != "enter_room":
                    continue
                if event.get("room") != room_id:
                    continue
                conditions = event.get("conditions", {})
                if self._check_condition(conditions, event.get("id", "")):
                    self._execute_action(event.get("action", {}))
                    results.append(event.get("id"))
            return results

        def check_after_activity(self, activity_id):
            results = []
            for event in self.events:
                if event.get("trigger") != "after_activity":
                    continue
                if event.get("activity") and event["activity"] != activity_id:
                    continue
                conditions = event.get("conditions", {})
                if self._check_condition(conditions, event.get("id", "")):
                    self._execute_action(event.get("action", {}))
                    results.append(event.get("id"))
            return results

        def check_periodic(self):
            results = []
            for event in self.events:
                if event.get("trigger") != "periodic":
                    continue
                conditions = event.get("conditions", {})
                if self._check_condition(conditions, event.get("id", "")):
                    self._execute_action(event.get("action", {}))
                    results.append(event.get("id"))
            return results

        def check_narrative_stage(self):
            if store.quest.is_narrative_stage():
                stage = store.quest.get_current_stage()
                if stage:
                    completion = stage.get("completion", {})
                    jump_label = completion.get("jump")
                    if jump_label:
                        return jump_label
            return None

    # 全局单例
    EventManager = EventManager()
