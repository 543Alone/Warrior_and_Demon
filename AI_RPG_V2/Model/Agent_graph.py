# -*- coding: UTF-8 -*-
"""
@Project ：Warrior_and_Demon 
@File    ：Agent_graph.py
@IDE     ：PyCharm 
@Author  ：Write Bug
@Date    ：2025/12/18 10:05
AI自己玩游戏
"""
import os
from dotenv import load_dotenv

# --- LangGraph & LangChain 核心组件 ---
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import SystemMessage, HumanMessage
# 这里复用你在 AI_Narrator.py 里用的 ChatXAI，也可以换成 ChatOpenAI
from langchain_xai import ChatXAI

# --- 引入你项目现有的文件 ---
from Agent_state import AgentState
from Agent_tools import move_tool, explore_tool, combat_round_tool
from Characters_intro import Relo  # 用来读取实时血量等信息注入给 AI

# 加载环境变量 (API Key)
load_dotenv()

# 1. 初始化 LLM
# 注意：Temperature 设低一点 (0.1~0.3)，让 AI 决策更稳定，不要在战斗时胡言乱语
llm = ChatXAI(
    model="grok-4-1-fast-reasoning-latest",  # 或者 "grok-beta"
    temperature=0.2,
    api_key=os.getenv("XAI_API_KEY")
)

# 2. 绑定工具
# AI 可以使用的所有动作
tools = [move_tool, explore_tool, combat_round_tool]
llm_with_tools = llm.bind_tools(tools)


# 3. 定义 Agent 节点逻辑
def agent_node(state: AgentState):
    """
    Agent 的大脑。接收当前对话历史，输出下一步动作（或回复）。
    """
    # 动态生成 System Prompt，让 AI 实时知道自己的状态
    # 这一步很重要，否则 AI 不知道自己快死了，也不会喝药
    sys_msg = SystemMessage(content=f"""
    你现在是文字 RPG 游戏《勇士与魔王》中的玩家。
    你的终极目标是：提升等级，收集装备，最后前往【魔王城】击败魔王。

    【当前状态】
    - 角色: {Relo.hero['name']}
    - HP: {Relo.hero['hp']}/{Relo.hero['max_hp']}
    - 等级: {Relo.hero['level']}
    - 当前位置: {Relo.current_location}
    - 敌人状态: {'遭遇敌袭！' if Relo.current_enemy else '无'}

    【决策指南】
    1. 如果血量低于 30%，优先寻找回复手段。
    2. 如果当前地点探索完毕，尝试使用 move_tool 去新地方。
    3. 如果遇到敌人，使用 combat_round_tool 战斗。
    4. 不要总是闲聊，要采取行动。
    """)

    # 构造消息列表：SystemPrompt + 历史记录
    messages = [sys_msg] + state["messages"]

    # 调用 LLM
    response = llm_with_tools.invoke(messages)

    # 返回更新后的状态
    return {"messages": [response]}


# 4. 构建 Graph
builder = StateGraph(AgentState)

# 添加节点
builder.add_node("agent", agent_node)
builder.add_node("tools", ToolNode(tools))

# 设置连线
builder.add_edge(START, "agent")

# 条件边：如果 Agent 决定调用工具 -> 去 tools 节点；如果 Agent 决定说话/结束 -> 结束
builder.add_conditional_edges(
    "agent",
    tools_condition,
)

# 工具执行完后，必须跳回 Agent 继续思考
builder.add_edge("tools", "agent")

# 编译图
graph = builder.compile()


# --- 运行部分的辅助函数 ---
def run_game_agent():
    print("🤖 AI 代理已启动... 正在初始化游戏...")

    # 初始输入
    initial_input = {"messages": [HumanMessage(content="游戏开始！请检查当前状态并开始冒险。")]}

    # 流式输出，观察 AI 的操作
    for event in graph.stream(initial_input, stream_mode="values"):
        # 取出最新的一条消息打印
        if "messages" in event:
            last_msg = event["messages"][-1]

            # 打印 AI 的思考 (content)
            if last_msg.content:
                print(f"\n🧠 [AI 思考]: {last_msg.content}")

            # 打印工具调用详情 (如果有)
            if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
                for call in last_msg.tool_calls:
                    print(f"🔧 [调用工具]: {call['name']} -> {call['args']}")

            # 打印工具的执行结果 (ToolMessage)
            if last_msg.type == "tool":
                print(f"📄 [工具返回]: {last_msg.content}")


if __name__ == "__main__":
    run_game_agent()