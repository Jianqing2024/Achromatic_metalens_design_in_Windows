import numpy as np
import sqlite3
import optuna
import os
from tqdm import tqdm
# Pylance会由于不知名bug异常报错，似乎有一些包冲突，不影响实际运行
from scipy.spatial import cKDTree # type: ignore

def calculate(shift0, shift1, shift2):
    main = 0

    base_dir = os.getcwd()
    DB_PATH = os.path.join(base_dir, "data", "Main.db")

    uri_path = f"file:{DB_PATH}?mode=ro"

    conn = sqlite3.connect(uri_path, uri=True)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM BaseParameter WHERE baseValue=(?)', (main,))
    row = cursor.fetchone()

    single = row[1]
    h = row[2]

    N = int(250) * 2
    l = N * single
    x = np.linspace(0, (l / 2), N*10)

    lambda0 = 0.6e-6
    lambda1 = 0.5e-6
    f = 60e-6 + shift0

    # 计算相位
    ftx0 = -(2 * np.pi) / lambda0 * (np.sqrt(x**2 + f**2) - f) + shift1
    ftx1 = -(2 * np.pi) / lambda1 * (np.sqrt(x**2 + f**2) - f) + shift2

    # wrap 到 [-π, π)
    ftx0 = (ftx0 + np.pi) % (2 * np.pi) - np.pi
    ftx1 = (ftx1 + np.pi) % (2 * np.pi) - np.pi

    cursor.execute('SELECT angleIn1, angleIn5 FROM Parameter WHERE baseValue=(?)', (main,))
    
    rows = cursor.fetchall()

    points = np.array(rows)  # 形状为 (M, 2)，M是数据库行数

    query_points = np.column_stack((ftx0, ftx1))

    tree = cKDTree(points, leafsize=40)
    conn.close()
    return tree, query_points 

def fun(shift0, shift1, shift2):
    tree, query_points = calculate(shift0, shift1, shift2)
    distances, indices = tree.query(query_points, p=1)
    
    di = np.sum(distances)
    return di

def fin(shift0, shift1, shift2):
    tree, query_points = calculate(shift0, shift1, shift2)
    distances, indices = tree.query(query_points, p=1)

    return indices

def objective(trial):
    # 设置各个shift的上下限：
    shift0 = trial.suggest_float("shift0", -10e-6, 10e-6)
    shift1 = trial.suggest_float("shift1", -np.pi, np.pi)
    shift2 = trial.suggest_float("shift2", -np.pi, np.pi)

    score = fun(shift0, shift1, shift2)
    return score

def logging_callback(study, trial):
    if study.best_trial.number == trial.number:
        print(f"Trial {trial.number:03d} found a better value. Value: {trial.value:.4f}")
# 关闭 Optuna 默认刷屏
optuna.logging.set_verbosity(optuna.logging.WARNING)

# 创建 study
study = optuna.create_study(direction="minimize")

# 用 tqdm 显示优雅进度条
N_TRIALS = 500
for _ in tqdm(range(N_TRIALS), desc="Optuna 优化中"):
    study.optimize(objective, n_trials=1, callbacks=[logging_callback])

# 显示结果
print("\n最优参数:", study.best_params)
print("最小偏差值:", study.best_value)

indices = fin(study.best_params['shift0'], study.best_params['shift1'], study.best_params['shift2'])
print(indices)
num_unique = len(set(indices))
print("Different Values: ", num_unique)