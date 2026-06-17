# -*- coding: UTF-8 -*-
from RPG.Warehouse.Items import items_list
from RPG.Warehouse.Weapons import weapons_list
from RPG.Warehouse.Armor import armors_list
from RPG.Characters_intro import Relo
from RPG.Setting.Style import Colors

def get_shop_items():
    # 商店出售基础物品和少量武器防具
    shop_inventory = []
    # 找点补给药
    for item in items_list:
        if item["name"] in ["🍎 小苹果", "🧪 强效治疗药水", "🍗 烤鸡腿"]:
            shop_inventory.append(item.copy())
    # 找点初级武器
    for w in weapons_list:
        if w["quality"] == "common":
            shop_inventory.append(w.copy())
    # 找点初级防具
    for a in armors_list:
        if a.get("quality") == "common":
            shop_inventory.append(a.copy())
    return shop_inventory

def buy_menu(player):
    shop_inventory = get_shop_items()
    while True:
        print(f"\n{Colors.YELLOW}=== 🛒 道具店 ==={Colors.END}")
        print(f"💰 你的金币: {player.get('gold', 0)}")
        print("老板：随便看随便挑，概不赊账！")
        print("-" * 30)
        
        for i, item in enumerate(shop_inventory):
            price = item.get("price", 999)
            print(f"[{i+1}] {item['name']} - 💰 {price} G")
            print(f"    描述: {item.get('desc', '')}")
            
        print("-" * 30)
        choice = input("输入商品编号购买 (输入 0 离开): ")
        
        if choice == '0':
            print("老板：慢走不送！")
            break
            
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(shop_inventory):
                item = shop_inventory[idx]
                price = item.get("price", 999)
                
                if player.get('gold', 0) >= price:
                    player['gold'] -= price
                    player['bag'].append(item.copy())
                    print(f"✅ 购买成功！获得了 [{item['name']}]。剩余金币: {player['gold']}")
                else:
                    print(f"❌ 钱不够！别来捣乱！")
            else:
                print("❌ 没有这件商品！")

def sell_menu(player):
    while True:
        print(f"\n{Colors.YELLOW}=== 💰 收购处 ==={Colors.END}")
        print(f"💰 你的金币: {player.get('gold', 0)}")
        print("老板：只要是值钱的东西，我这里统统半价回收！")
        print("-" * 30)
        
        # 整理背包，为了防止索引错乱，同时标记出被装备的物品
        sellable_items = []
        for original_idx, item in enumerate(player['bag']):
            is_equipped = False
            # 判断是否是当前装备
            if item is Relo.current_weapon or item is Relo.current_armor:
                is_equipped = True
                
            sellable_items.append({
                "real_index": original_idx,
                "item": item,
                "is_equipped": is_equipped
            })
            
        if not sellable_items:
            print(" (背包空空如也)")
        else:
            for i, info in enumerate(sellable_items):
                item = info["item"]
                sell_price = item.get("price", 10) // 2 # 半价回收
                equipped_tag = f"{Colors.RED}[装备中 - 不可售卖]{Colors.END}" if info["is_equipped"] else f"(售价: 💰 {sell_price} G)"
                print(f"[{i+1}] {item['name']} {equipped_tag}")
                
        print("-" * 30)
        choice = input("输入要出售的物品编号 (输入 0 离开): ")
        
        if choice == '0':
            print("老板：欢迎下次光临！")
            break
            
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(sellable_items):
                info = sellable_items[idx]
                if info["is_equipped"]:
                    print("❌ 你正穿着这件装备呢！必须先卸下（换上别的）才能卖！")
                else:
                    item = info["item"]
                    sell_price = item.get("price", 10) // 2
                    player['gold'] = player.get('gold', 0) + sell_price
                    # 从背包真实索引中移除
                    # 为了安全，直接用 python list remove，但因为字典一样，最好按引用或者索引移除
                    player['bag'].pop(info["real_index"])
                    print(f"✅ 卖出了 [{item['name']}]，获得 💰 {sell_price} G。")
            else:
                print("❌ 无效的编号！")
