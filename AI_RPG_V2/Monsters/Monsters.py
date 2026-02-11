# -*- coding: UTF-8 -*-
"""
@Project ：LangGraph 
@File    ：Monsters.py
@IDE     ：PyCharm 
@Author  ：Write Bug
@Date    ：2025/12/10 10:15 
"""

# 定义怪物库
monsters_list = [
    # --- 新手村/森林区域 (低级) ---
    {
        "name": "史莱姆",
        "hp": 30, "max_hp": 30, "base_atk": 5, "def": 0, "exp": 10, "spd": 5, "gold": [2, 5],
        "loot": [{"item": "精钢长剑", "chance": 0.3}, {"item": "小苹果", "chance": 0.5}]
    },
    {
        "name": "哥布林斥候",
        "hp": 60, "max_hp": 60, "base_atk": 12, "def": 2, "exp": 25, "spd": 7, "gold": [5, 12],
        "loot": [{"item": "双持匕首", "chance": 0.05}, {"item": "锁子甲", "chance": 0.3},
                 {"item": "小苹果", "chance": 0.5}, ]
    },
    {
        "name": "腐朽树精",
        "hp": 90, "max_hp": 90, "base_atk": 14, "def": 8, "exp": 45, "spd": 1, "gold": [10, 20],
        "loot": [{"item": "🧙‍♂️ 枯木法杖", "chance": 0.2}, {"item": "荆棘背心", "chance": 0.3},
                 {"item": "止血草", "chance": 0.5}]
    },
    {
        "name": " 潜行大师 (哥布林)",
        "hp": 40, "max_hp": 40, "base_atk": 10, "def": 0, "exp": 80, "spd": 10, "gold": [20, 50],
        "loot": [{"item": "忍者夜行衣", "chance": 0.2}, {"item": "纸箱", "chance": 0.3},
                 {"item": "敏捷药剂", "chance": 0.5}, ]
    },

    # --- 矿洞/地下城区域 (中级) ---
    {
        "name": "青牙巨魔",
        "hp": 100, "max_hp": 100, "base_atk": 12, "def": 5, "exp": 35, "spd": 8, "gold": [15, 30],
        "loot": [{"item": "巨型战斧", "chance": 0.3}, {"item": "力量药剂", "chance": 0.5},
                 {"item": "烤鸡腿", "chance": 0.7}]
    },
    {
        "name": "晶簇傀儡",
        "hp": 120, "max_hp": 120, "base_atk": 25, "def": 15, "exp": 55, "spd": 3, "gold": [30, 60],
        "loot": [{"item": "水晶护甲", "chance": 0.15}, {"item": "雷霆战锤", "chance": 0.05},
                 {"item": "硬石头", "chance": 0.8}]
    },
    {
        "name": "深渊教徒",
        "hp": 80, "max_hp": 80, "base_atk": 30, "def": 2, "exp": 65, "spd": 5, "gold": [25, 45],
        "loot": [{"item": "虚空法袍", "chance": 0.1}, {"item": "剧毒之牙", "chance": 0.1},
                 {"item": "神秘药水", "chance": 0.3}]
    },

    # --- 隐藏/特殊/恶搞区域 (特殊) ---
    {
        "name": "发狂的程序员",
        "hp": 100, "max_hp": 100, "base_atk": 20, "def": 10, "exp": 50, "spd": 20, "gold": [50, 100],
        "loot": [{"item": "机械键盘", "chance": 0.01}, {"item": "cos服", "chance": 0.2},
                 {"item": "浓缩咖啡", "chance": 0.8}]
    },
    {
        "name": "宝箱怪",
        "hp": 150, "max_hp": 150, "base_atk": 35, "def": 20, "exp": 80, "spd": 10, "gold": [200, 500],
        "loot": [{"item": "🩸 嗜血魔剑", "chance": 0.1}, {"item": "🔥 烈焰魔剑", "chance": 0.3},
                 {"item": "皇家骑士巨剑", "chance": 0.7}, {"item": "🛡️ 皇家骑士板甲", "chance": 0.7}]
    },
    {
        "name": "下水道忍者",
        "hp": 150, "max_hp": 150, "base_atk": 25, "def": 45, "exp": 70, "spd": 10, "gold": [40, 80],
        "loot": [{"item": "龟壳背包", "chance": 0.25}, {"item": "披萨", "chance": 0.5}]
    },

    # --- 元素高危区域 (高级) ---
    {
        "name": "极寒幽魂",
        "hp": 110, "max_hp": 110, "base_atk": 22, "def": 8, "exp": 60, "spd": 15, "gold": [30, 50],
        "loot": [{"item": "❄ 寒冰魔剑", "chance": 0.15}, {"item": "❄️ 寒冰射手", "chance": 0.15},
                 {"item": "刨冰", "chance": 0.5}]
    },
    {
        "name": "雷云风暴",
        "hp": 130, "max_hp": 130, "base_atk": 40, "def": 5, "exp": 90, "spd": 20, "gold": [40, 70],
        "loot": [{"item": "⚡ 宙斯之怒", "chance": 0.1}, {"item": "废旧电池", "chance": 0.5}]
    },

    # --- BOSS级 ---
    {
        "name": "月影骑士 (精英)",
        "hp": 500, "max_hp": 500, "base_atk": 65, "def": 30, "exp": 300, "spd": 30, "gold": [500, 800],
        "loot": [{"item": "🌑 月光大剑", "chance": 0.25}, {"item": "🧛 鲜血披风", "chance": 0.3},
                 {"item": "🌀 风暴细剑", "chance": 0.3}]
    },
    {
        "name": "湖中女神(黑化)",
        "hp": 800, "max_hp": 800, "base_atk": 80, "def": 40, "exp": 800, "spd": 30, "gold": [1000, 1500],
        "loot": [{"item": "圣剑·Excalibur", "chance": 0.05}, {"item": "👙 黄金比基尼", "chance": 0.15}]
    },
    {
        "name": "🔥 远古红龙",
        "hp": 1500, "max_hp": 1500, "base_atk": 120, "def": 60, "exp": 1500, "spd": 40, "gold": [2000, 3000],
        "loot": [{"item": "龙之牙", "chance": 0.2}, {"item": "🔥 凤凰羽衣", "chance": 0.3},
                 {"item": "💎 龙之宝玉", "chance": 1.0}]
    },

    # --- 四大试炼之门守卫 ---
    {
        "name": "堕落战神·阿瑞斯",
        "hp": 2000, "max_hp": 2000, "base_atk": 150, "def": 50, "exp": 2000, "spd": 20, "gold": [1000, 2000],
        "loot": [{"item": "诸神黄昏", "chance": 0.25}]
    },
    {
        "name": "影之主宰",
        "hp": 1500, "max_hp": 1500, "base_atk": 180, "def": 30, "exp": 2000, "spd": 80, "gold": [1000, 2000],
        "loot": [{"item": "冥界之刃", "chance": 0.25}]
    },
    {
        "name": "深渊凝视者",
        "hp": 1800, "max_hp": 1800, "base_atk": 200, "def": 40, "exp": 2000, "spd": 30, "gold": [1000, 2000],
        "loot": [{"item": "🔮 大天使之杖", "chance": 0.25}]
    },
    {
        "name": "腐化神射手",
        "hp": 1600, "max_hp": 1600, "base_atk": 160, "def": 30, "exp": 2000, "spd": 60, "gold": [1000, 2000],
        "loot": [{"item": "🏹 穿风神弓", "chance": 0.25}]
    },

    # --- 最终BOSS ---
    {
        "name": "魔王",
        "hp": 10000, "max_hp": 10000, "base_atk": 250, "def": 80, "exp": 99999, "spd": 50, "gold": [10000, 50000],
        "loot": [{"item": "世界和平奖章", "chance": 1.0}]
    }
]

monster_distribution = {
    "幽暗森林": {
        "史莱姆": 60,  # 极高概率 (遍地都是)
        "哥布林斥候": 30,  # 常见
        "腐朽树精": 8,  # 偶尔遇到
        "宝箱怪": 1,  # 2% 权重，很稀有
        "潜行大师 (哥布林)": 5  # 比较稀有
    },

    "水晶矿洞": {
        "青牙巨魔": 40,
        "晶簇傀儡": 30,
        "深渊教徒": 20,
        "宝箱怪": 2,  # 只有 2 权重，很难遇到
        "发狂的程序员": 1  # 1 权重，传说级遭遇
    },

    "冰封山谷": {
        "极寒幽魂": 40,
        "下水道忍者": 30,
        "宝箱怪": 3,
        "湖中女神(黑化)": 20,
    },

    "雷鸣废墟": {
        "雷云风暴": 40,
        "宝箱怪": 4,
        "发狂的程序员": 1,
    },

    "魔王城": {
        "月影骑士 (精英)": 40,
        "🔥 远古红龙": 40,
        "深渊教徒": 20
    }
}


def get_monster_by_name(name):
    for m in monsters_list:
        if m["name"] == name:
            # 返回副本，防止战斗修改原始数据
            return m.copy()
    return None
