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
from Characters_intro.Bag import get_item_data_by_name
from Monsters.Monsters import monsters_list
from Place.Map_A import world_map


def wander_action(player):
    # 实例化
    location_name = Relo.current_location
    # 获取原本数据
    current_location = world_map.get(location_name, {})

    print(f"\n🚶 你开始在 [{location_name}] 四处徘徊...")
    time.sleep(1)

    # 在安全区
    if current_location.get("safe_zone"):
        dice = random.random()
        if dice < 0.2:
            print("   💬 你遇到了村长，但他正在午睡。")
        elif dice < 0.4:
            print("🍀 运气不错！你在草丛里捡到了一个 [🍎 小苹果]！")
            item = get_item_data_by_name("🍎 小苹果")
            if item: player['bag'].append(item.copy())
        else:
            print("   🍃 风很喧嚣，这里一片祥和，什么也没发生。")
        return True

    # 读取当前地图的遇敌率
    encounter_rate = current_location.get("danger_level", 0)
    dice = random.random()
    print(f"开始投掷命运的骰子：{dice}")
    win = True
    if dice <= encounter_rate:
        # 随机抽怪
        enemy_template = random.choice(monsters_list)
        print(f"应召唤而来，你将面临的是{enemy_template['name']}")
        # 特殊逻辑：如果是宝箱怪和程序员（隐藏怪），让它很难遇到
        if enemy_template['name'] == "发狂的程序员":
            # 只有 1% 的概率真正触发发狂的程序员，剩下 99% 是错觉
            if random.random() < 0.01:
                win = start_battle(player, enemy_template, Relo.current_weapon)
                # 检查玩家是否死亡
                if not win and player['hp'] <= 0:
                    Death_enalty()
                    return False
            else:
                print("   👀 你感觉好像感受到了汗毛直立的怒火。")
        elif enemy_template['name'] == "宝箱怪":
            if random.random() < 0.1:
                win = start_battle(player, enemy_template, Relo.current_weapon)
                # 检查玩家是否死亡
                if not win and player['hp'] <= 0:
                    Death_enalty()
                    return False
            else:
                print("   👀 你感觉好像有东西在盯着你，但回过头什么也没有。")
            # 普通怪 (史莱姆/哥布林) 直接开打，不要犹豫！
        else:
            win = start_battle(player, enemy_template, Relo.current_weapon)
            # 检查玩家是否死亡
            if not win and player['hp'] <= 0:
                Death_enalty()
                return False
        if not win:
            return False

    elif dice < encounter_rate + 0.2:
        findable_items = ["🍎 小苹果", "💪 力量药剂", "生锈铁剑"]
        item_name = random.choice(findable_items)
        real_item = get_item_data_by_name(item_name)

        if real_item:
            print(f"   ✨ 眼前一亮！你在树桩下发现了 [{item_name}]！")
            player['bag'].append(real_item.copy())

    else:
        flavors = [
            "🍂 踩到了枯树枝，发出咔嚓的声音。",
            "💨 一阵阴风吹过，你打了个寒颤。",
            "👣 走了半天，好像又绕回了原地..."
        ]
        print(f"   {random.choice(flavors)}")

    return True


if __name__ == '__main__':
    wander_action(Relo.hero)