# -*- coding: UTF-8 -*-
"""
@Project ：LangGraph 
@File    ：Use_items.py
@IDE     ：PyCharm 
@Author  ：Write Bug
@Date    ：2025/12/12 10:18 
"""

def use_item(player, item_index, enemy=None):
    """
    使用背包的物品
    :param player: 玩家对象
    :param item_index: 物品在背包的索引
    :param enemy: 敌方对象，用于攻击性道具
    """
    if item_index < 0 or item_index >= len(player['bag']):
        print("❌ 找不到这个物品。")
        return False

    item = player['bag'][item_index]
    item_type = item.get('type', 'unknown')

    # 1. 装备类
    if 'atk' in item or 'def' in item:
        print(f"⚔️ 这是装备 [{item['name']}]，请在菜单输入 '3,e' 进入装备界面来穿戴。")
        return False

    used_success = False

    # 2. 回血类 (Heal)
    if item_type == 'heal':
        if player['hp'] >= player['max_hp']:
            print("❌ 你现在精神焕发，吃不下了！")
            return False

        recover = item.get('value', 0)
        player['hp'] = min(player['max_hp'], player['hp'] + recover)
        print(f"😋 你吃掉了 [{item['name']}]")
        print(f"   💚 恢复 {recover} 点生命 (HP: {player['hp']}/{player['max_hp']})")
        used_success = True

    # 3. 净化类 (Coffee) ->StatusSystem
    elif item_type == 'special':
        removed = []
        # 检查新版状态系统
        if 'statuses' in player:
            # 定义咖啡能解的状态：睡眠、麻痹、冰冻
            target_effects = ['sleep', 'paralyze', 'freeze']
            # 找出玩家当前有的这些状态
            to_remove = [k for k in player['statuses'] if k in target_effects]

            for k in to_remove:
                del player['statuses'][k]
                removed.append(k)

        if removed:
            print(f"   ☕ 喝下 [{item['name']}]，精神抖擞！解除了: {','.join(removed)}")
        else:
            print(f"   ☕ 喝下 [{item['name']}]，味道不错，但好像没发生什么特别的。")

        used_success = True

    # 4. Buff 类 (力量/敏捷)
    elif item_type.startswith('buff_'):
        if 'buffs' not in player: player['buffs'] = []

        # 解析类型：buff_atk -> atk, buff_hit -> hit
        buff_type = item_type.split('_')[1]
        real_duration = item.get('duration', 3)

        # 构造 Buff 对象
        buff = {
            'name': item['name'],
            'type': buff_type,
            'value': item['value'],
            'duration': real_duration + 1 # +1 抵消当回合消耗
        }
        player['buffs'].append(buff)

        desc = "攻击力" if buff_type == 'atk' else "命中率"
        val_str = f"+{item['value']}" if buff_type == 'atk' else f"+{int(item['value']*100)}%"

        print(f"   🧪 咕嘟咕嘟... [{item['name']}] 生效！")
        print(f"   ✨ {desc} {val_str} (持续 {real_duration} 回合)")
        used_success = True

        print(f"   💪 {player['name']} 获得了 {item['name']} 效果！(攻击力+{item['value']}, 持续{real_duration}回合)")
    # 5. 伤害类 (Grenade)
    elif item_type == 'damage':
        if enemy is None:
            print("❌ 这个东西只能在战斗中对着敌人用！")
            return False

        dmg = item.get('value', 50)
        enemy['hp'] -= dmg
        if enemy['hp'] < 0: enemy['hp'] = 0

        print(f"   🧨 既然不用瞄准... 去吧！[{item['name']}]！")
        print(f"   💥 轰！！！对手被炸得灰头土脸，受到 {dmg} 点伤害！")
        used_success = True

    # 未知物品
    else:
        print(f"❌ 暂时无法使用 [{item['name']}]")
        return False

    # 扣除逻辑
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