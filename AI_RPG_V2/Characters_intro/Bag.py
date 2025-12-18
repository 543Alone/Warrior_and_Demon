# -*- coding: UTF-8 -*-
"""
@Project ：LangGraph 
@File    ：Bag.py
@IDE     ：PyCharm 
@Author  ：Write Bug
@Date    ：2025/12/10 17:02 
"""
from Warehouse.Weapons import weapons_list
from Warehouse.Armor import armors_list
from Warehouse.Items import items_list

def get_item_data_by_name(item_name):
    # 搜索武器库
    for w in weapons_list:
        if w['name'] == item_name: return w
    # 搜索防具库
    for a in armors_list:
        if a['name'] == item_name: return a
    # 搜索物品库
    for i in items_list:
        if i['name'] == item_name: return i
    return None

def add_item_to_bag(player, new_item):
    """
    如果背包里已经有了，就数量+1；如果没有，就追加。
    """

    item_to_store = new_item.copy()

    # 确保有 quantity 字段
    if 'quantity' not in item_to_store:
        item_to_store['quantity'] = 1

    # 检查背包里是否已有同名物品
    for item in player['bag']:
        if item['name'] == new_item['name']:
            # 找到数量相加
            # 如果旧物品还没quantity字段，默认视为1
            current_qty = item.get('quantity', 1)
            # 获取新物品的数量（通常是1，但也可能是掉落了5个）
            add_qty = item_to_store.get('quantity', 1)

            item['quantity'] = current_qty + add_qty
            print(f"   🎒 {item['name']} 数量 +{add_qty} (当前: {item['quantity']})")
            return

    # 没找到，将拷贝后的对象放入背包
    player['bag'].append(item_to_store)
    print(f"   🎒 获得新物品: {item_to_store['name']}")