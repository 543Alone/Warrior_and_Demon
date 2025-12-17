# -*- coding: UTF-8 -*-
"""
@Project ：LangGraph 
@File    ：Use_items.py
@IDE     ：PyCharm 
@Author  ：Write Bug
@Date    ：2025/12/12 10:18 
"""


def use_item(player, item_index):
    """
    使用背包的物品
    :param player:
    :param item_index:
    :return:
    """
    if item_index < 0 or item_index >= len(player['bag']):
        print("❌ 找不到这个物品。")
        return False

    item = player['bag'][item_index]
    item_type = item.get('type', 'unknown')

    if 'atk' in item or 'def' in item:
        print(f"⚔️ 这是装备 [{item['name']}]，请在菜单输入 '3,e' 进入装备界面来穿戴。")
        return  False

    # 如果是回血道具
    elif item_type == 'heal':
        if player['hp'] >= player['max_hp']:
            print("❌ 你现在精神焕发，吃不下了！")
            return False
        recover_val = item.get('value', 0)
        old_hp = player['hp']

        # 防止溢出
        player['hp'] = min(player['max_hp'], old_hp + recover_val)
        print(f"😋 你吃掉了 [{item['name']}]")
        print(f"   💚 {player['name']} 恢复 {recover_val} 点生命值！(当前生命值: {player['hp']}/{player['max_hp']})")
        # 移除道具
        player['bag'].pop(item_index)
        return True

    # 咖啡效果
    elif item_type == 'special':
        # 移除技能效果
        for effect in ['sleep', 'paralyze']:
            if effect in player:
                player.pop(effect)
                print(f"   ❌ {player['name']} 的技能效果 {effect} 已解除。")
        # 移除道具
        player['bag'].pop(item_index)
        return True

    # 力量药剂
    elif item_type == 'buff_atk':
        # 添加buff效果，将在战斗中持续多个回合
        if 'buffs' not in player:
            player['buffs'] = []
        
        buff = {
            'name': '力量药剂',
            'type': 'atk',
            'value': item['value'],
            'duration': item['duration']
        }
        player['buffs'].append(buff)
        print(f"   💪 {player['name']} 获得了力量药剂效果！(攻击力+{item['value']}, 持续{item['duration']}回合)")
        # 移除道具
        player['bag'].pop(item_index)
        return True