# -*- coding: UTF-8 -*-
"""
@Project ：Warrior_and_Demon 
@File    ：text_api.py
@IDE     ：PyCharm 
@Author  ：Write Bug
@Date    ：2025/12/18 10:16 
"""
# test_ai.py
import os
from dotenv import load_dotenv
from langchain_xai import ChatXAI
from langchain_core.messages import HumanMessage

# 1. 加载环境变量
load_dotenv()
api_key = os.getenv("XAI_API_KEY")

print(f"🔑 检查 Key: {api_key[:5]}******" if api_key else "❌ 未找到 API Key！请检查 .env 文件位置")

# 2. 尝试调用
if api_key:
    try:
        llm = ChatXAI(
            model="grok-4-1-fast-reasoning-latest",
            api_key=api_key
        )
        print("🚀 正在发送请求给 xAI...")
        res = llm.invoke([HumanMessage(content="你好，如果你能听到我，请回复'收到'。")])
        print(f"✅ 成功: {res.content}")
    except Exception as e:
        print(f"❌ 调用失败: {e}")
