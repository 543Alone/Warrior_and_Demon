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
from Characters_intro import Relo
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

    # 1. 记录发起攻击
    combat_logs.append(f"   \n⚔️  {attacker['name']} 发起了攻击！")

    # 2. 基础数值准备
    total_atk = attacker['base_atk']
    hit_chance = 0.9
    dmg_multiplier = 1.0
    current_effect = None

    # 3. 玩家武器逻辑 (关键修复点：确保这里不会导致函数提前中断)
    if weapons:
        total_atk += weapons["atk"]
        hit_chance = weapons['hit_rate']
        current_effect = weapons.get("effect")
        combat_logs.append(f"   (使用武器: {weapons['name']} | 武器攻击: {weapons['atk']})")

        # 圣剑特效检查
        # 即使 Excalibur 报错或返回 None，也不会影响后续流程
        try:
            special_dmg = Excalibur(attacker, defender)
            if special_dmg:
                total_atk = int(attacker['base_atk'] * 2.5)  # 简单处理为基础攻击2.5倍
                combat_logs.append(f"   ✨ {Colors.YELLOW}圣剑光辉！对魔王造成 2.5倍 伤害！{Colors.END}")
        except Exception:
            pass  # 防止特效报错卡死

    # 4. Buff 处理
    if 'buffs' in attacker:
        for buff in attacker['buffs']:
            if buff['type'] == 'atk':
                total_atk += buff['value']
                combat_logs.append(f"      (💪 {buff['name']} 加成: +{buff['value']})")
            elif buff['type'] == 'hit':
                hit_chance += buff['value']

    # 5. 防御计算 (修复了无限叠加 Bug)
    def_val = defender.get('def', 0)
    if defender['name'] == Relo.hero['name']:
        def_val += Relo.current_armor.get('def', 0)

    # 6. 闪避计算
    defender_dodge = defender.get("dodge", 0.0)
    if defender['name'] == Relo.hero['name']:
        defender_dodge += Relo.current_armor.get('dodge', 0.0)

    # --- 命中判定 ---
    if random.random() > hit_chance:
        combat_logs.append(f"   🚫 {attacker['name']} 的攻击挥空了！(Miss)")
        return "\n".join(combat_logs)  # 🔴 这是一个返回点

    if random.random() < defender_dodge:
        combat_logs.append(f"   ⚡ {defender['name']} 身手敏捷，躲开了攻击！(Dodge)")
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
    combat_logs.append(f"   ➡️  击中了 {defender['name']}！{crit_text} 造成了 {final_dmg} 点伤害。")
    combat_logs.append(f"   🩸 {defender['name']} 剩余 HP: {defender['hp']}")

    # 9. 触发武器特效 (燃烧/吸血)
    if weapons:
        if current_effect == "hemophagia":
            apply_hemophagia_effect(attacker, final_dmg)
        elif current_effect == "burn":
            apply_burn_effect(defender)

    return "\n".join(combat_logs)
