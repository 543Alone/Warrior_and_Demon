# -*- coding: UTF-8 -*-
"""
@Project ：LangGraph
@File    ：Menu.py
@IDE     ：PyCharm
@Author  ：Write Bug
@Date    ：2025/12/10 15:11
"""


from Characters_intro import Relo

def equip_menu(player):
    """专门用来换装备的菜单函数"""
    print("\n" + "=" * 20)
    print(f"【背包 & {player['name']} 的装备】")

    # 获取当前职业
    cur_job = player.get('job', '战士')

    # 找出被其他人装备的物品
    equipped_by_others = []
    for p in Relo.party:
        if p != player:
            equipped_by_others.append(id(p.get('equipped_weapon')))
            equipped_by_others.append(id(p.get('equipped_armor')))

    # --- 1. 武器部分 ---
    my_weapons = [item for item in Relo.hero['bag'] if
                  'atk' in item and cur_job in item.get('usable_by', ['战士', '刺客', '法师', '牧师', '精灵'])
                  and id(item) not in equipped_by_others]
    # 获取当前身上的装备
    cur_w_name = player.get('equipped_weapon', {}).get('name', '无')

    if not my_weapons:
        print(" (背包里没有可用的武器)")
    else:
        print(f"当前装备: {cur_w_name}")
        print("可装备的武器:")
        for i, w in enumerate(my_weapons):
            mark = "*" if w['name'] == cur_w_name else " "
            print(f"{mark} {i}. {w['name']} (攻+{w['atk']})")

        try:
            choice = input("输入编号更换 (回车跳过): ")
            if choice.isdigit():
                idx = int(choice)
                if 0 <= idx < len(my_weapons):
                    # 直接修改字典内的键值
                    player['equipped_weapon'] = my_weapons[idx]
                    print(f"已装备: {player['equipped_weapon']['name']}")
        except:
            pass

    print("-" * 20)

    # --- 2. 防具部分 ---
    my_armors = [item for item in Relo.hero['bag'] if
                 'def' in item and cur_job in item.get('usable_by', ['战士', '刺客', '法师', '牧师', '精灵'])
                 and id(item) not in equipped_by_others]
    cur_a_name = player.get('equipped_armor', {}).get('name', '无')

    if not my_armors:
        print(" (背包里没有可用的防具)")
    else:
        print(f"当前装备: {cur_a_name}")
        print("可装备的防具:")
        for i, a in enumerate(my_armors):
            mark = "*" if a['name'] == cur_a_name else " "
            print(f"{mark} {i}. {a['name']} (防+{a['def']})")

        try:
            choice = input("输入编号更换 (回车跳过): ")
            if choice.isdigit():
                idx = int(choice)
                if 0 <= idx < len(my_armors):
                    # 直接修改字典内的键值
                    player['equipped_armor'] = my_armors[idx]
                    print(f"已装备: {player['equipped_armor']['name']}")
        except:
            pass

    print("=" * 20 + "\n")
