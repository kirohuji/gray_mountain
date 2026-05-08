# ============================================================
# StateManager — 状态/旗标管理系统
# 统一管理 flags、reality、anomaly_count 等状态
# 数据存储于 store._save，由 Ren'Py 自动保存/加载
# ============================================================

init python:
    class StateManager:
        """游戏状态管理器 — 薄封装 store._save"""

        # ---- 内部辅助 ----

        @staticmethod
        def _save():
            return store._save

        # ---- flags ----

        def set_flag(self, flag_name, value=True):
            self._save()["flags"][flag_name] = value

        def get_flag(self, flag_name, default=False):
            return self._save()["flags"].get(flag_name, default)

        def has_flag(self, flag_name):
            return self._save()["flags"].get(flag_name, False)

        # ---- anomaly ----

        def increment_anomaly(self, amount=1):
            self._save()["anomaly_count"] += amount

        def get_anomaly_count(self):
            return self._save()["anomaly_count"]

        # ---- reality ----

        def set_reality(self, value):
            self._save()["reality"] = max(0, min(100, value))

        def get_reality(self):
            return self._save()["reality"]

        def adjust_reality(self, delta):
            self.set_reality(self.get_reality() + delta)

        # ---- time ----

        def set_time(self, time_slot):
            valid_times = ["evening", "night", "late_night", "dawn"]
            if time_slot in valid_times:
                self._save()["time_slot"] = time_slot

        def get_time(self):
            return self._save()["time_slot"]

        # ---- examined items ----

        def mark_examined(self, item_id):
            if item_id not in self._save()["examined_items"]:
                self._save()["examined_items"].append(item_id)

        def is_examined(self, item_id):
            return item_id in self._save()["examined_items"]

        # ---- activities ----

        def mark_activity_completed(self, activity_id):
            self._save()["completed_activities"][activity_id] = True

        def is_activity_completed(self, activity_id):
            return self._save()["completed_activities"].get(activity_id, False)

        # ---- current room ----

        def set_current_room(self, room_id):
            self._save()["current_room"] = room_id

        def get_current_room(self):
            return self._save()["current_room"]

        # ---- quest stage ----

        def set_quest_stage(self, stage):
            self._save()["quest_stage"] = stage

        def get_quest_stage(self):
            return self._save()["quest_stage"]

        # ---- inventory ----

        def add_inventory_item(self, item_id):
            inv = self._save()["inventory"]
            if item_id not in inv:
                inv.append(item_id)

        def remove_inventory_item(self, item_id):
            inv = self._save()["inventory"]
            if item_id in inv:
                inv.remove(item_id)

        def has_inventory_item(self, item_id):
            return item_id in self._save()["inventory"]

        def get_inventory(self):
            return list(self._save()["inventory"])

        # ---- reset ----

        def reset(self):
            s = self._save()
            s["flags"] = {}
            s["anomaly_count"] = 0
            s["reality"] = 100
            s["time_slot"] = "evening"
            s["examined_items"] = []
            s["completed_activities"] = {}
            s["current_room"] = "foyer"
            s["quest_stage"] = None
            s["inventory"] = []

    StateManager = StateManager()
