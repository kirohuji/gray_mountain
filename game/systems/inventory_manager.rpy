# ============================================================
# InventoryManager — 线索背包系统
# 线索系统，非 RPG 背包。只做物品持有和查询。
# 物品列表存储于 store._save["inventory"]
# ============================================================

init python:
    import json

    class InventoryManager:
        """线索背包管理器"""

        def __init__(self):
            self.items = {}          # {item_id: item_data} 所有物品定义
            self._loaded = False

        def load(self):
            """从 items.json 加载物品数据"""
            if self._loaded:
                return

            try:
                with renpy.file("data/items.json") as f:
                    data = json.load(f)
                self.items = data.get("items", {})
                self._loaded = True
            except Exception as e:
                renpy.notify("无法加载 items.json: {}".format(e))

        # ---- 背包操作 ----

        def add_item(self, item_id):
            """添加物品到背包"""
            if item_id in self.items and item_id not in store._save["inventory"]:
                store._save["inventory"].append(item_id)
                return True
            return False

        def remove_item(self, item_id):
            """从背包移除物品"""
            inv = store._save["inventory"]
            if item_id in inv:
                inv.remove(item_id)

        def has_item(self, item_id):
            """检查是否持有物品"""
            return item_id in store._save["inventory"]

        def get_item(self, item_id):
            """获取物品定义数据"""
            return self.items.get(item_id, None)

        def get_item_name(self, item_id):
            """获取物品名称"""
            item = self.items.get(item_id)
            return item["name"] if item else item_id

        def get_item_description(self, item_id):
            """获取物品描述"""
            item = self.items.get(item_id)
            return item["description"] if item else ""

        def get_all_items(self):
            """获取背包中所有物品的列表"""
            return [
                {"id": iid, "name": self.get_item_name(iid),
                 "description": self.get_item_description(iid)}
                for iid in sorted(store._save["inventory"])
            ]

        def get_all_items_data(self):
            """获取所有物品定义（含未持有的）"""
            return self.items

        def is_empty(self):
            return len(store._save["inventory"]) == 0

    InventoryManager = InventoryManager()
