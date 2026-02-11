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
    print(f"   \n⚔️  {attacker['name']} 发起了攻击！")
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
        print(f"(使用武器: {weapons['name']} | 武器攻击: {weapons['atk']})")

    # 嗑药
    if 'buffs' in attacker:
        for buff in attacker['buffs']:
            if buff['type'] == 'atk':
                total_atk += buff['value']
                print(f"      (💪 {buff['name']} 加成: +{buff['value']}, 剩余{buff['duration']}回合)")

    # 闪避判断
    defender_dodge = defender.get("dodge", 0.0)
    def_percent_bonus = 0.0
    hp_regen = 0
    # 解析防具词条
    if "current_armor" in defender:
        armor = defender["current_armor"]
    else:
        # 为了简便，如果找不到当前护甲就算了，这里通常玩家会有防具加成
        import RPG.Characters_intro.Relo as Relo
        if defender.get("name") == "勇士":
            armor = Relo.current_armor
        else:
            armor = {}
            
    if armor and "affixes" in armor:
        for af in armor["affixes"]:
            if af["type"] == "dodge":
                defender_dodge += af["value"]
            elif af["type"] == "def_percent":
                def_percent_bonus += af["value"]
            elif af["type"] == "hp_regen":
                hp_regen += af["value"]

    # 定义Miss
    if random.random() > hit_chance:
        print(f"   🚫 {attacker['name']} 的攻击挥空了！(Miss)")
        return  # 攻击结束

    # 如果随机数小于闪避率，直接 Miss
    if random.random() < defender_dodge:
        print(f"   ⚡ {defender['name']} 身手敏捷，躲开了攻击！(Dodge)")
        return

    # 解析武器词条
    bonus_crit_rate = 0.0
    bonus_crit_dmg = 0.0
    bonus_lifesteal = 0.0
    
    if weapons and "affixes" in weapons:
        for af in weapons["affixes"]:
            if af["type"] == "crit_rate":
                bonus_crit_rate += af["value"]
            elif af["type"] == "crit_dmg":
                bonus_crit_dmg += af["value"]
            elif af["type"] == "lifesteal":
                bonus_lifesteal += af["value"]
            elif af["type"] == "atk_percent":
                total_atk = total_atk * (1 + af["value"])

    # 定义暴击
    is_crit = False
    if random.random() < (GAME_CONFIG["CRIT_RATE"] + bonus_crit_rate):
        is_crit = True
        dmg_multiplier = GAME_CONFIG["CRIT_DMG"] + bonus_crit_dmg
        print(f"   💥 {Colors.YELLOW}暴击!{Colors.END}")

    # 计算防御
    total_def = defender.get('def', 0)
    total_def = total_def * (1 + def_percent_bonus)

    # 计算伤害：(攻击 * 倍率) - 防御
    raw_dmg = (total_atk * dmg_multiplier) - total_def
    # 保证最少造成1点伤害
    final_dmg = int(max(1, raw_dmg))
    
    # 扣血指令
    defender['hp'] -= final_dmg
    # 小于0逻辑处理
    if defender['hp'] < 0:
        defender['hp'] = 0
    crit_text = "💥 暴击！" if is_crit else ""
    print(f"   ➡️  击中了 {defender['name']}！{crit_text} 造成了 {final_dmg} 点伤害。")

    # 护甲受击回血
    if hp_regen > 0 and defender['hp'] > 0:
        defender['hp'] = min(defender['max_hp'], defender['hp'] + int(hp_regen))
        print(f"   ✨ {defender['name']} 的防具触发复苏，回复了 {int(hp_regen)} 点生命！")

    # 定义嗜血和灼烧效果
    if weapons:
        if current_effect == "hemophagia" or bonus_lifesteal > 0:
            if current_effect == "hemophagia":
                bonus_lifesteal += 0.3 # 嗜血魔剑自带30%吸血
            heal = int(final_dmg * bonus_lifesteal)
            if heal > 0:
                attacker['hp'] = min(attacker['max_hp'], attacker['hp'] + heal)
                print(f"   💚 {attacker['name']} 触发吸血！恢复了 {heal} 点生命值！")
        elif current_effect == "burn":
            apply_burn_effect(defender)