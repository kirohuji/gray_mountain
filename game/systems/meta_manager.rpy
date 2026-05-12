# ============================================================
# MetaManager — 二周目 / 结局记录 / 全局解锁管理
# 使用 Ren'Py persistent 存储跨周目数据
# ============================================================

init python:
    class MetaManager:

        def __init__(self):
            # persistent 字段在第一次访问时自动初始化
            pass

        # ---- 游戏周目 ----

        @property
        def playthrough(self):
            if not hasattr(persistent, "_meta_playthrough"):
                persistent._meta_playthrough = 1
            return persistent._meta_playthrough

        def increment_playthrough(self):
            persistent._meta_playthrough = self.playthrough + 1

        def is_first_playthrough(self):
            return self.playthrough == 1

        def is_new_game_plus(self):
            return self.playthrough > 1

        # ---- 已通关结局 ----

        @property
        def cleared_endings(self):
            if not hasattr(persistent, "_meta_cleared_endings"):
                persistent._meta_cleared_endings = set()
            return persistent._meta_cleared_endings

        def unlock_ending(self, ending_id):
            self.cleared_endings.add(ending_id)

        def has_cleared_ending(self, ending_id):
            return ending_id in self.cleared_endings

        # ---- 已解锁的隐藏内容 ----

        @property
        def unlocked_content(self):
            if not hasattr(persistent, "_meta_unlocked"):
                persistent._meta_unlocked = set()
            return persistent._meta_unlocked

        def unlock(self, content_id):
            self.unlocked_content.add(content_id)

        def is_unlocked(self, content_id):
            return content_id in self.unlocked_content

        # ---- 真相解锁 ----

        @property
        def truth_unlocked(self):
            if not hasattr(persistent, "_meta_truth_unlocked"):
                persistent._meta_truth_unlocked = False
            return persistent._meta_truth_unlocked

        def unlock_truth(self):
            persistent._meta_truth_unlocked = True

        # ---- 重置（调试用） ----

        def reset_all(self):
            persistent._meta_playthrough = 1
            persistent._meta_cleared_endings = set()
            persistent._meta_unlocked = set()
            persistent._meta_truth_unlocked = False

    # 全局单例
    MetaManager = MetaManager()
