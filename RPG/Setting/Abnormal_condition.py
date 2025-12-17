# -*- coding: UTF-8 -*-
"""
@Project ：LangGraph 
@File    ：Abnormal_condition.py
@IDE     ：PyCharm 
@Author  ：Write Bug
@Date    ：2025/12/12 09:29 
"""

import random


def apply_burn_effect(defender):
    """
    应用燃烧效果到目标身上
    :param defender: 防守者对象
    """
    # 30%概率叠加一层燃烧
    if random.random() < 0.3:
        defender['burn_stack'] = defender.get('burn_stack', 0) + 1

    if defender['burn_stack'] > 0:
        print(f"   🔥 {defender['name']} 身上燃起了火焰！(当前层数: {defender['burn_stack']})")


def process_damage(enemy):
    """
    结算敌人的燃烧伤害
    :param enemy: 敌人对象
    """
    burn_stack = enemy.get('burn_stack', 0)
    if burn_stack > 0:
        burn_dmg = burn_stack * 10
        enemy['hp'] -= burn_dmg
        print(f"   🔥 灼烧造成 {burn_dmg} 伤害")


def apply_hemophagia_effect(attacker, final_dmg):
    """
    应用嗜血效果
    :param attacker: 攻击者对象
    :param final_dmg: 造成的最终伤害值
    """
    heal = int(final_dmg * 0.3)
    attacker['hp'] = min(attacker['max_hp'], attacker['hp'] + heal)
    print(f"   💚 {attacker['name']} 触发吸血！恢复了 {heal} 点生命值！")


def noise():
    print("   🔊 攻击音效")


def Excalibur(attacker, defender):
    """

    :param attacker: 攻击者对象
    :param defender: 防守者对象
    :return: 攻击伤害
    """
    base_atk = attacker.get('weapon', {}).get('atk', 0)
    weapon_effect = attacker.get('weapon', {}).get('effect', '')
    enemy_name = defender.get('name', '')
    # 如果对方是魔王并且武器的“effect” == demon_slayer_multiplier_2.5，伤害就是2.5倍
    if enemy_name == '魔王' and weapon_effect == 'demon_slayer_multiplier_2.5':
        return base_atk * 2.5
