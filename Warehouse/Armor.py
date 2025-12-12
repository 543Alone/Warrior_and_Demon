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
    {"name": "布衣", "def": 2, "dodge": 0.0, "desc": "在魔王眼里，你就是什么都没穿", "effect": None},
    {"name": "锁子甲", "def": 10, "dodge": -0.05, "desc": "有些沉重，稍微降低闪避", "effect": None},
    {"name": "🛡️ 皇家骑士板甲", "def": 25, "dodge": -0.15, "desc": "铁罐头一般的安全感", "effect": None},
    {"name": "忍者夜行衣", "def": 5, "dodge": 0.20, "desc": "防御不高，但只要打不中就不掉血", "effect": "stealth"},
    {"name": "🌵 荆棘背心", "def": 15, "dodge": 0.0, "desc": "来，宝宝，抱一个~", "effect": "reflect_damage"},
    {"name": "🔥 凤凰羽衣", "def": 12, "dodge": 0.05, "desc": "看，一点也不烫，对吗", "effect": "regen_hp"},
    {"name": "cos服", "def": 1, "dodge": 0.0, "desc": "老二次元了", "effect": "low_aggro"},
    {"name": "📦 纸箱", "def": 5, "dodge": 0.30, "desc": "致敬Solid Snake，魔王根本看不见你", "effect": "stealth_bonus"},
    {"name": "👙 黄金比基尼", "def": 80, "dodge": 0.0, "desc": "众所周知，布料越少防御越高 (仅限女性角色有效?)",
     "effect": "charm"},
    {"name": "🐢 龟壳背包", "def": 40, "dodge": -0.20, "desc": "防御力惊人，但重得让你想趴在地上走", "effect": None},
]
