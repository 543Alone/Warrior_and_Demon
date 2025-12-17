# -*- coding: UTF-8 -*-
"""
@Project ：LangGraph
@File    ：勇士与魔王.py
@IDE     ：PyCharm
@Author  ：Write Bug
@Date    ：2025/12/10 10:28
"""
import random
import time


class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    END = '\033[0m'


# 定义全局超参
GAME_CONFIG = {
    "CRIT_RATE": 0.2,  # 20% 暴击率
    "CRIT_DMG": 1.5,  # 暴击造成 1.5 倍伤害
    "TEXT_SPEED": 1.0,  # 战斗文字显示间隔(秒)
    "LEVEL_UP_SCALING": 1.15,  # 每次升级属性提升 15%
    "EXP_THRESHOLD_BASE": 100,  # 升到2级所需经验
    # 随机性种子 (用于调试，None表示完全随机)
    "RANDOM_SEED": None
}

# 定义武器库
weapons_list = [
    {"id": "w01", "name": "生锈铁剑", "atk": 5, "hit_rate": 0.95, "desc": "新手村捡来的，破伤风之刃", "effect": None},
    {"id": "w02", "name": "精钢长剑", "atk": 20, "hit_rate": 0.85, "desc": "标准的骑士装备", "effect": None},
    {"id": "w03", "name": "🗡 皇家骑士巨剑", "atk": 25, "hit_rate": 0.90, "desc": "王国卫队的制式武器，性能均衡",
     "effect": None},
    {"id": "w04", "name": "🗡️ 双持匕首", "atk": 30, "hit_rate": 1.0,
     "desc": "虽然单次伤害不高，但绝对不会失手 (100%命中)",
     "effect": None},
    {"id": "w05", "name": "⌨️ 机械键盘", "atk": 40, "hit_rate": 1.0, "desc": "物理与精神双重打击，特别是青轴",
     "effect": "noise"},
    {"id": "w10", "name": "巨型战斧", "atk": 45, "hit_rate": 0.65, "desc": "伤害爆炸，但太重了容易挥空 (高风险)",
     "effect": None},
    {"id": "w11", "name": "🔥 烈焰魔剑", "atk": 50, "hit_rate": 0.85, "desc": "附带魔法火焰，专门克制魔王",
     "effect": "burn"},
    {"id": "w12", "name": "🩸 嗜血魔剑", "atk": 50, "hit_rate": 0.85, "desc": "附带吸血，魔王也是碳基生物吗？",
     "effect": "hemophagia"},
    {"id": "w19", "name": "圣剑·Excalibur", "atk": 80, "hit_rate": 0.90, "desc": "专门为了斩杀魔王而存在的传说武器。",
     "effect": "demon_slayer_multiplier_2.5"},  # 对魔王造成2.5倍伤害
    {"id": "w99", "name": "龙之牙", "atk": 999, "hit_rate": 0.10, "desc": "威力巨大但全是Bug(很难命中)",
     "effect": None},  # 极端数值测试

]

# 定义防具库
armors_list = [
    {"name": "布衣", "def": 2, "dodge": 0.0, "desc": "在魔王眼里，你就是什么都没穿", "effect": None},
    {"name": "锁子甲", "def": 10, "dodge": -0.05, "desc": "有些沉重，稍微降低闪避", "effect": None},
    {"name": "🛡️ 骑士板甲", "def": 25, "dodge": -0.15, "desc": "铁罐头一般的安全感", "effect": None},
    {"name": "忍者夜行衣", "def": 5, "dodge": 0.20, "desc": "防御不高，但只要打不中就不掉血", "effect": "stealth"},
    {"name": "🌵 荆棘背心", "def": 15, "dodge": 0.0, "desc": "穿背心难，脱背心更难", "effect": "reflect_damage"},
    {"name": "🔥 凤凰羽衣", "def": 12, "dodge": 0.05, "desc": "救命啊着火了。。。", "effect": "regen_hp"},
    {"name": "cos服", "def": 1, "dodge": 0.0, "desc": "由于过于普通，魔王可能会无视你", "effect": "low_aggro"},
    {"name": "📦 纸箱", "def": 5, "dodge": 0.30, "desc": "致敬Solid Snake，魔王根本看不见你", "effect": "stealth_bonus"},
    {"name": "👙 黄金比基尼", "def": 80, "dodge": 0.0, "desc": "众所周知，布料越少防御越高 (仅限女性角色有效?)",
     "effect": "charm"},
    {"name": "🐢 龟壳背包", "def": 40, "dodge": -0.20, "desc": "防御力惊人，但重得让你想趴在地上走", "effect": None},
]

