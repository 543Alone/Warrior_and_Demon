# -*- coding: UTF-8 -*-
import random
from Setting.Style import Colors

# 武器词条池 (名称, 权重)
WEAPON_AFFIX_POOL = [
    {"type": "crit_rate", "name": "致命", "desc": "暴击率提升", "value_range": [0.05, 0.15],
     "format": "+{:.0f}% 暴击率"},
    {"type": "crit_dmg", "name": "残暴", "desc": "暴击伤害提升", "value_range": [0.2, 0.5],
     "format": "+{:.0f}% 暴击伤害"},
    {"type": "lifesteal", "name": "吸血", "desc": "造成伤害时回血", "value_range": [0.05, 0.20],
     "format": "+{:.0f}% 吸血"},
    {"type": "atk_percent", "name": "锋锐", "desc": "基础攻击力百分比加成", "value_range": [0.1, 0.3],
     "format": "+{:.0f}% 攻击力"}
]

# 防具词条池
ARMOR_AFFIX_POOL = [
    {"type": "dodge", "name": "灵动", "desc": "闪避率提升", "value_range": [0.05, 0.15], "format": "+{:.0f}% 闪避率"},
    {"type": "max_hp_percent", "name": "强健", "desc": "最大生命值提升", "value_range": [0.1, 0.3],
     "format": "+{:.0f}% 生命上限"},
    {"type": "def_percent", "name": "坚固", "desc": "基础防御百分比加成", "value_range": [0.1, 0.4],
     "format": "+{:.0f}% 防御力"},
    {"type": "hp_regen", "name": "复苏", "desc": "每次受击回复少量生命值", "value_range": [1, 5],
     "format": "受击回血 +{:.0f}"}
]


def get_max_affix_count(quality):
    mapping = {
        "common": 1,
        "rare": 2,
        "epic": 3,
        "unique": 4,
        "legendary": 5,
        "glitch": 6
    }
    return mapping.get(quality, 1)


def roll_affixes(pool, count):
    # 随机抽取词条种类 (不重复)
    chosen_templates = random.sample(pool, min(count, len(pool)))
    affixes = []
    for template in chosen_templates:
        val = random.uniform(template["value_range"][0], template["value_range"][1])
        affixes.append({
            "type": template["type"],
            "name": template["name"],
            "value": val,
            "format": template["format"]
        })
    return affixes


def get_forge_cost(item):
    base_price = item.get("price", 100)
    forge_count = item.get("forge_count", 0)
    # 每次洗炼成本是上一回的 1.5 倍
    cost = int(base_price * 0.5 * (1.5 ** forge_count))
    # 设定一个保底费用
    return max(cost, 50)


def display_affixes(item):
    if not item.get("affixes"):
        return "(无附加词条)"
    lines = []
    for af in item["affixes"]:
        # 格式化显示，比如 +15% 暴击率
        if af["value"] < 1:  # 百分比
            val_str = af["format"].format(af["value"] * 100)
        else:
            val_str = af["format"].format(af["value"])
        lines.append(f"{Colors.PURPLE}[{af['name']}] {val_str}{Colors.END}")
    return " | ".join(lines)


def forge_menu(player):
    while True:
        print(f"\n{Colors.YELLOW}=== 铁匠铺 ==={Colors.END}")
        print(f"💰 你的金币: {player.get('gold', 0)}")
        print("铁匠：只要钱到位，生锈的铁剑我也能给你敲成神器！")
        print("【洗炼规则】装备品质越高，能洗出的词条越多！洗炼会覆盖原有的所有随机词条。")
        print("-" * 30)

        from Characters_intro import Relo
        print("选择你要为谁洗炼装备:")
        for idx, p in enumerate(Relo.party):
            print(f"[{idx}] {p['name']}")
        p_choice = input(f"> ")
        target_p = Relo.party[int(p_choice)] if p_choice.isdigit() and 0 <= int(p_choice) < len(Relo.party) else player

        # 只能锻造对应角色穿在身上的装备
        weapon = target_p.get('equipped_weapon', {'name': '无', 'price': 0})
        armor = target_p.get('equipped_armor', {'name': '无', 'price': 0})

        w_cost = get_forge_cost(weapon)
        a_cost = get_forge_cost(armor)

        if weapon.get('name') != '无':
            print(f"[1] 洗炼武器: {weapon['name']} (品质: {weapon.get('quality', '普通')}) - 费用: 💰 {w_cost} G")
            print(f"    当前词条: {display_affixes(weapon)}")
        if armor.get('name') != '无':
            print(f"[2] 洗炼防具: {armor['name']} (品质: {armor.get('quality', '普通')}) - 费用: 💰 {a_cost} G")
            print(f"    当前词条: {display_affixes(armor)}")

        print("-" * 30)

        choice = input("选择你要洗炼的装备 (1-武器, 2-防具, 0-离开): ")
        if choice == '0':
            print("铁匠：没钱就去打怪赚！")
            break

        if choice in ['1', '2']:
            target_item = weapon if choice == '1' else armor
            if target_item.get('name') == '无':
                print("❌ 铁匠：你都没穿这件装备，洗个屁啊！")
                continue

            pool = WEAPON_AFFIX_POOL if choice == '1' else ARMOR_AFFIX_POOL
            cost = w_cost if choice == '1' else a_cost

            if player.get('gold', 0) >= cost:
                player['gold'] -= cost
                target_item['forge_count'] = target_item.get('forge_count', 0) + 1

                max_affixes = get_max_affix_count(target_item.get('quality', 'common'))
                # 随机生成词条数量，至少1条，最多达到品质上限
                roll_count = random.randint(1, max_affixes)

                new_affixes = roll_affixes(pool, roll_count)
                target_item['affixes'] = new_affixes

                print(f"叮叮当当... 洗炼完成！剩余金币: {player['gold']}")
                print(f"✨ 新词条: {display_affixes(target_item)}")
            else:
                print("❌ 铁匠：钱不够！别来消遣我！")
