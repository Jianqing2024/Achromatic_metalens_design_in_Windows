import numpy as np
from collections import defaultdict
import sqlite3
import os
import gdstk

def dataBaseClean():
    base_dir = os.getcwd()
    DB_PATH = os.path.join(base_dir, "MetaBase", "Main.db")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 清理指定的两个表
    target_tables = ['Parameter', 'BaseParameter']

    for table_name in target_tables:
        print(f"Clearing table: {table_name}")
        cursor.execute(f"DELETE FROM {table_name};")  # 删除表中所有数据
        cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table_name}';")  # 如果有自增ID，重置

    conn.commit()
    conn.close()
    
def defineMainvalue(P,H):
    ## 链接到主数据库
    base_dir = os.getcwd()
    DB_PATH = os.path.join(base_dir, "MetaBase", "Main.db")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    print('Empty database is now online')

    ## 定义参数
    #  定义并加载主参数，储存到附表
    baseValue = np.full((0, 2), np.nan)
    for p in P:
        for h in H:
            baseValue=np.vstack([baseValue, np.array([p, h])])
            
    BaseParameter = {i: tuple(row) for i, row in enumerate(baseValue)}
    for key, value in BaseParameter.items():
        cursor.execute("""
        INSERT INTO BaseParameter (baseValue, parameterA, parameterB)
        VALUES (?, ?, ?)
        """, (int(key), value[0], value[1]))
        
    conn.commit()
    conn.close()

def parameterFilling(structerClass, classParameter):
    ## 重新加载主参数序列
    base_dir = os.getcwd()
    DB_PATH = os.path.join(base_dir, "MetaBase", "Main.db")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM BaseParameter")

    rows = cursor.fetchall()

    #  转换为二维 numpy 矩阵
    mainValue = np.array(rows)
    
    ## 将主参数序列与类参数组合，并选择其中与类参数符合的量
    #  圆柱
    if structerClass==1:
        for row in mainValue:
            for C in classParameter:
                mainID=row[0]
                p=row[1]
                h=row[2]
                r=C
                if 2*r < p:
                    cursor.execute("""
                    INSERT INTO Parameter (class, baseValue, parameterA)
                    VALUES (?, ?, ?)
                    """, (structerClass, mainID, r))
    #  方形柱
    elif structerClass==2:
        for row in mainValue:
            for C in classParameter:
                mainID=row[0]
                p=row[1]
                h=row[2]
                l=C
                if l < p:
                    cursor.execute("""
                    INSERT INTO Parameter (class, baseValue, parameterA)
                    VALUES (?, ?, ?)
                    """, (structerClass, mainID, l))
    #  十字形柱
    elif structerClass==3:
        for row in mainValue:
            for C in classParameter[0]:
                for D in classParameter[1]:
                    mainID=row[0]
                    p=row[1]
                    h=row[2]
                    l=C
                    w=D
                    if l < p:
                        if l > w:
                            cursor.execute("""
                            INSERT INTO Parameter (class, baseValue, parameterA, parameterB)
                            VALUES (?, ?, ?, ?)
                            """, (structerClass, mainID, l, w))
    #   渔网柱
    elif structerClass==4:
        for row in mainValue:
            for C in classParameter[0]:
                for D in classParameter[1]:
                    for E in classParameter[2]:
                        mainID=row[0]
                        p=row[1]
                        h=row[2]
                        l=C
                        w=D
                        r=E
                        if l <= p:
                            if l > w:
                                if w > 2 * r :
                                    cursor.execute("""
                                    INSERT INTO Parameter (class, baseValue, parameterA, parameterB, parameterC)
                                    VALUES (?, ?, ?, ?, ?)
                                    """, (structerClass, mainID, l, w, r))
    conn.commit()
    conn.close()
    
