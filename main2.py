import optuna
import numpy as np
from time import time
import sqlite3
import matplotlib.pyplot as plt
import matlab.engine

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
    R=np.array([0.5e-3])
    f=np.array([3e-3])+shift2

    waveLength=np.array([0.532e-6,0.800e-6])

    conn = sqlite3.connect("structures.db", isolation_level=None)
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
    return bestFit,bestIdx
def objective(trial):
    shift0 = trial.suggest_float("shift0", -np.pi, np.pi)
    shift1 = trial.suggest_float("shift1", -np.pi, np.pi)
    shift2 = trial.suggest_float("shift2", -0.05e-3, 0.05e-3)
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
    R=np.array([0.5e-3])
    f=np.array([3e-3])+shift2
    single=2e-6

    waveLength=np.array([0.532e-6,0.800e-6])

    conn = sqlite3.connect("structures.db", isolation_level=None)
    cursor = conn.cursor()

    query="SELECT * FROM structures WHERE baseValue = ?"
    cursor.execute(query, (baseValue,))
    rows=cursor.fetchall()
    
    angle=np.zeros((waveLength.size,len(rows)))
    for idx, row in enumerate(rows):
        angle[0,idx],angle[1,idx]=row[7],row[9]
            
    X=create_matrix(R, single)
    
    targetPhi = np.zeros((waveLength.size,X.size))
    shift=[shift0,shift1]
    for idx, wav in enumerate(waveLength):
        targetPhi[idx,:]=wrap_to_pi(hyperbolic_phase(X, wav, f, shift[idx]))
    
    diff=np.zeros((len(rows)))
    bestIdx=np.zeros((X.size))
    for idx, Tphi in enumerate(targetPhi.T):
        for jdx, Ang in enumerate(angle.T):
            diff[jdx]=np.sum(np.abs(Tphi-Ang))

        bestIdx[idx] = np.argmin(diff)

    conn.close()
    return X,bestIdx

study = optuna.create_study(direction="minimize")
study.optimize(objective, n_trials=3)

bestEnd,bestBaseValue=function1(**study.best_params)

shift0,shift1,shift2, = study.best_params.values()

X,bestIdx=function2(shift0,shift1,shift2,int(bestBaseValue))

conn = sqlite3.connect("structures.db", isolation_level=None)
cursor = conn.cursor()

query="SELECT * FROM structures WHERE baseValue = ?"
cursor.execute(query, (int(bestBaseValue),))
rows=cursor.fetchall()
conn.close()
pitch=rows[0][2]

structure_array, R_array=build_structure_array(X, bestIdx, shape=(100, 100), pitch=pitch, center=None)

print(structure_array)
print(R_array)

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

eng = matlab.engine.start_matlab()
print("matlab引擎启动")
E532,E800 = eng.Phase_map_generation(structure_array, nargout=2)
print(E532)
print(E800)

# 关闭 MATLAB 引擎
eng.quit()