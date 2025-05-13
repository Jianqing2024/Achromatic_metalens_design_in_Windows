import numpy as np
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
    print('数据库已上线')

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