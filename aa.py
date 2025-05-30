import numpy as np
import sqlite3
import optuna
import os
# Pylance会由于不知名bug异常报错，似乎有一些包冲突，不影响实际运行
from scipy.spatial import cKDTree # type: ignore 

def fun(shift0, shift1, shift2):
    main = 0

    base_dir = os.getcwd()
    DB_PATH = os.path.join(base_dir, "data", "Main.db")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM BaseParameter WHERE baseValue=(?)', (main,))
    row = cursor.fetchone()

    single = row[1]
    h = row[2]

    N = int(250) * 2
    r = N * single
    x = np.linspace(-(N / 2), (N / 2), N)

    lambda0 = 0.6e-6
    lambda1 = 0.5e-6
    f = 60e-6 + shift0

    # 计算相位并规整到[0, 2π)
    ftx0 = -(2 * np.pi) / lambda0 * (np.sqrt(x**2 + f**2) - f) + shift1
    ftx0 = np.mod(ftx0, 2 * np.pi)  # wrapTo2Pi

    ftx1 = -(2 * np.pi) / lambda1 * (np.sqrt(x**2 + f**2) - f) + shift2
    ftx1 = np.mod(ftx1, 2 * np.pi)  # wrapTo2Pi

    cursor.execute('SELECT angleIn1, angleIn5 FROM Parameter WHERE baseValue=(?)', (main,))
    rows = cursor.fetchall()

    points = np.array(rows)  # 形状为 (M, 2)，M是数据库行数

    query_points = np.column_stack((ftx0, ftx1))

    tree = cKDTree(points, leafsize=40)
    distances, indices = tree.query(query_points, p=1)
    
    di = np.sum(distances)
    return di

def objective(trial):
    # 设置各个shift的上下限：
    shift0 = trial.suggest_float("shift0", -10e-6, 10e-6)
    shift1 = trial.suggest_float("shift1", -np.pi, np.pi)
    shift2 = trial.suggest_float("shift2", -np.pi, np.pi)

    score = fun(shift0, shift1, shift2)
    return score

study = optuna.create_study(direction="minimize")
study.optimize(objective, n_trials=500)

# 最优的目标函数值（例如最小的偏差）
print("Best objective value:", study.best_value)

# 最优的参数组合（shift0, shift1, shift2）
print("Best parameters:", study.best_params)