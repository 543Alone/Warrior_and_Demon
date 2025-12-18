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
        return False

    used_success = False
    # 如果是回血道具
    if item_type == 'heal':
        if player['hp'] >= player['max_hp']:
            print("❌ 你现在精神焕发，吃不下了！")
            return False

        recover_val = item.get('value', 0)
        old_hp = player['hp']

        # 防止溢出
        player['hp'] = min(player['max_hp'], old_hp + recover_val)

        print(f"😋 你吃掉了 [{item['name']}]")
        print(f"   💚 {player['name']} 恢复 {recover_val} 点生命值！(当前生命值: {player['hp']}/{player['max_hp']})")
        used_success = True

    # 咖啡效果
    elif item_type == 'special':
        # 移除技能效果
        removed_effects = []
        for effect in ['sleep', 'paralyze']:
            if effect in player:
                player.pop(effect)
                removed_effects.append(effect)

        if removed_effects:
            print(f"   ☕ 喝下 [{item['name']}]，精神抖擞！解除了: {','.join(removed_effects)}")
        else:
            print(f"   ☕ 喝下 [{item['name']}]，味道不错，但好像没发生什么特别的。")

        used_success = True

    # 力量药剂
    elif item_type == 'buff_atk':
    # 添加buff效果，将在战斗中持续多个回合
        if 'buffs' not in player:
            player['buffs'] = []

        # ⚡ 关键修改：duration + 1，抵消喝药回合的损耗
        real_duration = item.get('duration', 3)

        buff = {
            'name': item['name'],  # 使用物品名作为buff名
            'type': 'atk',
            'value': item['value'],
            'duration': real_duration + 1
        }
        player['buffs'].append(buff)

        print(f"   💪 {player['name']} 获得了 {item['name']} 效果！(攻击力+{item['value']}, 持续{real_duration}回合)")
        used_success = True

    # 其他未知物品
    else:
        print(f"❌ 暂时无法使用 [{item['name']}]")
        return False

    # 扣除数量逻辑 🔻
    if used_success:
        # 如果物品有 quantity 属性且大于 1，则减 1
        current_qty = item.get('quantity', 1)
        if current_qty > 1:
            item['quantity'] = current_qty - 1
            print(f"   (背包里还剩 {item['quantity']} 个 {item['name']})")
        else:
            # 数量为 1，或者没写数量，直接移除
            player['bag'].pop(item_index)

    return used_success
