import os
import sqlite3
import numpy as np
from scipy.io import savemat

db_path='D:/WORK/Achromatic_metalens_design_in_Windows/data/structures.db'

conn = sqlite3.connect(db_path, uri=True)
cursor = conn.cursor()

query = "SELECT anglein532, transin532, anglein800, transin800 FROM structures"
cursor.execute(query)

# 获取所有数据
rows = cursor.fetchall()
cursor.close()
conn.close()

phase532=np.zeros(10)
trans532=np.zeros(10)
phase800=np.zeros(10)
trans800=np.zeros(10)

for idx, row in enumerate(rows):
    phase532[idx],trans532[idx],phase800[idx],trans800[idx]=row

# 保存为 .mat 文件（变量名可自定义）
mat_dict = {
    'p532': phase532,
    't532': trans532,
    'p800': phase800,
    't800': trans800
}

save_path = 'D:/WORK/Achromatic_metalens_design_in_Windows/Numerical_stability_test/lum_r.mat'
savemat(save_path, mat_dict)

print(phase532)