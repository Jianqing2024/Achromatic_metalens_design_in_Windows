import optuna
import numpy as np
from time import time
import sqlite3
import matplotlib.pyplot as plt
import matlab.engine
import os

def hyperbolic_phase(r, wav, f, shift):
    phi = -2 * np.pi / wav * (np.sqrt(r**2 + f**2) - f)+shift
    return phi
def create_matrix(R, single):
    num_elements = int(R // single)
    if R % single != 0:
        num_elements += 1
    matrix = np.arange(0.5*single, num_elements * single, single)
    if matrix[-1] > R:
        matrix = matrix[matrix <= R]
    return matrix
def wrap_to_pi(angles):
    return (angles + np.pi) % (2 * np.pi) - np.pi
def function1(shift0,shift1,shift2):
    R,f0=read_R_f()
    f=f0+shift2

    waveLength=np.array([0.532e-6,0.800e-6])

    # 获取当前文件所在脚本的上一级（主目录）路径
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, '..', 'data')  # 如果当前脚本在子项目中
    DB_PATH = os.path.join(DATA_DIR, 'structures.db')

    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA synchronous = OFF")
    cursor.execute("PRAGMA journal_mode = MEMORY")

    cursor.execute("SELECT DISTINCT baseValue FROM structures ORDER BY baseValue")
    base_values = cursor.fetchall()

    Fit=np.zeros((len(base_values)))
    for dx, (base_val,) in enumerate(base_values):
        query="SELECT * FROM structures WHERE baseValue = ?"
        cursor.execute(query, (base_val,))
        rows=cursor.fetchall()
    
        angle=np.zeros((waveLength.size,len(rows)))
        for idx, row in enumerate(rows):
            angle[0,idx],angle[1,idx]=row[7],row[9]
            
        single=rows[0][2]
        X=create_matrix(R, single)
    
        targetPhi = np.zeros((waveLength.size,X.size))
        shift=[shift0,shift1]
        for idx, wav in enumerate(waveLength):
            targetPhi[idx,:]=wrap_to_pi(hyperbolic_phase(X, wav, f, shift[idx]))
    
        diff=np.zeros((len(rows)))
        Interpolation=np.zeros((X.size))
        for idx, Tphi in enumerate(targetPhi.T):
            for jdx, Ang in enumerate(angle.T):
                diff[jdx]=np.sum(np.abs(Tphi-Ang))

            Interpolation[idx] = diff[np.argmin(diff)]
    
        Fit[dx]=np.sum(Interpolation)
        
    bestFit = np.min(Fit)

    bestIdx = np.argmin(Fit)

    conn.close()
    return bestFit,(bestIdx+1)
def objective(trial):
    shift0 = trial.suggest_float("shift0", -np.pi, np.pi)
    shift1 = trial.suggest_float("shift1", -np.pi, np.pi)
    shift2 = trial.suggest_float("shift2", -1e-3, 1.25e-3)
    result1, result2 = function1(shift0,shift1,shift2)

    return result1
