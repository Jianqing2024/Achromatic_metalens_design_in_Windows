import matlab.engine
from scipy.io import savemat
from Data_quality_evaluation import main
import os
from Data_quality_evaluation import General_function as Gf
import numpy as np
import sqlite3

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

    savemat("D:\\WORK\\Achromatic_metalens_design_in_Windows\\Special_Phase_Implementation\\ft.mat", {
    'Ft': Ft
    })

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

r = 0.8e-3
single = row[0]        
H = row[1]
Fnum = 400
start = 23e-3
stop = 25e-3
U = int(r*2/single)
l = 20e-3

Ft = Random_Matrix_Generation(U, Fnum)
print(Ft.shape)

current_dir = os.getcwd()
path = os.path.join(current_dir, "Special_Phase_Implementation")
save_path = os.path.join(path, "data.mat")

eng = matlab.engine.start_matlab()
eng.cd(path, nargout=0)

target_wav = [0.780e-6,0.532e-6]

phase = [None, None]
Eout = [None,None]
for i, wav in enumerate(target_wav):
    [phase[i],Eout[i]] = eng.NBphase(r,single,wav,l,U,Fnum,start,stop,Ft,nargout=2)

shift, phase[1], total_diff = minimize_difference(phase[0], phase[1])