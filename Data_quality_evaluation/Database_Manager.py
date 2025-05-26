import sqlite3
import os

def TaskDatabase_Creat():
    base_dir = os.getcwd()
    DB_PATH = os.path.join(base_dir, "data", "Task.db")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 创建表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Parameter (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        class INTEGER NOT NULL,
        baseValue INTEGER NOT NULL,
        P REAL NOT NULL,
        H REAL NOT NULL,
        parameterA REAL NOT NULL,
        parameterB REAL,
        parameterC REAL,
        angleIn800 REAL,
        Dispersion REAL,
        Linear BOOL
        )
        """)

    # 提交更改并关闭连接
    conn.commit()
    conn.close()
    print("Main database has been created! ")