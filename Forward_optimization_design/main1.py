import numpy as np
from collections import defaultdict
from MetaSet import advancedStructure as adv
import MetaSet as ms
import importlib.util
import importlib.util
from time import time
import os
import optuna
import sqlite3

spec = importlib.util.spec_from_file_location("lumapi", "D:\\Program Files\\Lumerical\\v241\\api\\python\\lumapi.py")
lumapi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lumapi)

# 确定一个单独的、确定的baseValue

# 扫描现有数据库，确定缺位，形成任务目录

# 获取当前文件所在脚本的上一级（主目录）路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')  # 如果当前脚本在子项目中
DB_PATH = os.path.join(DATA_DIR, 'structures.db')

# 连接数据库
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()


# 将任务目录分为几份并行优化填充相位色散库；在单个并行中只打开一次FDTD窗口


study = optuna.create_study(direction="minimize")
study.optimize(objective, n_trials=3)