import sqlite3

def creatDatabase():
    # 显式指定路径
    db_path = r"D:\WORK\Achromatic_metalens_design_in_Windows\data\Task.db"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 创建表任务表
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Parameter (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        baseValue INTEGER NOT NULL,
        parameterA REAL,
        parameterB REAL,
        parameterC REAL,
        angleIn532 REAL NOT NULL,
        transIn532 REAL NOT NULL,
        angleIn800 REAL NOT NULL,
        transIn800 REAL NOT NULL
    )
    """)

    cursor.execute("DELETE FROM Parameter;")

    # 提交更改并关闭连接
    conn.commit()
    conn.close()
    print("Task database has been created! ")
    
