# -*- coding: UTF-8 -*-
"""
@Project ：Warrior_and_Demon 
@File    ：AI_Narrator.py
@IDE     ：PyCharm 
@Author  ：Write Bug
@Date    ：2025/12/17 16:58 
"""
import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_xai import ChatXAI

load_dotenv()

llm = ChatXAI(
    model="grok-4-1-fast-reasoning-latest",
    temperature=0.9,  # 调高创造力
    api_key=os.getenv("XAI_API_KEY"),
)


def narrate_battle(log_text):
    if not log_text:
        return ""

    prompt = f"""
    【角色设定】你是一位热血奇幻小说的金牌作家。
    【任务】根据下方的【战斗数据】，写一段 50字以内 的精彩打斗描写。

    【要求】
    1. 动作感：不要只写“造成了伤害”，要写“剑锋划破空气”、“重重砸在盾牌上”。
    2. 画面感：加入光影、声音、血液等细节描写。
    3. 准确性：如果数据里有“暴击”，描述必须震撼；如果是“Miss”，描述要滑稽或惊险。
    4. 结尾：必须包含 (造成xx点伤害) 或 (剩余HP:xx) 的数值提示。

    【战斗数据】：
    {log_text}
    """

    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content
    except Exception as e:
        return f"（AI 描写生成失败，直接显示日志）\n{log_text}"
