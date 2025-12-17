# -*- coding: UTF-8 -*-
"""
@Project ：LangGraph 
@File    ：Relo.py
@IDE     ：PyCharm 
@Author  ：Write Bug
@Date    ：2025/12/10 09:36 
"""
from RPG.Warehouse.Weapons import weapons_list
from RPG.Warehouse.Armor import armors_list
# 角色属性
hero = {
    "name": "勇士",
    "hp": 100,
    "max_hp": 100,
    "level":1,
    "max_cost": 5,  # 初始负重
    "base_atk": 10,  # 基础攻击力
    "def": 5,  # 基础防御
    "exp": 0,
    "SPD": 10,  # 基础移速，影响先手和逃跑
    "LUCK": 5,  # 幸运值，影响暴击和掉落
    "bag": [weapons_list[0], armors_list[0]],
}

demon = {
    "name": "魔王",
    "hp": 3000,  # 魔王血量厚
    "max_hp": 3000,
    "base_atk": 50,  # 魔王攻击高
    "def": 10,
    "burn_stack": 0,  # 被火焰层数
    "LUCK": 0,  # 不幸的成为了魔王
    "loot": [],  # 防止报错
}

# 玩家当前位置
current_location = "新手村"
# 定义两个全局变量存当前装备
current_weapon = weapons_list[0]
current_armor = armors_list[0]
