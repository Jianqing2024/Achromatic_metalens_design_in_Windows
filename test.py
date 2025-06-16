import scipy.io
from MetaSet import advancedStructure as ad
import numpy as np
from tqdm import tqdm
# 载入 .mat 文件
data = scipy.io.loadmat('target_radius_1.mat')
# 查看所有变量名
print(data.keys())

# 假设你要提取的矩阵变量名为 'A'
matrix = data['target_radius_1']

print(matrix)

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
        addtogroup("name");
    """
    fdtd.eval(str)

meta = ad.MetaEngine(hide=True)

meta.fdtd.load('danyuan_planewave_ SiN.fsp')

meta.Reset()

meta.fdtd.addstructuregroup()
meta.fdtd.set("name", "name")

x = np.linspace(-138e-6, 138e-6, 600)
y = np.linspace(-138e-6, 138e-6, 600)
h = 0.8e-6

counter = 0
batch_size = 5000
total_count = 0
for index in tqdm(np.ndindex(matrix.shape), total=matrix.size):
    i, j = index
    xx, yy = x[i], y[j]
    r = matrix[i, j]

    if not np.isnan(r):
        addMetaCircle(meta.fdtd, "SiN_2", r, h, xx, yy)
        counter += 1
        total_count += 1

        if counter >= batch_size:
            # 保存当前模型
            save_path = "test.fsp"
            meta.fdtd.save(save_path)

            # 重载初始结构文件并重置
            meta.fdtd.load("test.fsp")
            meta.Reset()
            counter = 0

# 最后一批不足 5000 的结构也要保存
if counter > 0:
    save_path = "test.fsp"
    meta.fdtd.save(save_path)
        
meta.fdtd.save("test.fsp")