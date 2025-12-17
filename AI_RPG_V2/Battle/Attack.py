# -*- coding: UTF-8 -*-
"""
@Project ：LangGraph 
@File    ：Attack.py
@IDE     ：PyCharm 
@Author  ：Write Bug
@Date    ：2025/12/10 09:40 
"""
import random

from RPG.Setting.Style import Colors
from RPG.Setting.Abnormal_condition import apply_burn_effect, apply_hemophagia_effect

# 定义全局超参
GAME_CONFIG = {
    "CRIT_RATE": 0.2,  # 20% 暴击率
    "CRIT_DMG": 1.5,  # 暴击造成 1.5 倍伤害
    "TEXT_SPEED": 1.0,  # 战斗文字显示间隔(秒)
    "LEVEL_UP_SCALING": 1.15,  # 每次升级属性提升 15%
    "EXP_THRESHOLD_BASE": 100,  # 升到2级所需经验
    # 随机性种子 (用于调试，None表示完全随机)
    "RANDOM_SEED": None
}


# 定义攻击逻辑
def attack_logic(attacker, defender, weapons=None):
    """
        计算一次攻击的所有逻辑：命中 -> 暴击 -> 扣血
        这里的 weapon 参数如果是 None，代表是裸手或者怪物攻击
    """
    combat_logs = []
    combat_logs.append(f"   \n⚔️  {attacker['name']} 发起了攻击！")
    # 计算总攻击力和命中率
    total_atk = attacker['base_atk']
    hit_chance = 0.9  # 默认命中率
    dmg_multiplier = 1.0  # 暴击
    current_effect = None

    # 只有玩家攻击时才有 weapon
    if weapons:
        total_atk += weapons["atk"]
        hit_chance = weapons['hit_rate']
        current_effect = weapons.get("effect")
        combat_logs.append(f"(使用武器: {weapons['name']} | 武器攻击: {weapons['atk']})")

    # 嗑药
    if 'buffs' in attacker:
        for buff in attacker['buffs']:
            if buff['type'] == 'atk':
                total_atk += buff['value']
                print(f"      (💪 {buff['name']} 加成: +{buff['value']}, 剩余{buff['duration']}回合)")

    # 闪避判断
    defender_dodge = defender.get("dodge", 0.0)

    # 定义Miss
    if random.random() > hit_chance:
        combat_logs.append(f"   🚫 {attacker['name']} 的攻击挥空了！(Miss)")
        return "\n".join(combat_logs)  # 攻击结束

        # 如果随机数小于闪避率，直接 Miss
    if random.random() < defender_dodge:
        combat_logs.append(f"   ⚡ {defender['name']} 身手敏捷，躲开了攻击！(Dodge)")
        return "\n".join(combat_logs)

    # 定义暴击
    is_crit = False
    if random.random() < GAME_CONFIG["CRIT_RATE"]:
        is_crit = True
        dmg_multiplier = GAME_CONFIG["CRIT_DMG"]
        combat_logs.append(f"   💥 {Colors.YELLOW}暴击!{Colors.END}")

    # 计算伤害：(攻击 * 倍率) - 防御
    raw_dmg = (total_atk * dmg_multiplier) - defender.get('def', 0)
    # 保证最少造成1点伤害
    final_dmg = int(max(1, raw_dmg))
    # 扣血指令
    defender['hp'] -= final_dmg
    # 小于0逻辑处理
    if defender['hp'] < 0:
        defender['hp'] = 0
    crit_text = "💥 暴击！" if is_crit else ""
    combat_logs.append(f"   ➡️  击中了 {defender['name']}！{crit_text} 造成了 {final_dmg} 点伤害。")
    combat_logs.append(f"🩸 {defender['name']} 剩余 HP: {defender['hp']}")

    # 定义嗜血和灼烧效果
    if weapons:
        if current_effect == "hemophagia":
            apply_hemophagia_effect(attacker, final_dmg)
        elif current_effect == "burn":
            apply_burn_effect(defender)

    return "\n".join(combat_logs)