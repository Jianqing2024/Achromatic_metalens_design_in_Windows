from scipy.io import savemat
import numpy as np
import sqlite3
import matlab.engine
import os
from tqdm import tqdm
from Data_quality_evaluation import main
import gdstk
from tqdm import tqdm
from scipy.spatial import cKDTree

def Create_template(id, cursor, lib):
    cursor.execute('SELECT class, parameterA, parameterB, parameterC FROM Parameter WHERE ID=(?)', (id,))
    row = cursor.fetchone()
    Class, parameterA, parameterB, parameterC = row
    if Class == 1:
        radius = parameterA*1e6
        cell_name = f"CIRCLE_{radius:.6f}"
        cell = lib.new_cell(cell_name)
        circle = gdstk.ellipse((0, 0), radius, tolerance=1e-3)
        cell.add(circle)
    elif Class == 2:
        long = parameterA*1e6
        cell_name = f"RECT_{long:.6f}"
        cell = lib.new_cell(cell_name)
        half = long/2
        rect = gdstk.rectangle((-half, -half),( half,  half))
        cell.add(rect)
    elif Class == 3:
        long, short = parameterA*1e6, parameterB*1e6
        cell_name = f"Cross_{long:.6f}_{short:.6f}"
        cell = lib.new_cell(cell_name)
        half_long = long/2
        half_short = short/2
        rect_h = gdstk.rectangle((-half_long, -half_short),( half_long,  half_short))
        rect_v = gdstk.rectangle((-half_short, -half_long),( half_short,  half_long))
        cell.add(rect_h)
        cell.add(rect_v)
    elif Class == 4:
        long, short, radius = parameterA*1e6, parameterB*1e6, parameterC
        cell_name = f"Fishnet_{long:.6f}_{short:.6f}_{radius:.6f}"
        cell = lib.new_cell(cell_name)
        half_long = long/2
        half_short = short/2
        rect_h = gdstk.rectangle((-half_long, -half_short),( half_long,  half_short))
        rect_v = gdstk.rectangle((-half_short, -half_long),( half_short,  half_long))
        circle = gdstk.ellipse((0, 0), radius, tolerance=1e-3)
        cell.add(rect_h)
        cell.add(rect_v)
        cell.add(circle)
    return cell

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
DB_PATH = os.path.join(base_dir, "data", "Main.db")
uri_path = f"file:{DB_PATH}?mode=ro"
conn = sqlite3.connect(uri_path, uri=True)
cursor = conn.cursor()

cursor.execute('SELECT parameterA, parameterB FROM BaseParameter WHERE baseValue=(?)', (best,))
row = cursor.fetchone()

r = 0.5e-3
single = row[0]
H = row[1]
wav = [0.780e-6, 0.532e-6]
l = 5e-3
Fnum = 25
start = 5e-3
stop = 5.5e-3
singleDownsampling = 0.8e-6
loop = 10
popnum = 10

U = int(r*2/single)
UDownsampling = int(r/singleDownsampling*2)

Ft = Random_Matrix_Generation(U, Fnum)

Ft_low = Random_Matrix_Generation(UDownsampling, Fnum)

current_dir = os.getcwd()
path = os.path.join(current_dir, "Special_Phase_Implementation")
save_path = os.path.join(path, "data.mat")

eng = matlab.engine.start_matlab() 
eng.cd(path, nargout=0)

phase = [np.zeros((U,U)), np.zeros((U,U))]
Eout = [np.zeros((U,U)),np.zeros((U,U))]
for i, wav in enumerate(wav):
    Eout_i, phase_i = eng.NBphase(r, single, wav, l, float(Fnum), start, stop, singleDownsampling, loop, popnum, Ft, Ft_low, nargout=2)
    phase[i] = np.array(phase_i)
    Eout[i] = np.array(Eout_i)
    print("Next")

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
id_list = np.unique(ids)

lib = gdstk.Library(unit=1e-6, precision=1e-9)
top = lib.new_cell("TOP")

x = np.linspace(-(r-0.5*single), (r-0.5*single), U)*1e6
y = np.linspace(-(r-0.5*single), (r-0.5*single), U)*1e6
X, Y = np.meshgrid(x, y)

ids[np.sqrt(X**2 + Y**2)>(r*1e6)] = np.nan

for id in tqdm(id_list):
    cell = Create_template(id, cursor, lib)
    positions = np.argwhere(ids == id)
    for po in positions:
        x, y = X[po[0],po[1]], Y[po[0],po[1]]
        ref = gdstk.Reference(cell, origin=(x, y))
        top.add(ref)

lib.write_gds("physical_parameter_circles.gds")
print("GDS 文件已生成")