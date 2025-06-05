import sqlite3
import os
import numpy as np

def DatabaseCreat(SpectralRange, material):
    base_dir = os.getcwd()
    DB_PATH = os.path.join(base_dir, "data", "Main.db")

    conn = sqlite3.connect(DB_PATH)
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
        angleIn1 REAL,
        angleIn2 REAL,
        angleIn3 REAL,
        angleIn4 REAL,
        angleIn5 REAL,
        transIn1 REAL,
        transIn2 REAL,
        transIn3 REAL,
        transIn4 REAL,
        transIn5 REAL
        )
        """)
    
    cursor.execute("DROP TABLE IF EXISTS SpectralParameters;")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS SpectralParameters (
        wav1 REAL NOT NULL,
        wav2 REAL NOT NULL,
        wav3 REAL NOT NULL,
        wav4 REAL NOT NULL,
        wav5 REAL NOT NULL,
        material TEXT
        )
        """)
    
    Range = np.linspace(SpectralRange[0], SpectralRange[1], 5)
    cursor.execute(
        "INSERT INTO SpectralParameters (wav1, wav2, wav3, wav4, wav5, material) VALUES (?, ?, ?, ?, ?, ?)",
        tuple(Range) + (material,))

    # 提交更改并关闭连接
    conn.commit()
    conn.close()
    print("Main database has been created! ")