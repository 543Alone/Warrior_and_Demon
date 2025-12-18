# -*- coding: UTF-8 -*-
"""
@Project ：Warrior_and_Demon 
@File    ：SaveSystem.py
@IDE     ：PyCharm 
@Author  ：Write Bug
@Date    ：2025/12/18 10:57 
"""
import json
import os

from Characters_intro import Relo
from Characters_intro.Bag import get_item_data_by_name

SAVE_FILE = "save_data.json"


def save_game():
    """保存游戏：将 hero 字典和当前位置写入文件"""
    data_to_save = {
        "hero_data": Relo.hero,
        "location": Relo.current_location
    }

    try:
        with open(SAVE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=4)
        print(f"\n💾 存档成功！数据已保存至 {SAVE_FILE}")
        return True
    except Exception as e:
        print(f"❌ 存档失败: {e}")
        return False


def _refresh_item_data(item_dict):
    """
    根据名字从原始数据库中重新获取物品数据。
    防止读档后物品变成“死数据”或丢失属性。
    """
    if not isinstance(item_dict, dict) or 'name' not in item_dict:
        return item_dict

    name = item_dict['name']
    # 从游戏原始库里找这个物品
    real_item = get_item_data_by_name(name)

    if real_item:
        # 拿到最新的物品数据副本（此时 quantity 通常是默认值）
        new_item = real_item.copy()

        # 从存档数据(item_dict)中提取数量，覆盖回去
        # 如果存档里没存quantity，默认是1
        saved_quantity = item_dict.get('quantity', 1)
        new_item['quantity'] = saved_quantity

        return new_item
    else:
        # 没找到（可能是绝版物品），就凑合用存档里的旧数据
        return item_dict


def load_game():
    """读取游戏"""
    if not os.path.exists(SAVE_FILE):
        print("\n❌ 未找到存档文件。")
        return False

    try:
        with open(SAVE_FILE, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)

        hero_data = loaded_data["hero_data"]

        # 刷新背包里的所有物品
        if 'bag' in hero_data:
            refreshed_bag = []
            for item in hero_data['bag']:
                # 把存档里的旧数据换成游戏里的新数据
                refreshed_bag.append(_refresh_item_data(item))
            hero_data['bag'] = refreshed_bag

        # 刷新身上穿的装备
        if 'equipped_weapon' in hero_data:
            hero_data['equipped_weapon'] = _refresh_item_data(hero_data['equipped_weapon'])

        if 'equipped_armor' in hero_data:
            hero_data['equipped_armor'] = _refresh_item_data(hero_data['equipped_armor'])

        # 更新全局状态
        Relo.hero.update(hero_data)
        Relo.current_location = loaded_data["location"]

        print(f"\n📂 读档成功！欢迎回到 {Relo.current_location}，{Relo.hero['name']} (Lv.{Relo.hero['level']})")
        return True
    except Exception as e:
        print(f"❌ 读档出错 (可能是存档版本过旧): {e}")
        return False
