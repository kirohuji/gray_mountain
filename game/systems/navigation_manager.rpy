# ============================================================
# NavigationManager — 房间移动系统
# 负责加载房间数据、管理当前房间、提供移动功能
# ============================================================

init python:
    import json
    import os

    class NavigationManager:
        """房间导航管理器"""

        def __init__(self):
            self.rooms = {}
            self.current_room = None
            self._loaded = False

        def load(self):
            """从 rooms.json 加载房间数据"""
            if self._loaded:
                return

            data_dir = os.path.join(config.gamedir, "data")
            rooms_path = os.path.join(data_dir, "rooms.json")

            try:
                with renpy.loader.load(rooms_path) as f:
                    data = json.load(f)
                self.rooms = data.get("rooms", {})
                self._loaded = True
            except Exception as e:
                renpy.notify("无法加载 rooms.json: {}".format(e))

        def get_current_room(self):
            """获取当前房间数据"""
            if self.current_room and self.current_room in self.rooms:
                return self.rooms[self.current_room]
            return None

        def get_room(self, room_id):
            """获取指定房间数据"""
            return self.rooms.get(room_id, None)

        def move_to(self, room_id):
            """移动到指定房间"""
            if room_id not in self.rooms:
                return False, "房间不存在"

            # 已经在目标房间，无需移动
            if self.current_room == room_id:
                return True, self.rooms[room_id]

            room = self.rooms[room_id]
            # 检查连接关系
            if self.current_room is not None:
                current = self.get_current_room()
                if current and room_id not in current.get("connections", []):
                    return False, "无法从这里去那里"

            self.current_room = room_id
            return True, room

        def can_move_to(self, room_id):
            """检查是否可以移动到指定房间"""
            if room_id not in self.rooms:
                return False
            if self.current_room is None:
                return True
            current = self.get_current_room()
            if current:
                return room_id in current.get("connections", [])
            return True

        def set_initial_room(self, room_id):
            """设置初始房间（绕过连接检查）"""
            if room_id in self.rooms:
                self.current_room = room_id
                return True
            return False

        def get_connections(self):
            """获取当前房间可移动到的目标"""
            current = self.get_current_room()
            if current:
                return current.get("connections", [])
            return []

        def get_room_description(self, room_id=None):
            """获取房间描述（支持时间变体）"""
            rid = room_id or self.current_room
            room = self.rooms.get(rid)
            if not room:
                return ""

            # 优先时间变体
            time_slot = store.state.get_time()
            time_desc = room.get("time_descriptions", {}).get(time_slot)
            if time_desc:
                return time_desc

            return room.get("default_description", "")

        def get_room_atmosphere(self, room_id=None):
            """获取房间氛围文本"""
            rid = room_id or self.current_room
            room = self.rooms.get(rid)
            if not room:
                return ""
            return room.get("atmosphere", "")

        def set_current_room(self, room_id):
            """直接设置当前房间（用于加载存档）"""
            self.current_room = room_id


    # 全局单例
    NavigationManager = NavigationManager()