# 角色属性
hero = {
    "name": "勇士",
    "level": 1,
    "hp": 100,
    "max_hp": 100,
    "max_cost": 5,  # 初始负重
    "base_atk": 10,  # 基础攻击力
    "def": 3,  # 基础防御
    "exp": 0,
    "SPD": 10,  # 基础移速，影响先手和逃跑
    "LUCK": 5,  # 幸运值，影响暴击和掉落
    "bag": [weapons_list[0], armors_list[0]],
}

demon = {
    "name": "魔王",
    "hp": 3000,  # 魔王血量厚
    "max_hp": 3000,
    "base_atk": 30,  # 魔王攻击高
    "def": 10,
    "burn_stack": 0,  # 被火焰层数
    "LUCK": 0,  # 不幸的成为了魔王
    "loot": [],  # 防止报错
}

# 定义怪物库
monsters_list = [
    {
        "name": "史莱姆",
        "hp": 30,
        "max_hp": 30,
        "base_atk": 5,
        "def": 0,
        "exp": 10,
        "burn_stack": 0,  # 被火焰层数
        "loot": [
            {"item": "精钢长剑", "chance": 0.3},  # 30% 掉落铁剑
            {"item": "🍎 小苹果", "chance": 0.5},  # 50% 掉落苹果
        ]
    },
    {
        "name": "哥布林斥候",
        "hp": 60,
        "max_hp": 60,
        "base_atk": 12,
        "def": 2,
        "exp": 25,
        "burn_stack": 0,  # 被火焰层数
        "loot": [
            {"item": "🗡️ 双持匕首", "chance": 0.05},  # 稀有掉落
            {"item": "锁子甲", "chance": 0.3},

        ]
    },
    {
        "name": "青牙巨魔",
        "hp": 100,
        "max_hp": 100,
        "base_atk": 12,
        "def": 5,
        "exp": 35,
        "burn_stack": 0,  # 被火焰层数
        "loot": [
            {"item": "巨型战斧", "chance": 0.3},
            {"item": "💪 力量药剂", "chance": 0.5},
            {"item": "🍗 烤鸡腿", "chance": 0.7},
        ]
    },
    {
        "name": "发狂的程序员",
        "hp": 100,
        "max_hp": 100,
        "base_atk": 20,
        "def": 10,
        "exp": 50,
        "burn_stack": 0,  # 被火焰层数
        "loot": [
            {"item": "⌨️ 机械键盘", "chance": 0.01},  # 极品掉落 1%
            {"item": "cos服", "chance": 0.2},
            {"item": "☕ 浓缩咖啡", "chance": 0.8},  # 必掉续命水
        ]
    },
    {
        "name": "宝箱怪",
        "hp": 150,
        "max_hp": 150,
        "base_atk": 35,
        "def": 20,
        "exp": 80,
        "burn_stack": 0,  # 被火焰层数
        "loot": [
            {"item": "🩸 嗜血魔剑", "chance": 0.1},  # 欧皇时刻
            {"item": "🔥 烈焰魔剑", "chance": 0.3},  # 欧皇时刻
            {"item": "🗡 皇家骑士巨剑", "chance": 0.7},
            {"item": "🛡️ 皇家骑士板甲", "chance": 0.7},
        ]
    }
]

