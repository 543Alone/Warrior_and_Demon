# -*- coding: UTF-8 -*-
import json
import os
import sys
import time

from langchain_core.messages import HumanMessage
from langchain_xai import ChatXAI

llm = ChatXAI(
    model="grok-4-1-fast-reasoning-latest",
    temperature=0.3,  # 降低温度，确保 JSON 格式稳定
    api_key=os.getenv("XAI_API_KEY"),
)


def stream_print(text, speed=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)


def get_companion_action(companion, party, enemy):
    """
    让大模型为伙伴做决定，强制输出 JSON
    """
    # 提取局势信息
    party_status = []
    for p in party:
        if p['hp'] > 0:
            mp_str = f" | MP: {p['mp']}/{p['max_mp']}" if 'max_mp' in p else ""
            party_status.append(f"- {p['name']} (HP: {p['hp']}/{p['max_hp']}{mp_str})")

    enemy_status = f"- {enemy['name']} (HP: {enemy['hp']}/{enemy.get('max_hp', 100)})"

    available_skills = companion.get('skills', ['attack'])
    # 添加武器专属技能
    if companion.get('equipped_weapon') and 'weapon_skill' in companion['equipped_weapon']:
        if companion['equipped_weapon']['weapon_skill'] not in available_skills:
            available_skills.append(companion['equipped_weapon']['weapon_skill'])

    prompt = f"""
你现在扮演一名名叫【{companion['name']}】的冒险者伙伴。
你的职业是：{companion.get('job', '冒险者')}。
你的性格：{companion.get('personality', '忠诚可靠')}。

【当前战况】
友方存活：
{chr(10).join(party_status)}
敌方：
{enemy_status}

【你可用的技能 (技能消耗20MP, MP不足时只能选择attack)】
{json.dumps(available_skills, ensure_ascii=False)}

【指令】
请根据当前战况，从上述可用技能中选择**一个**动作，并选择一个目标。
你必须严格输出如下格式的 JSON，**绝对不能有任何多余的文字、Markdown标记或解释**。你的输出将被直接使用 json.loads() 解析：

{{
  "thought": "你的思考过程，比如：勇士血量很低，我需要治疗他。",
  "action": "heal",
  "target_name": "勇士",
  "dialogue": "吃我一记治愈术！振作点！"
}}

注意：
1. action 字段必须是你【可用的技能】中的一个！
2. target_name 必须是【友方】或【敌方】的准确名字！
3. dialogue 是你在执行动作时喊出的话，要符合你的性格。
"""

    print(f"[{companion['name']}] 正在思考战术...", end="", flush=True)

    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        content = response.content.strip()

        # 去除可能包含的 Markdown 标记
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]

        decision = json.loads(content.strip())
        print("\r" + " " * 30 + "\r", end="")  # 清除“正在思考战术”

        # 打印台词
        print(f"🗣️ {companion['name']}: “", end="")
        stream_print(decision.get('dialogue', '看招！'), speed=0.03)
        print("”")

        return decision

    except Exception as e:
        print("\r" + " " * 30 + "\r", end="")
        print(f"🗣️ {companion['name']}: “头有点痛... 还是直接攻击吧！”")
        # 默认回退动作
        return {
            "action": "attack",
            "target_name": enemy['name'],
            "dialogue": "头有点痛... 还是直接攻击吧！"
        }
