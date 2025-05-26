import sqlite3
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import os

def Data_Quality_Assessment():
    db_path = 'D:/WORK/Achromatic_metalens_design_in_Windows/data/Main.db'
    table_name = 'Parameter'

    # 连接数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 查询所有数据
    query = f"""
        SELECT baseValue, angleIn532, angleIn800 FROM {table_name}
        WHERE angleIn532 IS NOT NULL AND angleIn800 IS NOT NULL
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    # 分类数据：每个 baseValue 一个组
    grouped_data = defaultdict(list)

    for baseValue, phi_532, phi_800 in rows:
        delta_phi = phi_532 - phi_800  # 色散（正方向）
        grouped_data[baseValue].append((phi_532, delta_phi))

    # 绘图
    
    # 绘图部分
    n_groups = len(grouped_data)
    fig, axes = plt.subplots(n_groups, 1, figsize=(7, 4 * n_groups), sharex=True)

    if n_groups == 1:
        axes = [axes]

    for ax, (base, points) in zip(axes, grouped_data.items()):
        phi_532_list, delta_phi_list = zip(*points)

        ax.scatter(phi_532_list, delta_phi_list, label=f'baseValue = {base}', alpha=0.7)
        ax.set_ylabel("Phase difference Δφ = φ532 - φ800 (rad)")
        ax.set_title(f"Phase-Dispersion Map for baseValue = {base}")
        ax.grid(True)
        ax.legend()

    axes[-1].set_xlabel("Phase at 532 nm (rad)")

    plt.tight_layout()
    
    save_path = 'D:/WORK/Achromatic_metalens_design_in_Windows/figures/phase_dispersion.svg'
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, format='jpg')

    plt.close() 

    def compute_fill_ratio(phi_array, delta_array, bins=20):
        H, _, _ = np.histogram2d(phi_array, delta_array, bins=bins)
        filled_cells = np.sum(H > 0)
        fill_ratio = filled_cells / (bins * bins)
        return fill_ratio

    result = []

    for base, points in grouped_data.items():
        if len(points) < 5:
            continue  # 样本过少，不具代表性

        phi_array, delta_array = zip(*points)
        phi_array = np.array(phi_array)
        delta_array = np.array(delta_array)

        delta_phi_range = np.max(delta_array) - np.min(delta_array)
        phi_range = np.max(phi_array) - np.min(phi_array)

        fill_ratio = compute_fill_ratio(phi_array, delta_array, bins=20)

        result.append({
            "base": base,
            "Δφ_range": delta_phi_range,
            "φ_range": phi_range,
            "fill_ratio": fill_ratio
        })

    best = sorted(result, key=lambda x: (x["Δφ_range"], x["fill_ratio"]), reverse=True)

    for item in best[:10]:
        print(f"base: {item['base']}, fill ratio = {item['fill_ratio']:.3f}, Δφ_range = {item['Δφ_range']:.2f}")
    
    return best[0]

def Task_Database_Module(mainValue):
    db_path = r"D:\WORK\Achromatic_metalens_design_in_Windows\data\Task.db"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 创建表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS TaskParameter (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        class INTEGER NOT NULL,
        baseValue INTEGER NOT NULL,
        P REAL NOT NULL,
        H REAL NOT NULL,
        parameterA REAL NOT NULL,
        parameterB REAL,
        parameterC REAL,
        angleIn800 REAL,
        Dispersion REAL
        )
        """)

    # 提交更改并关闭连接
    conn.commit()
    conn.close()
    print("Task database has been created! ")
    
    source_db_path = r"D:\WORK\Achromatic_metalens_design_in_Windows\data\Main.db"

    source_conn = sqlite3.connect(source_db_path)
    source_cursor = source_conn.cursor()
    
    source_cursor.execute(f"""
    SELECT baseValue, parameterA, parameterB, parameterB, angleIn532, angleIn800 FROM Parameter
    WHERE baseValue = {mainValue} AND angleIn532 IS NOT NULL AND angleIn800 IS NOT NULL
    """)
    rows = source_cursor.fetchall()
    source_conn.close()

    # 计算 Δφ
    processed = []
    base=1
    phi_532=2
    phi_800=3
    for baseValue, parameterA, parameterB, parameterB, angleIn532, angleIn800 in rows:
        delta_phi = angleIn532 - angleIn800
        processed.append((base, phi_532, phi_800, delta_phi))