# 定义物品库
items_list = [
    # --- 回复类 ---
    {"name": "🍎 小苹果", "type": "heal", "value": 20, "desc": "路边树上摘的，希望没有农药"},
    {"name": "🧪 强效治疗药水", "type": "heal", "value": 100, "desc": "炼金术士还是医生？"},
    {"name": "🍗 烤鸡腿", "type": "heal", "value": 50, "desc": "香气扑鼻，补充体力的好东西"},

    # --- 增益类 (Buff) ---
    {"name": "💪 力量药剂", "type": "buff_atk", "value": 10, "duration": 3, "desc": "喝了感觉充满了力量 (持续3回合)"},
    {"name": "⚡ 敏捷药剂", "type": "buff_hit", "value": 0.2, "duration": 3,
     "desc": "你的动作快到出现残影 (命中率+20%)"},

    # --- 特殊类 ---
    {"name": "☕ 浓缩咖啡", "type": "special", "value": 0,
     "desc": "虽然不加血，但你可以通宵打魔王了 (解除睡眠/麻痹状态)"},
    {"name": "💣 地精手雷", "type": "damage", "value": 80, "desc": "造成固定伤害，不需要命中率"}
]

# 定义位置
world_map = {
    "新手村": {
        "desc": "安全和平的小村庄，可以休息回血。",
        "connects_to": ["幽暗森林"],
        "safe_zone": True  # 安全区，不会遇怪
    },
    "幽暗森林": {
        "desc": "光线昏暗的森林，随处可见哥布林和史莱姆。",
        "connects_to": ["新手村", "魔王城"],
        "safe_zone": False,
        "danger_level": 0.4  # 40% 几率遇怪
    },
    "魔王城": {
        "desc": "最终决战之地，空气中弥漫着硫磺味。",
        "connects_to": ["幽暗森林"],
        "safe_zone": False,
        "is_boss_room": True  # 只有Boss
    }
}

# 玩家当前位置
current_location = "新手村"
# 定义两个全局变量存当前装备
current_weapon = weapons_list[0]
current_armor = armors_list[0]


# 定义血条
def show_health_bar(entity, max_bar_length=20):
    """
    显示实体血条
    :param entity: 实体对象(勇士/魔王/怪物等)
    :param max_bar_length: 血条最大长度
    """
    hp = entity.get("hp", 0)
    max_hp = entity.get("max_hp", hp if hp > 0 else 1)
    name = entity.get("name", "未知")

    # 计算血条长度
    if hp < 0: hp = 0
    bar_length = min(int(hp / max_hp * max_bar_length), max_bar_length)
    empty_length = max_bar_length - bar_length

    # 红色血条
    health_bar = f"{Colors.RED}{'#' * bar_length}{Colors.END}{' ' * empty_length}"
    print(f"{name} HP: [{health_bar}] {hp}/{max_hp}")

    ...


# 定义攻击逻辑
def attack_logic(attacker, defender, weapons=None):
    """
        计算一次攻击的所有逻辑：命中 -> 暴击 -> 扣血
        这里的 weapon 参数如果是 None，代表是裸手或者怪物攻击
    """
    print(f"   \n⚔️  {attacker['name']} 发起了攻击！")
    # 计算总攻击力和命中率
    total_atk = attacker['base_atk']
    hit_chance = 0.9  # 默认魔王命中率
    dmg_multiplier = 1.0  # 暴击
    current_effect = None

    # 只有玩家攻击时才有 weapon
    if weapons:
        total_atk += weapons["atk"]
        hit_chance = weapons['hit_rate']
        current_effect = weapons.get("effect")
        print(f"(使用武器: {weapons['name']} | 武器攻击: {weapons['atk']})")

    # 闪避判断
    defender_dodge = defender.get("dodge", 0.0)

    # 定义Miss
    if random.random() > hit_chance:
        print(f"   🚫 {attacker['name']} 的攻击挥空了！(Miss)")
        return  # 攻击结束

        # 如果随机数小于闪避率，直接 Miss
    if random.random() < defender_dodge:
        print(f"   ⚡ {defender['name']} 身手敏捷，躲开了攻击！(Dodge)")
        return

    # 定义暴击
    is_crit = False
    if random.random() < GAME_CONFIG["CRIT_RATE"]:
        is_crit = True
        dmg_multiplier = GAME_CONFIG["CRIT_DMG"]
        print(f"   💥 {Colors.YELLOW}暴击!{Colors.END}")

    # 计算伤害：(攻击 * 倍率) - 防御
    raw_dmg = (total_atk * dmg_multiplier) - defender.get('def', 0)
    # 保证最少造成1点伤害
    final_dmg = int(max(1, raw_dmg))
    # 扣血指令
    defender['hp'] -= final_dmg
    # 小于0逻辑处理
    if defender['hp'] < 0:
        defender['hp'] = 0
    crit_text = "💥 暴击！" if is_crit else ""
    print(f"   ➡️  击中了 {defender['name']}！{crit_text} 造成了 {final_dmg} 点伤害。")

    # 定义嗜血
    if weapons:
        if current_effect == "hemophagia":
            heal = int(final_dmg * 0.3)
            attacker['hp'] = min(attacker['max_hp'], attacker['hp'] + heal)
            print(f"   💚 {attacker['name']} 触发吸血！恢复了 {heal} 点生命值！")

    # 定义灼烧
    if current_effect == "burn":
        # 固定每次减少魔王10点生命值，0.3的概率可叠加一层
        if random.random() < 0.3:
            defender['burn_stack'] += 1
        if defender['burn_stack'] > 0:
            print(f"   🔥 {defender['name']} 身上燃起了火焰！(当前层数: {defender['burn_stack']})")
    ...


