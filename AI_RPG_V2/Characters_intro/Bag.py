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
