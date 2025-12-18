# -*- coding: UTF-8 -*-
"""
@Project ：Warrior_and_Demon 
@File    ：Agent_state.py
@IDE     ：PyCharm 
@Author  ：Write Bug
@Date    ：2025/12/18 09:35 
"""
# 新建一个 agent_state.py
from typing import TypedDict, Annotated, List

from langgraph.graph.message import add_messages


# 引入你现有的数据结构

class AgentState(TypedDict):
    messages: Annotated[List, add_messages]  # 聊天记录
    player: dict  # 直接复用 Relo.hero 的结构
    current_location: str  # 复用 Relo.current_location
    game_mode: str  # 新增：标记当前是 "exploration"(探索) 还是 "battle"(战斗)
