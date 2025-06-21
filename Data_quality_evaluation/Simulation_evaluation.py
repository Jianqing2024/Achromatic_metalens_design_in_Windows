import numpy as np
from scipy.io import savemat
import sqlite3
import optuna
import os
from tqdm import tqdm
# Pylance会由于不知名bug异常报错，似乎有一些PylanceBUG，不影响实际运行
from scipy.spatial import cKDTree # type: ignore
from .General_function import *
from MetaSet import advancedStructure as ad

def Optimizer1D(COM):
    def logging_callback1d(study, trial):
        if study.best_trial.number == trial.number:
            print(f"Trial {trial.number:03d} found a better value. Value: {trial.value:.4f}")
    def fun1d(trial):
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
        study.optimize(fun1d, n_trials=1, callbacks=[logging_callback1d])
        
    return study.best_params, study.best_value

def OneD_ObjectiveFunction(shift0, shift1, shift2, shift3, shift4, COM):
    base_dir = os.getcwd()
    DB_PATH = os.path.join(base_dir, "data", "Main.db")

    uri_path = f"file:{DB_PATH}?mode=ro"

    conn = sqlite3.connect(uri_path, uri=True)
    cursor = conn.cursor()

    ftx = []
    shift = [shift0, shift1, shift2, shift3, shift4]

    if COM.Over:
        for i in range(5):
            ftx.append(COM.TargetPhase_over[i]+shift[i])
    else:
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

    if COM.Over:
        for i in range(5):
            ftx.append(COM.TargetPhase_over[i]+shifts[i])
    else:
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

def Map_1D_Results_To_2D(COM, matched_ids):
    R_1D = COM.R_over  # 1D 半径点 (K,)
    
    # 构建二维坐标网格
    x = np.linspace(-COM.r, COM.r, COM.N)
    y = np.linspace(-COM.r, COM.r, COM.N)
    X, Y = np.meshgrid(x, y)
    R = np.sqrt(X**2 + Y**2)  # shape = (N, N)

    # 扁平化二维 R，准备映射
    flat_R = R.flatten()  # shape = (N*N,)
    matched_ids_1D = np.array(matched_ids)  # shape = (K,)

    # 使用 searchsorted 近似找到插值位置（向右插入）
    idx_float = np.searchsorted(R_1D, flat_R, side="left")
    idx_float = np.clip(idx_float, 1, len(R_1D) - 1)

    # 比较左右哪个更近
    left = R_1D[idx_float - 1]
    right = R_1D[idx_float]
    closer_to_right = np.abs(flat_R - right) < np.abs(flat_R - left)
    indices = idx_float - 1 + closer_to_right.astype(np.int32)  # 最终最近点索引

    # 映射结构 ID，恢复成二维阵列
    ID_array_flat = matched_ids_1D[indices]
    ID_array = ID_array_flat.reshape(R.shape)  # shape = (N, N)
    
    return ID_array, X, Y

def save_MAT(id_matrix, X, Y):
    def Query_angleIn_by_ID(id_matrix, angle_index):
        """
        查询 angleIn{angle_index}，支持大规模 ID 阵列。
        """
        ids_flat = id_matrix.flatten().tolist()
        id_to_angle = {}

        base_dir = os.getcwd()
        DB_PATH = os.path.join(base_dir, "data", "Main.db")
        uri_path = f"file:{DB_PATH}?mode=ro"
        conn = sqlite3.connect(uri_path, uri=True)
        cursor = conn.cursor()

        # 分批查询，每批最多 999 个 ID
        BATCH_SIZE = 999
        for i in range(0, len(ids_flat), BATCH_SIZE):
            batch = ids_flat[i:i+BATCH_SIZE]
            placeholder = ','.join('?' for _ in batch)
            query = f'''
                SELECT id, angleIn{angle_index} FROM Parameter 
                WHERE id IN ({placeholder})
            '''
            cursor.execute(query, batch)
            rows = cursor.fetchall()
            id_to_angle.update({row[0]: row[1] for row in rows})

        conn.close()

        # 构造最终结果矩阵
        angle_matrix_flat = [id_to_angle.get(i, np.nan) for i in ids_flat]
        angle_matrix = np.array(angle_matrix_flat).reshape(id_matrix.shape)

        return angle_matrix

    # 正确创建一个长度为 5 的列表来存储相位矩阵
    phase = []
    for i in range(5):
        phase_i = Query_angleIn_by_ID(id_matrix, i + 1)  # angleIn1~5
        phase.append(phase_i)

    # 保存为 .mat 文件
    savemat('dataPhase.mat', {
        'phase0': phase[0],
        'phase1': phase[1],
        'phase2': phase[2],
        'phase3': phase[3],
        'phase4': phase[4],
        'X': X,
        'Y': Y
    })

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
    meta.fdtd.set("mesh accuracy", 1)
    meta.fdtd.set("y min bc", "periodic")
    meta.fdtd.set("simulation time", 3e-12)
    
    #  建立基底
    meta.fdtd.addrect()
    meta.fdtd.set("name","base")
    meta.fdtd.set("x", 0)
    meta.fdtd.set("y", 0)
    meta.fdtd.set("material", "SiO2 (Glass) - Palik")
    meta.fdtd.set("x span", 2*COM.r+COM.single)
    meta.fdtd.set("y span", COM.single*2)
    meta.fdtd.set("z min", -0.5e-6)
    meta.fdtd.set("z max", 0)
    
    #  建立光源。请在运行时手动调试波长
    meta.fdtd.addplane()
    meta.fdtd.set("x span", 2*COM.r+COM.single)
    meta.fdtd.set("y span", COM.single)
    meta.fdtd.set("wavelength start", COM.Wav[-1])
    meta.fdtd.set("wavelength stop", COM.Wav[0])
    
    #  建立监视器
    meta.fdtd.addpower(name="Monitor")
    meta.fdtd.set("monitor type", "2D Y-normal")
    meta.fdtd.set("x", 0)
    meta.fdtd.set("x span", 2*COM.r+COM.single)
    meta.fdtd.set("y", 0)
    meta.fdtd.set("z min", 1e-6)
    meta.fdtd.set("z max", COM.f_target+10e-6)
    
    meta.materialSet()
    
    for i, id in tqdm(enumerate(matched_ids), total=len(matched_ids), desc="Structs"):
        cursor.execute("SELECT class, parameterA, parameterB, parameterC FROM Parameter WHERE ID = ?", (int(id),))
        
        result = cursor.fetchone()
        
        strClass, parameterA, parameterB, parameterC = result
        x = COM.D[i]
        meta.structureBuild_ForDataEvaluation(strClass, [parameterA, parameterB, parameterC], COM.H, i)
        meta.fdtd.select(str(i))
        meta.fdtd.set("x", x)
        
    meta.fdtd.save("OneD.fsp")
    
def get_data():
    meta = ad.MetaEngine(hide = True)
    meta.fdtd.load("OneD.fsp")
    aaa = meta.fdtd.getdata("Monitor", "Ex")
    
    savemat('MonitorData.mat', {'dataa': aaa})