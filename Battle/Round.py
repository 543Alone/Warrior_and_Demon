# -*- coding: UTF-8 -*-
"""
@Project ：LangGraph 
@File    ：Round.py
@IDE     ：PyCharm 
@Author  ：Write Bug
@Date    ：2025/12/8 16:56 
"""
import random

from Battle.Battle_Monster import start_battle, GAME_CONFIG
from Characters_intro import Relo
from Characters_intro.Relo import hero, demon, current_weapon, current_armor
from Monsters.Monsters import monsters_list
from Place.Map_A import world_map
from Setting.Menu import equip_menu
from Setting.Style import Colors
from Place.Hover import wander_action
from Battle.Death_penalty import Death_enalty
from Setting.Use_items import use_item


# 定义战斗
# 战斗主逻辑
def main_game_loop():
    print(f"{Colors.YELLOW}=== 欢迎来到《勇士大陆》 ==={Colors.END}")

    # 游戏开始前先选一次装备
    equip_menu(Relo.hero)

    while True:
        # 获取当前地点的字典数据
        location_data = world_map.get(Relo.current_location)

        print(f"\n" + "-" * 30)
        print(f"📍 地点：{Colors.BLUE}{Relo.current_location}{Colors.END}")
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
            # 注意：这里要用 location_data，不能用 world_map直接取
            targets = location_data["connects_to"]
            for i, dest in enumerate(targets):
                print(f"{i + 1}. {dest}")

            try:
                idx = int(input("输入序号: ")) - 1
                if 0 <= idx < len(targets):
                    next_loc_name = targets[idx]
                    next_loc_data = world_map[next_loc_name]

                    # 移动成功
                    Relo.current_location = next_loc_name

                    # 遇敌判定 (不在安全区 且 不是BOSS房)
                    if not next_loc_data.get("safe_zone") and not next_loc_data.get("is_boss_room"):
                        # 假设 50% 概率遇怪
                        if random.random() < 0.4:
                            # 随机抽一个小怪
                            wild_enemy = random.choice(monsters_list)
                            # 触发战斗
                            if wild_enemy['name'] == "发狂的程序员":
                                if random.random() < 0.01:
                                    win = start_battle(hero, wild_enemy)
                                    if not win and hero['hp'] == 0:
                                        Death_enalty()
                                else:
                                    print("   👀 你感觉好像感受到了汗毛直立的怒火。")
                            elif wild_enemy['name'] == "宝箱怪":
                                if random.random() < 0.1:
                                    win = start_battle(hero, wild_enemy)
                                    if not win and hero['hp'] == 0:
                                        Death_enalty()
                                else:
                                    print("   👀 你感觉好像有东西在盯着你，但回过头什么也没有。")
            except ValueError:
                print("输入错误")

        elif choice == "2":
            if location_data.get("safe_zone"):
                Relo.hero['hp'] = Relo.hero['max_hp']
                print("💤 睡得很香，HP已回满！")
            else:
                print("❌ 野外睡觉会被狼叼走的！")


        elif choice == "3":
            while True:  # 创建一个新的循环来处理背包界面
                print(f"\n{Colors.CYAN}═════════ 📊 角色状态 ═════════{Colors.END}")
                print(
                    f"🤴 英雄: {Relo.hero['name']}  (Lv.{int(Relo.hero['level'])})  (Exp:{int(Relo.hero['exp'])}/{Relo.hero['level'] * GAME_CONFIG["EXP_THRESHOLD_BASE"]})")
                print(f"❤️ 血量: {Colors.RED}{Relo.hero['hp']}/{Relo.hero['max_hp']}{Colors.END}")
                print(
                    f"🗡️ 攻击: {Relo.hero['base_atk'] + Relo.current_weapon['atk']} (基础{Relo.hero['base_atk']} + 武器{Relo.current_weapon['atk']})")
                print(
                    f"🛡️ 防御: {Relo.hero['def'] + Relo.current_armor['def']} (基础{Relo.hero.get('def', 0)} + 防具{Relo.current_armor['def']})")
                print()
                print("-" * 30)
                print(f"当前装备: [{Relo.current_weapon['name']}] & [{Relo.current_armor['name']}]")
                print(f"\n{Colors.YELLOW}🎒 背包清单:{Colors.END}")
                if not Relo.hero['bag']:
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

                    display_list = list(stacked_bag.keys())

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
                print("输入 [序号] 使用物品 | 'e' 换装备 | 'q' 返回")

                sub_choice = input("你的选择: ")

                if sub_choice == 'q':
                    break

                elif sub_choice == 'e':
                    equip_menu(hero)

                elif sub_choice.isdigit():
                    idx = int(sub_choice) - 1  # 修正：用户输入从1开始，转换为从0开始的索引

                    if 0 <= idx < len(display_list):
                        # 获取玩家选的名字
                        target_name = display_list[idx]

                        real_index = -1
                        for bag_i, item in enumerate(hero['bag']):
                            if item['name'] == target_name:
                                real_index = bag_i
                                break  # 找到一个就停，只吃一个

                        if real_index != -1:
                            use_item(hero, real_index)
                            # 使用完后循环会继续，重新统计堆叠数量，所以显示会自动更新
                        else:
                            print("❌ 发生奇怪的错误：找不到物品。")
                    else:
                        print("❌ 输入的序号不对。")
                else:
                    print("输入无效")
        elif choice == '4':
            is_alive = wander_action(hero)
            if not is_alive and hero['hp'] == 0:
                Death_enalty()

        elif choice == "9" and location_data.get("is_boss_room"):
            print("勇者推开了魔王殿的大门...")
            win = start_battle(Relo.hero, Relo.demon, Relo.current_weapon)
            if win:
                print("🏆 恭喜通关！！")
                break
            else:
                break