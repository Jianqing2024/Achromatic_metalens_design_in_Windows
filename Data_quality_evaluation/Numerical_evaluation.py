import sqlite3
import os
import numpy as np

def Empty_array(N):
    x = np.linspace(-np.pi, np.pi, N)
    y = np.linspace(-np.pi, np.pi, N)

    mask = np.zeros((N, N), dtype=bool)
    return x, y, mask

def BaseParameter_Check():
    base_dir = os.getcwd()
    DB_PATH = os.path.join(base_dir, "data", "Main.db")

    uri_path = f"file:{DB_PATH}?mode=ro"

    conn = sqlite3.connect(uri_path, uri=True)
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM BaseParameter')
    rows = cursor.fetchall()
    conn.close()
    return int(rows[0][0])

def Numerical_Evaluation(N):
    BPnum = BaseParameter_Check()
    
    base_dir = os.getcwd()
    DB_PATH = os.path.join(base_dir, "data", "Main.db")

    uri_path = f"file:{DB_PATH}?mode=ro"

    conn = sqlite3.connect(uri_path, uri=True)
    cursor = conn.cursor()
    
    NUM = np.zeros(BPnum)
    
    for i in range(BPnum):
        cursor.execute('SELECT angleIn1, angleIn5 FROM Parameter WHERE baseValue=(?)', (i,))
        rows = cursor.fetchall()
        
        x, y, mask = Empty_array(N)
        for row in rows:
            px, py = row
            
            ix = (np.abs(x - px)).argmin()
            iy = (np.abs(y - py)).argmin()
            mask[iy, ix] = True
            
        NUM[i] = np.count_nonzero(mask)
    
    NUM = NUM/(N**2)
    return NUM