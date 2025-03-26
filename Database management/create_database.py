import sqlite3

# 创建 SQLite 数据库
db_file = "nanostructures.db"

# 连接数据库
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# 创建纳米结构表
cursor.execute("""
CREATE TABLE IF NOT EXISTS nanostructures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    structure_info TEXT UNIQUE
);
""")

# 创建测量数据表
cursor.execute("""
CREATE TABLE IF NOT EXISTS measurements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    structure_id INTEGER,
    wavelength REAL,
    phase_shift REAL,
    transmission REAL,
    FOREIGN KEY (structure_id) REFERENCES nanostructures(id)
);
""")

# 提交更改并关闭数据库连接
conn.commit()
conn.close()

print(f"数据库 {db_file} 创建完成！")
print("bbb")