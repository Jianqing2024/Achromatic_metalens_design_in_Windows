import numpy as np
import os

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