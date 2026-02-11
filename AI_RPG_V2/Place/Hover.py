# -*- coding: UTF-8 -*-
"""
@Project ：LangGraph
@File    ：Hover.py
@IDE     ：PyCharm
@Author  ：Write Bug
@Date    ：2025/12/11 09:57
"""
import random
import time

from Battle.Battle_Monster import start_battle
from Battle.Death_penalty import Death_enalty
from Characters_intro import Relo
from Characters_intro.Bag import get_item_data_by_name, add_item_to_bag
from Monsters.Monsters import monster_distribution, get_monster_by_name
from Place.Map_A import world_map


def wander_action(player):
    # 实例化全局
    location_name = Relo.current_location
    # 获取原本数据
    current_location_data = world_map.get(location_name, {})

    print(f"\n你开始在 [{location_name}] 四处徘徊...")
    time.sleep(1)

    # 在安全区
    if current_location_data.get("safe_zone"):
        dice = random.random()

        # 彩蛋：如果新手村里有休息的伙伴，有几率遇到他们
        if location_name == "新手村" and Relo.reserve_party and dice < 0.3:
            buddy = random.choice(Relo.reserve_party)
            print(f"   你在村口遇到了正在休息的【{buddy['job']}·{buddy['name']}】。")
            if buddy['job'] == "法师":
                print(f"   {buddy['name']}: “喂！笨蛋勇士，别以为我是在等你回来才坐在这里的！”")
            elif buddy['job'] == "牧师":
                print(f"   {buddy['name']}: “勇士大人，您平安无事就好，我在村里一直在为您祈祷。”")
            elif buddy['job'] == "刺客":
                print(f"   {buddy['name']}: “... (默默地点了点头，擦拭着手中的匕首)”")
            elif buddy['job'] == "精灵":
                print(f"   {buddy['name']}: “愿风指引你的道路。如果需要我的弓箭，随时回村长家找我。”")
            return True

        if dice < 0.2:
            if location_name == "村长家":
                print("   你遇到了村长，但他正在午睡。")
            elif location_name == "商业街":
                print("   你看到道具店的老板正在打盹。")
            else:
                print("   💬 你遇到了几位正在聊天的村民。")
        elif dice < 0.5:
            print("   运气不错！你在地上捡到了一个 [小苹果]！")
            item = get_item_data_by_name("小苹果")
            if item:
                add_item_to_bag(player, item)
        else:
            print("   🍃 风很喧嚣，这里一片祥和，什么也没发生。")
        return True

    # 战斗/遭遇判定逻辑
    encounter_rate = current_location_data.get("danger_level", 0)
    dice = random.random()
    print(f"开始投掷命运的骰子：{dice}")

    if dice <= encounter_rate + 0.2:
        spawn_key = current_location_data.get("spawn_table")
        enemy_template = None

        # 权重选怪 (核心逻辑)
        if spawn_key and spawn_key in monster_distribution:
            spawn_config = monster_distribution[spawn_key]
            population = list(spawn_config.keys())
            weights = list(spawn_config.values())

            # 按权重抽取
            monster_name = random.choices(population, weights=weights, k=1)[0]
            enemy_template = get_monster_by_name(monster_name)

        # 保底
        if not enemy_template:
            print("   （警告：该区域没有配置怪物，一只迷路的史莱姆出现了）")
            enemy_template = get_monster_by_name("史莱姆")

        # 分支处理：根据怪物类型决定由于发生什么
        win = True  # 默认状态

        # --- 分支 A: 宝箱怪 (交互逻辑) ---
        if "宝箱怪" in enemy_template['name']:
            print("\n你在路边发现了一个神秘的宝箱！")

            # 动态削弱逻辑：如果是新手村，把怪改弱
            current_monster = enemy_template

            if location_name == "幽暗森林":
                print("   (直觉: 这个箱子看起来破破烂烂的，似乎没什么威胁)")
                current_monster['base_atk'] = 15
                current_monster['hp'] = 50
                current_monster['name'] = "朽木宝箱怪"
            else:
                print("   (直觉: 箱子缝隙里透出极度危险的血光！)")

            # 玩家选择
            choice = input("   要尝试打开它吗？(y/打开 / n/离开): ").lower()

            if choice == 'y':
                print(f"   咔嚓！箱子突然咬了过来！它是 {current_monster['name']}！")
                win = start_battle(player, current_monster, None)
            else:
                print("  你觉得小命要紧，转身离开了。")
                return True  # 直接结束本次徘徊


        elif enemy_template['name'] == "发狂的程序员":
            # 既然权重已经很难抽到了，这里给个 50% 几率真打吧，不然太没存在感了
            if random.random() < 0.5:
                print(f"   他嘴里念叨着 'Bug... Bug...' 向你冲来！")
                win = start_battle(player, enemy_template, None)
                # 检查玩家是否死亡
                if not win and player['hp'] <= 0:
                    Death_enalty()
                    return False
            else:
                print("   你看到一个秃顶的人影闪过，但似乎只是加班产生的幻觉。")
                return True

        else:
            print(f"⚔️ 遭遇战！面前冲出来一只 {enemy_template['name']}！")
            win = start_battle(player, enemy_template, None)

        # 战斗后结算 (通用)
        # 如果打输了且人死了
        if not win and player['hp'] <= 0:
            Death_enalty()
            return False

        # 如果打赢了或者没死，返回 True 继续游戏
        return True

    # 没遇到怪，捡垃圾逻辑
    elif dice < encounter_rate + 0.4:
        findable_items = ["小苹果", "力量药剂", "生锈铁剑"]
        item_name = random.choice(findable_items)
        real_item = get_item_data_by_name(item_name)

        if real_item:
            print(f"   ✨ 眼前一亮！你在树桩下发现了 [{item_name}]！")
            add_item_to_bag(player, real_item)

    # 纯路过
    else:
        if "森林" in location_name:
            flavors = [
                "🍂 踩到了枯树枝，惊起了一群乌鸦。",
                "🌲 树影婆娑，仿佛有什么东西在盯着你。",
                "🍄 你看到一朵发光的蘑菇，但没敢去碰。"
            ]
        elif "矿洞" in location_name:
            flavors = [
                "💧 滴答... 滴答... 水滴声在空旷的洞穴里回荡。",
                "⛏️ 脚下踢到了一把断掉的矿镐。",
                "🦇 头顶传来蝙蝠扑腾翅膀的声音。"
            ]
        else:
            # 通用文案
            flavors = [
                "💨 一阵风吹过，卷起了地上的尘土。",
                "👣 走了半天，好像又绕回了原地...",
                "☀️ 阳光有些刺眼，你眯起了眼睛。"
            ]

        print(f"   {random.choice(flavors)}")

    return True


if __name__ == '__main__':
    # 测试代码
    while True:
        alive = wander_action(Relo.hero)
        if not alive:
            break
        input("按回车继续徘徊...")
