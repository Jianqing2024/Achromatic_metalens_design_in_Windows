import sqlite3

# 连接数据库
conn = sqlite3.connect("nanostructures.db")
cursor = conn.cursor()

# 清除表中的所有数据
cursor.execute("DELETE FROM measurements;")
cursor.execute("DELETE FROM nanostructures;")

# 提交更改并关闭连接
conn.commit()
conn.close()

print("所有数据已清除，但表结构仍然存在。")
print("bbb")