# 定义菜单
def equip_menu(player):
    """专门用来换装备的菜单函数"""
    global current_weapon, current_armor

    print("\n" + "=" * 20)
    print("【🎒 背包 & 装备】")

    my_weapons = [item for item in player['bag'] if 'atk' in item]
    if not my_weapons:
        print(" (背包里没有武器)")
    else:
        # 换武器
        print("可装备的武器:")
        for i, w in enumerate(my_weapons):
            # 标记当前装备的
            mark = "*" if w == current_weapon else " "
            print(f"{mark} {i}. {w['name']} (攻+{w['atk']})")

        try:
            choice = input("输入编号更换 (回车跳过): ")
            if choice.isdigit():
                idx = int(choice)
                if 0 <= idx < len(my_weapons):
                    current_weapon = my_weapons[idx]
                    print(f"✅ 已装备: {current_weapon['name']}")
        except:
            pass

    print("-" * 20)

    # 换防具
    my_armors = [item for item in player['bag'] if 'def' in item]

    if not my_armors:
        print(" (背包里没有防具)")
    else:
        print("可装备的防具:")
        for i, a in enumerate(my_armors):
            mark = "*" if a == current_armor else " "
            print(f"{mark} {i}. {a['name']} (防+{a['def']})")

        try:
            choice = input("输入编号更换 (回车跳过): ")
            if choice.isdigit():
                idx = int(choice)
                if 0 <= idx < len(my_armors):
                    # 先移除旧防具的加成 (防止无限叠加BUG)
                    player['def'] -= current_armor.get('def', 0)

                    # 换新装备
                    current_armor = my_armors[idx]

                    # 加上新防具加成
                    player['def'] += current_armor['def']
                    player['dodge'] = current_armor.get('dodge', 0)
                    print(f"✅ 已装备: {current_armor['name']} (当前防御: {player['def']})")
        except:
            pass

    print("=" * 20 + "\n")


# 定义掉落
def get_item_data_by_name(item_name):
    # 搜索武器库
    for w in weapons_list:
        if w['name'] == item_name: return w
    # 搜索防具库
    for a in armors_list:
        if a['name'] == item_name: return a
    # 搜索物品库
    for i in items_list:
        if i['name'] == item_name: return i
    return None


