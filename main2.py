import optuna
import numpy as np
from time import time
from function2 import f2

def objective(trial):

    shift0 = trial.suggest_float("shift0", -np.pi, np.pi)
    shift1 = trial.suggest_float("shift1", -np.pi, np.pi)
    shift2 = trial.suggest_float("shift2", -0.05e-3, 0.05e-3)
    result1, result2 = f2(shift0,shift1,shift2)

    # 只返回第一个结果，作为优化目标
    return result1

study = optuna.create_study(direction="minimize")
study.optimize(objective, n_trials=10)

r1,r2=f2(**study.best_params)
print(r1,r2)