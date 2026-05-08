# ============================================================
# 第一章：归途
# 采用 NavigationManager + QuestManager + EventManager 架构
# 探索模式 + 线性叙事场景
# ============================================================

label ch01_start:
    # ---- 系统初始化 ----
    python:
        nav.load()
        quest.load()
        inv.load()
        events.load()
        state.reset()
        nav.set_initial_room("foyer")
        quest.start_quest("ch01")

    # 章节标题
    scene black
    centered "第一章：归途"

    # ---- 开场叙事：吉姆送汤姆回家 ----
    scene bg_apartment_foyer
    with dissolve

    "哈里斯大道的公寓和你离开时一模一样。窄长的棕色石砖公寓——波士顿最常见的那种——门廊窄，天花板却意外地高。"

    "吉姆帮你开了门，把行李靠墙放在鞋柜旁。衣帽架上挂着你那件旧风衣，雨伞桶里斜插着一把黑伞。他站在门口，没有进来。"

    "客厅的窗帘拉着。空气里有久未通风的沉闷——不是灰尘的气味，是封闭的空间自己产生的气味。旧木头。干涸的水垢。寂静。"

    jim "药在茶几上——哈丁医生开的，每晚一片。"
    jim "我明天再来看你。"

    "门关上的声音。钥匙转动的声音。锁舌卡入锁扣的金属声——比他需要的更响。"

    "然后——完全地、彻底地——安静了。"

    jump explore_loop


# ============================================================
# 主探索循环
# ============================================================

label explore_loop:
    python:
        # 检查是否应该触发叙事
        narrative_jump = events.check_narrative_stage()
        if narrative_jump:
            renpy.jump(narrative_jump)

    # 显示探索界面
    show screen room_explore

    "你站在[get_room_name(nav.current_room)]。你想做什么？"

    hide screen room_explore
    jump explore_loop


# ============================================================
# 房间移动处理
# ============================================================

label move_to_room:
    python:
        dest = store._hovered_dest if hasattr(store, '_hovered_dest') and store._hovered_dest else "livingroom"
        success, result = nav.move_to(dest)

    if success:
        scene expression nav.get_current_room()["background"]
        with dissolve

        python:
            room_data = nav.get_current_room()
            desc = nav.get_room_description()
            if desc:
                renpy.say(narrator, desc)

            # 触发进入房间事件
            events.check_enter_room(dest)
            events.check_periodic()

            # 检查任务推进
            if quest.check_stage_completion():
                quest.advance_stage()
    else:
        python:
            renpy.say(narrator, result if isinstance(result, str) else "你无法去那里。")

    jump explore_loop


# ============================================================
# 活动处理
# ============================================================

label handle_activity:
    python:
        act_id = store._hovered_activity if hasattr(store, '_hovered_activity') and store._hovered_activity else None
        if not act_id:
            renpy.jump("explore_loop")

        # 从 activities.json 查找活动数据
        all_acts = _load_activities_data()
        activity = all_acts.get(act_id)

        if not activity:
            renpy.jump("explore_loop")

        # 标记完成
        state.mark_activity_completed(act_id)
        state.mark_examined(act_id)
        if activity.get("flag"):
            state.set_flag(activity["flag"])

        # 跳转到叙事 label
        narrative_label = activity.get("narrative", {}).get("jump")
        if narrative_label:
            renpy.jump(narrative_label)

        # 否则显示描述文本并返回
        desc = activity.get("description", "")
        if desc:
            renpy.say(narrator, desc)

        renpy.jump("after_activity")

    jump explore_loop


label after_activity:
    python:
        # 触发活动后事件
        if hasattr(store, '_hovered_activity') and store._hovered_activity:
            events.check_after_activity(store._hovered_activity)

        # 检查任务推进
        if quest.check_stage_completion():
            quest.advance_stage()

    jump explore_loop


# ============================================================
# 活动叙事 Labels
# ============================================================

# ---- 玄关 ----

