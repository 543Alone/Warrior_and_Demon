# -*- coding: UTF-8 -*-
import random
import time

from Battle.Attack import attack_logic
from Characters_intro import Relo
from Characters_intro.Bag import get_item_data_by_name, add_item_to_bag
from Model.AI_Narrator import narrate_battle, generate_monster_intro
from Model.AI_Companion import get_companion_action
from Setting.Abnormal_condition import StatusSystem
from Setting.Level import check_level_up
from Setting.Style import Colors, show_health_bar
from Setting.Use_items import use_item


def start_battle(player, enemy_template, current_weapon):
    print(f"\n" + "!" * 30)
    enemy = enemy_template.copy()

    # 初始化状态
    if 'statuses' not in enemy: enemy['statuses'] = {}
    if 'spd' not in enemy: enemy['spd'] = 10

    for p in Relo.party:
        if 'statuses' not in p: p['statuses'] = {}

    print(f"  遭遇战！一只 {Colors.RED}{enemy['name']}{Colors.END} (SPD: {enemy['spd']}) 出现了！")

    try:
        generate_monster_intro(enemy['name'])
    except:
        print(f"👿 {enemy['name']}: 吼！！！")

    print("!" * 30)

    turn = 1
    # 战斗循环条件：队伍里有人存活，且敌人存活
    while any(p['hp'] > 0 for p in Relo.party) and enemy['hp'] > 0:
        print(f"\n═══════ Round {turn} ═══════")

        # 排序行动队列（按速度降序）
        combatants = [p for p in Relo.party if p['hp'] > 0] + [enemy]
        combatants.sort(key=lambda x: x.get('spd', 10), reverse=True)

        # 显示血条
        for c in combatants:
            show_health_bar(c)

        for actor in combatants:
            # 在队列中可能已经死了
            if actor['hp'] <= 0 or enemy['hp'] <= 0:
                continue

            # 检查控制状态
            is_skip, msg = StatusSystem.check_control(actor)
            if is_skip:
                print(f"\n⚡ {actor['name']} 回合:")
                print(f"   {msg} (跳过行动)")
                continue

            if actor == Relo.hero:
                # 勇士回合（手动输入）
                print(f"\n{Colors.CYAN}[你的回合] 请选择行动：{Colors.END}")
                while True:
                    available_skills = ["attack", "flee", "item"]
                    if Relo.hero.get('equipped_weapon') and 'weapon_skill' in Relo.hero['equipped_weapon']:
                        available_skills.insert(1, Relo.hero['equipped_weapon']['weapon_skill'])

                    skill_str_list = []
                    for i, sk in enumerate(available_skills):
                        skill_str_list.append(f"{i + 1}. {sk}")

                    skill_menu = "  ".join(skill_str_list)
                    print(f"你的行动:  {skill_menu}")
                    cmd = input("> ")

                    # 根据可用的序号来解析
                    action = "attack"
                    if cmd.isdigit():
                        idx = int(cmd) - 1
                        if 0 <= idx < len(available_skills):
                            action = available_skills[idx]

                    if action == "flee":
                        escape_rate = 0.5
                        if actor.get('spd', 10) > enemy.get('spd', 10): escape_rate = 0.8
                        if random.random() < escape_rate:
                            print(f"💨 {Colors.GREEN}逃跑成功！你溜之大吉。{Colors.END}")
                            return True
                        else:
                            print(f" {Colors.RED}逃跑失败！被拦住了！{Colors.END}")
                            break
                    elif action == "item":
                        # ====== 使用物品逻辑 ======
                        print(" 选择你要使用的物品 (输入序号，返回按 q):")
                        for i, item in enumerate(Relo.hero.get('bag', [])):
                            print(f"  [{i}] {item['name']}")
                        item_cmd = input("> ")
                        if item_cmd.isdigit():
                            if use_item(Relo.hero, int(item_cmd), enemy=enemy):
                                break
                        else:
                            continue
                    else:
                        # 武器专属技能或者普通攻击
                        if action == "ragnarok" and Relo.hero.get('mp', 0) >= 40:
                            Relo.hero['mp'] -= 40
                            print("   ☄️ 诸神的黄昏降临，毁天灭地的一击！")
                            original_atk = Relo.hero['base_atk']
                            Relo.hero['base_atk'] *= 2.5
                            logs = attack_logic(Relo.hero, enemy, weapons=current_weapon)
                            Relo.hero['base_atk'] = original_atk
                            narrate_battle(logs, Relo.hero, enemy)
                            break
                        elif action == "shadow_strike" and Relo.hero.get('mp', 0) >= 20:
                            Relo.hero['mp'] -= 20
                            print("    遁入暗影，一击必杀！")
                            if 'buffs' not in Relo.hero: Relo.hero['buffs'] = []
                            Relo.hero['buffs'].append(
                                {'type': 'crit_rate', 'name': '必定暴击', 'value': 1.0, 'duration': 1})
                            logs = attack_logic(Relo.hero, enemy, weapons=current_weapon)
                            narrate_battle(logs, Relo.hero, enemy)
                            break
                        elif action == "holy_light" and Relo.hero.get('mp', 0) >= 50:
                            Relo.hero['mp'] -= 50
                            print("    大天使之杖闪耀，降下神圣之光！")
                            for p in [x for x in Relo.party if x['hp'] > 0]:
                                heal = 150
                                p['hp'] = min(p.get('max_hp', 100), p['hp'] + heal)
                                print(f"    {p['name']} 恢复了 {heal} 点生命值！")
                            break
                        elif action == "wind_arrow" and Relo.hero.get('mp', 0) >= 30:
                            Relo.hero['mp'] -= 30
                            print("    穿风神弓拉满，箭矢如狂风暴雨！")
                            hits = random.randint(2, 3)
                            for i in range(hits):
                                logs = attack_logic(Relo.hero, enemy, weapons=current_weapon)
                                narrate_battle(logs, Relo.hero, enemy)
                                if enemy['hp'] <= 0: break
                            break
                        else:
                            if action != "attack":
                                if Relo.hero.get('mp', 0) >= 20:
                                    Relo.hero['mp'] -= 20
                                    print(f" 勇士释放了武器专属技能：【{action}】！")
                                else:
                                    print(f" MP不足，只能进行普通攻击！")
                                    action = "attack"

                            logs = attack_logic(Relo.hero, enemy,
                                                current_weapon if action == "attack" else current_weapon)
                            narrate_battle(logs, Relo.hero, enemy)
                            break

            elif actor in Relo.party:
                # AI 伙伴回合
                print(f"\n{Colors.PURPLE}[{actor['name']} 的回合]{Colors.END}")
                decision = get_companion_action(actor, Relo.party, enemy)
                act = decision.get('action')
                target_name = decision.get('target_name', enemy['name'])

                # MP 检查 (如果释放了非普通攻击技能，消耗 20 MP)
                if act != 'attack':
                    if actor.get('mp', 0) >= 20:
                        actor['mp'] -= 20
                    else:
                        print(f"   ( MP不足，{actor['name']} 改为普通攻击！)")
                        act = "attack"

                # 寻找目标对象
                target = None
                if target_name == enemy['name']:
                    target = enemy
                else:
                    for p in Relo.party:
                        if p['name'] == target_name: target = p
                if not target: target = enemy  # 默认找敌人

                if act == "attack":
                    logs = attack_logic(actor, enemy, weapons=None)
                    narrate_battle(logs, actor, enemy)
                elif act == "heal":
                    heal_amt = int(actor.get('base_atk', 20) * 1.5)
                    target['hp'] = min(target.get('max_hp', 100), target['hp'] + heal_amt)
                    print(f"    {actor['name']} 施展了治愈术，{target['name']} 恢复了 {heal_amt} 点 HP！")
                elif act == "buff":
                    print(f"    {actor['name']} 释放了增益魔法！")
                    if 'buffs' not in target: target['buffs'] = []
                    # 刺客给队友加暴击、速度
                    target['buffs'].append({"type": "crit_rate", "name": "迅捷指令", "value": 0.2, "duration": 3})
                    target['buffs'].append({"type": "spd", "name": "迅捷指令", "value": 0.5, "duration": 3})
                    print(f"    {target['name']} 的速度和暴击率提升了！")
                elif act == "debuff":
                    print(f"    {actor['name']} 对 {enemy['name']} 施放了破甲诅咒！防御下降！")
                    if 'buffs' not in enemy: enemy['buffs'] = []
                    enemy['buffs'].append({'name': '破甲诅咒', 'type': 'def', 'value': -10, 'duration': 3})
                elif act == "shield":
                    if 'buffs' not in target: target['buffs'] = []
                    target['buffs'].append({'name': '自然护盾', 'type': 'def', 'value': 20, 'duration': 3})
                    target['buffs'].append({'name': '精灵庇护', 'type': 'def_percent', 'value': 0.5, 'duration': 3})
                    print(f"    {actor['name']} 为 {target['name']} 施加了【自然护盾】！防御大幅提升！")
                else:
                    wep = actor.get('equipped_weapon')
                    if act not in ["attack", "heal", "buff", "debuff", "shield"]:
                        print(f"    {actor['name']} 释放了武器绝技：【{act}】！")

                        if act == "ragnarok" and actor.get('mp', 0) >= 40:
                            actor['mp'] -= 40
                            print("    诸神的黄昏降临，毁天灭地的一击！")
                            # 增加临时攻击力
                            original_atk = actor['base_atk']
                            actor['base_atk'] *= 2.5
                            logs = attack_logic(actor, enemy, weapons=wep)
                            actor['base_atk'] = original_atk
                            narrate_battle(logs, actor, enemy)

                        elif act == "shadow_strike" and actor.get('mp', 0) >= 20:
                            actor['mp'] -= 20
                            print("    遁入暗影，一击必杀！")
                            if 'buffs' not in actor: actor['buffs'] = []
                            actor['buffs'].append(
                                {'type': 'crit_rate', 'name': '必定暴击', 'value': 1.0, 'duration': 1})
                            logs = attack_logic(actor, enemy, weapons=wep)
                            narrate_battle(logs, actor, enemy)

                        elif act == "holy_light" and actor.get('mp', 0) >= 50:
                            actor['mp'] -= 50
                            print("    大天使之杖闪耀，降下神圣之光！")
                            for p in [x for x in Relo.party if x['hp'] > 0]:
                                heal = 150
                                p['hp'] = min(p.get('max_hp', 100), p['hp'] + heal)
                                print(f"    {p['name']} 恢复了 {heal} 点生命值！")

                        elif act == "wind_arrow" and actor.get('mp', 0) >= 30:
                            actor['mp'] -= 30
                            print("    穿风神弓拉满，箭矢如狂风暴雨！")
                            hits = random.randint(2, 3)
                            for i in range(hits):
                                logs = attack_logic(actor, enemy, weapons=wep)
                                narrate_battle(logs, actor, enemy)
                                if enemy['hp'] <= 0: break
                        else:
                            # 默认武器绝技处理
                            logs = attack_logic(actor, enemy, weapons=wep)
                            narrate_battle(logs, actor, enemy)
                    else:
                        logs = attack_logic(actor, enemy, weapons=None)
                        narrate_battle(logs, actor, enemy)

            else:
                # 敌人回合
                print(f"\n{Colors.RED}[敌方回合 - {enemy['name']}]{Colors.END}")
                time.sleep(0.5)
                # 随机选择一个存活的队员
                living_party = [p for p in Relo.party if p['hp'] > 0]
                if living_party:
                    target = random.choice(living_party)
                    enemy_logs = attack_logic(enemy, target, weapons=None)
                    narrate_battle(enemy_logs, target, enemy)

        # 战斗结算与清理
        if enemy['hp'] <= 0:
            break

        if Relo.hero['hp'] <= 0:
            print(f"\n☠️ 勇士阵亡了...")
            return False

        # --- 回合结算 ---
        print(f"\n--- 回合结算 ---")
        for actor in [p for p in Relo.party if p['hp'] > 0] + [enemy]:
            logs = StatusSystem.resolve_turn_end(actor)
            for l in logs: print(f"   ({actor['name']}) {l}")

            if 'buffs' in actor and actor['buffs']:
                for buff in actor['buffs'][:]:
                    buff['duration'] -= 1
                    if buff['duration'] <= 0:
                        print(f"    {actor['name']} 的 [{buff['name']}] 效果消失了。")
                        actor['buffs'].remove(buff)

        if Relo.hero['hp'] <= 0:
            print(f"\n☠️ 勇士在异常状态中阵亡了...")
            return False

        turn += 1

    # 胜利结算
    if enemy['hp'] <= 0:
        print(f"\n 胜利！打败了 {enemy['name']}！")
        exp_gain = enemy.get('exp', 0)
        Relo.hero['exp'] += exp_gain  # 经验暂时全给勇士
        print(f"   勇士获得经验: {exp_gain}")

        gold_range = enemy.get('gold', [0, 0])
        gold_dropped = random.randint(gold_range[0], gold_range[1])
        if gold_dropped > 0:
            Relo.hero['gold'] = Relo.hero.get('gold', 0) + gold_dropped
            print(f"   💰 获得金币: {gold_dropped}")

        # 检查升级
        old_level = Relo.hero.get('level', 1)
        check_level_up(Relo.hero)
        new_level = Relo.hero.get('level', 1)

        # 如果勇士升级了，给所有存活的伙伴也升一级
        if new_level > old_level:
            levels_gained = new_level - old_level
            scale = 1.15  # 和主角一致的成长倍率
            for p in Relo.party:
                if p != Relo.hero and p['hp'] > 0:
                    p['level'] = p.get('level', old_level) + levels_gained
                    
                    for _ in range(levels_gained):
                        p['max_hp'] = int(p['max_hp'] * scale)
                        p['max_mp'] = int(p.get('max_mp', 50) * scale)
                        p['base_atk'] = max(int(p['base_atk'] * scale), p['base_atk'] + 1)
                        p['def'] = max(int(p.get('def', 5) * scale), p.get('def', 5) + 1)
                        p['spd'] = max(int(p.get('spd', 10) * scale), p.get('spd', 10) + 1)
                        
                    p['hp'] = p['max_hp']
                    p['mp'] = p['max_mp']
                    print(f"    伙伴 {p['name']} 也升级了！(Lv.{p['level']}) 属性全面提升，并恢复了全部状态！")

        # 掉落逻辑
        loot_list = enemy.get('loot', [])
        dropped_items = []
        for loot in loot_list:
            chance_multiplier = 1.5 if enemy.get('max_hp', 0) >= 500 else 1.0
            if random.random() < (loot['chance'] * chance_multiplier):
                dropped_items.append(loot['item'])

        if not dropped_items and loot_list and random.random() < 0.3:
            best_chance_item = max(loot_list, key=lambda x: x['chance'])
            print(f"   (保底触发) 运气不好，但你还是在尸体上翻到了点东西...")
            dropped_items.append(best_chance_item['item'])

        for item_name in dropped_items:
            real_item = get_item_data_by_name(item_name)
            if real_item:
                print(f"    战利品！发现了 [{item_name}]")
                add_item_to_bag(Relo.hero, real_item)

        for p in Relo.party:
            StatusSystem.clear_status(p)
        return True
