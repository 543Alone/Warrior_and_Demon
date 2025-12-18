# -*- coding: UTF-8 -*-
"""
@Project ：LangGraph
@File    ：Menu.py
@IDE     ：PyCharm
@Author  ：Write Bug
@Date    ：2025/12/10 15:11
"""
from AI_RPG_V2.Characters_intro import Relo


def equip_menu(player):
    """专门用来换装备的菜单函数"""
    print("\n" + "=" * 20)
    print("【🎒 背包 & 装备】")

    # --- 1. 武器部分 ---
    my_weapons = [item for item in player['bag'] if 'atk' in item]
    if not my_weapons:
        print(" (背包里没有武器)")
    else:
        print("可装备的武器:")
        for i, w in enumerate(my_weapons):
            mark = "*" if w == Relo.current_weapon else " "
            print(f"{mark} {i}. {w['name']} (攻+{w['atk']})")

        try:
            choice = input("输入编号更换 (回车跳过): ")
            if choice.isdigit():
                idx = int(choice)
                if 0 <= idx < len(my_weapons):
                    Relo.current_weapon = my_weapons[idx]
                    print(f"✅ 已装备: {Relo.current_weapon['name']}")
        except:
            pass

    print("-" * 20)

    # --- 2. 防具部分 ---
    my_armors = [item for item in player['bag'] if 'def' in item]

    if not my_armors:
        print(" (背包里没有防具)")
    else:
        print("可装备的防具:")
        for i, a in enumerate(my_armors):
            mark = "*" if a == Relo.current_armor else " "
            print(f"{mark} {i}. {a['name']} (防+{a['def']})")

        try:
            choice = input("输入编号更换 (回车跳过): ")
            if choice.isdigit():
                idx = int(choice)
                if 0 <= idx < len(my_armors):
                    # 【关键修改】只切换装备引用，不再直接修改 player['def'] 数值
                    Relo.current_armor = my_armors[idx]
                    print(f"✅ 已装备: {Relo.current_armor['name']}")
        except:
            pass

    print("=" * 20 + "\n")
