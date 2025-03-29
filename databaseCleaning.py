import sqlite3

conn = sqlite3.connect("structures.db")
cursor = conn.cursor()
# 清空数据库内的数据
cursor.execute("DELETE FROM structures;")
cursor.execute("DELETE FROM sqlite_sequence WHERE name='structures';")

conn.commit()
conn.close()    