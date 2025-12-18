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

from AI_RPG_V2.Characters_intro import Relo

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


def load_game():
    """读取游戏"""
    if not os.path.exists(SAVE_FILE):
        print("\n❌ 未找到存档文件。")
        return False

    try:
        with open(SAVE_FILE, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)

        # 覆盖当前全局状态
        # 注意：这里我们用 update 更新字典，而不是直接替换变量，这样可以保持引用
        Relo.hero.update(loaded_data["hero_data"])
        Relo.current_location = loaded_data["location"]

        print(f"\n📂 读档成功！欢迎回到 {Relo.current_location}，{Relo.hero['name']} (Lv.{Relo.hero['level']})")
        return True
    except Exception as e:
        print(f"❌ 读档文件损坏或格式错误: {e}")
        return False
