import subprocess

# 穷举扫参
subprocess.run(["python", "fishnet_achromatic_Parallel.py"])

# 最优化计算
subprocess.run(["python", "script2.py"])

# 导出到MATLAB远场计算
subprocess.run(["python", "script3.py"])