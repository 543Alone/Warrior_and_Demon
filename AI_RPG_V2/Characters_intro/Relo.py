# -*- coding: UTF-8 -*-
"""
@Project ：LangGraph 
@File    ：Relo.py
@IDE     ：PyCharm 
@Author  ：Write Bug
@Date    ：2025/12/10 09:36 
"""
from Monsters.Monsters import get_monster_by_name
from Warehouse.Armor import armors_list
from Warehouse.Weapons import weapons_list

# 先创建独立的副本，防止修改全局模板
_init_weapon = weapons_list[0].copy()
_init_armor = armors_list[0].copy()

# 角色属性
hero = {
    "name": "勇士",
    "hp": 100,
    "max_hp": 100,
    "mp": 50,
    "max_mp": 50,
    "level": 1,
    "base_atk": 10,
    "def": 5,
    "spd": 8,
    "exp": 0,
    "lock": 0,
    "gold": 100,
    "bag": [_init_weapon, _init_armor],  # 初始背包
    "equipped_weapon": _init_weapon,
    "equipped_armor": _init_armor,

    # 记录 Buff 列表
    "buffs": [],
    "statuses": {}
}

# 全局队伍列表，游戏一开始只有勇士自己
party = [hero]

# 存放在新手村休息的伙伴名册
reserve_party = []

# 已击败的四大门神记录 (存Boss名字)
defeated_bosses = []

# 当前状态
current_location = "新手村"
current_enemy = None