# 定义徘徊
def wander_action(player, location_data):
    print(f"\n🚶 你开始在 [{current_location}] 四处徘徊...")
    time.sleep(1)  # 增加一点沉浸感

    # --- 情况 A: 安全区逻辑 ---
    if location_data.get("safe_zone"):
        dice = random.random()
        if dice < 0.2:
            print("   💬 你遇到了村长，但他正在午睡。")
        elif dice < 0.4:
            # 捡漏逻辑
            print("   🍀 运气不错！你在草丛里捡到了一个 [🍎 小苹果]！")
            # 记得用你修好的 get_item_data_by_name
            item = get_item_data_by_name("🍎 小苹果")
            if item: player['bag'].append(item.copy())
        else:
            print("   🍃 风很喧嚣，这里一片祥和，什么也没发生。")
        return

    # --- 情况 B: 危险区/野外逻辑 ---
    # 获取当前地图的危险度，如果没有设定，默认 0.4
    encounter_rate = location_data.get("danger_level", 0.4)

    dice = random.random()
    print(f"命运骰子的数字是：{dice}")
    win = True
    # --- 区间 1: 遭遇战斗 (0 ~ encounter_rate) ---
    if dice < encounter_rate:
        # 随机抽怪
        enemy_template = random.choice(monsters_list)
        print(f"应命运召唤而来，是：{enemy_template["name"]}")
        # 特殊逻辑：如果是宝箱怪和程序员（隐藏怪），让它很难遇到
        if enemy_template['name'] == "发狂的程序员":
            # 只有 5% 的概率真正触发发狂的程序员，剩下 95% 是错觉
            if random.random() < 0.05:
                win = start_battle(player, enemy_template)
            else:
                print("   👀 你感觉好像感受到了汗毛直立的怒火。")
        elif enemy_template['name'] == "宝箱怪":
            if random.random() < 0.1:
                win = start_battle(player, enemy_template)
            else:
                print("   👀 你感觉好像有东西在盯着你，但回过头什么也没有。")
            # 普通怪 (史莱姆/哥布林) 直接开打，不要犹豫！
        else:
            start_battle(player, enemy_template)
        if not win:
            return False

    # --- 区间 2: 捡到东西 (encounter_rate ~ encounter_rate + 0.2) ---
    # 注意：这里用 elif，且不需要减号，而是接着上面的概率往后延
    elif dice < encounter_rate + 0.2:
        findable_items = ["🍎 小苹果", "💪 力量药剂", "生锈铁剑"]
        item_name = random.choice(findable_items)
        real_item = get_item_data_by_name(item_name)

        if real_item:
            print(f"   ✨ 眼前一亮！你在树桩下发现了 [{item_name}]！")
            player['bag'].append(real_item.copy())

    # --- 区间 3: 啥也没有 (剩余概率) ---
    else:
        flavors = [
            "🍂 踩到了枯树枝，发出咔嚓的声音。",
            "💨 一阵阴风吹过，你打了个寒颤。",
            "👣 走了半天，好像又绕回了原地..."
        ]
        print(f"   {random.choice(flavors)}")

    return win


# 定义升级
def check_level_up(player):
    """
    检查是否满足升级条件，如果满足则提升属性
    """
    # 计算下一级所需的经验值：当前等级 * 基础阈值 (例如 1级升2级需100，2级升3级需200)
    required_exp = player['level'] * GAME_CONFIG["EXP_THRESHOLD_BASE"]

    if player['exp'] >= required_exp:
        # 扣除经验值 (或者你可以选择不扣除，而是累积经验制，看你喜好)
        # 这里采用：扣除当前升级所需经验，保留溢出部分
        player['exp'] -= required_exp
        player['level'] += 1

        # 获取成长倍率
        scale = GAME_CONFIG["LEVEL_UP_SCALING"]  # 1.15

        # --- 属性提升计算 ---
        # 生命上限提升 (取整)
        old_hp = player['max_hp']
        player['max_hp'] = int(old_hp * scale)

        # 攻击力提升 (保底 +1，防止前期数值太低乘法无效)
        old_atk = player['base_atk']
        add_atk = int(old_atk * scale) - old_atk
        if add_atk < 1: add_atk = 1
        player['base_atk'] += add_atk

        # 防御力提升 (保底 +1，每两级至少加1点防御)
        old_def = player['def']
        # 防御成长慢一点，这里做一个简单判断
        player['def'] = int(old_def * scale)
        if player['def'] == old_def:  # 如果乘完没变
            player['def'] += 1

        # 升级回满血
        player['hp'] = player['max_hp']

        print(f"\n" + "=" * 30)
        print(f"🎉 {Colors.YELLOW}恭喜升级！你升到了 Lv.{player['level']}！{Colors.END}")
        print(f"   ❤️ 生命上限: {old_hp} -> {player['max_hp']}")
        print(f"   ⚔️ 基础攻击: {old_atk} -> {player['base_atk']}")
        print(f"   🛡️ 基础防御: {old_def} -> {player['def']}")
        print(f"   ✨ 状态已完全恢复！")
        print("=" * 30 + "\n")

        # 递归检查（防止一次获得巨量经验连升两级的情况）
        check_level_up(player)


