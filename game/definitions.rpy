## 图像定义
image bg_apartment_foyer = Transform("images/bg/apartment_foyer.png", fit="cover")

# 占位背景——后续替换为实际背景图
image bg_apartment_livingroom_evening = Transform("images/bg/apartment_livingroom.png", fit="cover")
image bg_apartment_corridor_night = Transform("images/bg/scene1.png", fit="cover")
image bg_apartment_bedroom_night = Transform("images/bg/apartment_bedroom.png", fit="cover")
image bg_apartment_studio_evening = Transform("images/bg/scene1.png", fit="cover")

## 角色定义
define jim = Character("吉姆", kind = adv, ctc = "ctc")
define elena = Character("艾琳娜", kind = adv, ctc = "ctc")
define narrator = Character(kind = adv, ctc = "ctc", what_xalign = 0.5, what_italic = True, what_size = 30)

## 存档数据——所有游戏状态集中在此 dict，Ren'Py 自动保存/加载
default _save = {
    "flags": {},
    "reality": 100,
    "time_slot": "evening",
    "anomaly_count": 0,
    "current_room": "foyer",
    "quest_stage": None,
    "examined_items": [],
    "completed_activities": {},
    "inventory": [],
}

# ---- 系统管理器 store 别名（init 999 确保在所有系统文件加载后执行）----
init 999 python:
    store.state = StateManager
    store.nav = NavigationManager
    store.quest = QuestManager
    store.inv = InventoryManager
    store.events = EventManager
    store.meta = MetaManager
    store.time_mgr = TimeManager
