import numpy as np
from collections import defaultdict
from MetaSet import advancedStructure as adv
import MetaSet as ms
import importlib.util
import importlib.util
from time import time
import os
import optuna

spec = importlib.util.spec_from_file_location("lumapi", "D:\\Program Files\\Lumerical\\v241\\api\\python\\lumapi.py")
lumapi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lumapi)

# 确定一个单独的、确定的baseValue
# 扫描现有数据库，确定缺位，形成任务目录
# 将任务目录分为几份并行优化填充相位色散库；在单个并行中只打开一次FDTD窗口

study = optuna.create_study(direction="minimize")
study.optimize(objective, n_trials=3)