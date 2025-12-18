# -*- coding: UTF-8 -*-
"""
@Project ：LangGraph 
@File    ：Death_penalty.py
@IDE     ：PyCharm 
@Author  ：Write Bug
@Date    ：2025/12/11 17:57 
"""
import time

from Characters_intro import Relo
from Characters_intro.Relo import hero


def Death_enalty():
    print("村民发现了昏迷的你，把你拖回了村子。")

    # --- 复活逻辑 ---
    Relo.current_location = "新手村"  # 强制送回新手村
    hero['hp'] = hero['max_hp']  # 满血复活

    # 死亡惩罚：扣除 50% 当前经验
    lost_exp = int(hero['exp'] / 2)
    hero['exp'] -= lost_exp

    print(f"🏥 经过村长的治疗，你醒了过来。")
    print(f"📉 代价：经验值减少了 {lost_exp} 点。")

    time.sleep(2)
    return Relo.current_location