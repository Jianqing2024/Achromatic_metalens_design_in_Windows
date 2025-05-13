import sqlite3

db_path = r"D:\WORK\Achromatic_metalens_design_in_Windows\data\Main.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 创建表
cursor.execute("""
CREATE TABLE IF NOT EXISTS BaseParameter (
    baseValue INTEGER PRIMARY KEY,
    parameterA REAL NOT NULL,
    parameterB REAL NOT NULL
    )
    """)

cursor.execute("""
CREATE TABLE IF NOT EXISTS Parameter (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    class INTEGER NOT NULL,
    baseValue INTEGER NOT NULL,
    parameterA REAL NOT NULL,
    parameterB REAL,
    parameterC REAL,
    angleIn532 REAL,
    angleIn599 REAL,
    angleIn666 REAL,
    angleIn733 REAL,
    angleIn800 REAL,
    transIn532 REAL,
    transIn599 REAL,
    transIn666 REAL,
    transIn733 REAL,
    transIn800 REAL
    )
    """)

# 提交更改并关闭连接
conn.commit()
conn.close()
print("Main database has been created! ")