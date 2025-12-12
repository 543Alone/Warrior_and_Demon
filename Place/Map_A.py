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
        "desc": "安全和平的小村庄，可以休息回血。",
        "connects_to": ["幽暗森林"],
        "safe_zone": True  # 安全区，不会遇怪
    },
    "幽暗森林": {
        "desc": "光线昏暗的森林，随处可见哥布林和史莱姆。",
        "connects_to": ["新手村", "魔王城"],
        "safe_zone": False,
        "danger_level": 0.4  # 40% 几率遇怪
    },
    "魔王城": {
        "desc": "最终决战之地，空气中弥漫着硫磺味。",
        "connects_to": ["幽暗森林"],
        "safe_zone": False,
        "is_boss_room": True  # 只有Boss
    }
}
