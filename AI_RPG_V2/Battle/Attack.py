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
from Setting.Abnormal_condition import StatusSystem
from Setting.Armor_Effects import ArmorEffectSystem
from Setting.Style import Colors


class CombatEngine:
    """
    战斗计算引擎：负责处理攻击判定、伤害计算、特效触发
    """

    # 默认配置
    DEFAULT_CONFIG = {
        "CRIT_RATE": 0.2,  # 暴击率
        "CRIT_DMG": 1.5,  # 暴击伤害
        "BASE_HIT": 0.9,  # 命中率
        "SPD_DODGE_RATIO": 0.02,  # 每1点速度差提供 2% 闪避
        "MAX_DODGE": 0.75  # 闪避上限 75% (防止无敌)
    }

    def __init__(self, config=None):
        self.config = config if config else self.DEFAULT_CONFIG

    def _get_real_speed(self, character):
        """
        计算角色的实时速度 (基础速度 * 护甲修正)
        """
        base_spd = character.get('spd', 10)  # 默认速度10

        # 护甲修正
        multiplier = 1.0
        armor = character.get('equipped_armor')
        if armor:
            # 例如 spd = -0.15，则倍率变成 0.85
            multiplier += armor.get('spd', 0.0)

        return max(1, int(base_spd * multiplier))

    def _check_hit(self, attacker, defender, weapon, logs):
        """
        计算命中率 (引入速度差机制)
        """
        # 1. 攻击者的基础命中 (武器命中)
        hit_chance = self.config["BASE_HIT"]
        if weapon:
            hit_chance = weapon.get('hit_rate', hit_chance)

        # 2. 计算双方实时速度
        atk_spd = self._get_real_speed(attacker)
        def_spd = self._get_real_speed(defender)

        # 3. 计算速度带来的闪避加成
        # 只有当防守方比攻击方快时，才有额外闪避
        speed_diff = def_spd - atk_spd
        dodge_bonus = 0.0
        if speed_diff > 0:
            dodge_bonus = min(speed_diff * self.config["SPD_DODGE_RATIO"], self.config["MAX_DODGE"])

            # 这里不需要打印，太啰嗦，但为了调试你可以取消注释
            # logs.append(f"   (速度差 {speed_diff} 带来 {int(dodge_bonus*100)}% 闪避率)")

        # 4. 调用防具的特殊效果
        hit_malus = ArmorEffectSystem.get_hit_rate_modifier(defender)
        hit_chance -= hit_malus  # 降低命中率

        # 5. 最终判定
        # 最终命中率 = 攻击者命中 - (基础闪避 + 速度闪避)
        final_hit_rate = hit_chance - dodge_bonus

        # 随机数判定
        roll = random.random()

        # 比如 final_hit_rate 是 0.6， roll 出了 0.7 -> Miss
        if roll > final_hit_rate:
            # 区分是速度躲的，还是装备特效干扰的 (可选优化)
            if hit_malus > 0 and roll <= (hit_chance + hit_malus):
                # 如果原本能打中(roll < hit)，但因为速度快(roll > final)导致没打中
                logs.append(f"   🌫️ {defender['name']} 的装备干扰了攻击判断！")
            elif speed_diff > 0:
                logs.append(f"   ⚡ {defender['name']} 凭借惊人的速度闪避成功！")
            else:
                logs.append(f"   🚫 {attacker['name']} 攻击未命中 (Miss)")
            return False

        return True

    def process_attack(self, attacker, defender, weapon_override=None):
        """
        [主入口] 执行一次完整的攻击流程
        :return: logs (str) 战斗日志
        """
        logs = []
        logs.append(f"   \n⚔️  {attacker['name']} 发起了攻击！")

        weapon = weapon_override if weapon_override else attacker.get('equipped_weapon')
        if weapon:
            logs.append(f"   (使用武器: {weapon['name']} | 攻+{weapon['atk']})")

        # 1. 命中判定
        if not self._check_hit(attacker, defender, weapon, logs):
            return "\n".join(logs)

        # 2. 伤害计算
        final_dmg, is_crit = self._calculate_damage(attacker, defender, weapon, logs)

        # 3. 执行扣血
        defender['hp'] -= final_dmg
        if defender['hp'] < 0: defender['hp'] = 0

        crit_txt = f" {Colors.YELLOW}💥 暴击!{Colors.END}" if is_crit else ""
        logs.append(f"   ➡️  击中 {defender['name']}！{crit_txt} 造成 {final_dmg} 点伤害。")
        logs.append(f"   🩸 {defender['name']} 剩余 HP: {defender['hp']}")

        # 4. 触发特效
        self._apply_effects(attacker, defender, weapon, final_dmg, logs)

        return "\n".join(logs)

    def _calculate_damage(self, attacker, defender, weapon, logs):
        """内部方法：计算伤害数值"""
        # 基础攻击
        total_atk = attacker.get('base_atk', 10)
        if weapon:
            total_atk += weapon.get('atk', 0)

        # 圣剑特效
        if weapon and weapon.get('effect') == "demon_slayer_multiplier_2.5" and defender.get('name') == "魔王":
            total_atk = int(attacker['base_atk'] * 2.5)
            logs.append(f"   ✨ {Colors.YELLOW}圣剑光辉！对魔王伤害倍增！{Colors.END}")

        # 调用防具特效系统修正攻击力 (Cos服、魅惑等)
        total_atk = ArmorEffectSystem.apply_damage_reduction(attacker, defender, total_atk, logs)

        # 暴击
        is_crit = False
        multiplier = 1.0
        if random.random() < self.config["CRIT_RATE"]:
            is_crit = True
            multiplier = self.config["CRIT_DMG"]

        # 防御计算
        def_val = defender.get('def', 0)
        # 加上防具防御值
        if defender.get('equipped_armor'):
            def_val += defender['equipped_armor'].get('def', 0)
        # 破甲特效
        if weapon and weapon.get('effect') == "ignore_def":
            def_val = 0
            logs.append(f"   🌑 月光无视了护甲！")

        raw = (total_atk * multiplier) - def_val
        final_dmg = int(max(1, raw))
        return final_dmg, is_crit

    def _apply_effects(self, attacker, defender, weapon, dmg, logs):
        """
        特效系统
        :param attacker: 攻击者对象
        :param defender: 防守者对象
        :param weapon: 武器对象
        :param dmg: 伤害数值
        :param logs: 日志列表
        :return:  无
        """
        if weapon and weapon.get('effect'):
            eff = weapon['effect']

            # 吸血
            if eff == "hemophagia":
                heal = int(dmg * 0.3)
                attacker['hp'] += heal
                logs.append(f"   🩸 嗜血！恢复 {heal} 生命！")

            # 机械键盘
            elif eff == "noise":
                logs.append("   🔊 咔哒咔哒！精神攻击！")

            # 异常状态 (自动对接 StatusSystem)
            elif eff in StatusSystem.CONFIG:
                if random.random() < 0.3:  # 30% 几率
                    StatusSystem.apply_status(defender, eff)

        # 调用防具特效系统 (反伤、吸血披风等)
        ArmorEffectSystem.on_combat_end_trigger(attacker, defender, dmg, logs)


# 实例化
default_engine = CombatEngine()


def attack_logic(attacker, defender, weapons=None):
    return default_engine.process_attack(attacker, defender, weapons)
