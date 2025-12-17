# -*- coding: UTF-8 -*-
"""
@Project ：LangGraph
@File    ：Menu.py
@IDE     ：PyCharm
@Author  ：Write Bug
@Date    ：2025/12/10 15:11
"""
from RPG.Characters_intro import Relo


def equip_menu(player):
    """专门用来换装备的菜单函数"""
    print("\n" + "=" * 20)
    print("【🎒 背包 & 装备】")

    my_weapons = [item for item in player['bag'] if 'atk' in item]
    if not my_weapons:
        print(" (背包里没有武器)")
    else:
        # 换武器
        print("可装备的武器:")
        for i, w in enumerate(my_weapons):
            # 标记当前装备的
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

    # 换防具
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
                    # 先移除旧防具的加成 (防止无限叠加BUG)
                    player['def'] -= Relo.current_armor.get('def', 0)

                    # 换新装备
                    Relo.current_armor = my_armors[idx]

                    # 加上新防具加成
                    player['def'] += Relo.current_armor['def']
                    player['dodge'] = Relo.current_armor.get('dodge', 0)
                    print(f"✅ 已装备: {Relo.current_armor['name']} (当前防御: {player['def']})")
        except:
            pass

    print("=" * 20 + "\n")
