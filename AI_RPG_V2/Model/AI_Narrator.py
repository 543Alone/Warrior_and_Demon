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

# 加载 .env 文件中的环境变量
load_dotenv()
# print(os.getenv("XAI_API_KEY"))

llm = ChatXAI(
    model="grok-4-1-fast-reasoning-latest",
    temperature=0.7,
    max_retries=2,
    api_key=os.getenv("XAI_API_KEY"),  # 从环境变量中获取API密钥
)


def narrate_battle(log_text):
    """
    接收枯燥的战斗数据，输出精彩的战斗描写
    """
    if not log_text:
        return ""

    prompt = f"""
    你是一个奇幻小说的战斗解说员。
    请根据以下【系统日志】，写一段简短、激烈、有画面感的战斗描述（50字左右）。

    【要求】
    1. 必须包含关键数值（造成多少伤害、剩余多少血）。
    2. 不要单纯翻译日志，要加入动作描写（挥剑、格挡、鲜血飞溅）。
    3. 如果是 Miss 或 闪避，要描写得很尴尬或很灵巧。

    【系统日志】：
    {log_text}
    """

    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content
    except Exception as e:
        return f"(AI 排线了，显示原始日志)\n{log_text}"