def databaseCount():
    base_dir = os.getcwd()
    DB_PATH = os.path.join(base_dir, "MetaBase", "Main.db")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM Parameter')
    count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM Parameter WHERE class = 1')
    count1 = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM Parameter WHERE class = 2')
    count2 = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM Parameter WHERE class = 3')
    count3 = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM Parameter WHERE class = 4')
    count4 = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT baseValue) FROM Parameter")
    num_classes = cursor.fetchone()[0]

    print(f"Total number of tasks: {count}\nClass1: {count1} | Class2: {count2} | Class3: {count3} | Class4: {count4}\nBasicValue quantities: {num_classes}")
    conn.close()
    return count

def resumeTaskDirectory():
    # 连接数据库
    base_dir = os.getcwd()
    DB_PATH = os.path.join(base_dir, "MetaBase", "Main.db")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 允许用列名访问数据
    cursor = conn.cursor()

    # 查询所有 angleIn1 为 NULL 的行，只获取需要的字段
    query = f"""
        SELECT ID, class, baseValue FROM Parameter
        WHERE angleIn1 IS NULL
    """
    cursor.execute(query)

    # 使用 defaultdict 自动创建列表分组
    result = defaultdict(list)
    for row in cursor.fetchall():
        key = (row['class'], row['baseValue'])  # 分组依据
        result[key].append(row['ID'])           # 加入 ID

    conn.close()
    return dict(result)  # 转为普通 dict 返回

def dataInput(meta, id, conn, cursor):
    fields = [
        "angleIn1", "angleIn2", "angleIn3", "angleIn4", "angleIn5",
        "transIn1", "transIn2", "transIn3", "transIn4", "transIn5"
    ]
    values = meta.Ex + meta.Trans  # 两个列表合并，顺序和字段对应

    set_clause = ", ".join([f"{field} = ?" for field in fields])
    sql = f"UPDATE Parameter SET {set_clause} WHERE ID = ?"
    cursor.execute(sql, values + [id])
    conn.commit()
    
