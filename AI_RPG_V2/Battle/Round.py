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
from Characters_intro.Relo import hero
from Monsters.Monsters import monsters_list, monster_distribution, get_monster_by_name
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
        print("1. 🚶 移动 (Move)")
        print("2. 💤 休息 (Rest)")
        print("3. 🎒 状态与装备 (Status)")
        print("4. 🔍 在周围徘徊 (Explore)")
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
                input_val = input("输入序号 (输入 0 或其他取消): ")
                if not input_val.isdigit(): continue

                idx = int(input_val) - 1
                if 0 <= idx < len(targets):
                    next_loc_name = targets[idx]
                    next_loc_data = world_map[next_loc_name]

                    # 移动成功
                    print(f"🚶 正在前往 [{next_loc_name}]...")
                    Relo.current_location = next_loc_name

                    # 遇敌判定 (不在安全区 且 不是BOSS房)
                    if not next_loc_data.get("safe_zone") and not next_loc_data.get("is_boss_room"):

                        # 30% 概率在半路被拦截 (移动遇敌率可以设低一点)
                        if random.random() < 0.3:
                            spawn_key = next_loc_data.get("spawn_table")

                            if spawn_key and spawn_key in monster_distribution:
                                spawn_config = monster_distribution[spawn_key]
                                names = list(spawn_config.keys())
                                weights = list(spawn_config.values())

                                # 抽怪
                                monster_name = random.choices(names, weights=weights, k=1)[0]
                                wild_enemy = get_monster_by_name(monster_name)

                                # 因为半路突然出现个宝箱让你选有点怪，简化处理，直接打普通怪
                                if "宝箱怪" in wild_enemy['name'] or "程序员" in wild_enemy['name']:
                                    print("   💨 草丛里有什么东西一闪而过，你没看清。")
                                else:
                                    print(f"⚔️ 糟糕！你在半路遭遇了拦截！是 {wild_enemy['name']}！")
                                    # 修正：必须传入 current_weapon
                                    win = start_battle(hero, wild_enemy, Relo.current_weapon)

                                    if not win and hero['hp'] <= 0:
                                        Death_enalty()
                                        # 复活后通常会回城，这里continue重新循环即可
                            else:
                                print("   (周围很安静，你安全抵达)")
                    else:
                        print(f"   安全抵达 [{next_loc_name}]。")

            except ValueError:
                print("输入错误")

        elif choice == "2":
            if location_data.get("safe_zone"):
                Relo.hero['hp'] = Relo.hero['max_hp']
                print(f"💤 睡得很香，HP已回满！目前HP: {Relo.hero['hp']}")
            else:
                print("❌ 这里太危险了，睡着了会被怪物抬走的！(只有安全区能回血)")


        elif choice == "3":
            while True:
                # 重新计算一下面板，防止装备更换后显示不同步
                current_atk = Relo.hero['base_atk'] + Relo.current_weapon['atk']
                current_def = Relo.hero['def'] + Relo.current_armor['def']

                print(f"\n{Colors.CYAN}═════════ 📊 角色状态 ═════════{Colors.END}")
                print(f"🤴 英雄: {Relo.hero['name']}  (Lv.{int(Relo.hero['level'])})  (Exp:{int(Relo.hero['exp'])}/{Relo.hero['level'] * GAME_CONFIG["EXP_THRESHOLD_BASE"]})")
                print(f"❤️ 血量: {Colors.RED}{Relo.hero['hp']}/{Relo.hero['max_hp']}{Colors.END}")
                print(f"🗡️ 攻击: {current_atk} (基础{Relo.hero['base_atk']} + 武器{Relo.current_weapon['atk']})")
                print(f"🛡️ 防御: {current_def} (基础{Relo.hero['def']} + 防具{Relo.current_armor['def']})")
                print("-" * 30)
                # 增加颜色显示
                print(f"当前武器: {Relo.current_weapon['name']}")
                print(f"当前护甲: {Relo.current_armor['name']}")

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

                        # 简单的类型判断图标
                        icon = "📦"
                        val_str = ""
                        if 'atk' in item_data:
                            icon = "⚔️";
                            val_str = f"(攻+{item_data['atk']})"
                        elif 'def' in item_data:
                            icon = "🛡️";
                            val_str = f"(防+{item_data['def']})"
                        elif item_data.get('type') == 'heal':
                            icon = "🧪";
                            val_str = f"(回+{item_data['value']})"

                        print(f"   [{index}] {icon} {name} {val_str}{count_str}")
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
                            print("❌ 错误: 物品不存在")
                    else:
                        print("❌ 序号无效")

        elif choice == '4':
            # 直接调用我们刚才修好的 Hover 逻辑
            # Hover 里已经包含了权重判断、宝箱怪削弱、死亡惩罚等所有逻辑
            is_alive = wander_action(hero)

            # Hover 内部已经处理了 Death_enalty，这里只需要判断如果死了退出循环或者怎么处理
            # 其实 wander_action 里的 Death_enalty 执行完后，玩家血量还是0，
            # 下一次循环 location 可能变回新手村了

        # 选项 9: BOSS战
        elif choice == "9" and location_data.get("is_boss_room"):
            print(f"\n{Colors.RED}🔥 警告：你即将面对最终的恐惧...{Colors.END}")
            confirm = input("确定要挑战吗？(y/n): ")
            if confirm.lower() == 'y':
                print("勇者推开了魔王殿的大门...")
                # 这里的 Relo.demon 建议也用 get_monster_by_name 获取，或者你之前定义好的
                win = start_battle(Relo.hero, Relo.demon, Relo.current_weapon)
                if win:
                    print("🏆 恭喜通关！！游戏结束。")
                    break
            else:
                print("你怂了，退回了门口。")
