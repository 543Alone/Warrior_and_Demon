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

from Battle.Attack import attack_logic
from Characters_intro.Bag import get_item_data_by_name, add_item_to_bag
from Model.AI_Narrator import narrate_battle, generate_monster_intro
from Setting.Abnormal_condition import StatusSystem
from Setting.Level import check_level_up
from Setting.Style import Colors, show_health_bar
from Setting.Use_items import use_item


# 定义战斗
def start_battle(player, enemy_template, current_weapon):
    # 复制敌人数据
    print(f"\n" + "!" * 30)
    enemy = enemy_template.copy()

    # 确保双方都有 status 字段
    if 'statuses' not in player: player['statuses'] = {}
    if 'statuses' not in enemy: enemy['statuses'] = {}

    # 确保怪物有 SPD，如果没有默认为 10
    if 'spd' not in enemy: enemy['spd'] = 10

    # 怪物登场
    print(f"⚠️  遭遇战！一只 {Colors.RED}{enemy['name']}{Colors.END} (SPD: {enemy['spd']}) 出现了！")

    # AI 生成挑衅台词
    try:
        generate_monster_intro(enemy['name'])
    except:
        print(f"👿 {enemy['name']}: 吼！！！")

    print("!" * 30)

    turn = 1
    while player['hp'] > 0 and enemy['hp'] > 0:
        print(f"\n═══════ Round {turn} ═══════")
        show_health_bar(player)
        show_health_bar(enemy)

        # 速度判定
        p_spd = player.get('spd', 10)
        e_spd = enemy.get('spd', 10)

        # 判断谁先手 (玩家速度 >= 怪物速度 则玩家先手)
        player_first = p_spd >= e_spd

        # --- 玩家菜单 ---
        print(f"\n{Colors.CYAN}[你的回合] 请选择行动：{Colors.END}")
        print("1.⚔️ 攻击(Attack)  2.🎒 物品(Item)  3.🏃 逃跑(Flee)")

        action = input("你的选择 (1-3): ")

        player_acted = False  # 标记玩家是否有效消耗了回合

        # =================================================
        # CASE A: 怪物比你快 (且你要打架)，怪物先手！
        # =================================================
        if not player_first and action in ['1', '2']:
            print(f"\n⚡ {enemy['name']} 动作比你快，抢先发动攻击！")
            time.sleep(0.5)

            # 怪物先动前，检查控制
            is_skip, msg = StatusSystem.check_control(enemy)
            if is_skip:
                print(f"   {msg} (跳过攻击)")
            else:
                # 2. 怪物攻击
                enemy_logs = attack_logic(enemy, player, weapons=None)
                # 3. AI 播报
                narrate_battle(enemy_logs, player, enemy)

            # 检查玩家是否阵亡
            if player['hp'] <= 0:
                print(f"\n☠️ 你在敌人的快攻下倒下了...")
                return False

        # =================================================
        # CASE B: 玩家行动阶段
        # =================================================

        # --- 选项 1: 攻击 ---
        if action == "1":
            # 玩家动前，检查控制 (如果有的话)
            is_skip, msg = StatusSystem.check_control(player)
            if is_skip:
                print(f"   {msg} (无法行动)")
            else:
                # 2. 玩家攻击
                logs = attack_logic(player, enemy, current_weapon)
                # 3. AI 播报
                narrate_battle(logs, player, enemy)

            player_acted = True

        # --- 选项 2: 使用物品 ---
        elif action == "2":
            # 显示 Buff 状态
            if 'buffs' in player and player['buffs']:
                print(f"\n✨ 当前激活的状态 (Buffs):")
                for buff in player['buffs']:
                    # 显示名称、数值和剩余回合
                    # 比如：力量药剂: +10 (剩余 3 回合)
                    print(f"   🔥 {buff['name']}: +{buff.get('value', 0)} (剩余 {buff['duration']} 回合)")
            else:
                print(f"\n✨ 当前无增益状态")

            if not player.get('bag'):
                print("   (背包空空如也，浪费了一次查看机会)")
            else:
                # 列出背包
                print("\n🎒 战斗背包:")
                for i, item in enumerate(player['bag']):
                    tag = ""
                    if item.get('type') == 'heal':
                        tag = "(可食用)"
                    elif item.get('type', '').startswith('buff'):
                        tag = "(Buff药)"
                    qty = item.get('quantity', 1)
                    # 如果数量大于 1，就显示 xN，否则不显示
                    qty_str = f" x{qty}" if qty > 1 else ""

                    # 把 qty_str 加到 print 里
                    print(f"   [{i}] {item['name']}{qty_str} {tag}")

                print("输入序号使用 (输入其他取消):")
                try:
                    idx = int(input("> "))
                    # 调用 use_item，如果返回 True，说明真的吃了，消耗回合
                    if use_item(player, idx, enemy=enemy):
                        player_acted = True  # 成功使用了才算行动
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
            # 简单算法：或者可以用 p_spd / e_spd 计算概率
            escape_rate = 0.5
            if p_spd > e_spd: escape_rate = 0.8  # 比它快容易跑
            print(f"💨 {Colors.GREEN}逃跑成功！你溜之大吉。{Colors.END}")

            if random.random() < escape_rate:
                print(f"💨 {Colors.GREEN}逃跑成功！你利用速度优势溜了。{Colors.END}")
                return True
            else:
                print(f"🚫 {Colors.RED}逃跑失败！被 {enemy['name']} 拦住了！{Colors.END}")
                player_acted = True  # 逃跑失败也算行动过，会挨打

        # --- 无效输入 ---
        else:
            print("❌ 无效的指令，请重新输入。")
            continue  # 跳过本次循环，重新选择

        # =================================================
        # 胜利判定 (玩家行动后)
        # =================================================
        if enemy['hp'] <= 0:
            print(f"\n🎉 胜利！打败了 {enemy['name']}！")
            exp_gain = enemy.get('exp', 0)
            player['exp'] += exp_gain
            print(f"   获得经验: {exp_gain}")

            # 升级
            check_level_up(player)

            # print(f"恭喜升级~，目前等级为 {player['level']}")

            # 掉落逻辑
            loot_list = enemy.get('loot', [])
            dropped_items = []

            # 1. 正常随机掉落
            for loot in loot_list:
                # 幸运加成：也就是你可以给 player 加一个 luck 属性，这里先简单处理
                # 比如：BOSS 战掉落率翻倍
                chance_multiplier = 1.0
                if enemy['max_hp'] >= 500:  # 简单的 BOSS 判定
                    chance_multiplier = 1.5

                if random.random() < (loot['chance'] * chance_multiplier):
                    dropped_items.append(loot['item'])

            # 2. 保底机制 (Bad Luck Protection)
            # 如果什么都没掉，且怪物有掉落列表
            if not dropped_items and loot_list:
                if random.random() < 0.5:
                    # 假设 loot_list 是按稀有度排的，那我们可能要取 chance 最大的
                    best_chance_item = max(loot_list, key=lambda x: x['chance'])
                    print(f"   (保底触发) 运气不好，但你还是在尸体上翻到了点东西...")
                    dropped_items.append(best_chance_item['item'])

            # 3. 结算进背包
            for item_name in dropped_items:
                real_item = get_item_data_by_name(item_name)
                if real_item:
                    print(f"   🎁 战利品！发现了 [{item_name}]")
                    add_item_to_bag(player, real_item)

            # 战斗结束清理状态
            StatusSystem.clear_status(player)
            return True

        # =================================================
        # CASE C: 怪物行动阶段 (后手)
        # 如果玩家先动了，且怪物还没死，且怪物这回合还没动过(即非先手)
        # =================================================
        if player_first and player_acted:
            print(f"\n{Colors.RED}[敌方回合]{Colors.END}")
            time.sleep(0.5)

            # 1. 检查控制
            is_skip, msg = StatusSystem.check_control(enemy)
            if is_skip:
                print(f"   {msg} (跳过攻击)")
            else:
                # 2. 怪物攻击
                enemy_logs = attack_logic(enemy, player, weapons=None)
                # 3. AI 播报
                narrate_battle(enemy_logs, player, enemy)

            if player['hp'] <= 0:
                print(f"\n☠️ 胜败乃兵家常事...")
                return False

        # =================================================
        # 回合结束结算阶段 (Turn End Phase)
        # =================================================
        print(f"\n--- 回合结算 ---")

        # 1. 结算异常状态 (燃烧、中毒、HOT)
        p_logs = StatusSystem.resolve_turn_end(player)
        for l in p_logs: print(f"   (你) {l}")

        e_logs = StatusSystem.resolve_turn_end(enemy)
        for l in e_logs: print(f"   (敌) {l}")

        # 2. 结算 Buff 持续时间 (力量药剂等)
        if 'buffs' in player and player['buffs']:
            for buff in player['buffs'][:]:  # 切片复制遍历，防止删除出错
                buff['duration'] -= 1
                if buff['duration'] <= 0:
                    print(f"   📉 [{buff['name']}] 的效果消失了。")
                    player['buffs'].remove(buff)

        # 3. 再次检查死亡 (因为可能被烧死/毒死)
        if player['hp'] <= 0:
            print(f"\n☠️ 你倒在了异常状态的折磨下...")
            return False

        if enemy['hp'] <= 0:
            print(f"\n🎉 {enemy['name']} 痛苦地倒下了！(异常状态击杀)")
            # 这里简单处理，如果毒死也给经验，逻辑同上
            player['exp'] += enemy.get('exp', 0)
            check_level_up(player)
            # 掉落略...
            return True

        turn += 1
