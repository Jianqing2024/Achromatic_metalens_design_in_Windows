import scipy.io
from MetaSet import advancedStructure as ad
import numpy as np
from tqdm import tqdm
import time
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

#meta.fdtd.load('danyuan_planewave_ SiN.fsp')

#meta.Reset()

#meta.fdtd.addstructuregroup()
#meta.fdtd.set("name", "name")

#meta.fdtd.save("test.fsp")

x = np.linspace(-138e-6, 138e-6, 600)
y = np.linspace(-138e-6, 138e-6, 600)
h = 0.8e-6

valid_indices = np.argwhere(~np.isnan(matrix))  # 提前筛选出所有有效点

batch_size = 5000
batches = [valid_indices[i:i+batch_size] for i in range(0, len(valid_indices), batch_size)]

material = "SiN_2"

for file_index, batch in enumerate(tqdm(batches, desc="写入批次")):
    meta = ad.MetaEngine(hide=True)
    meta.fdtd.load('danyuan_planewave_ SiN.fsp')
    meta.Reset()
    meta.fdtd.addstructuregroup()
    meta.fdtd.set("name", "name")

    # 内层 tqdm：当前批次中结构写入
    for i, j in tqdm(batch, desc=f"写入结构 test{file_index+1}", leave=False):
        r = matrix[i, j]
        xx, yy = x[i], y[j]
        addMetaCircle(meta.fdtd, material, r, h, xx, yy)

    save_path = f"test{file_index+1}.fsp"
    meta.fdtd.save(save_path)
    print(f"[保存成功] {save_path}")
    time.sleep(1)