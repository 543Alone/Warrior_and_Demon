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
    {"id": "w01", "name": "生锈铁剑", "atk": 5, "hit_rate": 0.95, "quality": "common", "price": 10,
     "desc": "新手村捡来的，破伤风之刃", "effect": None, "usable_by": ["战士", "刺客"]},
    {"id": "w02", "name": "精钢长剑", "atk": 20, "hit_rate": 0.85, "quality": "common", "price": 50,
     "desc": "标准的骑士装备", "effect": None, "usable_by": ["战士"]},

    # --- 🔵 稀有 (有点东西) ---
    {"id": "w04", "name": "双持匕首", "atk": 30, "hit_rate": 1.0, "quality": "rare", "price": 200,
     "desc": "虽然单次伤害不高，但绝对不会失手", "effect": None, "usable_by": ["刺客", "战士"]},
    {"id": "w10", "name": "巨型战斧", "atk": 45, "hit_rate": 0.65, "quality": "rare", "price": 300,
     "desc": "伤害爆炸，但太重了容易挥空", "effect": None, "usable_by": ["战士"]},
    {"id": "w05", "name": "机械键盘", "atk": 40, "hit_rate": 1.0, "quality": "rare", "price": 400,
     "desc": "物理与精神双重打击，特别是青轴", "effect": "noise", "usable_by": ["战士", "刺客", "法师", "牧师", "精灵"]},

    # --- 🟣 史诗 (高级货) ---
    {"id": "w03", "name": "皇家骑士巨剑", "atk": 45, "hit_rate": 0.90, "quality": "epic", "price": 1000,
     "desc": "王国卫队的制式武器，性能均衡", "effect": None, "usable_by": ["战士"], "weapon_skill": "heavy_slash"},
    {"id": "w20", "name": "雷霆战锤", "atk": 55, "hit_rate": 0.75, "quality": "epic", "price": 1200,
     "desc": "矮人打造的附魔锤，每一击都伴随着雷鸣", "effect": "paralyze", "usable_by": ["战士", "牧师"],
     "weapon_skill": "thunder_strike"},

    # --- 🌸 神器 (魔法装备) ---
    {"id": "w11", "name": "🔥 烈焰魔剑", "atk": 50, "hit_rate": 0.85, "quality": "unique", "price": 2500,
     "desc": "附带魔法火焰，专门克制魔王", "effect": "burn", "usable_by": ["战士"], "weapon_skill": "flame_slash"},
    {"id": "w12", "name": "🩸 嗜血魔剑", "atk": 50, "hit_rate": 0.85, "quality": "unique", "price": 3000,
     "desc": "附带吸血，魔王也是碳基生物吗？", "effect": "hemophagia", "usable_by": ["战士", "刺客"]},
    {"id": "w13", "name": "❄ 寒冰魔剑", "atk": 50, "hit_rate": 0.85, "quality": "unique", "price": 2500,
     "desc": "水坎·冰封破！", "effect": "congelation", "usable_by": ["战士"], "weapon_skill": "ice_break"},
    {"id": "w21", "name": "🌑 月光大剑", "atk": 65, "hit_rate": 0.90, "quality": "unique", "price": 3500,
     "desc": "剑身主要由魔法光辉构成，能穿透物理防御。", "effect": "ignore_def", "usable_by": ["战士"]},

    # --- 🌟 传说 (版本答案) ---
    {"id": "w19", "name": "圣剑·Excalibur", "atk": 80, "hit_rate": 0.90, "quality": "legendary", "price": 9999,
     "desc": "专门为了斩杀魔王而存在的传说武器。", "effect": "demon_slayer_multiplier_2.5", "usable_by": ["战士"],
     "weapon_skill": "excalibur"},
    {"id": "w22", "name": "诸神黄昏", "atk": 100, "hit_rate": 0.85, "quality": "legendary", "price": 12000,
     "desc": "蕴含着毁灭诸神力量的巨剑，极具破坏力。", "effect": "ignore_def", "usable_by": ["战士"],
     "weapon_skill": "ragnarok"},
    {"id": "w23", "name": "冥界之刃", "atk": 75, "hit_rate": 1.0, "quality": "legendary", "price": 11000,
     "desc": "刀刃上流淌着深渊之血，必定命中且刀刀致命。", "effect": "hemophagia", "usable_by": ["刺客"],
     "weapon_skill": "shadow_strike"},

    # --- 💀 崩坏 (官方外挂) ---
    {"id": "w99", "name": "龙之牙", "atk": 999, "hit_rate": 0.10, "quality": "glitch", "price": 10000,
     "desc": "威力巨大但全是Bug(很难命中)", "effect": None, "usable_by": ["战士", "刺客", "法师", "牧师", "精灵"]},
    {"id": "w24", "name": "剧毒之牙", "atk": 40, "hit_rate": 0.95, "quality": "epic", "price": 1000,
     "desc": "涂满剧毒的匕首", "effect": "poison", "usable_by": ["刺客"]},
    {"id": "w25", "name": "🌀 风暴细剑", "atk": 55, "hit_rate": 0.95, "quality": "epic", "price": 1500,
     "desc": "轻盈得仿佛能切开风", "effect": "wind_strike", "usable_by": ["战士", "刺客"]},
]

# 法师/远程武器列表也顺便加一下
weapons_list2 = [
    {"name": "🧙‍♂️ 枯木法杖", "atk": 15, "hit_rate": 0.90, "quality": "common", "price": 150, "desc": "枯木枯木落！",
     "effect": "mana_restore", "usable_by": ["法师", "牧师"]},
    {"name": "❄️ 寒冰射手", "atk": 35, "hit_rate": 0.95, "quality": "rare", "price": 400, "desc": "不是豌豆射手",
     "effect": "freeze", "usable_by": ["精灵", "刺客"], "weapon_skill": "frost_arrow"},
    {"name": "⚡ 宙斯之怒", "atk": 60, "hit_rate": 0.75, "quality": "unique", "price": 2500, "desc": "友军之怒",
     "effect": "paralyze", "usable_by": ["法师", "牧师"], "weapon_skill": "thunder_storm"},
    {"name": "🔮 大天使之杖", "atk": 70, "hit_rate": 0.95, "quality": "legendary", "price": 11000,
     "desc": "散发着神圣光辉的法杖，拥有极其纯净的魔力。", "effect": "mana_restore", "usable_by": ["法师", "牧师"],
     "weapon_skill": "holy_light"},
    {"name": "🏹 穿风神弓", "atk": 85, "hit_rate": 1.0, "quality": "legendary", "price": 11500,
     "desc": "由世界树枝干打造的神弓，箭矢快如闪电。", "effect": "ignore_def", "usable_by": ["精灵"],
     "weapon_skill": "wind_arrow"},
]
