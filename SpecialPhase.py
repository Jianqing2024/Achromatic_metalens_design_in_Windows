import matlab.engine
from scipy.io import savemat
from Data_quality_evaluation import main
import os
from MetaSet import advancedStructure as ad
import numpy as np
import sqlite3
from tqdm import tqdm

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

def minimize_difference(A, B):
    """
    给矩阵 B 加上一个常数 c，使得 sum(|A - (B+c)|) 最小
    返回 c 和加完后的 B_new
    """
    A = np.asarray(A)
    B = np.asarray(B)

    # 最优 c = median(A - B)
    D = A - B
    c = np.median(D)

    B_new = B + c
    total_diff = np.sum(np.abs(A - B_new))

    return c, B_new, total_diff

best = int(main.Preliminary_numerical_evaluation(48))

print(best)

base_dir = os.getcwd()
DB_PATH = os.path.join(base_dir, "data", "Main.db")
uri_path = f"file:{DB_PATH}?mode=ro"
conn = sqlite3.connect(uri_path, uri=True)
cursor = conn.cursor()

cursor.execute('SELECT parameterA, parameterB FROM BaseParameter WHERE baseValue=(?)', (best,))
row = cursor.fetchone()

r = 20e-6
single = row[0]        
H = row[1]
wav = [0.780e-6, 0.532e-6]
l = 1e-3
Fnum = 16
start = 240e-6
stop = 440e-6
singleDownsampling = 0.4e-6
loop = 18
popnum = 10

U = int(r*2/single)
UDownsampling = int(r/singleDownsampling*2)

x = np.linspace(-(r - 0.5*single), (r - 0.5*single), U)
y = np.linspace(-(r - 0.5*single), (r - 0.5*single), U)
X, Y = np.meshgrid(x, y)

Ft = Random_Matrix_Generation(U, Fnum)
Ft_low = Random_Matrix_Generation(UDownsampling, Fnum)
print(Ft.shape)

current_dir = os.getcwd()
path = os.path.join(current_dir, "Special_Phase_Implementation")
save_path = os.path.join(path, "data.mat")

eng = matlab.engine.start_matlab()
eng.cd(path, nargout=0)

target_wav = [0.780e-6,0.532e-6]

phase = [np.zeros((U,U)), np.zeros((U,U))]
Eout = [np.zeros((U,U)),np.zeros((U,U))]
for i, wav in enumerate(target_wav):
    Eout_i, phase_i = eng.NBphase(r, single, wav, l, float(Fnum), start, stop, singleDownsampling, loop, popnum, Ft, Ft_low, nargout=2)

    phase[i] = np.array(phase_i)
    Eout[i] = np.array(Eout_i)

id = np.zeros((U, U), dtype=int)

for i in range(U):
    for j in range(U):
        cursor.execute("""
            SELECT ID, 
            ((angleIn1 - ?) * (angleIn1 - ?) + (angleIn5 - ?) * (angleIn5 - ?)) AS diff
            FROM Parameter
            WHERE baseValue = (?)
            ORDER BY diff ASC
            LIMIT 1;
                       """, (phase[0][i,j], phase[0][i,j], phase[1][i,j], phase[1][i,j], best))

        row = cursor.fetchone()
        id[i,j] = row[0]

meta = ad.MetaEngine(parallel=False, template=True, SpectralRange=[target_wav[0], target_wav[1]])

#  建立fdtd区域
meta.fdtd.addfdtd()
meta.fdtd.set("x",0)
meta.fdtd.set("y",0)
meta.fdtd.set("x span", 2*r+single)
meta.fdtd.set("y span", 2*r+single)
meta.fdtd.set("z max", 2e-6)
meta.fdtd.set("z min", -1e-6)
meta.fdtd.set("mesh accuracy", 1)
meta.fdtd.set("y min bc", "periodic")

#  建立基底
meta.fdtd.addrect()
meta.fdtd.set("name","base")
meta.fdtd.set("x", 0)
meta.fdtd.set("y", 0)
meta.fdtd.set("material", "SiO2 (Glass) - Palik")
meta.fdtd.set("x span", 2*r+single)
meta.fdtd.set("y span", 2*r+single)
meta.fdtd.set("z min", -1e-6)
meta.fdtd.set("z max", 0)

#  建立光源。请在运行时手动调试波长
meta.fdtd.addplane()
meta.fdtd.set("x", 0)
meta.fdtd.set("y", 0)
meta.fdtd.set("z", -0.5e-6)
meta.fdtd.set("x span", 2*r+single)
meta.fdtd.set("y span", 2*r+single)
meta.fdtd.set("wavelength start", target_wav[1])
meta.fdtd.set("wavelength stop", target_wav[0])

#  建立监视器
meta.fdtd.addpower(name="Monitor plane")
meta.fdtd.set("monitor type", "2D Z-normal")
meta.fdtd.set("x", 0)
meta.fdtd.set("x span", 2*r+single)
meta.fdtd.set("y", 0)
meta.fdtd.set("y span", 2*r+single)
meta.fdtd.set("z", 1.6e-6)

meta.fdtd.save("AllWav.fsp")

meta.materialSet()

for i in tqdm(range(U), desc="Rows"):
    for j in tqdm(range(U), desc="Cols", leave=False):
        cursor.execute("SELECT class, parameterA, parameterB, parameterC FROM Parameter WHERE ID = ?", (int(id[i,j]),))
        result = cursor.fetchone()
        strClass, parameterA, parameterB, parameterC = result
        x = X[i,j]
        y = Y[i,j]
        name = f"{i}_{j}"
        meta.structureBuild_ForDataEvaluation(strClass, [parameterA, parameterB, parameterC], H, name)
        meta.fdtd.select(name)
        meta.fdtd.set("x", x)
        meta.fdtd.set("y", y)

cursor.close()
conn.close()
    
meta.fdtd.save("AllWav.fsp")

meta.fdtd.load("AllWav.fsp")
meta.fdtd.run()
meta.fdtd.save("AllWav.fsp")

meta.fdtd.load("AllWav.fsp")

Ex_plane = meta.fdtd.getresult("Monitor plane", "Ex")
Ex_plane = np.squeeze(Ex_plane)

savemat("D:\\WORK\\Achromatic_metalens_design_in_Windows\\Special_Phase_Implementation\\End.mat", 
        {'Ex_plane': Ex_plane})