import matlab.engine
import sqlite3
from scipy.io import savemat
from Data_quality_evaluation import main
import os
from Data_quality_evaluation import General_function as Gf
import numpy as np

best = main.Preliminary_numerical_evaluation(48)

COM = Gf.Command(best)

current_dir = os.getcwd()
path = os.path.join(current_dir, "Special_Phase_Implementation")
save_path = os.path.join(path, "data.mat")

eng = matlab.engine.start_matlab()
    
eng.cd(path, nargout=0)      # type: ignore

target_wav = [0.8e-6,0.5e-6]

for wav in target_wav:
    savemat(save_path, {
        'r': COM.r,
        'single': COM.single,
        'lambda': wav
    })
    eng.run('aaa.m', nargout=0) # type: ignore

