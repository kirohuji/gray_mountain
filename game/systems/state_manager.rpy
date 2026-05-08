# ============================================================
# StateManager — 状态/旗标管理系统
# 统一管理 flags、reality、anomaly_count 等状态
# ============================================================

init python:
    class StateManager:
        """游戏状态管理器 — 包装 flags 字典和全局状态"""

        def __init__(self):
            self.flags = {}
            self.anomaly_count = 0
            self.reality = 100
            self.time_slot = "evening"
            self.examined_items = []
            self.completed_activities = {}

        def set_flag(self, flag_name, value=True):
            """设置旗标"""
            self.flags[flag_name] = value

        def get_flag(self, flag_name, default=False):
            """获取旗标"""
            return self.flags.get(flag_name, default)

        def has_flag(self, flag_name):
            """检查旗标是否为真"""
            return self.flags.get(flag_name, False)

        def toggle_flag(self, flag_name):
            """切换旗标"""
            self.flags[flag_name] = not self.flags.get(flag_name, False)

        def increment_anomaly(self, amount=1):
            """增加异常计数"""
            self.anomaly_count += amount

        def get_anomaly_count(self):
            return self.anomaly_count

        def set_time(self, time_slot):
            """设置时间槽"""
            valid_times = ["evening", "night", "late_night", "dawn"]
            if time_slot in valid_times:
                self.time_slot = time_slot

        def get_time(self):
            return self.time_slot

        def set_reality(self, value):
            """设置现实值 0-100"""
            self.reality = max(0, min(100, value))

        def get_reality(self):
            return self.reality

        def adjust_reality(self, delta):
            """调整现实值"""
            self.reality = max(0, min(100, self.reality + delta))

        def mark_examined(self, item_id):
            """标记物品已被调查"""
            if item_id not in self.examined_items:
                self.examined_items.append(item_id)

        def is_examined(self, item_id):
            return item_id in self.examined_items

        def mark_activity_completed(self, activity_id):
            """标记活动已完成"""
            self.completed_activities[activity_id] = True

        def is_activity_completed(self, activity_id):
            return self.completed_activities.get(activity_id, False)

        def reset(self):
            """重置所有状态（新游戏用）"""
            self.flags = {}
            self.anomaly_count = 0
            self.reality = 100
            self.time_slot = "evening"
            self.examined_items = []
            self.completed_activities = {}

        # ---- 序列化支持（存档用） ----

        def to_dict(self):
            return {
                "flags": self.flags,
                "anomaly_count": self.anomaly_count,
                "reality": self.reality,
                "time_slot": self.time_slot,
                "examined_items": self.examined_items,
                "completed_activities": self.completed_activities,
            }

        def from_dict(self, d):
            self.flags = d.get("flags", {})
            self.anomaly_count = d.get("anomaly_count", 0)
            self.reality = d.get("reality", 100)
            self.time_slot = d.get("time_slot", "evening")
            self.examined_items = d.get("examined_items", [])
            self.completed_activities = d.get("completed_activities", {})

    # 全局单例
    StateManager = StateManager()
