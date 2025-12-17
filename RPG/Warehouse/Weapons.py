# -*- coding: UTF-8 -*-
"""
@Project ：LangGraph 
@File    ：Weapons.py
@IDE     ：PyCharm 
@Author  ：Write Bug
@Date    ：2025/12/10 09:34 
"""

# 定义武器库
weapons_list = [
    # --- ⚪ 普通 (破烂) ---
    {"id": "w01", "name": "生锈铁剑", "atk": 5, "hit_rate": 0.95, "quality": "common", "desc": "新手村捡来的，破伤风之刃", "effect": None},
    {"id": "w02", "name": "精钢长剑", "atk": 20, "hit_rate": 0.85, "quality": "common", "desc": "标准的骑士装备", "effect": None},

    # --- 🔵 稀有 (有点东西) ---
    {"id": "w04", "name": "🗡️ 双持匕首", "atk": 30, "hit_rate": 1.0, "quality": "rare", "desc": "虽然单次伤害不高，但绝对不会失手", "effect": None},
    {"id": "w10", "name": "巨型战斧", "atk": 45, "hit_rate": 0.65, "quality": "rare", "desc": "伤害爆炸，但太重了容易挥空", "effect": None},
    {"id": "w05", "name": "⌨️ 机械键盘", "atk": 40, "hit_rate": 1.0, "quality": "rare", "desc": "物理与精神双重打击，特别是青轴", "effect": "noise"},

    # --- 🟣 史诗 (高级货) ---
    {"id": "w03", "name": "🗡 皇家骑士巨剑", "atk": 45, "hit_rate": 0.90, "quality": "epic", "desc": "王国卫队的制式武器，性能均衡", "effect": None},
    {"id": "w20", "name": "⚡ 雷霆战锤", "atk": 55, "hit_rate": 0.75, "quality": "epic", "desc": "矮人打造的附魔锤，每一击都伴随着雷鸣", "effect": "paralyze"},

    # --- 🌸 神器 (魔法装备) ---
    {"id": "w11", "name": "🔥 烈焰魔剑", "atk": 50, "hit_rate": 0.85, "quality": "unique", "desc": "附带魔法火焰，专门克制魔王", "effect": "burn"},
    {"id": "w12", "name": "🩸 嗜血魔剑", "atk": 50, "hit_rate": 0.85, "quality": "unique", "desc": "附带吸血，魔王也是碳基生物吗？", "effect": "hemophagia"},
    {"id": "w13", "name": "❄ 寒冰魔剑", "atk": 50, "hit_rate": 0.85, "quality": "unique", "desc": "水坎·冰封破！", "effect": "congelation"},
    {"id": "w21", "name": "🌑 月光大剑", "atk": 65, "hit_rate": 0.90, "quality": "unique", "desc": "剑身主要由魔法光辉构成，能穿透物理防御。", "effect": "ignore_def"},

    # --- 🌟 传说 (版本答案) ---
    {"id": "w19", "name": "圣剑·Excalibur", "atk": 80, "hit_rate": 0.90, "quality": "legendary", "desc": "专门为了斩杀魔王而存在的传说武器。", "effect": "demon_slayer_multiplier_2.5"},

    # --- 💀 崩坏 (官方外挂) ---
    {"id": "w99", "name": "龙之牙", "atk": 999, "hit_rate": 0.10, "quality": "glitch", "desc": "威力巨大但全是Bug(很难命中)", "effect": None},
]

# 法师/远程武器列表也顺便加一下
weapons_list2 = [
    {"name": "🧙‍♂️ 枯木法杖", "atk": 15, "hit_rate": 0.90, "quality": "common", "desc": "枯木枯木落！", "effect": "mana_restore"},
    {"name": "❄️ 寒冰射手", "atk": 35, "hit_rate": 0.95, "quality": "rare", "desc": "不是豌豆射手", "effect": "freeze"},
    {"name": "⚡ 宙斯之怒", "atk": 60, "hit_rate": 0.75, "quality": "unique", "desc": "友军之怒", "effect": "paralyze"},
]
