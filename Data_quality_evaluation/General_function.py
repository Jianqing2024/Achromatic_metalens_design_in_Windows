import numpy as np
import os
import sqlite3

class Command:
    #  定义一个用于在不同的模块间传递参数的对象
    def __init__(self, mainValue):
        # 初始化
        self.D = np.array([])
        self.mainValue = mainValue
        
        self.TargetPhase:list[float] = []
        self.TargetPhase_over:list[float] = []
        
        self.r_target, self.f_target = Read_Parameter()

        # 读取数据库
        base_dir = os.getcwd()
        DB_PATH = os.path.join(base_dir, "data", "Main.db")
        uri_path = f"file:{DB_PATH}?mode=ro"
        conn = sqlite3.connect(uri_path, uri=True)
        cursor = conn.cursor()

        cursor.execute('SELECT parameterA, parameterB FROM BaseParameter WHERE baseValue=(?)', (self.mainValue,))
        row = cursor.fetchone()
        
        self.single = row[0]        
        self.H = row[1]
        
        cursor.execute("SELECT material FROM SpectralParameters")
        self.material = cursor.fetchone()[0]
        
        #  波长段校验
        cursor.execute("SELECT wav1, wav2, wav3, wav4, wav5 FROM SpectralParameters")
        
        self.Wav = np.array(cursor.fetchone())
        
        #  与之前的定义不同，N指的是一个半径上的数量，而非一条直径上的数量
        self.r, self.N = Exact_Value(self.r_target, self.single)
        
        self.R = np.linspace(0.5*self.single, self.r, self.N)

        for i in range(5):
            self.TargetPhase.append(Target_Phase_Standrad_1D(self.R, self.Wav[i], self.f_target))
            
        conn.close()

        self.R_over = np.linspace(0.5*self.single, 1.5 * self.r, 4 * self.N)
        
        for i in range(5):
            self.TargetPhase_over.append(Target_Phase_Standrad_1D(self.R_over, self.Wav[i], self.f_target))

        self.Over = False

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
    return r, f

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