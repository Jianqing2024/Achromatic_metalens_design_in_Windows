import numpy as np
import sqlite3
import optuna
import os
from tqdm import tqdm
# Pylance会由于不知名bug异常报错，似乎有一些PylanceBUG，不影响实际运行
from scipy.spatial import cKDTree # type: ignore
from .General_function import *

def Optimizer(COM):
    def logging_callback(study, trial):
        if study.best_trial.number == trial.number:
            print(f"Trial {trial.number:03d} found a better value. Value: {trial.value:.4f}")
    def fun(trial):
        # 设置各个shift的上下限：
        shift0 = trial.suggest_float("shift0", -np.pi, np.pi)
        shift1 = trial.suggest_float("shift1", -np.pi, np.pi)
        shift2 = trial.suggest_float("shift2", -np.pi, np.pi)
        shift3 = trial.suggest_float("shift3", -np.pi, np.pi)
        shift4 = trial.suggest_float("shift4", -np.pi, np.pi)
        score = OneD_ObjectiveFunction(shift0, shift1, shift2, shift3, shift4, COM)
        return score
    
    optuna.logging.set_verbosity(optuna.logging.WARNING)

    # 创建 study
    study = optuna.create_study(direction="minimize")

    # 用 tqdm 显示进度条
    N_TRIALS = 500
    for _ in tqdm(range(N_TRIALS), desc="Optuna ING"):
        study.optimize(fun, n_trials=1, callbacks=[logging_callback])
        
    return study.best_params, study.best_value

def OneD_ObjectiveFunction(shift0, shift1, shift2, shift3, shift4, COM):
    base_dir = os.getcwd()
    DB_PATH = os.path.join(base_dir, "data", "Main.db")

    uri_path = f"file:{DB_PATH}?mode=ro"

    conn = sqlite3.connect(uri_path, uri=True)
    cursor = conn.cursor()

    ftx = []
    shift = [shift0, shift1, shift2, shift3, shift4]

    for i in range(5):
        ftx.append(COM.TargetPhase[i]+shift[i])

    # 拼接成查询点 (N, 5)
    query_points = np.column_stack(ftx)

    # 查询时连带结构 ID 一起取出
    cursor.execute('SELECT angleIn1, angleIn2, angleIn3, angleIn4, angleIn5 FROM Parameter WHERE baseValue=(?)', (COM.mainValue,))
    rows = cursor.fetchall()

    points = np.array([row[0:] for row in rows])     # 相位点组成的数组，形状为 (M, 5)

    # 构建 KD 树
    tree = cKDTree(points, leafsize=40)
    conn.close()
    
    distances, indices = tree.query(query_points, k=1)
    
    diff=np.sum(distances)
    return diff



"""        
    elif Command.Controller == 2: # 输出远场相位值
        base_dir = os.getcwd()
        DB_PATH = os.path.join(base_dir, "data", "Main.db")

        uri_path = f"file:{DB_PATH}?mode=ro"

        conn = sqlite3.connect(uri_path, uri=True)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM BaseParameter WHERE baseValue=(?)', (main,))
        row = cursor.fetchone()
        
        single = row[1]
        
        ApproximateR, f, WavMax, WavMin = Read_Parameter()
        Wav = np.linspace(WavMax, WavMin, 5)
        r, N = Exact_Value(ApproximateR, single)
        l = np.linspace(0, r, N)
        
        ftx = []
        shift = [shift0, shift1, shift2, shift3, shift4]

        for i in range(5):
            ftx.append(Target_Phase_Standrad_1D(l, Wav[i], f + shiftF) + shift[i])

        # 拼接成查询点 (N, 5)
        query_points = np.column_stack(ftx)

        # 查询时连带结构 ID 一起取出
        cursor.execute('SELECT id, angleIn1, angleIn2, angleIn3, angleIn4, angleIn5 FROM Parameter WHERE baseValue=(?)', (main,))
        rows = cursor.fetchall()

        # 拆分结构 ID 和相位数据
        ids = [row[0] for row in rows]                   # 结构 ID 列表，长度为 M
        points = np.array([row[1:] for row in rows])     # 相位点组成的数组，形状为 (M, 5)

        # 构建 KD 树
        tree = cKDTree(points, leafsize=40)
        conn.close()
        
        distances, indices = tree.query(query_points, k=1)
        closest_phase = points[indices]
        return closest_phase
        
    elif Command.Controller == 3: # 输出Index
        base_dir = os.getcwd()
        DB_PATH = os.path.join(base_dir, "data", "Main.db")

        uri_path = f"file:{DB_PATH}?mode=ro"

        conn = sqlite3.connect(uri_path, uri=True)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM BaseParameter WHERE baseValue=(?)', (main,))
        row = cursor.fetchone()
        
        single = row[1]
        
        ApproximateR, f, WavMax, WavMin = Read_Parameter()
        Wav = np.linspace(WavMax, WavMin, 5)
        r, N = Exact_Value(ApproximateR, single)
        l = np.linspace(0, r, N)
        
        ftx = []
        shift = [shift0, shift1, shift2, shift3, shift4]

        for i in range(5):
            ftx.append(Target_Phase_Standrad_1D(l, Wav[i], f + shiftF) + shift[i])

        # 拼接成查询点 (N, 5)
        query_points = np.column_stack(ftx)

        # 查询时连带结构 ID 一起取出
        cursor.execute('SELECT id, angleIn1, angleIn2, angleIn3, angleIn4, angleIn5 FROM Parameter WHERE baseValue=(?)', (main,))
        rows = cursor.fetchall()

        # 拆分结构 ID 和相位数据
        ids = [row[0] for row in rows]                   # 结构 ID 列表，长度为 M
        points = np.array([row[1:] for row in rows])     # 相位点组成的数组，形状为 (M, 5)

        # 构建 KD 树
        tree = cKDTree(points, leafsize=40)
        conn.close()

        # 最近邻查询 (N 个查询点，每个返回 1 个最近邻)
        distances, indices = tree.query(query_points, k=1)

        # 用索引反查数据库结构 ID（返回 N 个结构点的 ID）
        matched_ids = [ids[i] for i in indices]
        return matched_ids
"""