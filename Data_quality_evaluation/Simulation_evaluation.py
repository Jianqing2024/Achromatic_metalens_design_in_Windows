import numpy as np
import sqlite3
import optuna
import os
from tqdm import tqdm
# Pylance会由于不知名bug异常报错，似乎有一些PylanceBUG，不影响实际运行
from scipy.spatial import cKDTree # type: ignore
from .General_function import *

def OneD_Test(main):
    base_dir = os.getcwd()
    DB_PATH = os.path.join(base_dir, "data", "Main.db")

    uri_path = f"file:{DB_PATH}?mode=ro"

    conn = sqlite3.connect(uri_path, uri=True)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM BaseParameter WHERE baseValue=(?)', (main,))
    row = cursor.fetchone()
    
    single = row[1]
    h = row[2]
    
    ApproximateR, f, WavMax, WavMin = Read_Parameter()
    Wav = np.linspace(WavMax, WavMin, 5)
    r, N = Exact_Value(ApproximateR, single)
    l = np.linspace(0, r, N)
    
    ftx=[]
    for i in range(5):
        ftx[i] = Target_Phase_Standrad_1D(l, Wav[i], f)