def resumeCount():
    base_dir = os.getcwd()
    DB_PATH = os.path.join(base_dir, "MetaBase", "Main.db")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM Parameter
        WHERE angleIn5 IS NULL
    """)
    result = cursor.fetchone()[0]
    conn.close()
    print(f'Total number of resume tasks: {result}')
    return result
    
def dataInput_Parallel(Ex, Trans, id, conn, cursor):
    fields = [
        "angleIn1", "angleIn2", "angleIn3", "angleIn4", "angleIn5",
        "transIn1", "transIn2", "transIn3", "transIn4", "transIn5"
    ]
    values = Ex + Trans  # 两个列表合并，顺序和字段对应

    set_clause = ", ".join([f"{field} = ?" for field in fields])
    sql = f"UPDATE Parameter SET {set_clause} WHERE ID = ?"
    cursor.execute(sql, values + [id])
    conn.commit()

def Create_template(id, cursor, lib):
    cursor.execute('SELECT class, parameterA, parameterB, parameterC FROM Parameter WHERE ID=(?)', (id,))
    row = cursor.fetchone()
    Class, parameterA, parameterB, parameterC = row
    if Class == 1:
        radius = parameterA*1e6
        cell_name = f"CIRCLE_{radius:.6f}"
        cell = lib.new_cell(cell_name)
        circle = gdstk.ellipse((0, 0), radius, tolerance=1e-3)
        cell.add(circle)
    elif Class == 2:
        long = parameterA*1e6
        cell_name = f"RECT_{long:.6f}"
        cell = lib.new_cell(cell_name)
        half = long/2
        rect = gdstk.rectangle((-half, -half),( half,  half))
        cell.add(rect)
    elif Class == 3:
        long, short = parameterA*1e6, parameterB*1e6
        cell_name = f"Cross_{long:.6f}_{short:.6f}"
        cell = lib.new_cell(cell_name)
        half_long = long/2
        half_short = short/2
        rect_h = gdstk.rectangle((-half_long, -half_short),( half_long,  half_short))
        rect_v = gdstk.rectangle((-half_short, -half_long),( half_short,  half_long))
        cell.add(rect_h)
        cell.add(rect_v)
    elif Class == 4:
        long, short, radius = parameterA*1e6, parameterB*1e6, parameterC
        cell_name = f"Fishnet_{long:.6f}_{short:.6f}_{radius:.6f}"
        cell = lib.new_cell(cell_name)
        half_long = long/2
        half_short = short/2
        rect_h = gdstk.rectangle((-half_long, -half_short),( half_long,  half_short))
        rect_v = gdstk.rectangle((-half_short, -half_long),( half_short,  half_long))
        circle = gdstk.ellipse((0, 0), radius, tolerance=1e-3)
        cell.add(rect_h)
        cell.add(rect_v)
        cell.add(circle)
    return cell

def write_GDS_from_id_matrix(ids, output_filename="metalens_layout.gds", db_path=None):
    """将结构 ID 矩阵直接写入 GDS 文件。

    唯一必需输入为 ids 矩阵（2D numpy array，每个元素为数据库中的结构 ID）。
    周期 single 从数据库自动读取（通过 ids 中任意有效 ID 反查 baseValue）。
    半径 r 根据 ids 矩阵尺寸和 single 自动计算。

    Args:
        ids (np.ndarray):  (U, U) 的结构 ID 矩阵，圆外区域应为 np.nan
        output_filename (str): 输出 GDS 文件名
        db_path (str, optional): 数据库路径，默认使用 MetaBase/Main.db
    """
    import gdstk
    from tqdm import tqdm

    if db_path is None:
        base_dir = os.getcwd()
        db_path = os.path.join(base_dir, "MetaBase", "Main.db")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # ---- 从数据库自动获取 single（周期）----
    # 取 ids 中第一个有效 ID，反查其 baseValue，再查 single
    valid_mask = ~np.isnan(ids)
    if not np.any(valid_mask):
        raise ValueError("ids 矩阵中没有有效 ID（全为 NaN）。")

    first_id = int(ids[valid_mask][0])
    cursor.execute("SELECT baseValue FROM Parameter WHERE ID = ?", (first_id,))
    row = cursor.fetchone()
    if row is None:
        raise ValueError(f"ID {first_id} 在数据库中不存在。")
    base_value = row[0]

    cursor.execute("SELECT parameterA FROM BaseParameter WHERE baseValue = ?", (base_value,))
    row = cursor.fetchone()
    if row is None:
        raise ValueError(f"baseValue {base_value} 在数据库中不存在。")
    single = row[0]  # 周期 (m)

    # ---- 计算几何参数 ----
    U = ids.shape[0]
    r = U * single / 2  # 半径 (m)

    print(f"Auto-detected: U={U}, single={single*1e9:.0f}nm, r={r*1e6:.1f}um")

    # ---- 坐标网格 (um) ----
    x = np.linspace(-(r - 0.5 * single), (r - 0.5 * single), U) * 1e6
    y = np.linspace(-(r - 0.5 * single), (r - 0.5 * single), U) * 1e6
    X, Y = np.meshgrid(x, y)

    # 圆形掩膜
    ids_copy = ids.copy()
    ids_copy[np.sqrt(X**2 + Y**2) > (r * 1e6)] = np.nan
    id_list = np.unique(ids_copy[~np.isnan(ids_copy)]).astype(int)

    # ---- GDS 生成 ----
    lib = gdstk.Library(unit=1e-6, precision=1e-9)
    top = lib.new_cell("TOP")

    for sid in tqdm(id_list, desc="Writing GDS"):
        cell = Create_template(int(sid), cursor, lib)
        positions = np.argwhere(ids_copy == sid)
        for po in positions:
            px, py = X[po[0], po[1]], Y[po[0], po[1]]
            ref = gdstk.Reference(cell, origin=(px, py))
            top.add(ref)

    lib.write_gds(output_filename)
    print(f"GDS 文件已生成: {output_filename}")

    conn.close()