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
from AI_RPG_V2.Characters_intro import Relo
from AI_RPG_V2.Setting.Abnormal_condition import apply_burn_effect, apply_hemophagia_effect, Excalibur
from AI_RPG_V2.Setting.Style import Colors

# 定义全局超参
GAME_CONFIG = {
    "CRIT_RATE": 0.2,  # 20% 暴击率
    "CRIT_DMG": 1.5,  # 暴击造成 1.5 倍伤害
    "TEXT_SPEED": 1.0,  # 战斗文字显示间隔(秒)
    "LEVEL_UP_SCALING": 1.15,  # 每次升级属性提升 15%
    "EXP_THRESHOLD_BASE": 100,  # 升到2级所需经验
    "RANDOM_SEED": None
}


def attack_logic(attacker, defender, weapons=None):
    """
    计算一次攻击的所有逻辑
    """
    combat_logs = []
    combat_logs.append(f"   \n⚔️  {attacker['name']} 发起了攻击！")

    # 1. 基础攻击力
    total_atk = attacker['base_atk']
    hit_chance = 0.9
    dmg_multiplier = 1.0
    current_effect = None

    # 2. 如果有武器 (玩家攻击)
    if weapons:
        total_atk += weapons["atk"]
        hit_chance = weapons['hit_rate']
        current_effect = weapons.get("effect")
        combat_logs.append(f"(使用武器: {weapons['name']} | 武器攻击: {weapons['atk']})")

        # 特殊逻辑：检查是否触发 Excalibur 效果 (如：打魔王加成)
        # 如果 Excalibur 返回了数值，说明触发了倍率，覆盖当前攻击力
        special_dmg = Excalibur(attacker, defender)
        if special_dmg:
            # 这里简单处理：如果触发特效，基于基础攻击力翻倍
            total_atk = int(total_atk * 2.5)
            combat_logs.append(f"   ✨ {Colors.YELLOW}圣剑光辉！对魔王造成 2.5倍 伤害！{Colors.END}")

    # 3. 处理 Buff (嗑药效果)
    if 'buffs' in attacker:
        for buff in attacker['buffs']:
            if buff['type'] == 'atk':
                total_atk += buff['value']
                combat_logs.append(f"      (💪 {buff['name']} 加成: +{buff['value']})")
            # 这里补充了命中率药剂的逻辑
            elif buff['type'] == 'hit':
                hit_chance += buff['value']

    # 4. 计算防御力 (核心修复点)
    def_val = defender.get('def', 0)
    # 如果被打的是勇士，我们要加上他身上穿的护甲防御力
    if defender['name'] == Relo.hero['name']:
        def_val += Relo.current_armor.get('def', 0)
        # 调试用，不想看可以注释掉
        # combat_logs.append(f"(防御方穿戴: {Relo.current_armor['name']} +{Relo.current_armor['def']}防)")

    # 5. 闪避判断
    defender_dodge = defender.get("dodge", 0.0)
    # 如果玩家穿了装备，加上装备的闪避修正
    if defender['name'] == Relo.hero['name']:
        defender_dodge += Relo.current_armor.get('dodge', 0.0)

    # --- 判定环节 ---
    if random.random() > hit_chance:
        combat_logs.append(f"   🚫 {attacker['name']} 的攻击挥空了！(Miss)")
        return "\n".join(combat_logs)

    if random.random() < defender_dodge:
        combat_logs.append(f"   ⚡ {defender['name']} 身手敏捷，躲开了攻击！(Dodge)")
        return "\n".join(combat_logs)

    # 6. 暴击判定
    is_crit = False
    if random.random() < GAME_CONFIG["CRIT_RATE"]:
        is_crit = True
        dmg_multiplier = GAME_CONFIG["CRIT_DMG"]
        combat_logs.append(f"   💥 {Colors.YELLOW}暴击!{Colors.END}")

    # 7. 最终伤害计算
    raw_dmg = (total_atk * dmg_multiplier) - def_val
    final_dmg = int(max(1, raw_dmg))  # 至少造成1点强制伤害

    defender['hp'] -= final_dmg
    if defender['hp'] < 0: defender['hp'] = 0

    crit_text = "💥 暴击！" if is_crit else ""
    combat_logs.append(f"   ➡️  击中了 {defender['name']}！{crit_text} 造成了 {final_dmg} 点伤害。")
    combat_logs.append(f"🩸 {defender['name']} 剩余 HP: {defender['hp']}")

    # 8. 触发武器特效
    if weapons:
        if current_effect == "hemophagia":
            apply_hemophagia_effect(attacker, final_dmg)
        elif current_effect == "burn":
            apply_burn_effect(defender)

    return "\n".join(combat_logs)
