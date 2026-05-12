# ============================================================
# TimeManager — 时间推进系统
# 管理时间槽（evening/night/late_night/dawn）的变化
# ============================================================

init python:
    class TimeManager:

        TIME_SLOTS = ["evening", "night", "late_night", "dawn"]
        TIME_SLOT_LABELS = {
            "evening": "傍晚",
            "night": "深夜",
            "late_night": "凌晨",
            "dawn": "黎明",
        }

        def __init__(self):
            self.current_index = 0

        def init_from_state(self):
            current = store.state.get_time()
            if current in self.TIME_SLOTS:
                self.current_index = self.TIME_SLOTS.index(current)
            else:
                self.current_index = 0

        def advance(self):
            if self.current_index < len(self.TIME_SLOTS) - 1:
                self.current_index += 1
                new_time = self.TIME_SLOTS[self.current_index]
                store.state.set_time(new_time)
                return new_time
            return None

        def set_time(self, time_slot):
            if time_slot in self.TIME_SLOTS:
                self.current_index = self.TIME_SLOTS.index(time_slot)
                store.state.set_time(time_slot)
                return True
            return False

        def get_current(self):
            return self.TIME_SLOTS[self.current_index]

        def get_label(self, time_slot=None):
            ts = time_slot or self.get_current()
            return self.TIME_SLOT_LABELS.get(ts, ts)

        def is_past(self, time_slot):
            if time_slot not in self.TIME_SLOTS:
                return False
            return self.TIME_SLOTS.index(time_slot) <= self.current_index

        def get_transition_description(self, old_time, new_time):
            descriptions = {
                ("evening", "night"): "夜幕完全落下了。",
                ("night", "late_night"): "夜更深了。街灯的光变得稀薄，黑暗似乎有了重量。",
                ("late_night", "dawn"): "天际开始发亮。不是温暖的金色——是灰蓝色的、冷的黎明。",
            }
            return descriptions.get((old_time, new_time), "")

    # 全局单例
    TimeManager = TimeManager()
