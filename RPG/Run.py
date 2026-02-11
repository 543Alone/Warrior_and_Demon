# -*- coding: UTF-8 -*-
"""
@Project ：LangGraph 
@File    ：Run.py
@IDE     ：PyCharm 
@Author  ：Write Bug
@Date    ：2025/12/10 09:43 
"""
import sys
import os
# 将父目录加入环境变量，这样就能识别 'RPG.' 开头的导入了
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Battle import Round

if __name__ == '__main__':
    Round.main_game_loop()


