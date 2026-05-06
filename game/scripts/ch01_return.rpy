# 第一章：归途
# 场景 1 - 公寓·玄关

label ch01_start:
    # 预加载资源
    $ renpy.image_preload("images/scene1.png")

    # 章节标题
    scene black
    centered "第一章：归途"

    jump sc01_foyer

label sc01_foyer:
    scene bg apartment_foyer
    with dissolve

    "哈里斯大道的公寓和你离开时一模一样。窄长的棕色石砖公寓——波士顿最常见的那种——门廊窄，天花板却意外地高。"

    "吉姆帮你开了门，把行李靠墙放在鞋柜旁。衣帽架上挂着你那件旧风衣，雨伞桶里斜插着一把黑伞。他站在门口，没有进来。"

    "客厅的窗帘拉着。空气里有久未通风的沉闷——不是灰尘的气味，是封闭的空间自己产生的气味。旧木头。干涸的水垢。寂静。"

    jim "药在茶几上——哈丁医生开的，每晚一片。"

    jim "我明天再来看你。"

    "门关上的声音。钥匙转动的声音。锁舌卡入锁扣的金属声——比他需要的更响。"

    "然后——完全地、彻底地——安静了。"

    jump sc01_foyer_explore

label sc01_foyer_explore:
    scene bg apartment_foyer
    "你站在玄关。目光落在几个地方上。你想先看看什么？"

    menu:
        "行李袋":
            jump sc01_foyer_bag
        "电话答录机":
            jump sc01_foyer_phone
        "鞋柜":
            jump sc01_foyer_shoes
        "玄关的镜子":
            jump sc01_foyer_mirror
        "（先不看了，往前走）":
            jump sc01_foyer_done

label sc01_foyer_bag:
    $ flags["examined_bag"] = True

    "深灰色的帆布袋靠在鞋柜侧面。不是你平时出门用的那一只——这是疗养院的物品，侧面贴着一张白色标签，上面用墨水写着你的名字：{i}卡特，汤姆。{/i}"

    "袋子的侧面有一层灰白色的粉末。你用拇指抹了一下——很细，滑腻。不像普通的灰尘，倒更像是……石粉。"

    "你打开袋口。里面是你的几件换洗衣物，叠得不整齐——不是你的叠法。是别人帮你收拾的。"

    "你不想去回忆是谁。"

    $ renpy.notify("你不想回忆的事情，你的手还记得。")
    jump sc01_foyer_explore

label sc01_foyer_phone:
    $ flags["heard_voicemail"] = True

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

    $ flags["anomaly_count"] = flags.get("anomaly_count", 0) + 1
    jump sc01_foyer_explore

label sc01_foyer_shoes:
    $ flags["examined_shoes"] = True

    "老旧的橡木鞋柜。你蹲下来打开柜门——你的鞋整齐地排列在底层。皮鞋，帆布鞋，一双你冬天穿的厚靴子。"

    "她的鞋在最顶层。三双。你不是故意去看的。"

    "最外面那双——她春天常穿的浅口平底鞋——鞋底边缘嵌着一圈灰白色的细砂。"

    "她不穿这双鞋去疗养院。这双鞋是她在家穿的。"

    "所以这些砂子——是在她离开家{i}之前{/i}就在那里的。"

    $ flags["anomaly_count"] = flags.get("anomaly_count", 0) + 1
    jump sc01_foyer_explore

label sc01_foyer_mirror:
    $ flags["touched_mirror"] = True

    "你无意中瞥了一眼门边的穿衣镜。"

    "镜子里的你——比上次照镜子时瘦了很多。颧骨突出了，眼窝凹陷。你穿着那件从疗养院穿回来的灰色外套，领口有一圈深色的汗渍。"

    "你盯着镜子看了三秒。"

    "然后你注意到——镜子里的你，比你晚了一瞬间才停下动作。"

    "你揉了揉眼睛。再看。一切正常。"

    "{i}一切正常。{/i}"

    $ flags["anomaly_count"] = flags.get("anomaly_count", 0) + 1
    jump sc01_foyer_explore

label sc01_foyer_done:
    "你深吸了一口气。这才只是进门而已。"
    "玄关之外，公寓的其他房间还在等着你。"
    return
