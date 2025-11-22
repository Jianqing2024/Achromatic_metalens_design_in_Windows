import numpy as np
from scipy.io import savemat

def ParameterSave(save_path, COM):
    savemat(save_path, {
    'r': COM.r,
    'single': COM.single,
    'lambda': [0.780e-6, 0.532e-6]
    })