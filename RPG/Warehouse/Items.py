# -*- coding: UTF-8 -*-
"""
@Project ：LangGraph 
@File    ：Items.py
@IDE     ：PyCharm 
@Author  ：Write Bug
@Date    ：2025/12/10 10:01 
"""
# 定义物品库
items_list = [
    # --- 回复类 ---
    {"name": "🍎 小苹果", "type": "heal", "value": 20, "price": 10, "desc": "路边树上摘的，希望没有农药"},
    {"name": "🧪 强效治疗药水", "type": "heal", "value": 100, "price": 50, "desc": "炼金术士还是医生？"},
    {"name": "🍗 烤鸡腿", "type": "heal", "value": 50, "price": 30, "desc": "香气扑鼻，补充体力的好东西"},

    # --- 增益类 (Buff) ---
    {"name": "💪 力量药剂", "type": "buff_atk", "value": 10, "duration": 3, "price": 80, "desc": "喝了感觉充满了力量 (持续3回合)"},
    {"name": "⚡ 敏捷药剂", "type": "buff_hit", "value": 0.2, "duration": 3, "price": 80, "desc": "你的动作快到出现残影 (命中率+20%)"},

    # --- 特殊类 ---
    {"name": "☕ 浓缩咖啡", "type": "special", "value": 0, "price": 100, "desc": "虽然不加血，但你可以通宵打魔王了 (解除睡眠/麻痹状态)"},
    {"name": "💣 地精手雷", "type": "damage", "value": 80, "price": 200, "desc": "造成固定伤害，不需要命中率"}
]
