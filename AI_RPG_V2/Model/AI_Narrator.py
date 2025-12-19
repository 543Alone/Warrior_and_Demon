# -*- coding: UTF-8 -*-
"""
@Project ：Warrior_and_Demon 
@File    ：AI_Narrator.py
@IDE     ：PyCharm 
@Author  ：Write Bug
@Date    ：2025/12/17 16:58 
"""
import os
import sys
import time

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_xai import ChatXAI

load_dotenv()

llm = ChatXAI(
    model="grok-4-1-fast-reasoning-latest",
    temperature=0.9,  # 调高创造力
    api_key=os.getenv("XAI_API_KEY"),
)


def narrate_battle(log_text, player, enemy):
    if not log_text:
        return ""

    # 计算血量百分比
    p_hp_pct = (player['hp'] / player['max_hp']) * 100
    # 防止分母为0（不太可能）
    e_max = enemy.get('max_hp', 100)
    e_hp_pct = (enemy['hp'] / e_max) * 100 if e_max > 0 else 0

    # 生成战况提示
    context_hint = "战斗正酣，双方势均力敌。"

    # 逻辑 A: 碾压局 (玩家血量 > 80% 且 敌人血量 < 30%)
    if p_hp_pct > 80 and e_hp_pct < 30:
        context_hint = f"【碾压局面】玩家毫发无伤，气势如虹。敌人({enemy['name']})身受重伤，眼神中流露出极度的恐惧和绝望，动作开始变形。"

    # 逻辑 B: 险胜/苦战 (玩家血量 < 20%)
    elif p_hp_pct < 20:
        context_hint = "【生死一线】玩家已经是强弩之末，浑身是血，视线模糊。这每一次攻击都是凭借意志力挥出的绝地反击，充满悲壮感。"

    # 逻辑 C: 敌人濒死 (敌人血量 < 10%)
    elif e_hp_pct < 10:
        context_hint = f"【斩杀前奏】敌人({enemy['name']})已经是风中残烛，只剩下最后一口气，它的防守已经溃散。"

    prompt = f"""
    【角色设定】你是一位西方魔法世界小说的金牌作家。
    【任务】根据下方的【战斗数据】，写一段 100字以内 的精彩打斗描写。
    
    【当前战局】：{context_hint}

    【要求】
    1. 动作感：不要只写“造成了伤害”，要写“剑锋划破空气”、“重重砸在盾牌上”。
    2. 画面感：加入光影、声音、血液等细节描写。
    3. 准确性：如果数据里有“暴击”，描述必须震撼；如果是“Miss”，描述要滑稽或惊险。
    4. 情绪共鸣：**必须**体现【当前战局】中描述的氛围（如敌人的恐惧、玩家的绝望反击）。
    5. 结尾：必须包含 (造成xx点伤害) 或 (剩余HP:xx) 的数值提示。

    【战斗数据】：
    {log_text}
    """

    try:
        full_response = ""
        # 实时流式输出
        for chunk in llm.stream([HumanMessage(content=prompt)]):
            content = chunk.content
            if content:
                stream_print(content, speed=0.02)
                full_response += content
        print("\n")
        return full_response
    except Exception as e:
        print(f"Error:{e}")
        return log_text


def stream_print(text, speed=0.03):
    """
    流式输出
    :param text: 文本
    :param speed: 输出速度
    :return:
    """
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)


def generate_monster_intro(monster_name):
    """
    专门用于流式生成怪物开场白
    """
    prompt = f"你扮演一只{monster_name}，对勇者说一句只有20字的挑衅台词，语气要符合该怪物的特征（比如凶狠、阴险或呆萌）。不要带引号。"

    # 先打印名字前缀，不换行 (end="")
    print(f"👿 {monster_name}: “", end="")
    sys.stdout.flush()

    full_text = ""
    try:
        # 使用流式接口
        for chunk in llm.stream([HumanMessage(content=prompt)]):
            content = chunk.content
            if content:
                # 调用打字机效果，速度稍微慢一点更有压迫感 (0.05)
                stream_print(content, speed=0.05)
                full_text += content
    except Exception as e:
        print(f"(吼叫声卡住了...) {e}")

    # 打印结束的引号并换行
    print("”\n")
    return full_text