# 定义回合
def start_battle(player, enemy_template, ):
    global current_weapon  # 引用全局已装备的武器

    # 复制敌人数据
    enemy = enemy_template.copy()

    print(f"\n" + "!" * 30)
    print(f"⚠️  遭遇战！一只 {Colors.RED}{enemy['name']}{Colors.END} 出现了！")
    print("!" * 30)

    turn = 1
    while player['hp'] > 0 and enemy['hp'] > 0:
        print(f"\n--- Round {turn} ---")
        show_health_bar(player)
        show_health_bar(enemy)
        time.sleep(GAME_CONFIG["TEXT_SPEED"])

        # --- 玩家回合 ---
        attack_logic(player, enemy, current_weapon)

        # 结算燃烧伤害
        if enemy.get('burn_stack', 0) > 0:
            burn_dmg = enemy['burn_stack'] * 10
            enemy['hp'] -= burn_dmg
            print(f"   🔥 灼烧造成 {burn_dmg} 伤害")

        # 检查胜利
        if enemy['hp'] <= 0:
            print(f"\n🎉 胜利！打败了 {enemy['name']}！")
            player['exp'] += enemy.get('exp', 0)
            print(f"   获得经验: {enemy.get('exp', 0)}")

            check_level_up(player)

            # 掉落逻辑
            for loot in enemy.get('loot', []):
                if random.random() < loot['chance']:
                    item_name = loot['item']
                    real_item = get_item_data_by_name(item_name)
                    if real_item:

                        print(f"   🎁 哇！掉落了 [{item_name}]")
                        player['bag'].append(real_item)
                    else:
                        print(f"   (系统错误：掉落了 {item_name} 但找不到数据)")
            return True

        # --- 怪物回合 ---
        time.sleep(GAME_CONFIG["TEXT_SPEED"])
        attack_logic(enemy, player, weapons=None)  # 怪物不用武器

        if player['hp'] <= 0:
            print(f"\n☠️ 胜败乃兵家常事... 大侠请重新来过。")
            return False

        turn += 1
        ...


# 死亡惩罚
def Death_penalty(player):
    global current_location
    print("村民发现了昏迷的你，把你拖回了村子。")

    # --- 复活逻辑 ---
    current_location = "新手村"  # 强制送回新手村
    hero['hp'] = player['max_hp']  # 满血复活

    # 死亡惩罚：扣除 50% 当前经验
    lost_exp = int(player['exp'] / 2)
    hero['exp'] -= lost_exp

    print(f"🏥 经过村长的治疗，你醒了过来。")
    print(f"📉 代价：经验值减少了 {lost_exp} 点。")

    time.sleep(2)


