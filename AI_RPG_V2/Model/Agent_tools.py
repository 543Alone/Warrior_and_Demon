# -*- coding: UTF-8 -*-
"""
@Project ：Warrior_and_Demon 
@File    ：Agent_tools.py
@IDE     ：PyCharm 
@Author  ：Write Bug
@Date    ：2025/12/18 09:37 
"""
from langchain_core.tools import tool
import random
from Battle.Attack import attack_logic
from Characters_intro import Relo
from Place.Map_A import world_map
from Monsters.Monsters import monster_distribution, get_monster_by_name


# --- 工具 1: 移动 ---
@tool
def move_tool(target_location: str):
    """
    当玩家想要移动去其他地方时调用。输入必须是地名，例如 "幽暗森林", "新手村"。
    """
    current_data = world_map.get(Relo.current_location)
    valid_targets = current_data.get("connects_to", [])

    if target_location in valid_targets:
        Relo.current_location = target_location
        # 顺便返回新地点的描述
        new_desc = world_map[target_location]["desc"]
        Relo.current_enemy = None  # 移动后脱离战斗（如果有的话）
        return f"✅ 成功移动到了 {target_location}。\n环境：{new_desc}"
    else:
        return f"❌ 无法移动。从 {Relo.current_location} 只能去：{', '.join(valid_targets)}。"


# --- 工具 2: 探索/徘徊 ---
@tool
def explore_tool():
    """
    当玩家想要在当前地点徘徊、探索、寻找怪物或宝物时调用。
    """
    location_name = Relo.current_location
    location_data = world_map.get(location_name)

    # 1. 安全区逻辑
    if location_data.get("safe_zone"):
        return f"你在 {location_name} 转了一圈。这里很安全，大家都在休息，什么也没发生。"

    # 2. 遭遇战逻辑 (简化版 Hover)
    encounter_rate = location_data.get("danger_level", 0.5)

    if random.random() < encounter_rate:
        # 抽怪逻辑
        spawn_key = location_data.get("spawn_table")
        if spawn_key:
            spawn_config = monster_distribution[spawn_key]
            monster_name = random.choices(list(spawn_config.keys()), list(spawn_config.values()))[0]

            # 【关键】把怪存入全局变量，进入“战斗状态”
            Relo.current_enemy = get_monster_by_name(monster_name)

            return f"⚠️ 遭遇敌袭！一只【{monster_name}】挡住了去路！(HP: {Relo.current_enemy['hp']})\n玩家进入战斗状态。"

    return "🍃 你四处搜寻了一番，除了一些枯枝败叶，什么也没发现。"


# --- 工具 3: 战斗 (单回合) ---
@tool
def combat_round_tool(action_type: str):
    """
    仅在战斗状态下使用。
    action_type: "attack" (攻击) 或 "flee" (逃跑)。
    """
    enemy = Relo.current_enemy
    player = Relo.hero

    if not enemy:
        return "🤔 此时四周无人，你对着空气挥舞了几下。（没有敌人）"

    if enemy['hp'] <= 0:
        Relo.current_enemy = None
        return f"敌人 {enemy['name']} 已经倒下了。战斗结束。"

    logs = []

    # === 玩家行动 ===
    if action_type == "attack":
        # 计算玩家伤害
        p_log = attack_logic(player, enemy, Relo.current_weapon)
        logs.append(f"【你的回合】\n{p_log}")

        if enemy['hp'] <= 0:
            Relo.current_enemy = None  # 战斗胜利，清空敌人
            # 结算经验
            exp_gain = enemy.get('exp', 0)
            player['exp'] += exp_gain
            return f"{p_log}\n🎉 胜利！你击败了 {enemy['name']}！获得 {exp_gain} 经验。"

    elif action_type == "flee":
        if random.random() < 0.5:
            Relo.current_enemy = None
            return "💨 你成功逃离了战斗！"
        else:
            logs.append("🚫 逃跑失败！被敌人拦住了！")

    # === 敌人反击 (如果还没死) ===
    if enemy['hp'] > 0:
        e_log = attack_logic(enemy, player, None)
        logs.append(f"\n【敌方回合】\n{e_log}")

        if player['hp'] <= 0:
            return f"{'\n'.join(logs)}\n💀 你被打败了... (HP归零)"

    return "\n".join(logs)
