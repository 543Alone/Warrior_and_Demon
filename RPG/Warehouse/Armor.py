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
    {"name": "布衣", "def": 2, "dodge": 0.0, "quality": "common", "price": 10, "desc": "在魔王眼里，你就是什么都没穿", "effect": None},
    {"name": "锁子甲", "def": 10, "dodge": -0.05, "quality": "common", "price": 50, "desc": "有些沉重，稍微降低闪避", "effect": None},
    {"name": "🛡️ 皇家骑士板甲", "def": 25, "dodge": -0.15, "quality": "rare", "price": 300, "desc": "铁罐头一般的安全感", "effect": None},
    {"name": "忍者夜行衣", "def": 5, "dodge": 0.20, "quality": "rare", "price": 250, "desc": "防御不高，但只要打不中就不掉血", "effect": "stealth"},
    {"name": "🌵 荆棘背心", "def": 15, "dodge": 0.0, "quality": "rare", "price": 400, "desc": "来，宝宝，抱一个~", "effect": "reflect_damage"},
    {"name": "🔥 凤凰羽衣", "def": 12, "dodge": 0.05, "quality": "epic", "price": 1200, "desc": "看，一点也不烫，对吗", "effect": "regen_hp"},
    {"name": "cos服", "def": 1, "dodge": 0.0, "quality": "common", "price": 100, "desc": "老二次元了", "effect": "low_aggro"},
    {"name": "📦 纸箱", "def": 5, "dodge": 0.30, "quality": "rare", "price": 150, "desc": "致敬Solid Snake，魔王根本看不见你", "effect": "stealth_bonus"},
    {"name": "👙 黄金比基尼", "def": 80, "dodge": 0.0, "quality": "unique", "price": 5000, "desc": "众所周知，布料越少防御越高 (仅限女性角色有效?)","effect": "charm"},
    {"name": "🐢 龟壳背包", "def": 40, "dodge": -0.20, "quality": "epic", "price": 1500, "desc": "防御力惊人，但重得让你想趴在地上走", "effect": None},
    {"name": "🔮 虚空法袍", "def": 10, "dodge": 0.15, "quality": "unique", "price": 3000, "desc": "看似布料，实则由魔法力场编织，能让身体变得虚幻。", "effect": "magic_dodge"},
    {"name": "💎 水晶护甲", "def": 55, "dodge": -0.10, "quality": "epic", "price": 2000, "desc": "由地下发光水晶打磨而成，因为是透明的，所以里面还是要穿衣服的。", "effect": "reflect_light"},
    {"name": "🧛 鲜血披风", "def": 15, "dodge": 0.05, "quality": "unique", "price": 3500, "desc": "散发着腥甜气息的披风，似乎能渴望敌人的生命。", "effect": "life_steal_passive"},
]
