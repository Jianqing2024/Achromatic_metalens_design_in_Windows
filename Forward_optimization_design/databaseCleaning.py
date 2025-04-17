import sqlite3
import os

def Clean():
    # 获取当前文件所在脚本的上一级（主目录）路径
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, '..', 'data')  # 如果当前脚本在子项目中
    DB_PATH = os.path.join(DATA_DIR, 'structures.db')

    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 清空数据库内的数据
    cursor.execute("DELETE FROM structures;")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='structures';")

    conn.commit()
    print("数据库清理完成")
    conn.close()