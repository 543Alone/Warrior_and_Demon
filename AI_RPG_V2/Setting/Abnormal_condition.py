# -*- coding: UTF-8 -*-
"""
@Project ：LangGraph 
@File    ：Abnormal_condition.py
@IDE     ：PyCharm 
@Author  ：Write Bug
@Date    ：2025/12/12 09:29 
"""

import random


class StatusSystem:
    """
    异常状态管理器
    """

    # 定义所有支持的状态类型及其对应的中文名（用于显示）
    CONFIG = {
        # 持续伤害 (DOT)
        "burn": {"name": "🔥 灼烧", "type": "dot", "value": 10, "duration": 3},
        "poison": {"name": "🤢 中毒", "type": "dot", "value": 0.05, "is_percent": True, "duration": 4},
        "decay": {"name": "💀 凋零", "type": "dot", "value": 0.08, "is_percent": True, "duration": 3},

        # 控制 (Control)
        "freeze": {"name": "❄️ 冰冻", "type": "hard_cc", "duration": 2},  # 硬控：必跳过回合
        "paralyze": {"name": "⚡ 麻痹", "type": "soft_cc", "chance": 0.5, "duration": 3},  # 软控：50%几率跳过

        # 增益 (Buff/HOT)
        "regen": {"name": "🌿 持续恢复", "type": "hot", "value": 20, "duration": 3},
    }

    @staticmethod
    def apply_status(target, status_key):
        """施加状态"""
        if status_key not in StatusSystem.CONFIG:
            return False

        cfg = StatusSystem.CONFIG[status_key]
        if 'statuses' not in target:
            target['statuses'] = {}

        # 逻辑：已有状态则刷新时间并叠加层数(部分状态不可叠加层数可在此限制)
        if status_key in target['statuses']:
            target['statuses'][status_key]['duration'] = cfg['duration']
            target['statuses'][status_key]['stack'] += 1
            print(f"   {cfg['name']} 效果加深！(层数: {target['statuses'][status_key]['stack']})")
        else:
            target['statuses'][status_key] = {'stack': 1, 'duration': cfg['duration']}
            print(f"   {target['name']} 陷入了 {cfg['name']} 状态！")
        return True

    @staticmethod
    def resolve_turn_end(character):
        """回合结束结算"""
        if 'statuses' not in character or not character['statuses']:
            return []

        logs = []
        name = character['name']

        # 复制 keys 防止遍历时删除报错
        current_statuses = list(character['statuses'].keys())

        for key in current_statuses:
            state = character['statuses'][key]
            cfg = StatusSystem.CONFIG.get(key, {})

            # --- DOT (伤害) ---
            if cfg.get('type') == 'dot':
                dmg = 0
                if cfg.get('is_percent'):
                    # 百分比伤害 (最大生命值 * 百分比 * 层数)
                    base_dmg = character['max_hp'] * cfg['value']
                    dmg = int(base_dmg * state['stack'])
                else:
                    # 固定伤害
                    dmg = state['stack'] * cfg['value']

                character['hp'] -= dmg
                logs.append(f"{cfg['name']} 侵蚀着身体，造成 {dmg} 点伤害")

            # --- HOT (恢复) ---
            elif cfg.get('type') == 'hot':
                heal = state['stack'] * cfg['value']
                character['hp'] = min(character['max_hp'], character['hp'] + heal)
                logs.append(f"{cfg['name']} 滋润着身体，恢复 {heal} 点生命")

            # --- 减少持续时间 ---
            state['duration'] -= 1
            if state['duration'] <= 0:
                del character['statuses'][key]
                logs.append(f"{name} 的 {cfg['name']} 状态消散了。")

        if character['hp'] < 0: character['hp'] = 0
        return logs

    @staticmethod
    def check_control(character):
        """
        检查控制状态
        :return: (is_skip_turn, message)
        """
        if 'statuses' not in character:
            return False, ""

        statuses = character['statuses']

        # 1. 检查冰冻 (Hard CC) - 100% 跳过
        if 'freeze' in statuses:
            return True, f"❄️ {character['name']} 被冻成了冰雕，无法动弹！"

        # 2. 检查麻痹 (Soft CC) - 50% 跳过
        if 'paralyze' in statuses:
            if random.random() < StatusSystem.CONFIG['paralyze']['chance']:
                return True, f"⚡ {character['name']} 全身麻痹，动弹不得！"
            else:
                # 麻痹但没触发，可以行动，但提示一下
                print(f"   ⚡ {character['name']} 强忍着麻痹感行动了！")

        return False, ""

    @staticmethod
    def clear_status(character):
        """战斗结束后清理临时状态 (可选)"""
        if 'statuses' in character:
            character['statuses'] = {}

