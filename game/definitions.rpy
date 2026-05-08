## 图像定义
image bg apartment_foyer = Transform("images/bg/scene1.png", fit="cover")

## 角色定义
define jim = Character("吉姆", kind = adv, ctc = "ctc")
define elena = Character("艾琳娜", kind = adv, ctc = "ctc")
define narrator = Character(kind = adv, ctc = "ctc", what_xalign = 0.5, what_italic = True, what_size = 30)

## 存档变量（default 声明）
default flags = {}
default current_room = "foyer"
default quest_stage = "ch01_enter_home"
default time_slot = "evening"
default reality = 100
default anomaly_count = 0
default examined_items = []
default completed_activities = {}
default inventory_items = []
default chapter_completed = {}

# ---- 系统管理器 store 别名（init 999 确保在所有系统文件加载后执行）----
init 999 python:
    store.state = StateManager
    store.nav = NavigationManager
    store.quest = QuestManager
    store.inv = InventoryManager
    store.events = EventManager
    store.meta = MetaManager
    store.time_mgr = TimeManager
