import numpy as np
import matlab.engine

# 启动 MATLAB 引擎
eng = matlab.engine.start_matlab()

# 生成一个 NumPy 数组
array = np.random.rand(10, 10)  # 生成 10x10 随机矩阵

# 将 NumPy 数组转换为 MATLAB 格式
matlab_array = matlab.double(array.tolist())  

# 调用 MATLAB 的自定义函数 "myscript"
result = eng.myscript(matlab_array)

# 关闭 MATLAB 引擎
eng.quit()

# 输出 MATLAB 计算结果
print(result)
