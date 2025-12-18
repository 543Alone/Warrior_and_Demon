# -*- coding: UTF-8 -*-
"""
@Project ：LangGraph 
@File    ：Battle_Monster.py
@IDE     ：PyCharm 
@Author  ：Write Bug
@Date    ：2025/12/10 15:33 
"""
import random
import time

from langchain_core.messages import HumanMessage

from AI_RPG_V2.Model.AI_Narrator import narrate_battle, llm
from Battle.Attack import attack_logic, GAME_CONFIG
from Characters_intro.Bag import get_item_data_by_name, add_item_to_bag
from Setting.Style import Colors, show_health_bar
from Setting.Level import check_level_up
from Setting.Abnormal_condition import process_damage
from Setting.Use_items import use_item

def get_monster_intro(monster_name):
    """让 LLM 生成怪物开场白"""
    prompt = f"你是一只【{monster_name}】。玩家遇到了你，请你用凶狠或搞笑的语气说一句开场白（20字以内）。"
    return "（LLM生成的开场白）"

# 定义战斗
def start_battle(player, enemy_template, current_weapon):
    # 复制敌人数据
    print(f"\n" + "!" * 30)
    enemy = enemy_template.copy()
    print(f"⚠️  遭遇战！一只 {Colors.RED}{enemy['name']}{Colors.END} 出现了！")
    intro_text = llm.invoke([HumanMessage(content=f"你扮演一只{enemy['name']}，对勇者说一句只有20字的挑衅台词。")])
    print(f"👿 {enemy['name']}: “{intro_text.content}”")
    print("!" * 30)

    turn = 1
    while player['hp'] > 0 and enemy['hp'] > 0:
        print(f"\n═══════ Round {turn} ═══════")
        show_health_bar(player)
        show_health_bar(enemy)

        print(f"\n{Colors.CYAN}[你的回合] 请选择行动：{Colors.END}")
        print("1. ⚔️ 攻击 (Attack)")
        print("2. 🎒 物品 (Item)")
        print("3. 🏃 逃跑 (Flee)")

        action = input("你的选择 (1-3): ")

        player_acted = False  # 标记玩家是否采取了有效行动

        # --- 选项 1: 攻击 ---
        if action == "1":
            logs = attack_logic(player, enemy, current_weapon)
            # print(f"\n[系统日志]:\n{logs}")
            # 调用AI
            story = narrate_battle(logs)
            # 保留原始数据供调试
            # print(f"[系统原始数据]:\n{logs}")
            player_acted = True

        # --- 选项 2: 使用物品 ---
        elif action == "2":
            # 查看当前持续的Buff
            if 'buffs' in player and player['buffs']:
                print(f"\n✨ 当前激活的状态 (Buffs):")
                for buff in player['buffs']:
                    # 显示名称、数值和剩余回合
                    # 比如：力量药剂: +10 (剩余 3 回合)
                    print(f"   🔥 {buff['name']}: +{buff.get('value', 0)} (剩余 {buff['duration']} 回合)")
            else:
                print(f"\n✨ 当前无增益状态")
            if not player['bag']:
                print("   (背包空空如也，浪费了一次查看机会)")
            else:
                # 简单列出背包
                print("\n🎒 战斗背包:")
                for i, item in enumerate(player['bag']):
                    tag = ""
                    if item.get('type') == 'heal':
                        tag = "(可食用)"
                    elif item.get('type', '').startswith('buff'):
                        tag = "(Buff药)"
                    print(f"   [{i}] {item['name']} {tag}")

                    qty = item.get('quantity', 1)
                    # 如果数量大于 1，就显示 xN，否则不显示
                    qty_str = f" x{qty}" if qty > 1 else ""

                    # 把 qty_str 加到 print 里
                    print(f"   [{i}] {item['name']}{qty_str} {tag}")

                print("输入序号使用 (输入其他取消):")
                try:
                    idx = int(input("> "))
                    # 调用 use_item，如果返回 True，说明真的吃了，消耗回合
                    if use_item(player, idx):
                        player_acted = True
                    else:
                        print("   (你放下了背包，准备继续战斗)")
                        # 没吃药，continue回到循环开头，不进入怪物回合
                        continue
                except:
                    print("   (取消操作)")
                    continue

        # --- 选项 3: 逃跑 ---
        elif action == "3":
            # 简单的逃跑算法：50% 概率
            # 进阶版：比较 player['SPD'] 和 enemy['SPD']
            print("Trying to run away...")
            time.sleep(0.5)
            if random.random() < 0.5:
                print(f"💨 {Colors.GREEN}逃跑成功！你溜之大吉。{Colors.END}")
                return True  # 逃跑算作存活，返回 True
            else:
                print(f"🚫 {Colors.RED}逃跑失败！被 {enemy['name']} 拦住了！{Colors.END}")
                player_acted = True  # 逃跑失败也算行动过，会挨打

        # --- 无效输入 ---
        else:
            print("❌ 无效的指令，请重新输入。")
            continue  # 跳过本次循环，重新选择

        # 如果怪物死了，不用等它反击，直接胜利
        if enemy['hp'] <= 0:
            print(f"\n🎉 胜利！打败了 {enemy['name']}！")
            player['exp'] += enemy.get('exp', 0)
            print(f"   获得经验: {enemy.get('exp', 0)}")

            # 升级
            check_level_up(player)

            # print(f"恭喜升级~，目前等级为 {player['level']}")

            # 掉落逻辑
            for loot in enemy.get('loot', []):
                if random.random() < loot['chance']:
                    item_name = loot['item']
                    real_item = get_item_data_by_name(item_name)
                    if real_item:
                        print(f"   🎁 哇！掉落了 [{item_name}]")
                        add_item_to_bag(player, real_item)
            return True


        # --- 怪物回合 ---
        if player_acted:
            print(f"\n{Colors.RED}[敌方回合]{Colors.END}")
            time.sleep(GAME_CONFIG["TEXT_SPEED"])

            # 结算玩家的 Buff 持续时间 (放在这里结算)
            if 'buffs' in player:
                for buff in player['buffs'][:]:
                    buff['duration'] -= 1
                    if buff['duration'] <= 0:
                        print(f"   📉 你的 [{buff['name']}] 效果结束了。")
                        player['buffs'].remove(buff)

        # 怪物攻击
        enemy_logs = attack_logic(enemy, player, weapons=None)  # 怪物不用武器

        if enemy_logs:  # 确保有日志
            enemy_story = narrate_battle(enemy_logs)

        # 结算燃烧伤害
        process_damage(enemy)

        if player['hp'] <= 0:
            print(f"\n☠️ 胜败乃兵家常事... 大侠请重新来过。")
            return False

        turn += 1
