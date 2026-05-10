## 图像定义
image bg_apartment_foyer_evening = Transform("images/bg/bg_apartment_foyer_evening.jpg", fit="cover")
image bg_apartment_corridor_evening = Transform("images/bg/bg_apartment_corridor_evening.jpg", fit="cover")
image bg_apartment_bathroom_evening = Transform("images/bg/bg_apartment_bathroom_evening.jpg", fit="cover")
image bg_apartment_studio_evening = Transform("images/bg/bg_apartment_studio_evening.jpg", fit="cover")
image bg_apartment_livingroom_evening = Transform("images/bg/bg_apartment_livingroom_evening.jpg", fit="cover")
image bg_apartment_kitchen_evening = Transform("images/bg/bg_apartment_kitchen_evening.jpg", fit="cover")
image bg_apartment_bedroom_evening = Transform("images/bg/bg_apartment_bedroom_evening.jpg", fit="cover")
image bg_apartment_balcony_evening = Transform("images/bg/bg_apartment_balcony_evening.jpg", fit="cover")

## 角色立绘
image jim_default = Transform("images/characters/詹姆斯_吉姆_霍顿/default.png", zoom=0.6)
image elena_default = Transform("images/characters/艾丽娜/default.png", zoom=0.6)

## CG 插画
image cg_elena_bedroom = Transform("images/cg/艾琳娜-卧室-cg.jpg", fit="cover")
image cg_elena_bedroom2 = Transform("images/cg/艾琳娜-卧室2-cg.jpg", fit="cover")
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
    "character_statuses": {},
    "relationships": {},
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
    store.chars = CharacterManager
