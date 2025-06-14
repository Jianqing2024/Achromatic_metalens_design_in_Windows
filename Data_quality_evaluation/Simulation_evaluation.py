import numpy as np
import sqlite3
import optuna
import os
from tqdm import tqdm
# Pylance会由于不知名bug异常报错，似乎有一些PylanceBUG，不影响实际运行
from scipy.spatial import cKDTree # type: ignore
from .General_function import *
from MetaSet import advancedStructure as ad

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

    cursor.execute('SELECT angleIn1, angleIn2, angleIn3, angleIn4, angleIn5 FROM Parameter WHERE baseValue=(?)', (COM.mainValue,))
    rows = cursor.fetchall()

    points = np.array([row[0:] for row in rows])     # 相位点组成的数组，形状为 (M, 5)

    # 构建 KD 树
    tree = cKDTree(points, leafsize=40)
    conn.close()
    
    distances, indices = tree.query(query_points, k=1)
    
    diff=np.sum(distances)
    return diff

def OneD_Index(parameter, COM):
    shifts = [parameter[f'shift{i}'] for i in range(5)]
    
    base_dir = os.getcwd()
    DB_PATH = os.path.join(base_dir, "data", "Main.db")

    uri_path = f"file:{DB_PATH}?mode=ro"

    conn = sqlite3.connect(uri_path, uri=True)
    cursor = conn.cursor()

    ftx = []

    for i in range(5):
        ftx.append(COM.TargetPhase[i]+shifts[i])

    # 拼接成查询点 (N, 5)
    query_points = np.column_stack(ftx)

    # 查询时连带结构 ID 一起取出
    cursor.execute('SELECT id, angleIn1, angleIn2, angleIn3, angleIn4, angleIn5 FROM Parameter WHERE baseValue=(?)', (COM.mainValue,))
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

def OneD_ModelAndRun(matched_ids, COM):
    COM.D = np.concatenate([-np.flip(COM.R), COM.R])
    matched_ids = np.concatenate([np.flip(matched_ids), matched_ids])
    
    base_dir = os.getcwd()
    DB_PATH = os.path.join(base_dir, "data", "Main.db")

    uri_path = f"file:{DB_PATH}?mode=ro"

    conn = sqlite3.connect(uri_path, uri=True)
    cursor = conn.cursor()
    
    meta = ad.MetaEngine(parallel=False, template=True, SpectralRange=[COM.Wav[0], COM.Wav[-1]])
    
    #  建立fdtd区域
    meta.fdtd.addfdtd()
    meta.fdtd.set("x",0)
    meta.fdtd.set("y",0)
    meta.fdtd.set("x span", 2*COM.r+COM.single)
    meta.fdtd.set("y span", COM.single)
    meta.fdtd.set("z max", COM.f_target+10e-6)
    meta.fdtd.set("z min", -0.5e-6)
    
    #  建立基底
    meta.fdtd.addrect()
    meta.fdtd.set("name","base")
    meta.fdtd.set("x", 0)
    meta.fdtd.set("y", 0)
    meta.fdtd.set("material", "SiO2 (Glass) - Palik")
    meta.fdtd.set("x span", 2*COM.r+COM.single)
    meta.fdtd.set("y span", COM.single)
    meta.fdtd.set("z min", -0.5e-6)
    meta.fdtd.set("z max", 0)
    
    #  建立光源。请在运行时手动调试波长
    meta.fdtd.addplane()
    meta.fdtd.set("x span", 2*COM.r+COM.single)
    meta.fdtd.set("y span", COM.single)
    meta.fdtd.set("wavelength start", COM.WavMin)
    meta.fdtd.set("wavelength stop", COM.WavMax)
    
    #  建立监视器
    meta.fdtd.addpower(name="Monitor")
    meta.fdtd.set("monitor type", "2D Y-normal")
    meta.fdtd.set("x", 0)
    meta.fdtd.set("x span", 2*COM.r+COM.single)
    meta.fdtd.set("y", 0)
    meta.fdtd.set("z min", 1e-6)
    meta.fdtd.set("z max", COM.f_target+10e-6)
    
    meta.materialSet()
    
    for i, id in enumerate(matched_ids):
        cursor.execute("SELECT class, parameterA, parameterB, parameterC FROM Parameter WHERE ID = ?", (int(id),))
        
        result = cursor.fetchone()
        
        strClass, parameterA, parameterB, parameterC = result
        x = COM.D[i]
        print(COM.H)
        meta.structureBuild_ForDataEvaluation(strClass, [parameterA, parameterB, parameterC], COM.H, i)
        meta.fdtd.select(str(i))
        meta.fdtd.set("x", x)
        
    meta.fdtd.save("OneD.fsp")