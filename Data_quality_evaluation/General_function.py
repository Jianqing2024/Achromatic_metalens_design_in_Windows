import numpy as np
import os
import sqlite3

class Command:
    def __init__(self, mainValue):
        # 初始化
        self.mainValue = mainValue
        
        self.TargetPhase:list[float] = []
        
        self.r_target, self.f_target, self.WavMax, self.WavMin = Read_Parameter()
        self.Wav = np.linspace(self.WavMax, self.WavMin, 5)

        # 读取数据库资源进行计算
        base_dir = os.getcwd()
        DB_PATH = os.path.join(base_dir, "data", "Main.db")
        uri_path = f"file:{DB_PATH}?mode=ro"
        conn = sqlite3.connect(uri_path, uri=True)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM BaseParameter WHERE baseValue=(?)', (self.mainValue,))
        row = cursor.fetchone()
        
        self.single = row[1]
        
        self.r, self.N = Exact_Value(self.r_target, self.single)
        
        self.R = np.linspace(0, self.r, self.N)

        for i in range(5):
            self.TargetPhase.append(Target_Phase_Standrad_1D(self.R, self.Wav[i], self.f_target))
            
        conn.close()

#######################################################################################################################################################

def Target_Phase_Standrad_1D(x: np.ndarray, wav, f):
    ftx = -(2 * np.pi) / wav * (np.sqrt(x**2 + f**2) - f)
    # wrap 到 [-π, π)
    ftx = (ftx + np.pi) % (2 * np.pi) - np.pi
    return ftx

def Read_Parameter():
    base_dir = os.getcwd()
    filename = os.path.join(base_dir, "data", "parameter.txt")

    with open(filename, 'r') as f:
        lines = f.readlines()

    r = np.float64(lines[0].split('=')[1])
    f = np.float64(lines[1].split('=')[1])
    WavMax = np.float64(lines[2].split('=')[1])
    WavMin = np.float64(lines[3].split('=')[1])
    return r, f, WavMax, WavMin

def Exact_Value(ApproximateR, single):
    approx_N = round(ApproximateR / single)
    
    # 确保 N 是正偶整数
    if approx_N % 2 != 0:
        lower_even = approx_N - 1
        upper_even = approx_N + 1
    else:
        lower_even = approx_N - 2
        upper_even = approx_N + 2

    candidates = [lower_even, approx_N, upper_even]
    
    even_candidates = [N for N in candidates if N > 0 and N % 2 == 0]

    best_N = min(even_candidates, key=lambda N: abs(N * single - ApproximateR))
    r = best_N * single
    return r, best_N