label act_examine_bag:
    scene expression nav.get_current_room()["background"]
    with dissolve

    "深灰色的帆布袋靠在鞋柜侧面。不是你平时出门用的那一只——这是疗养院的物品，侧面贴着一张白色标签，上面用墨水写着你的名字：{i}卡特，汤姆。{/i}"

    $ show_image_card("images/cg/box.png")

    "袋子的侧面有一层灰白色的粉末。你用拇指抹了一下——很细，滑腻。不像普通的灰尘，倒更像是……石粉。"

    "你打开袋口。里面是你的几件换洗衣物，叠得不整齐——不是你的叠法。是别人帮你收拾的。"

    "你不想去回忆是谁。"

    $ renpy.notify("你不想回忆的事情，你的手还记得。")
    $ state.increment_anomaly(1)

    jump after_activity


label act_examine_phone:
    scene expression nav.get_current_room()["background"]
    with dissolve

    $ show_image_card("images/cg/box1.png")

    "玄关柜上的电话答录机。红灯正在闪烁——有未读留言。"

    "你按下播放键。磁带转动的沙沙声。"

    "「汤姆，我是吉姆。你到家了吗？给我回个电话。我——算了，你听到打给我。」"

    "他的声音里有某种他试图掩饰的东西。你认识他太久了，听得出那种\"不想在录音里说\"的语气。"

    "（沉默。持续了大约四秒。然后——）"

    "一阵极低频的嗡鸣。不是从电话里传来的——更像是电话偶然接收到了什么不应该通过电波传送的声音。低沉得像从很深的地下发出来的。"

    "大约持续了七秒。然后挂断。"

    "留言计数器显示：{b}2 条新留言{/b}。"

    "但你知道你只听了两条。然而计数器在你眨眼之后变成了{b}1{/b}。"

    "你没有再去按播放。"

    $ state.increment_anomaly(1)

    jump after_activity


label act_examine_shoes:
    scene expression nav.get_current_room()["background"]
    with dissolve

    "老旧的橡木鞋柜。你蹲下来打开柜门——你的鞋整齐地排列在底层。皮鞋，帆布鞋，一双你冬天穿的厚靴子。"

    "她的鞋在最顶层。三双。你不是故意去看的。"

    "最外面那双——她春天常穿的浅口平底鞋——鞋底边缘嵌着一圈灰白色的细砂。"

    "她不穿这双鞋去疗养院。这双鞋是她在家穿的。"

    "所以这些砂子——是在她离开家{i}之前{/i}就在那里的。"

    $ state.increment_anomaly(1)

    jump after_activity


label act_examine_mirror:
    scene expression nav.get_current_room()["background"]
    with dissolve

    "你无意中瞥了一眼门边的穿衣镜。"

    "镜子里的你——比上次照镜子时瘦了很多。颧骨突出了，眼窝凹陷。你穿着那件从疗养院穿回来的灰色外套，领口有一圈深色的汗渍。"

    "你盯着镜子看了三秒。"

    "然后你注意到——镜子里的你，比你晚了一瞬间才停下动作。"

    "你揉了揉眼睛。再看。一切正常。"

    "{i}一切正常。{/i}"

    $ state.increment_anomaly(1)

    jump after_activity


# ---- 客厅 ----

label act_examine_medicine:
    scene expression nav.get_current_room()["background"]
    with dissolve

    "茶几上的白色小药瓶。标签上写着：{i}卡特，汤姆。每晚一片，睡前服用。哈丁医生。{/i}"

    "你拧开瓶盖。药片是白色的，圆的，没有任何标记。闻起来没有味道。"

    "一枚药片安静地躺在你的掌心里。你盯着它看了一会儿，然后把它放回了瓶里。"

    $ inv.add_item("medicine_bottle")
    $ renpy.notify("获得：[inv.get_item_name('medicine_bottle')]")

    jump after_activity


# ---- 走廊 ----

label act_examine_corridor_sketch:
    scene expression nav.get_current_room()["background"]
    with dissolve

    "墙上的炭笔素描——艾琳娜画的。画的是五渔村的悬崖和小巷，层层叠叠的房屋像挂在崖壁上。左下角有她的签名，日期是三年前。"

    "你伸手碰了一下画框。玻璃上有一层薄薄的灰。灰下面——画本身——炭笔的线条有些模糊了。不是水渍，更像是多年被人触碰后磨损的。"

    jump after_activity


# ---- 卧室 ----

