# -*- coding: UTF-8 -*-
"""
@Project ：LangGraph 
@File    ：Attack.py
@IDE     ：PyCharm 
@Author  ：Write Bug
@Date    ：2025/12/10 09:40 
"""
import random

# 引入 Relo 是为了获取当前的装备数据
from Setting.Abnormal_condition import apply_burn_effect, apply_hemophagia_effect, Excalibur
from Setting.Style import Colors

# 定义全局超参
GAME_CONFIG = {
    "CRIT_RATE": 0.2,
    "CRIT_DMG": 1.5,
    "TEXT_SPEED": 1.0,
    "LEVEL_UP_SCALING": 1.15,
    "EXP_THRESHOLD_BASE": 100,
    "RANDOM_SEED": None
}


def attack_logic(attacker, defender, weapons=None):
    """
    计算一次攻击的所有逻辑
    """
    combat_logs = []
    combat_logs.append(f"   \n⚔️  {attacker['name']} 发起了攻击！")

    total_atk = attacker['base_atk']
    hit_chance = 0.9
    dmg_multiplier = 1.0
    current_effect = None

    # --- 1. 武器逻辑 ---
    real_weapon = weapons
    if not real_weapon and 'equipped_weapon' in attacker:
        real_weapon = attacker['equipped_weapon']

    if real_weapon:
        total_atk += real_weapon["atk"]
        hit_chance = real_weapon['hit_rate']
        current_effect = real_weapon.get("effect")
        combat_logs.append(f"   (使用武器: {real_weapon['name']} | 攻+{real_weapon['atk']})")

        try:
            special_dmg = Excalibur(attacker, defender)
            if special_dmg:
                total_atk = int(attacker['base_atk'] * 2.5)
                combat_logs.append(f"   ✨ {Colors.YELLOW}圣剑光辉！造成 2.5倍 伤害！{Colors.END}")
        except:
            pass

    # --- 2. Buff 逻辑 ---
    if 'buffs' in attacker:
        for buff in attacker['buffs']:
            if buff['type'] == 'atk':
                total_atk += buff['value']
            elif buff['type'] == 'hit':
                hit_chance += buff['value']

    # --- 3. 防御逻辑 ---
    def_val = defender.get('def', 0)

    if 'equipped_armor' in defender:
        armor = defender['equipped_armor']
        def_val += armor.get('def', 0)
        # combat_logs.append(f"   (护甲: {armor['name']} 抵消了部分伤害)")

    # --- 4. 闪避逻辑 ---
    defender_dodge = defender.get("dodge", 0.0)
    if 'equipped_armor' in defender:
        defender_dodge += defender['equipped_armor'].get('dodge', 0.0)

    # --- 5. 判定与结算 ---
    if random.random() > hit_chance:
        combat_logs.append(f"   🚫 {attacker['name']} Miss")
        return "\n".join(combat_logs)  # 🔴 这是一个返回点

    if random.random() < defender_dodge:
        combat_logs.append(f"   ⚡ {defender['name']} Dodge")
        return "\n".join(combat_logs)  # 🔴 这是一个返回点

    # 7. 暴击判定
    is_crit = False
    if random.random() < GAME_CONFIG["CRIT_RATE"]:
        is_crit = True
        dmg_multiplier = GAME_CONFIG["CRIT_DMG"]
        combat_logs.append(f"   💥 {Colors.YELLOW}暴击!{Colors.END}")

    # 8. 结算伤害
    raw_dmg = (total_atk * dmg_multiplier) - def_val
    final_dmg = int(max(1, raw_dmg))

    defender['hp'] -= final_dmg
    if defender['hp'] < 0: defender['hp'] = 0

    crit_text = "💥 暴击！" if is_crit else ""
    combat_logs.append(f"   ➡️  击中 {defender['name']}！{crit_text} 造成 {final_dmg} 点伤害。")
    combat_logs.append(f"   🩸 {defender['name']} 剩余 HP: {defender['hp']}")

    # 9. 触发武器特效 (燃烧/吸血)
    if real_weapon:
        if current_effect == "hemophagia":
            apply_hemophagia_effect(attacker, final_dmg)
        elif current_effect == "burn":
            apply_burn_effect(defender)

    return "\n".join(combat_logs)
