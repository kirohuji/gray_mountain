# ============================================================
# CharacterManager — 角色状态与关系管理系统
# 统一管理角色元数据、生死状态、异常现身、角色间关系值
# 数据存储于 store._save["character_statuses"] 和 ["relationships"]
# 角色定义数据来源于 data/characters.json
# ============================================================

init python:
    import json

    class CharacterManager:

        def __init__(self):
            self.characters = {}      # {char_id: character_data} 角色定义
            self._loaded = False

        def load(self):
            if self._loaded:
                return

            try:
                with renpy.file("data/characters.json") as f:
                    data = json.load(f)
                self.characters = data.get("characters", {})

                save = store._save

                # 初始化角色状态（仅首次）
                if "character_statuses" not in save:
                    save["character_statuses"] = {}
                    for char_id, char_data in self.characters.items():
                        if not char_data.get("is_player_character", False):
                            save["character_statuses"][char_id] = char_data.get("status", "alive")

                # 初始化关系值（仅首次）
                if "relationships" not in save:
                    save["relationships"] = {}
                    default_rels = data.get("default_relationships", {})
                    for from_char, rels in default_rels.items():
                        save["relationships"][from_char] = dict(rels)

                self._loaded = True
            except Exception as e:
                renpy.notify("无法加载 characters.json: {}".format(e))

        # ---- 角色数据查询 ----

        def get_character(self, char_id):
            return self.characters.get(char_id, None)

        def get_display_name(self, char_id):
            char = self.characters.get(char_id)
            return char["display_name"] if char else char_id

        def get_full_name(self, char_id):
            char = self.characters.get(char_id)
            return char.get("full_name", char_id) if char else char_id

        def get_role(self, char_id):
            char = self.characters.get(char_id)
            return char.get("role", "unknown") if char else "unknown"

        def description(self, char_id):
            char = self.characters.get(char_id)
            return char.get("description", "") if char else ""

        def get_all_characters(self):
            return list(self.characters.keys())

        def get_characters_by_role(self, role):
            return [
                cid for cid, cdata in self.characters.items()
                if cdata.get("role") == role
            ]

        # ---- 状态管理 ----

        def get_status(self, char_id):
            char = self.characters.get(char_id)
            if char and char.get("is_player_character"):
                return "alive"
            return store._save["character_statuses"].get(char_id, "alive")

        def set_status(self, char_id, status):
            valid = ["alive", "dead", "anomaly_present", "missing", "incapacitated"]
            if status not in valid:
                return False
            char = self.characters.get(char_id)
            if char and not char.get("is_player_character"):
                store._save["character_statuses"][char_id] = status
                return True
            return False

        def is_alive(self, char_id):
            return self.get_status(char_id) == "alive"

        def is_present(self, char_id):
            return self.get_status(char_id) in ("alive", "anomaly_present")

        def can_appear_as_anomaly(self, char_id):
            char = self.characters.get(char_id)
            return char.get("can_appear_as_anomaly", False) if char else False

        def is_available(self, char_id, chapter=None):
            char = self.characters.get(char_id)
            if not char:
                return False
            if char.get("is_player_character"):
                return True
            if chapter is not None:
                intro = char.get("chapter_introduced", 99)
                if chapter < intro:
                    return False
            return self.is_present(char_id)

        # ---- 关系管理 ----

        def get_relationship(self, from_char, to_char):
            rels = store._save["relationships"].get(from_char, {})
            return rels.get(to_char, 0)

        def set_relationship(self, from_char, to_char, value):
            value = max(0, min(100, int(value)))
            if from_char not in store._save["relationships"]:
                store._save["relationships"][from_char] = {}
            store._save["relationships"][from_char][to_char] = value

        def adjust_relationship(self, from_char, to_char, delta):
            current = self.get_relationship(from_char, to_char)
            self.set_relationship(from_char, to_char, current + delta)

        def get_relationship_label(self, from_char, to_char):
            value = self.get_relationship(from_char, to_char)
            if value >= 90:
                return "挚爱"
            elif value >= 75:
                return "深厚"
            elif value >= 60:
                return "友好"
            elif value >= 40:
                return "一般"
            elif value >= 20:
                return "疏远"
            else:
                return "陌生"

        def get_all_relationships_for(self, char_id):
            return dict(store._save["relationships"].get(char_id, {}))

        # ---- 角色对象映射 ----

        def get_character_object(self, char_id):
            try:
                return getattr(store, char_id, None)
            except Exception:
                return None

        def has_character_object(self, char_id):
            return self.get_character_object(char_id) is not None

        # ---- 批量查询 ----

        def get_introduced_characters(self, chapter):
            return [
                cid for cid, cdata in self.characters.items()
                if cdata.get("chapter_introduced", 99) <= chapter
            ]

        def get_available_characters(self, chapter):
            return [
                cid for cid in self.get_introduced_characters(chapter)
                if self.is_available(cid, chapter)
            ]

        # ---- 重置 ----

        def reset(self):
            save = store._save
            save["character_statuses"] = {}
            save["relationships"] = {}

            for char_id, char_data in self.characters.items():
                if not char_data.get("is_player_character", False):
                    save["character_statuses"][char_id] = char_data.get("status", "alive")

            try:
                with renpy.file("data/characters.json") as f:
                    data = json.load(f)
                default_rels = data.get("default_relationships", {})
                for from_char, rels in default_rels.items():
                    save["relationships"][from_char] = dict(rels)
            except Exception:
                pass

    CharacterManager = CharacterManager()
