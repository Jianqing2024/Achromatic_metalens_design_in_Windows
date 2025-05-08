import numpy as np
import importlib.util
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

spec = importlib.util.spec_from_file_location("lumapi", "D:\\Program Files\\Lumerical\\v241\\api\\python\\lumapi.py")
lumapi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lumapi)

pi=np.pi

def Task_directory_generation(bool_matrix):
    rows, cols = bool_matrix.shape
    neighbors_dict = {}

    # 遍历所有为 False 的位置
    for i in range(rows):
        for j in range(cols):
            if not bool_matrix[i, j]:
                neighbors = []

                # 遍历邻域（从 i-1 到 i+1，j-1 到 j+1）
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        ni, nj = i + di, j + dj

                        # 排除自己
                        if di == 0 and dj == 0:
                            continue

                        # 边界检查
                        if 0 <= ni < rows and 0 <= nj < cols:
                            if bool_matrix[ni, nj]:  # 只要非0的
                                neighbors.append((ni, nj))

                # 如果有非零邻居，则记录
                if neighbors:
                    neighbors_dict[(i, j)] = neighbors
    return neighbors_dict

## 确定一个单独的、确定的baseValue
p=0.4e-6
h=0.6e-6

## 扫描现有数据库，确定缺位，形成任务目录
# 获取当前文件所在脚本的上一级（主目录）路径
DB_PATH = 'D:/WORK/Achromatic_metalens_design_in_Windows/data/structures.db'
# 连接数据库
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("SELECT * FROM structures WHERE P = ? AND H = ?", (p, h))

results = cursor.fetchall()
conn.close()

# 初始化双相位空间
sweep532=10
sweep800=10

bins_532 = np.linspace(-pi, pi, sweep532 + 1)
bins_800 = np.linspace(-pi, pi, sweep800 + 1)

# 填充已有的空间
Phase_space={}
for row in results:
    id        = row[0]
    phase_532 = row[7]
    phase_800 = row[9]

    # 获取 bin 索引（从 0 开始）
    bin_532 = np.digitize(phase_532, bins_532) - 1
    bin_800 = np.digitize(phase_800, bins_800) - 1
    
    Phase_space[id] = [bin_532, bin_800]

phaseMatrix_Bool = np.zeros((sweep532,sweep800),dtype=bool)
for i, j in np.ndindex(phaseMatrix_Bool.shape):
    for key, value in Phase_space.items(): 
        if value[0]-i==0 and value[1]-j==0:
            phaseMatrix_Bool[i,j]=True
            break

plt.imshow(phaseMatrix_Bool, cmap=mcolors.ListedColormap(['grey', 'green']))
plt.title('Task directory')
plt.xlabel('Phase in 532')
plt.ylabel('Phase in 800')
plt.xticks([])
plt.yticks([])
plt.grid(False)
plt.show(block=False)
#plt.close()
#plt.pause(10)

directory_generation=Task_directory_generation(phaseMatrix_Bool)
matched_keys = []
DIC={}
for key, values in directory_generation.items():
    DIC_Key_532=(bins_532[key[0]+1]+bins_532[key[0]])/2
    DIC_Key_800=(bins_800[key[1]+1]+bins_800[key[1]])/2
    
    DICkey=tuple([DIC_Key_532, DIC_Key_800])

    for value in values:
        for keykey, value_list in Phase_space.items():
            if (value_list[0]-value[0])+(value_list[1]-value[1])==0 :
                matched_keys.append(keykey)
    DIC[DICkey]=matched_keys
    matched_keys = []

for key ,value in DIC.items():
    print(f'key: {key}   value: {value}\n')

# 填充相位色散库