# 战斗主逻辑
def main_game_loop():
    global current_location

    print(f"{Colors.YELLOW}=== 欢迎来到《勇士与魔王》 ==={Colors.END}")

    # 游戏开始前先选一次装备
    equip_menu(hero)

    while True:
        # 获取当前地点的字典数据
        location_data = world_map[current_location]
        danger_level = location_data.get("danger_level", 0.5)

        print(f"\n" + "-" * 30)
        print(f"📍 地点：{Colors.BLUE}{current_location}{Colors.END}")
        print(f"📝 描述：{location_data['desc']}")
        print("-" * 30)

        # 行动菜单
        print("1. 🚶 移动")
        print("2. 💤 休息 (回血)")
        print("3. 🎒 状态与装备")
        print("4. 🔍 在周围徘徊 (练级/寻宝)")
        if location_data.get("is_boss_room"):
            print(f"9. ⚔️ {Colors.RED}决战魔王！{Colors.END}")

        choice = input("请选择: ")

        if choice == "1":
            # 移动逻辑
            print("可以去的地方:")
            # 这里用 location_data，不能用 world_map直接取
            targets = location_data["connects_to"]
            for i, dest in enumerate(targets):
                print(f"{i + 1}. {dest}")

            try:
                idx = int(input("输入序号: ")) - 1
                if 0 <= idx < len(targets):
                    next_loc_name = targets[idx]
                    next_loc_data = world_map[next_loc_name]

                    # 移动成功
                    current_location = next_loc_name

                    # 遇敌判定 (不在安全区 且 不是BOSS房)
                    if not next_loc_data.get("safe_zone") and not next_loc_data.get("is_boss_room"):
                        if random.random() < danger_level:
                            # 随机抽一个小怪
                            wild_enemy = random.choice(monsters_list)
                            # 触发战斗
                            if wild_enemy['name'] == "发狂的程序员":
                                if random.random() < 0.05:
                                    win = start_battle(hero, wild_enemy)
                                    if not win and hero['hp'] == 0:
                                        Death_penalty(hero)
                                else:
                                    print("   👀 你感觉好像感受到了汗毛直立的怒火。")
                            elif wild_enemy['name'] == "宝箱怪":
                                if random.random() < 0.1:
                                    win = start_battle(hero, wild_enemy)
                                    if not win and hero['hp'] == 0:
                                        Death_penalty(hero)
                                else:
                                    print("   👀 你感觉好像有东西在盯着你，但回过头什么也没有。")
                        else:
                            print("路上很安全...")
            except ValueError:
                print("输入错误")

        elif choice == "2":
            if location_data.get("safe_zone"):
                hero['hp'] = hero['max_hp']
                print("💤 睡得很香，HP已回满！")
            else:
                print("❌ 野外睡觉会被狼叼走的！")


        elif choice == "3":
            print(f"\n{Colors.CYAN}═════════ 📊 角色状态 ═════════{Colors.END}")
            print(
                f"🤴 英雄: {hero['name']}  (Lv.{hero['level']})  (Epx:{hero['exp']}/{hero['level'] * GAME_CONFIG["EXP_THRESHOLD_BASE"]})")
            print(f"❤️ 血量: {Colors.RED}{hero['hp']}/{hero['max_hp']}{Colors.END}")
            print(
                f"🗡️ 攻击: {hero['base_atk'] + current_weapon['atk']} (基础{hero['base_atk']} + 武器{current_weapon['atk']})")
            print(
                f"🛡️ 防御: {hero['def'] + current_armor['def']} (基础{hero.get('def', 0)} + 防具{current_armor['def']})")
            print("-" * 30)
            print(f"当前装备: [{current_weapon['name']}] & [{current_armor['name']}]")
            print(f"\n{Colors.YELLOW}🎒 背包清单 (堆叠显示):{Colors.END}")
            if not hero['bag']:
                print("   (空空如也)")
            else:
                stacked_bag = {}

                # 遍历背包，统计数量
                for item in hero['bag']:
                    name = item['name']
                    if name in stacked_bag:
                        stacked_bag[name]['count'] += 1
                    else:
                        # 第一次遇到这个物品，存入数据和初始数量1
                        stacked_bag[name] = {
                            'data': item,  # 存物品原始数据方便读取属性
                            'count': 1
                        }

                # 遍历统计好的字典进行显示
                # index 用于显示序号 (虽然堆叠显示后，序号就不能直接对应背包index了，这里仅作展示用)
                index = 1
                for name, info in stacked_bag.items():
                    item_data = info['data']
                    count = info['count']

                    # 只有数量大于1才显示 xN
                    count_str = f"{Colors.YELLOW} x{count}{Colors.END}" if count > 1 else ""

                    # 根据类型显示不同图标
                    if 'atk' in item_data:
                        print(f"   [{index}] ⚔️ {name} (攻+{item_data['atk']}){count_str}")
                    elif 'def' in item_data:
                        print(f"   [{index}] 🛡️ {name} (防+{item_data['def']}){count_str}")
                    elif 'type' in item_data and item_data['type'] == 'heal':
                        print(f"   [{index}] 🧪 {name} (回血+{item_data['value']}){count_str}")
                    else:
                        print(f"   [{index}] 📦 {name}{count_str}")

                    index += 1

            print("═══════════════════════════════")
            ch = input("要更换装备吗? (y/n): ")
            if ch == 'y':
                equip_menu(hero)

        elif choice == "4":
            # --- 调用徘徊逻辑 ---
            is_alive = wander_action(hero, location_data)
            if not is_alive and hero['hp'] == 0:
                Death_penalty(hero)

        elif choice == "9" and location_data.get("is_boss_room"):
            print("勇者推开了魔王殿的大门...")
            win = start_battle(hero, demon)
            if win:
                print("🏆 恭喜通关！！")
                break
            else:
                break


if __name__ == '__main__':
    main_game_loop()
