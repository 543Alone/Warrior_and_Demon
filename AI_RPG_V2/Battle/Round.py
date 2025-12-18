# -*- coding: UTF-8 -*-
"""
@Project ：LangGraph 
@File    ：Round.py
@IDE     ：PyCharm 
@Author  ：Write Bug
@Date    ：2025/12/8 16:56 
"""
import random

from Battle.Battle_Monster import start_battle
from Battle.Death_penalty import Death_enalty
from Characters_intro import Relo
from Characters_intro.Relo import hero
from Monsters.Monsters import monster_distribution, get_monster_by_name
from Place.Hover import wander_action
from Place.Map_A import world_map
from Save.SaveSystem import load_game, save_game
from Setting.Menu import equip_menu
from Setting.Style import Colors


# 定义战斗
# 战斗主逻辑
def main_game_loop():
    print(f"{Colors.YELLOW}=== 欢迎来到《勇士大陆》 ==={Colors.END}")

    # 游戏开始时询问是否读档
    print("1. 新的开始")
    print("2. 读取存档")
    start_choice = input("请选择: ")
    if start_choice == "2":
        if not load_game():
            print("   (将开始新游戏)")

    # 初始装备检查(防止空)
    if 'equipped_weapon' not in hero:
        equip_menu(hero)

    while True:
        # 获取当前地点的字典数据
        location_data = world_map.get(Relo.current_location)

        print(f"\n" + "-" * 30)
        print(f"📍 地点：{Colors.BLUE}{Relo.current_location}{Colors.END}")
        print(f"📝 描述：{location_data['desc']}")
        print("-" * 30)

        # 行动菜单
        print("1. 🚶 移动 (Move)")
        print("2. 💤 休息/存档 (Rest)")
        print("3. 🎒 状态与装备 (Status)")
        print("4. 🔍 在周围徘徊 (Explore)")
        print("5. 💾 保存游戏")
        if location_data.get("is_boss_room"):
            print(f"9. ⚔️ {Colors.RED}决战魔王！{Colors.END}")

        choice = input("请选择: ")

        if choice == "1":
            # 移动逻辑
            print("可以去的地方:")
            targets = location_data["connects_to"]
            for i, dest in enumerate(targets):
                print(f"{i + 1}. {dest}")

            try:
                input_val = input("输入序号 (0取消): ")
                # 兼容性处理：防止空输入报错
                if not input_val.isdigit(): continue

                idx = int(input_val) - 1
                if 0 <= idx < len(targets):
                    next_loc_name = targets[idx]
                    next_loc_data = world_map[next_loc_name]

                    print(f"🚶 正在前往 [{next_loc_name}]...")
                    Relo.current_location = next_loc_name

                    # 💀 遇敌判定逻辑 💀
                    # 只有不在安全区，且不是BOSS房时，才会在路上遇怪
                    if not next_loc_data.get("safe_zone") and not next_loc_data.get("is_boss_room"):

                        # 30% 概率半路遭袭
                        if random.random() < 0.3:
                            spawn_key = next_loc_data.get("spawn_table")

                            if spawn_key and spawn_key in monster_distribution:
                                # 1. 权重抽怪
                                spawn_config = monster_distribution[spawn_key]
                                names = list(spawn_config.keys())
                                weights = list(spawn_config.values())
                                monster_name = random.choices(names, weights=weights, k=1)[0]

                                # 2. 获取怪物数据
                                wild_enemy = get_monster_by_name(monster_name)

                                # 3. 触发战斗
                                if "宝箱" in wild_enemy['name']:
                                    print("   💨 草丛里有个箱子一闪而过，你没理会。(赶路中不处理宝箱)")
                                else:
                                    print(f"⚔️ 糟糕！你在半路遭遇了拦截！是 {wild_enemy['name']}！")

                                    # 注意：这里传 None 是因为 attack_logic 会自己去 hero 字典里找装备
                                    win = start_battle(Relo.hero, wild_enemy, None)

                                    # 4. 战败判定
                                    if not win and Relo.hero['hp'] <= 0:
                                        # 死亡惩罚，并可能被送回城
                                        Death_enalty()
                                        # 如果死了，循环继续，位置会被 Death_enalty 重置回新手村
                            else:
                                print("   (周围很安静，你安全抵达)")
                        else:
                            print(f"   ✨ 一路顺风，安全抵达 [{next_loc_name}]。")
                    else:
                        print(f"   安全抵达 [{next_loc_name}]。")

            except ValueError:
                print("输入错误")

        elif choice == "2":
            if location_data.get("safe_zone"):
                Relo.hero['hp'] = Relo.hero['max_hp']
                print(f"💤 睡得很香，HP已回满！目前HP: {Relo.hero['hp']}，并顺手保存了进度。")
            else:
                print("❌ 这里太危险了，睡着了会被怪物抬走的！(只有安全区能回血)")


        elif choice == "3":
            # --- 状态栏更新 ---
            # 从 hero 字典里取装备

            cur_w = Relo.hero['equipped_weapon']
            cur_a = Relo.hero['equipped_armor']

            current_atk = Relo.hero['base_atk'] + cur_w['atk']
            current_def = Relo.hero['def'] + cur_a['def']

            print(f"\n{Colors.CYAN}═══ 📊 {Relo.hero['name']} (Lv.{Relo.hero['level']}) ═══{Colors.END}")
            print(f"❤️ HP: {Relo.hero['hp']}/{Relo.hero['max_hp']}")
            print(f"⚔️ 攻: {current_atk} (武: {cur_w['name']})")
            print(f"🛡️ 防: {current_def} (甲: {cur_a['name']})")
            print("-" * 20)

            # 背包显示逻辑 (保持不变，省略...)
            # 这里的 equip_menu(hero) 已经适配了
            print("输入 'e' 换装备 | 'q' 返回")
            sub = input("> ")
            if sub == 'e': equip_menu(hero)
        # 徘徊遇敌
        elif choice == '4':
            # 徘徊
            wander_action(hero)
        # 保存
        elif choice == '5':
            save_game()

        # 选项 9: BOSS战
        elif choice == "9" and location_data.get("is_boss_room"):
            # Boss战
            start_battle(Relo.hero, Relo.demon, None)
