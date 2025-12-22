# -*- coding: UTF-8 -*-
"""
@Project ：Warrior_and_Demon 
@File    ：Armor_Effects.py
@IDE     ：PyCharm 
@Author  ：Write Bug
@Date    ：2025/12/19 15:33 
"""
import random


class ArmorEffectSystem:
    # 当敌人攻击玩家时候，根据玩家的防具特效，降低敌人的命中率
    @staticmethod
    def get_hit_rate_modifier(defender):
        """
        命中率修正 (Passive)
        :param defender: 敌人
        :return: 修正值
        """
        armor = defender.get('equipped_armor')
        if not armor or not armor.get('effect'):
            return 0.0

        effect = armor['effect']

        # 潜行：降低 10% 命中
        if effect == "stealth": return 0.10
        # 纸箱：降低 30% 命中
        if effect == "stealth_bonus": return 0.30
        # 魅惑：降低 10% 命中
        if effect == "charm": return 0.10
        # 水晶反射：降低 15% 命中 (致盲)
        if effect == "reflect_light": return 0.15

        return 0.0

    # 当敌人攻击玩家时，降低敌人的攻击力数值
    @staticmethod
    def apply_damage_reduction(attacker, defender, raw_atk, logs):
        """
        伤害修正 (Passive)
        :param attacker: 攻击者
        :param defender: 敌人
        :param raw_atk: 攻击力数值
        :param logs: 日志
        :return: 修正后的攻击力数值
        """
        armor = defender.get('equipped_armor')
        if not armor or not armor.get('effect'):
            return raw_atk

        effect = armor['effect']

        # Cos服：降低敌人 30% 攻击力
        if effect == "low_aggro":
            loss = int(raw_atk * 0.3)
            logs.append(f"   🥺 {defender['name']} 的奇装异服让对方迟疑了 (攻击 -{loss})")
            return raw_atk - loss

        # 魅惑：降低敌人 10% 攻击力
        if effect == "charm":
            loss = int(raw_atk * 0.1)
            logs.append(f"   😍 {attacker['name']} 被魅惑了，手软无力 (攻击 -{loss})")
            return raw_atk - loss

        return raw_atk

    # 战斗结算后触发的效果：反伤、回血、吸血增强
    @staticmethod
    def on_combat_end_trigger(attacker, defender, damage_taken, logs):
        """
        受击/攻击后触发 (Reactive)
        :param attacker: 攻击者 (正在打你的人)
        :param defender: 防守者 (穿着防具的人)
        :param damage_taken: 这次受到的实际伤害
        :param logs: 战斗日志列表
        :return:
        """
        # 防守方的防具特效 (反伤、受击回血)
        def_armor = defender.get('equipped_armor')
        if def_armor and def_armor.get('effect'):
            eff = def_armor['effect']

            # 荆棘反伤
            if eff == "reflect_damage" and damage_taken > 0:
                reflect = max(1,int(damage_taken * 0.2))
                if reflect > 0:
                    attacker['hp'] -= reflect
                    logs.append(f"   🌵 荆棘背心刺伤了对手，造成 {reflect} 点反伤！")

            # 凤凰羽衣 (受击回血)
            if eff == "regen_hp":
                if random.random() < 0.3:  # 30% 概率
                    heal = 15
                    defender['hp'] += heal  # 记得加 max_hp 限制
                    logs.append(f"   🔥 凤凰羽衣泛起火光，恢复了 {heal} 点生命！")

        # 攻击方的防具特效
        atk_armor = attacker.get('equipped_armor')
        if atk_armor and atk_armor.get('effect'):
            eff = atk_armor['effect']

            # 鲜血披风 (被动吸血)
            if eff == "life_steal_passive":
                # 只有造成了伤害才吸血
                if damage_taken > 0:
                    heal = int(damage_taken * 0.15)  # 15% 吸血
                    if heal < 1: heal = 1
                    attacker['hp'] += heal
                    logs.append(f"   🧛 鲜血披风吸取了 {heal} 点生命...")

