import numpy as np 
from scipy.io import savemat 
import os 
import sqlite3 
from tqdm import tqdm 

base_dir = os.getcwd() 
DB_PATH = os.path.join(base_dir, "data", "Main.db") 
uri_path = f"file:{DB_PATH}?mode=ro" 
conn = sqlite3.connect(uri_path, uri=True) 
cursor = conn.cursor() 
ids = np.load("id.npy", allow_pickle=True) 
U = int(np.sqrt(ids.size))

phase780 = np.zeros([U, U]) 
phase532 = np.zeros([U, U]) 

cursor.execute("SELECT ID, angleIn1, angleIn5 FROM Parameter")
data = cursor.fetchall()

lookup = {ID: (a1, a5) for ID, a1, a5 in data}

for i in range(U):
    for j in range(U):
        phase780[i,j], phase532[i,j] = lookup[int(ids[i,j])]
        
savemat("D:\\WORK\\Achromatic_metalens_design_in_Windows\\figure\\End.mat", {'phase532': phase532, 'phase780': phase780})