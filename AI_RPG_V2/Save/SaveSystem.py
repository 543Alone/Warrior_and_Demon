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
        "party_data": Relo.party,
        "reserve_party_data": Relo.reserve_party,
        "defeated_bosses": Relo.defeated_bosses,
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

        # 恢复动态数据 (数量、锻造词条等)
        if 'quantity' in item_dict:
            new_item['quantity'] = item_dict['quantity']
        if 'affixes' in item_dict:
            new_item['affixes'] = item_dict['affixes']
        if 'forge_count' in item_dict:
            new_item['forge_count'] = item_dict['forge_count']

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

        # 兼容旧版本存档
        if "hero_data" in loaded_data and "party_data" not in loaded_data:
            party_data = [loaded_data["hero_data"]]
        else:
            party_data = loaded_data.get("party_data", [])

        refreshed_party = []
        for char_data in party_data:
            # 刷新背包里的所有物品
            if 'bag' in char_data:
                refreshed_bag = []
                for item in char_data['bag']:
                    refreshed_bag.append(_refresh_item_data(item))
                char_data['bag'] = refreshed_bag

            # 刷新身上穿的装备
            if 'equipped_weapon' in char_data:
                char_data['equipped_weapon'] = _refresh_item_data(char_data['equipped_weapon'])

            if 'equipped_armor' in char_data:
                char_data['equipped_armor'] = _refresh_item_data(char_data['equipped_armor'])

            refreshed_party.append(char_data)

        refreshed_reserve = []
        for char_data in loaded_data.get("reserve_party_data", []):
            if 'bag' in char_data:
                char_data['bag'] = [_refresh_item_data(item) for item in char_data['bag']]
            if 'equipped_weapon' in char_data:
                char_data['equipped_weapon'] = _refresh_item_data(char_data['equipped_weapon'])
            if 'equipped_armor' in char_data:
                char_data['equipped_armor'] = _refresh_item_data(char_data['equipped_armor'])
            refreshed_reserve.append(char_data)

        # 更新全局状态
        Relo.party = refreshed_party
        Relo.reserve_party = refreshed_reserve
        Relo.defeated_bosses = loaded_data.get("defeated_bosses", [])

        if len(Relo.party) > 0:
            Relo.hero.update(Relo.party[0])  # 保持 Relo.hero 引用指向队长
            Relo.party[0] = Relo.hero  # 确保列表中存的是那个字典对象

        Relo.current_location = loaded_data.get("location", "新手村")

        print(f"\n📂 读档成功！欢迎回到 {Relo.current_location}，{Relo.hero['name']} (Lv.{Relo.hero.get('level', 1)})")
        return True
    except Exception as e:
        print(f"❌ 读档出错 (可能是存档版本过旧): {e}")
        return False
