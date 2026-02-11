# -*- coding: UTF-8 -*-
"""
@Project ：LangGraph 
@File    ：Round.py
@IDE     ：PyCharm 
@Author  ：Write Bug
@Date    ：2025/12/8 16:56 
"""
import random

from Battle.Attack import GAME_CONFIG
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
from Setting.Use_items import use_item
from Setting.Shop import buy_menu, sell_menu
from Setting.Forge import forge_menu


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

    # 初始装备检查
    if 'equipped_weapon' not in hero:
        equip_menu(hero)

    while True:
        # 获取当前地点的字典数据
        location_data = world_map.get(Relo.current_location)

        print(f"\n" + "-" * 30)
        print(f" 地点：{Colors.BLUE}{Relo.current_location}{Colors.END}")
        print(f" 描述：{location_data['desc']}")
        print("-" * 30)

        # 行动菜单
        print("1.  移动 (Move)")
        print("2.  休息/存档 (Rest)")
        print("3.  状态与装备 (Status)")
        print("4.  在周围徘徊 (Explore)")
        print("5.  保存游戏")
        if location_data.get("is_boss_room"):
            print(f"9.  {Colors.RED}决战魔王！{Colors.END}")
        if Relo.current_location == "商业街":
            print("6.  访问道具店 (Buy)")
            print("7.  出售物品 (Sell)")
            print("8.  访问铁匠铺 (Forge)")
        if Relo.current_location == "村长家":
            print("10.  和村长交谈 (Talk)")

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

                    # 遇敌判定逻辑
                    # 只有不在安全区，且不是BOSS房时，才会在路上遇怪
                    if not next_loc_data.get("safe_zone") and not next_loc_data.get("is_boss_room"):

                        # 30% 概率半路遭袭
                        if random.random() < 0.3:
                            spawn_key = next_loc_data.get("spawn_table")

                            if spawn_key and spawn_key in monster_distribution:
                                # 1. 权重抽怪
                                spawn_config = monster_distribution[spawn_key]
                                monster_name = random.choices(list(spawn_config.keys()), list(spawn_config.values()))[0]
                                wild_enemy = get_monster_by_name(monster_name)

                                # 3. 触发战斗
                                if "宝箱" in wild_enemy['name']:
                                    print("    草丛里有个箱子一闪而过，你没理会。(赶路中不处理宝箱)")
                                else:
                                    print(f"️ 糟糕！你在半路遭遇了拦截！是 {wild_enemy['name']}！")

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
                            print(f"    一路顺风，安全抵达 [{next_loc_name}]。")
                    else:
                        print(f"   安全抵达 [{next_loc_name}]。")
            except:
                pass

        elif choice == "2":
            if location_data.get("safe_zone"):
                for p in Relo.party:
                    p['hp'] = p.get('max_hp', 100)
                    if 'max_mp' in p:
                        p['mp'] = p['max_mp']
                print(f" 睡得很香，全队 HP 和 MP 已回满！并顺手保存了进度。")
                save_game()
            else:
                print(" 这里太危险了，睡着了会被怪物抬走的！(只有安全区能休息)")


        elif choice == "3":
            print(f"\n{Colors.CYAN}═════════  队伍状态 ═════════{Colors.END}")
            for p in Relo.party:
                cur_w = p.get('equipped_weapon', {'name': '无', 'atk': 0})
                cur_a = p.get('equipped_armor', {'name': '无', 'def': 0, 'spd': 0.0})

                current_atk = p.get('base_atk', 10) + cur_w.get('atk', 0)
                current_def = p.get('def', 5) + cur_a.get('def', 0)

                base_spd = p.get('spd', 10)
                armor_spd_mod = cur_a.get('spd', 0.0)
                real_spd = int(base_spd * (1 + armor_spd_mod))

                if p == hero:
                    print(
                        f"🤴 英雄: {p['name']}  (Lv.{int(p.get('level', 1))}) (EXP:{p.get('exp', 0)}/{p.get('level', 1) * GAME_CONFIG['EXP_THRESHOLD_BASE']})")
                else:
                    print(f" {p.get('job', '伙伴')}: {p['name']}")

                mp_str = f" |  MP: {p['mp']}/{p['max_mp']}" if 'max_mp' in p else ""
                print(f"    HP: {p['hp']}/{p['max_hp']}{mp_str}")
                print(f"    攻: {current_atk} (武: {cur_w['name']})")
                print(f"    防: {current_def} (甲: {cur_a['name']})")
                print(f"    速: {real_spd} (基础{base_spd} | 修正 {int(armor_spd_mod * 100)}%)")
                print("-" * 20)

            print(f"{Colors.YELLOW} 背包清单:{Colors.END}")
            if not Relo.hero['bag']:
                print("   (空空如也)")
            else:
                for i, item in enumerate(Relo.hero['bag']):
                    tag = ""
                    # 简单区分一下类型显示
                    if 'atk' in item:
                        tag = f"(攻+{item['atk']})"
                    elif 'def' in item:
                        tag = f"(防+{item['def']})"
                    elif item.get('type') == 'heal':
                        tag = f"(回+{item['value']})"
                    elif item.get('type', '').startswith('buff'):
                        tag = "(Buff药)"

                    qty = item.get('quantity', 1)
                    qty_str = f" x{qty}" if qty > 1 else ""

                    print(f"   [{i}] {item['name']}{qty_str} {tag}")

            print("════════════════════════════")
            print("输入 [序号] 使用物品 | 'e' 换装备 | 'q' 返回")
            sub = input("> ")

            if sub == 'e':
                equip_menu(hero)
            elif sub.isdigit():
                # 尝试使用物品
                use_item(hero, int(sub))

        elif choice == '4':
            # 徘徊
            wander_action(hero)
        # 保存
        elif choice == '5':
            save_game()
        elif choice == 'exit'.lower():
            # 退出停止
            break

        # 选项 6, 7, 8: 商业街功能
        elif choice == '6' and Relo.current_location == "商业街":
            buy_menu(Relo.hero)
        elif choice == '7' and Relo.current_location == "商业街":
            sell_menu(Relo.hero)
        elif choice == '8' and Relo.current_location == "商业街":
            forge_menu(Relo.hero)

        # 选项 10: 村长家功能
        elif choice == '10' and Relo.current_location == "村长家":
            print("\n村长：年轻人，村子外面的史莱姆越来越多了。多去铁匠铺提升一下装备吧！")
            if Relo.hero['hp'] < Relo.hero['max_hp']:
                print("村长看你受了伤，施展了治愈术！")
                for p in Relo.party:
                    p['hp'] = p.get('max_hp', 100)
                    if 'max_mp' in p:
                        p['mp'] = p['max_mp']
                print(" 全队生命值和法力值已恢复满！")

            print("\n村长：如果你觉得一个人太危险，我这里有几位年轻人愿意追随你！")

            if len(Relo.party) > 1:
                cur_comp = Relo.party[1]
                print(f"   (你当前已经有伙伴：{cur_comp['job']}【{cur_comp['name']}】)")
                print("0.  让当前伙伴在村里休息")

            templates = [
                {"name": "莉娜", "job": "法师", "personality": "傲娇且毒舌，但内心很善良", "hp": 60, "max_hp": 60,
                 "mp": 100, "max_mp": 100, "base_atk": 25, "def": 2, "spd": 12, "buffs": [], "statuses": {},
                 "skills": ["attack", "debuff"]},
                {"name": "艾伦", "job": "牧师", "personality": "温柔体贴，总是担心勇士的安危", "hp": 80, "max_hp": 80,
                 "mp": 80, "max_mp": 80, "base_atk": 15, "def": 5, "spd": 9, "buffs": [], "statuses": {},
                 "skills": ["attack", "heal"]},
                {"name": "影", "job": "刺客", "personality": "沉默寡言，干净利落，像个冷酷的杀手", "hp": 70, "max_hp": 70,
                 "mp": 50, "max_mp": 50, "base_atk": 30, "def": 8, "spd": 18, "buffs": [], "statuses": {},
                 "skills": ["attack", "buff"]},
                {"name": "希尔瓦", "job": "精灵", "personality": "高傲优雅的游侠，箭术百发百中", "hp": 75, "max_hp": 75,
                 "mp": 80, "max_mp": 80, "base_atk": 22, "def": 4, "spd": 15, "buffs": [], "statuses": {},
                 "skills": ["attack", "shield"]}
            ]

            idx_map = {}
            opt_idx = 1
            for r in Relo.reserve_party:
                print(f"{opt_idx}. 🍻 召回休息中的【{r['job']}·{r['name']}】 (Lv.{r.get('level', 1)})")
                idx_map[str(opt_idx)] = ('reserve', r)
                opt_idx += 1

            for t in templates:
                if not any(p['name'] == t['name'] for p in Relo.party) and not any(
                        p['name'] == t['name'] for p in Relo.reserve_party):
                    print(f"{opt_idx}.  招募新人【{t['job']}·{t['name']}】")
                    idx_map[str(opt_idx)] = ('new', t)
                    opt_idx += 1

            print(f"{opt_idx}.  离开")
            recruit_choice = input("你的选择: ")

            if recruit_choice == '0' and len(Relo.party) > 1:
                removed = Relo.party.pop(1)
                Relo.reserve_party.append(removed)
                print(f" 你让 {removed['job']}【{removed['name']}】 在酒馆休息了。(装备已保留)")

            elif recruit_choice in idx_map:
                if len(Relo.party) > 1:
                    print("村长：你已经有伙伴了！如果想换人，先让当前的伙伴去休息。")
                else:
                    action_type, companion_data = idx_map[recruit_choice]
                    if action_type == 'reserve':
                        Relo.reserve_party.remove(companion_data)
                        Relo.party.append(companion_data)
                        print(f" 成功召回了老朋友 {companion_data['job']}【{companion_data['name']}】！")
                    else:
                        companion = companion_data.copy()
                        Relo.party.append(companion)
                        print(f" 成功招募了 {companion['job']}【{companion['name']}】！")


        elif choice == 'exit'.lower():
            break

        # 选项 9: BOSS战
        elif choice == "9" and location_data.get("is_boss_room"):
            print("\n你来到了魔王大殿前，面前矗立着五扇宏伟的大门：")
            print("1. 🔴 鲜血之门 (战士试炼) - 推荐挑战：战士")
            print("2. ⚫ 暗影之门 (刺客试炼) - 推荐挑战：刺客")
            print("3. 🟣 虚空之门 (法师试炼) - 推荐挑战：法师/牧师")
            print("4. 🟢 荆棘之门 (精灵试炼) - 推荐挑战：精灵")

            if len(set(Relo.defeated_bosses)) >= 4:
                print("5.  【魔王大殿】(已解锁)")
            else:
                print(f"5.  【魔王大殿】(封印中，已击杀门神: {len(set(Relo.defeated_bosses))}/4)")

            print("0.  返回")
            door_choice = input("你要推开哪扇门？")

            if door_choice == '1':
                boss = get_monster_by_name("堕落战神·阿瑞斯")
                win = start_battle(Relo.hero, boss, None)
                if win:
                    Relo.defeated_bosses.append(boss['name'])
                elif Relo.hero['hp'] <= 0:
                    Death_enalty()
            elif door_choice == '2':
                boss = get_monster_by_name("影之主宰")
                win = start_battle(Relo.hero, boss, None)
                if win:
                    Relo.defeated_bosses.append(boss['name'])
                elif Relo.hero['hp'] <= 0:
                    Death_enalty()
            elif door_choice == '3':
                boss = get_monster_by_name("深渊凝视者")
                win = start_battle(Relo.hero, boss, None)
                if win:
                    Relo.defeated_bosses.append(boss['name'])
                elif Relo.hero['hp'] <= 0:
                    Death_enalty()
            elif door_choice == '4':
                boss = get_monster_by_name("腐化神射手")
                win = start_battle(Relo.hero, boss, None)
                if win:
                    Relo.defeated_bosses.append(boss['name'])
                elif Relo.hero['hp'] <= 0:
                    Death_enalty()
            elif door_choice == '5':
                if len(set(Relo.defeated_bosses)) >= 4:
                    print("\n 勇者推开了魔王殿的大门，最终决战开始了！")
                    win = start_battle(Relo.hero, get_monster_by_name("魔王"), None)
                    if win:
                        print("\n 恭喜通关！世界恢复了和平！")
                        break
                    elif Relo.hero['hp'] <= 0:
                        Death_enalty()
                else:
                    print("\n 封印力量太强，必须击败前四扇门内的所有守卫！")
            else:
                pass
