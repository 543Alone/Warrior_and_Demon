# -*- coding: UTF-8 -*-
"""
@Project ：LangGraph 
@File    ：Level.py
@IDE     ：PyCharm 
@Author  ：Write Bug
@Date    ：2025/12/11 13:22 
"""
from Battle.Attack import GAME_CONFIG, Colors


def check_level_up(player):
    """
    检查是否满足升级条件，如果满足则提升属性
    """
    # 计算下一级所需的经验值：当前等级 * 基础阈值 (例如 1级升2级需100，2级升3级需200)
    # 也可以改成固定100： required_exp = player['level'] * 100
    required_exp = player['level'] * GAME_CONFIG["EXP_THRESHOLD_BASE"]

    if player['exp'] >= required_exp:
        # 扣除经验值 (或者你可以选择不扣除，而是累积经验制，看你喜好)
        # 这里采用：扣除当前升级所需经验，保留溢出部分
        player['exp'] -= required_exp
        player['level'] += 1

        # 获取成长倍率
        scale = GAME_CONFIG["LEVEL_UP_SCALING"]  # 1.15

        # --- 属性提升计算 ---
        # 生命上限提升 (取整)
        old_hp = player['max_hp']
        player['max_hp'] = int(old_hp * scale)

        # 2. 攻击力提升 (保底 +1，防止前期数值太低乘法无效)
        old_atk = player['base_atk']
        add_atk = int(old_atk * scale) - old_atk
        if add_atk < 1: add_atk = 1
        player['base_atk'] += add_atk

        # 防御力提升 (保底 +1，每两级至少加1点防御)
        old_def = player['def']
        # 防御成长慢一点，这里做一个简单判断
        player['def'] = int(old_def * scale)
        if player['def'] == old_def:  # 如果乘完没变
            player['def'] += 1

        # 升级回满血
        player['hp'] = player['max_hp']

        print(f"\n" + "=" * 30)
        print(f"🎉 {Colors.YELLOW}恭喜升级！你升到了 Lv.{player['level']}！{Colors.END}")
        print(f"   ❤️ 生命上限: {old_hp} -> {player['max_hp']}")
        print(f"   ⚔️ 基础攻击: {old_atk} -> {player['base_atk']}")
        print(f"   🛡️ 基础防御: {old_def} -> {player['def']}")
        print(f"   ✨ 状态已完全恢复！")
        print("=" * 30 + "\n")

        # 递归检查（防止一次获得巨量经验连升两级的情况）
        check_level_up(player)
