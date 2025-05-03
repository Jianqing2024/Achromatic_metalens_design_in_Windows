import os
import sqlite3
import numpy as np

db_path='D:/WORK/Achromatic_metalens_design_in_Windows/data/structures.db'

conn = sqlite3.connect(db_path, uri=True)
cursor = conn.cursor()

query = "SELECT structure_id, phase, transmittance FROM structures"
cursor.execute(query)

# 获取所有数据
rows = cursor.fetchall()

# 转换为 NumPy 数组（便于存入 .mat 文件）
data_array = np.array(rows)