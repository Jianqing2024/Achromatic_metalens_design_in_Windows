import numpy as np
from collections import defaultdict
import sqlite3

def dataBaseClean():
    conn = sqlite3.connect('D:/WORK/Achromatic_metalens_design_in_Windows/data/Main.db')
    cursor = conn.cursor()

    # 获取所有用户自建的表名（排除SQLite系统表）
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name NOT LIKE 'sqlite_%';
    """)
    tables = cursor.fetchall()

    # 遍历每个表，执行 DELETE 语句
    for (table_name,) in tables:
        print(f"Clearing table: {table_name}")
        cursor.execute(f"DELETE FROM {table_name};")  # 删除表中所有数据
        cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table_name}';")  # 如果有自增ID，重置

    conn.commit()
    conn.close()

def defineMainvalue(P,H):
    ## 链接到主数据库
    DB_PATH = 'D:/WORK/Achromatic_metalens_design_in_Windows/data/Main.db'
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    print('Database is now online!')

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
    DB_PATH = 'D:/WORK/Achromatic_metalens_design_in_Windows/data/Main.db'
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
                                if w <= 2 * r :
                                    cursor.execute("""
                                    INSERT INTO Parameter (class, baseValue, parameterA, parameterB, parameterC)
                                    VALUES (?, ?, ?, ?, ?)
                                    """, (structerClass, mainID, l, w, r))
    conn.commit()
    conn.close()
    
def databaseCount():
    DB_PATH = 'D:/WORK/Achromatic_metalens_design_in_Windows/data/Main.db'
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

def resumeTaskDirectory():
    # 连接数据库
    DB_PATH = 'D:/WORK/Achromatic_metalens_design_in_Windows/data/Main.db'
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 允许用列名访问数据
    cursor = conn.cursor()

    # 查询所有 angleIn532 为 NULL 的行，只获取需要的字段
    query = f"""
        SELECT ID, class, baseValue FROM Parameter
        WHERE angleIn532 IS NULL
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
        "angleIn532", "angleIn599", "angleIn666", "angleIn733", "angleIn800",
        "transIn532", "transIn599", "transIn666", "transIn733", "transIn800"
    ]
    values = meta.Ex + meta.Trans  # 两个列表合并，顺序和字段对应

    set_clause = ", ".join([f"{field} = ?" for field in fields])
    sql = f"UPDATE Parameter SET {set_clause} WHERE ID = ?"
    cursor.execute(sql, values + [id])
    conn.commit()
    
def resumeCount():
    DB_PATH = 'D:/WORK/Achromatic_metalens_design_in_Windows/data/Main.db'
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM Parameter
        WHERE angleIn532 IS NULL
    """)
    result = cursor.fetchone()[0]
    conn.close()
    print(f'Total number of resume tasks: {result}')
    
def dataInput_Parallel(Ex, Trans, id, conn, cursor):
    fields = [
        "angleIn532", "angleIn599", "angleIn666", "angleIn733", "angleIn800",
        "transIn532", "transIn599", "transIn666", "transIn733", "transIn800"
    ]
    values = Ex + Trans  # 两个列表合并，顺序和字段对应

    set_clause = ", ".join([f"{field} = ?" for field in fields])
    sql = f"UPDATE Parameter SET {set_clause} WHERE ID = ?"
    cursor.execute(sql, values + [id])
    conn.commit()