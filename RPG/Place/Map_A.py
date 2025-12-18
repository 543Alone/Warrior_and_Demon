# -*- coding: UTF-8 -*-
"""
@Project ：LangGraph 
@File    ：Map_A.py
@IDE     ：PyCharm 
@Author  ：Write Bug
@Date    ：2025/12/10 15:40 
"""

# 定义位置
world_map = {
    "新手村": {
        "desc": "安全区。",
        "connects_to": ["幽暗森林"],
        "safe_zone": True
    },
    "幽暗森林": {
        "desc": "阴森的森林，适合新手练级。",
        "connects_to": ["新手村", "水晶矿洞", "冰封山谷"], # 连接增加了
        "safe_zone": False,
        "spawn_table": "幽暗森林",  # 对应 monster_distribution 的 key
        "danger_level": 0.4  # 40% 几率遇怪

    },
    "水晶矿洞": {
        "desc": "充满了魔法水晶和深渊气息。",
        "connects_to": ["幽暗森林", "雷鸣废墟"],
        "safe_zone": False,
        "spawn_table": "水晶矿洞",
        "danger_level": 0.4  # 40% 几率遇怪
    },
    "冰封山谷": {
        "desc": "寒风刺骨，据说湖中女神沉睡于此。",
        "connects_to": ["幽暗森林", "魔王城"],
        "safe_zone": False,
        "spawn_table": "冰封山谷",
        "danger_level": 0.4  # 40% 几率遇怪
    },
    "雷鸣废墟": {
        "desc": "充满了危险的雷电。",
        "connects_to": ["水晶矿洞", "魔王城"],
        "safe_zone": False,
        "spawn_table": "雷鸣废墟",
        "danger_level": 0.4  # 40% 几率遇怪
    },
    "魔王城": {
        "desc": "BOSS战之地。",
        "connects_to": ["冰封山谷", "雷鸣废墟"],
        "is_boss_room": True
    }
}