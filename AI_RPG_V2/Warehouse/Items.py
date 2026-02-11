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
    {"name": "小苹果", "type": "heal", "value": 20, "price": 10, "desc": "路边树上摘的，希望没有农药"},
    {"name": "止血草", "type": "heal", "value": 35, "price": 20, "desc": "就是个草而已。"},
    {"name": "烤鸡腿", "type": "heal", "value": 50, "price": 30, "desc": "香气扑鼻，补充体力的好东西"},
    {"name": "披萨", "type": "heal", "value": '30%', "price": 40, "desc": "太多cheese了！"},
    {"name": "强效治疗药水", "type": "heal", "value": 100, "price": 50, "desc": "炼金术士还是医生？"},
    {"name": "魔法药水", "type": "restore_mp", "value": 50, "price": 30, "desc": "补充法力值，法师的最爱"},
    {"name": "回城卷轴", "type": "teleport", "value": 0, "price": 100,
     "desc": "撕碎后瞬间传送回新手村（仅限非战斗时使用）"},

    # --- 增益类 (Buff) ---
    {"name": "力量药剂", "type": "buff_atk", "value": 10, "duration": 3, "price": 80,
     "desc": "喝了感觉充满了力量 (持续3回合)"},
    {"name": "敏捷药剂", "type": "buff_hit", "value": 0.2, "duration": 3, "price": 80,
     "desc": "你的动作快到出现残影 (命中率+20%)"},

    # --- 特殊类 ---
    {"name": "浓缩咖啡", "type": "special", "value": 0, "price": 100,
     "desc": "虽然不加血，但你可以通宵打魔王了 (解除睡眠/麻痹状态)"},
    {"name": "神秘药水", "type": "buff_lock", "value": 0.01, "duration": "+∞", "price": 500,
     "desc": "据说有个人掉进这个药水池中，变成了主角！"},

    # --- 投掷类 ---
    {"name": "硬石头", "type": "damage", "value": 5, "price": 5, "desc": "朝着对面脑袋扔一个，没什么伤害但是侮辱性极强"},
    {"name": "地精手雷", "type": "damage", "value": 80, "price": 200, "desc": "造成固定伤害，不需要命中率"},
    {"name": "刨冰", "type": "heal", "value": 40, "price": 30, "desc": "透心凉，心飞扬"},
    {"name": "废旧电池", "type": "damage", "value": 10, "price": 5, "desc": "千万不要乱扔垃圾"},
    {"name": "💎 龙之宝玉", "type": "special", "value": 1000, "price": 5000, "desc": "非常值钱的宝物"},
    {"name": "世界和平奖章", "type": "special", "value": 0, "price": 9999, "desc": "证明你拯救了世界"},
]
