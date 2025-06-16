from MetaSet import advancedStructure as ad
from MetaSet import structSet as ss
import numpy as np
import scipy.io

# 载入 .mat 文件
data = scipy.io.loadmat('your_file.mat')  # 替换为你的文件名

# 查看所有变量名
print(data.keys())

# 假设你要提取的矩阵变量名为 'A'
matrix = data['A']  # 这是一个 NumPy ndarray

# 确认维度
print(matrix.shape)
print(type(matrix))  # 应该是 <class 'numpy.ndarray'>

def addMetaCircle(fdtd, material, radius, high, x, y):
    """建立一个圆柱结构,结构的底面在z=0处,位置在正中

    Args:
        fdtd (fdtd): 必须在选中的fdtd窗口中进行设置
        material (str): 材料名为字符串,必须与FDTD材料库完全一致
        radius (double): 字面
        high (double): 字面
        name (str): 默认为cylinder
    """
    str = f"""
        addcircle;
    
        set("x", {x});
        set("y", {y});
        
        set("radius", {radius});
    
        set("z max", {high});
        set("z min", 0);
        
        set("material", "{material}");
    """
    fdtd.eval(str)

meta = ad.MetaEngine(hide=False)

x = np.linspace(-150e-6, 150e-6, 600)
y = np.linspace(-150e-6, 150e-6, 600)
r = 0.4e-6
h = 0.6e-6

for xx in x:
    for yy in y:
        addMetaCircle(meta.fdtd, "SiO2 (Glass) - Palik", r, h, xx, yy)