label act_examine_sketchbook:
    scene expression nav.get_current_room()["background"]
    with dissolve

    "床头柜上摊开的那本速写本。翻到的那一页是五渔村的速写——同样的悬崖和小巷，但比墙上那幅更早。纸面泛黄了，炭笔线条模糊得像褪色的梦。"

    "你翻到下一页。空白。再下一页——艾琳娜画的自画像。寥寥几笔，但抓住了她歪头笑的样子。"

    "你翻回去，合上了速写本。"

    $ inv.add_item("sketchbook")
    $ renpy.notify("获得：[inv.get_item_name('sketchbook')]")

    jump after_activity


# ---- 画室 ----

label act_examine_easel:
    scene expression nav.get_current_room()["background"]
    with dissolve

    "画架立在窗边。画布上一片空白。"

    "但如果你凑近了看——在从窗户进来的光线以特定角度落在画布上时——你能看到一些极淡的铅笔线条。不是一幅完整的构图，更像是——一个姿势。一个人坐在窗边的姿势。"

    jump after_activity


label act_examine_paints:
    scene expression nav.get_current_room()["background"]
    with dissolve

    "颜料管整齐地排列在桌上。有些变硬了——盖子没拧紧。在那些变硬的颜料管旁边，有一管灰色的颜料是新的，盖子拧得很紧。"

    "标签上写着：Payne's Gray。"

    "这种灰色——介于蓝黑之间的沉重的灰——你以前不怎么用。它不是你调色盘上的颜色。"

    jump after_activity


# ---- 卧室 ----

label act_look_out_window:
    scene expression nav.get_current_room()["background"]
    with dissolve

    "窗外是波士顿的夜。路灯下——细小的白色的东西开始飘落。"

    "下雪了。在这个深夜里，像灰尘一样细小、一样安静。"

    "你把手贴在玻璃上。玻璃是冰的。"

    jump after_activity


# ============================================================
# 线性叙事场景
# ============================================================

# ---- Scene 02：沉睡 ----

label sc02_sleep:
    hide screen room_explore

    $ nav.move_to("livingroom")
    scene expression nav.get_current_room()["background"]
    with dissolve

    "你坐到沙发上。沙发微微陷了下去。"

    "你原本只是想闭一会儿眼。"

    "可意识几乎是在一瞬间沉了下去。"

    scene black
    with Dissolve(2.0)

    pause 3.0

    # 推进到电话铃响阶段
    python:
        quest.set_stage("ch01_phone_rings")

    jump explore_loop


# ---- Scene 03：电话 ----

label sc03_phone_rings:
    hide screen room_explore

    scene black
    pause 0.5

    # 电话铃声（TODO: 添加 SFX）
    "（电话突然响了起来。空荡的公寓被震得格外刺耳。）"

    $ nav.set_initial_room("livingroom")
    scene expression nav.get_current_room()["background"]
    with Dissolve(1.0)

    "你按了按额头，缓慢地站起身。长时间的疲惫让你的视线微微发黑，后背也泛着一阵迟钝的酸痛。"

    "电话依旧响着。"

    "你拖着脚步穿过昏暗的走廊，来到墙边的电话机前。"

    $ nav.set_initial_room("corridor")
    scene expression nav.get_current_room()["background"]
    with dissolve

    # 推进阶段：等待玩家接电话
    python:
        quest.set_stage("ch01_phone_answered")

    jump explore_loop


label sc03_phone_answer:
    hide screen room_explore

    $ nav.set_initial_room("corridor")
    scene expression nav.get_current_room()["background"]
    with dissolve

    "你拿起听筒。"

    "吉姆的声音——隔着很远的距离，像是从隧道尽头传来的。"

    "「……打了好几次……你没接……」"

    "「什么时候？」你问。"

    "吉姆说了什么。但那个词被一阵低频的嗡鸣盖住了。像是昨天。像是上周。像是刚才。"

    "「你说什么？」"

    "嗡鸣更响了。然后断了。"

    "你拿着听筒。沉默了几秒。"

    "然后你听到了别的声音——从卧室传来的。很轻。是布料的窸窣。"

    $ state.increment_anomaly(1)

    # 推进阶段
    python:
        quest.set_stage("ch01_bedroom_elena")

    jump explore_loop


# ---- Scene 04：重逢 ----

