# -*- coding: UTF-8 -*-
"""
@Project ：LangGraph 
@File    ：Relo.py
@IDE     ：PyCharm 
@Author  ：Write Bug
@Date    ：2025/12/10 09:36 
"""
from Warehouse.Weapons import weapons_list
from Warehouse.Armor import armors_list

# 角色属性
hero = {
    "name": "勇士",
    "hp": 100,
    "max_hp": 100,
    "level": 1,
    "base_atk": 10,
    "def": 5,
    "exp": 0,
    "bag": [weapons_list[0], armors_list[0]],  # 初始背包

    "equipped_weapon": weapons_list[0],
    "equipped_armor": armors_list[0],

    # 记录 Buff 列表
    "buffs": []
}

demon = {
    "name": "魔王",
    "hp": 3000,
    "max_hp": 3000,
    "base_atk": 50,
    "def": 10,
    "burn_stack": 0,
    "loot": []
}

current_location = "新手村"
current_enemy = None