def build_structure_array(R_samples, structure_ids, shape=(100, 100), pitch=0.5, center=None):
    """
    构建结构阵面：根据每个点的物理半径 R 值查找结构 ID。

    参数:
        R_samples: ndarray, shape=(N,)，预计算的 R 值
        structure_ids: ndarray, shape=(N,)，对应结构 ID(无实际含义,仅标识结构）
        shape: tuple,阵面尺寸 (H, W)
        pitch: float,每个结构之间的距离(单位自定，比如 μm)
        center: tuple 或 None,阵面中心位置 (i0, j0)。默认是阵面几何中心。

    返回:
        structure_array: shape=(H, W)，结构 ID 的二维数组
        R_array: shape=(H, W)，每个点到中心的实际物理半径
    """
    H, W = shape
    if center is None:
        center = (H // 2, W // 2)  # 默认以阵面中心为圆心

    # 构造坐标网格（单位：实际物理距离）
    y = (np.arange(H) - center[0]) * pitch
    x = (np.arange(W) - center[1]) * pitch
    X, Y = np.meshgrid(x, y)
    R_array = np.sqrt(X**2 + Y**2)  # 每个结构到圆心的实际距离（R）

    # 最近邻查找结构 ID
    R_flat = R_array.ravel()[:, None]
    R_diff = np.abs(R_flat - R_samples[None, :])
    nearest_idx = np.argmin(R_diff, axis=1)
    structure_flat = structure_ids[nearest_idx]
    structure_array = structure_flat.reshape(H, W)

    return structure_array, R_array
def function2(shift0,shift1,shift2,baseValue):
    R,f0=read_R_f()
    f=f0+shift2
    single=2e-6

    waveLength=np.array([0.532e-6,0.800e-6])
    # 获取当前文件所在脚本的上一级（主目录）路径
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, '..', 'data')  # 如果当前脚本在子项目中
    DB_PATH = os.path.join(DATA_DIR, 'structures.db')

    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query="SELECT * FROM structures WHERE baseValue = ?"
    cursor.execute(query, (baseValue,))
    rows=cursor.fetchall()
    print(rows)
    
    angle=np.zeros((waveLength.size,len(rows)))
    index=np.zeros(len(rows))
    for idx, row in enumerate(rows):
        angle[0,idx],angle[1,idx]=row[7],row[9]
        index[idx]=row[0]
    
    X=create_matrix(R, single)
    
    targetPhi = np.zeros((waveLength.size,X.size))
    shift=[shift0,shift1]
    for idx, wav in enumerate(waveLength):
        targetPhi[idx,:]=wrap_to_pi(hyperbolic_phase(X, wav, f, shift[idx]))
    
    diff=np.zeros((len(rows)))
    bestIdx=np.zeros(X.size)
    for idx, Tphi in enumerate(targetPhi.T):
        for jdx, Ang in enumerate(angle.T):
            diff[jdx]=np.sum(np.abs(Tphi-Ang))

        best = np.argmin(diff)
        bestIdx[idx]=index[best]

    conn.close()
    return X,bestIdx
def read_R_f():
    # 获取当前脚本所在目录（如 your_script.py）
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 构建指向 data 文件夹中参数文件的路径
    filename = os.path.join(current_dir, '..', 'data', 'parameter.txt')

    with open(filename, 'r') as f:
        lines = f.readlines()

    R = np.float64(lines[0].split('=')[1])
    f = np.float64(lines[1].split('=')[1])
    return R, f

def mainFunction2():
    R,f0=read_R_f()
    print(f"参数确认:R={R},f0={f0}")

    study = optuna.create_study(direction="minimize")
    study.optimize(objective, n_trials=3)

    bestEnd,bestBaseValue=function1(**study.best_params)
    print(bestBaseValue)

    shift0,shift1,shift2, = study.best_params.values()

    X,bestIdx=function2(shift0,shift1,shift2,int(bestBaseValue))

    # 获取当前文件所在脚本的上一级（主目录）路径
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, '..', 'data')  # 如果当前脚本在子项目中
    DB_PATH = os.path.join(DATA_DIR, 'structures.db')

    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query="SELECT * FROM structures WHERE baseValue = ?"
    cursor.execute(query, (int(bestBaseValue),))
    rows=cursor.fetchall()
    conn.close()
    pitch=rows[0][2]

    structure_array, R_array=build_structure_array(X, bestIdx, shape=(100, 100), pitch=pitch, center=None)

    fig, axs = plt.subplots(1, 2, figsize=(12, 5))

    im1 = axs[0].imshow(structure_array, cmap='tab20')
    axs[0].set_title("Structure ID")
    axs[0].axis('off')
    fig.colorbar(im1, ax=axs[0])

    im2 = axs[1].imshow(R_array, cmap='viridis')
    axs[1].set_title("R Value")
    axs[1].axis('off')
    fig.colorbar(im2, ax=axs[1])

    plt.tight_layout()
    plt.show()

    print("正在进入matlab引擎")

    eng = matlab.engine.start_matlab()

    # 2. 拼接 matlabFuncs 文件夹路径
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MATLAB_FUNC_DIR = os.path.join(BASE_DIR, 'matlabFuncs')

    # 3. 添加路径
    eng.addpath(MATLAB_FUNC_DIR, nargout=0)

    E532, E800 = eng.Far_field_simulation(structure_array, nargout=2)
    print(E532)
    print(E800)

    eng.quit()