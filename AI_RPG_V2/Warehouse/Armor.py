# -*- coding: UTF-8 -*-
"""
@Project ：LangGraph 
@File    ：Armor.py
@IDE     ：PyCharm 
@Author  ：Write Bug
@Date    ：2025/12/10 09:50 
"""
# 定义防具库
armors_list = [
    {"name": "布衣", "def": 2, "spd": 0.0, "quality": "common", "price": 10, "desc": "在魔王眼里，你就是什么都没穿",
     "effect": None, "usable_by": ["战士", "刺客", "法师", "牧师", "精灵"]},
    {"name": "锁子甲", "def": 10, "spd": -0.05, "quality": "common", "price": 50, "desc": "有些沉重，稍微降低闪避",
     "effect": None, "usable_by": ["战士", "刺客", "精灵"]},
    {"name": "🛡️ 皇家骑士板甲", "def": 25, "spd": -0.15, "quality": "rare", "price": 300, "desc": "铁罐头一般的安全感",
     "effect": None, "usable_by": ["战士"]},
    {"name": "忍者夜行衣", "def": 5, "spd": 0.20, "quality": "rare", "price": 250,
     "desc": "防御不高，但只要打不中就不掉血", "effect": "stealth", "usable_by": ["刺客", "精灵"]},  # 降低敌人30%命中率
    {"name": "荆棘背心", "def": 15, "spd": 0.0, "quality": "rare", "price": 400, "desc": "来，宝宝，抱一个~",
     "effect": "reflect_damage", "usable_by": ["战士"]},  # 反伤
    {"name": "🔥 凤凰羽衣", "def": 12, "spd": 0.05, "quality": "epic", "price": 1200, "desc": "看，一点也不烫，对吗",
     "effect": "regen_hp", "usable_by": ["法师", "牧师", "精灵"]},
    {"name": "cos服", "def": 1, "spd": 0.0, "quality": "common", "price": 100, "desc": "老二次元了",
     "effect": "low_aggro", "usable_by": ["战士", "刺客", "法师", "牧师", "精灵"]},  # 降低敌人30%攻击力
    {"name": "纸箱", "def": 5, "spd": 0.30, "quality": "rare", "price": 150, "desc": "致敬Solid Snake，魔王根本看不见你",
     "effect": "stealth_bonus", "usable_by": ["刺客", "战士"]},  # 降低敌人10%命中率
    {"name": "👙 黄金比基尼", "def": 80, "spd": 0.0, "quality": "unique", "price": 5000,
     "desc": "众所周知，布料越少防御越高 (仅限女性角色有效?)", "effect": "charm", "usable_by": ["法师", "精灵", "刺客"]},
    # 降低敌人10%防御力、攻击力、命中率、速度
    {"name": "龟壳背包", "def": 40, "spd": -0.20, "quality": "epic", "price": 1500,
     "desc": "防御力惊人，但重得让你想趴在地上走", "effect": None, "usable_by": ["战士", "牧师"]},
    {"name": "虚空法袍", "def": 10, "spd": 0.15, "quality": "unique", "price": 3000,
     "desc": "看似布料，实则由魔法力场编织，能让身体变得虚幻。", "effect": "magic_spd", "usable_by": ["法师", "牧师"]},
    # 有20%概率免疫魔法伤害（未实现）
    {"name": "水晶护甲", "def": 55, "spd": -0.10, "quality": "epic", "price": 2000,
     "desc": "由地下发光水晶打磨而成，因为是透明的，所以里面还是要穿衣服的。", "effect": "reflect_light",
     "usable_by": ["战士", "法师", "牧师"]},  # 没想好怎么写
    {"name": "🧛 鲜血披风", "def": 15, "spd": 0.05, "quality": "unique", "price": 3500,
     "desc": "散发着腥甜气息的披风，似乎能渴望敌人的生命。", "effect": "life_steal_passive", "usable_by": ["刺客"]},
    # 增加30%嗜血效果
]
