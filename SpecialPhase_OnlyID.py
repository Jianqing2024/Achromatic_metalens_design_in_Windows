from scipy.io import savemat
import numpy as np
import sqlite3
import matlab.engine
import os
from tqdm import tqdm
from MetaEval import main
from tqdm import tqdm
from scipy.spatial import cKDTree
from MetaSweep.dataManager import write_GDS_from_id_matrix

def Random_Matrix_Generation(U, Fnum):
    xb = int(U / np.sqrt(Fnum))

    if U%Fnum >= 0:
        KeyError("Please adjust the number of focal points.")

    block_size = int(np.sqrt(Fnum))
    PB = []
    for i in range(xb):
        row = []
        for j in range(xb):
            random_numbers = np.random.permutation(Fnum)
            block = random_numbers.reshape(block_size, block_size)
            row.append(block)
        PB.append(row)

    Ft = np.block(PB)+1

    return Ft

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
wav = [0.8e-6, 0.532e-6]
l = 1.5e-3
Fnum = 25
start = 1.1e-3
stop = 1.6e-3
singleDownsampling = single * 2
loop = 10
popnum = 10

U = int(r*2/single)
UDownsampling = int(r/singleDownsampling*2)

Ft = Random_Matrix_Generation(U, Fnum)

Ft_low = Random_Matrix_Generation(UDownsampling, Fnum)

current_dir = os.getcwd()
path = os.path.join(current_dir, "MetaPhase")
save_path = os.path.join(path, "data.mat")

eng = matlab.engine.start_matlab() 
try:
    eng.cd(path, nargout=0)

    phase = [np.zeros((U,U)), np.zeros((U,U))]
    Eout = [np.zeros((U,U)),np.zeros((U,U))]
    for i, wav in enumerate(wav):
        Eout_i, phase_i = eng.NBphase(r, single, wav, l, float(Fnum), start, stop, singleDownsampling, loop, popnum, Ft, Ft_low, nargout=2)
        phase[i] = np.array(phase_i)
        Eout[i] = np.array(Eout_i)
        print("Next")
finally:
    eng.quit()

phase780 = np.zeros([U, U])
phase532 = np.zeros([U, U])
ids = np.zeros([U, U])

cursor.execute("""
    SELECT ID, angleIn1, angleIn5
    FROM Parameter
    WHERE baseValue = ?
""", (best,))

data = np.array(cursor.fetchall())  

angles = data[:, 1:3]   # (N, 2)
tree = cKDTree(angles)

query = np.stack([
    phase[0].ravel(),
    phase[1].ravel()
], axis=1)   # (U*U, 2)

dist, idx = tree.query(query, k=1)

nearest = data[idx]

ids[:]       = nearest[:,0].reshape(U, U)
phase780[:]  = nearest[:,1].reshape(U, U)
phase532[:]  = nearest[:,2].reshape(U, U)

savemat("D:\\WORK\\Achromatic_metalens_design_in_Windows\\figure\\End.mat", {'phase532': phase532, 'phase780': phase780})

np.save("id.npy", ids)
print("ID has been saved")

# 生成 GDS 文件：唯一输入为 ID 矩阵，周期 single 从数据库自动读取
write_GDS_from_id_matrix(ids, "physical_parameter_circles.gds")