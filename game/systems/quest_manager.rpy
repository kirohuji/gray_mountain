# ============================================================
# QuestManager — 任务/阶段管理系统
# 负责加载任务数据、管理当前阶段、判断完成条件
# 当前阶段存储于 store._save["quest_stage"]
# ============================================================

init python:
    import json

    class QuestManager:

        def __init__(self):
            self.quests = {}
            self.current_quest = None
            self._loaded = False

        def load(self):
            if self._loaded:
                return

            try:
                with renpy.file("data/quests.json") as f:
                    data = json.load(f)
                self.quests = data.get("quests", {})
                self._loaded = True
            except Exception as e:
                renpy.notify("无法加载 quests.json: {}".format(e))

        # ---- 当前阶段 ----

        @property
        def current_stage(self):
            return store._save["quest_stage"]

        @current_stage.setter
        def current_stage(self, value):
            store._save["quest_stage"] = value

        # ---- 任务操作 ----

        def start_quest(self, quest_id):
            if quest_id not in self.quests:
                return False

            quest = self.quests[quest_id]
            self.current_quest = quest_id
            initial_stage = quest.get("initial_stage")
            if initial_stage:
                self.set_stage(initial_stage)
            return True

        def set_stage(self, stage_id):
            quest = self.get_current_quest_data()
            if not quest:
                return False

            if stage_id not in quest.get("stages", {}):
                return False

            self.current_stage = stage_id
            stage = quest["stages"][stage_id]

            on_enter = stage.get("on_enter", {})
            if on_enter.get("set_room"):
                store.nav.set_initial_room(on_enter["set_room"])

            return True

        def get_current_stage(self):
            quest = self.get_current_quest_data()
            if not quest or not self.current_stage:
                return None
            return quest.get("stages", {}).get(self.current_stage, None)

        def get_current_quest_data(self):
            if not self.current_quest:
                return None
            return self.quests.get(self.current_quest, None)

        def get_stage_description(self):
            stage = self.get_current_stage()
            if not stage:
                return ""
            return stage.get("description", "")

        def get_stage_hint(self):
            stage = self.get_current_stage()
            if not stage:
                return ""
            return stage.get("hint", "")

        # ---- 完成检查 ----

        def check_stage_completion(self):
            stage = self.get_current_stage()
            if not stage:
                return False

            completion = stage.get("completion", {})
            ctype = completion.get("type", "")

            if ctype == "activities_completed":
                min_count = completion.get("min_count", 0)
                exam_count = len(store._save["examined_items"])
                return exam_count >= min_count

            elif ctype == "enter_room":
                target = completion.get("room", "")
                return store.nav.current_room == target

            elif ctype == "do_activity":
                target = completion.get("activity", "")
                return store._save["completed_activities"].get(target, False)

            elif ctype == "narrative":
                return False

            return False

        def advance_stage(self):
            stage = self.get_current_stage()
            if not stage:
                return None

            next_stage = stage.get("next_stage")
            if next_stage:
                self.set_stage(next_stage)
                return next_stage
            return None

        def is_narrative_stage(self):
            stage = self.get_current_stage()
            if not stage:
                return False
            return stage.get("is_narrative_trigger", False)

    QuestManager = QuestManager()
