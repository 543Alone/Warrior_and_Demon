# -*- coding: UTF-8 -*-
"""
@Project ：LangGraph 
@File    ：Style.py
@IDE     ：PyCharm 
@Author  ：Write Bug
@Date    ：2025/12/10 09:38 
"""

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    END = '\033[0m'


def show_health_bar(entity, max_bar_length=20):
    """
    显示实体血条
    :param entity: 实体对象(勇士/魔王/怪物等)
    :param max_bar_length: 血条最大长度
    """
    hp = entity.get("hp", 0)
    max_hp = entity.get("max_hp", hp if hp > 0 else 1)
    name = entity.get("name", "未知")

    # 计算血条长度
    if hp < 0: hp = 0
    bar_length = min(int(hp / max_hp * max_bar_length), max_bar_length)
    empty_length = max_bar_length - bar_length

    # 红色血条
    health_bar = f"{Colors.RED}{'#' * bar_length}{Colors.END}{' ' * empty_length}"
    print(f"{name} HP: [{health_bar}] {hp}/{max_hp}")

    ...
