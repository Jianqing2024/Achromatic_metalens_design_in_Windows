from scipy.io import savemat
import numpy as np
import sqlite3
import matlab.engine
import os
from MetaEval import main
from scipy.spatial import cKDTree
from MetaSweep.dataManager import write_GDS_from_id_matrix

best = int(main.Preliminary_numerical_evaluation(48))

base_dir = os.getcwd()
DB_PATH = os.path.join(base_dir, "MetaBase", "Main.db")
uri_path = f"file:{DB_PATH}?mode=ro"
conn = sqlite3.connect(uri_path, uri=True)
cursor = conn.cursor()

cursor.execute('SELECT parameterA, parameterB FROM BaseParameter WHERE baseValue=(?)', (best,))
row = cursor.fetchone()

r = 0.25e-3
single = row[0]
H = row[1]
U = int(r * 2 / single)               # 超透镜直径对应的单元数
wav = [0.8e-6, 0.532e-6]
l = 1.5e-3
Fnum = 25
start = 1.1e-3
stop = 1.6e-3
current_dir = os.getcwd()
path = os.path.join(current_dir, "MetaPhase")

eng = matlab.engine.start_matlab() 
try:
    eng.cd(path, nargout=0)

    phase = [None, None]
    for i, wav in enumerate(wav):
        phase[i] = np.array(eng.main(r, single, wav, l, float(Fnum), start, stop, 50.0, nargout=1))
        print("Next")
finally:
    eng.quit()

cursor.execute("""
    SELECT ID, angleIn1, angleIn5
    FROM Parameter
    WHERE baseValue = ?
""", (best,))

data = np.array(cursor.fetchall())
conn.close()

angles = data[:, 1:3]                 # (N, 2)
tree = cKDTree(angles)

query = np.stack([
    phase[0].ravel(),
    phase[1].ravel()
], axis=1)                             # (U*U, 2)

_, idx = tree.query(query, k=1)       # 丢弃距离，只取索引

ids      = data[idx, 0].astype(int).reshape(U, U)
phase780 = data[idx, 1].reshape(U, U)
phase532 = data[idx, 2].reshape(U, U)

savemat("D:\\WORK\\Achromatic_metalens_design_in_Windows\\figure\\End.mat", {'phase532': phase532, 'phase780': phase780})

np.save("id.npy", ids)
print("ID has been saved")

# 生成 GDS 文件：唯一输入为 ID 矩阵，周期 single 从数据库自动读取
write_GDS_from_id_matrix(ids, "physical_parameter_circles.gds")