label sc04_reunion:
    hide screen room_explore

    $ nav.set_initial_room("bedroom")
    scene expression nav.get_current_room()["background"]
    with dissolve

    "艾琳娜坐在床边。"

    "你僵在门口。"

    "这不可能是真的。"

    "你的大脑在那一瞬间失去了所有语言的能力。"

    "你用力地眨了一下眼睛。也许你还在做梦。也许那通电话根本没有响过。也许你从未从沙发上醒来。"

    "但艾琳娜还在那里。"

    "她穿着那件淡色的家居裙。头发松松地垂在肩侧，恢复了光泽——不是疗养院末期那种干枯——是更早的，是你们搬进这间公寓的第二年冬天，她裹着毯子坐在北窗下看你画画的样子。皮肤有血色。嘴唇是粉的。呼吸平稳。"

    elena "你怎么去了这么久。我以为你只是去买颜料。"

    "「我去了——」"

    "你停顿了。你依稀记得之前发生的事。你跪在碎石路上痛哭。"

    elena "你去了哪里？"

    "她站起来，走到你面前。她的手指贴上你的脸颊——温的，软的。你握住那只手。"

    "「你恢复好了？」"

    elena "医生说恢复得很好。你怎么了？你看起来像是见了鬼。"

    "你上前抱住了她。"

    "「我以为你……」"

    elena "说什么傻话呢？你最近是不是有些健忘呀，我不是已经恢复了吗？"

    "「什么时候？」"

    elena "前段时间——你不是陪我去疗养院了吗？然后就好了呀。"

    "她的眼睛没有躲避。她的语气里没有迟疑。但你不记得。或者你记得的不是这样。你记得跪在路边，哭到喘不过气，有人把你从地上拉起来。"

    "「但是……我记得当时我……」"

    elena "你一定是记错了。我现在不是好好的吗？"

    "你看到了床头柜上摊着的速写本。"

    "翻到的那一页，是艾琳娜在五渔村的速写。你最喜欢的画。纸面泛黄，炭笔线条模糊。"

    "艾琳娜拉着你站到窗边，背对着你，看着外面波士顿的夜。她的背影被街灯勾出柔和的轮廓。"

    "这时的窗外，波士顿开始飘起了雪。"

    "你看着那些雪花从黑暗中落下来，落在路灯的光晕里，像灰尘一样细小、一样安静。你忽然觉得整个世界都变得不真实了。"

    # 推进阶段
    python:
        quest.set_stage("ch01_doorbell")

    jump explore_loop


# ---- Scene 05：门铃 ----

label sc05_doorbell:
    hide screen room_explore

    $ nav.set_initial_room("bedroom")
    scene expression nav.get_current_room()["background"]
    with dissolve

    "（叮——）"

    "门铃响了。"

    "你下意识回过头。第二声门铃又响了。"

    "艾琳娜没有动，只是站在窗边看着你。"

    elena "有人找你，你是邀请了客人了？"

    "「我记得应该……没有……你等我一下。」"

    "你离开卧室，走到玄关，打开门。"

    $ nav.set_initial_room("foyer")
    scene expression nav.get_current_room()["background"]
    with dissolve

    "门外站着吉姆，呼吸有些急促。"

    jim "谢天谢地，你终于开门了。"

    "「怎么了？」"

    jim "你忘了吗？今天和哈丁医生有约。"

    "你愣住了。"

    "吉姆拿着玄关的大衣，拉着你出来。冷风灌进楼道。你被半推着往外走。"

    "你忍不住回过头——公寓的门还开着一道缝。"

    jim "你现在状态很差。哈丁医生已经等了你一下午了。"

    scene black
    with Dissolve(2.0)

    "两人下楼。雪比刚才更大了。"

    "你坐进出租车。关上车门的时候，忽然怔了一下。"

    "你忘了跟她说再见。你忘了问她要不要带什么东西回来。"

    "出租车缓缓驶离哈里斯大道。车窗外的公寓越来越远。"

    "你把脸转向车窗。玻璃上映出你自己的脸——苍白的、疲惫的、眼眶发红的。"

    pause 2.0

    # 第一章结束
    python:
        state.set_flag("ch01_complete")
        meta.increment_playthrough()

    centered "第一章 归途 · 完"

    # TODO: 跳转到第二章
    # jump ch02_start

    return
