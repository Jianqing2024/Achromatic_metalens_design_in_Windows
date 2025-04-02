import optuna
import numpy as np

# 定义目标函数（可以换成 Lumapi 的 FDTD 仿真）
def objective(trial):
    x = trial.suggest_float("x", -5, 5)
    y = trial.suggest_float("y", -5, 5)
    
    # 目标函数（这里只是一个简单示例）
    return (x - 2) ** 2 + (y + 3) ** 2  

# 创建优化任务（最小化目标函数）
study = optuna.create_study(direction="minimize")
study.optimize(objective, n_trials=500)  # 运行 50 次优化

# 输出最优参数
print("Best parameters:", study.best_params)
print("Best value:", study.best_value)
