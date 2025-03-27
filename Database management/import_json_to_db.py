import json
import sqlite3

# 读取 JSON 文件
json_file = "data.json"
with open(json_file, "r") as file:
    data = json.load(file)

# 连接数据库
db_file = "nanostructures.db"
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# 处理 JSON 数据
for item in data:
    structure_info = item["structure_info"]

    # 插入或获取纳米结构 ID
    cursor.execute("INSERT OR IGNORE INTO nanostructures (structure_info) VALUES (?)", (structure_info,))
    cursor.execute("SELECT id FROM nanostructures WHERE structure_info = ?", (structure_info,))
    structure_id = cursor.fetchone()[0]

    # 插入测量数据
    for measurement in item["measurements"]:
        wavelength = measurement["wavelength"]
        phase_shift = measurement["phase_shift"]
        transmission = measurement["transmission"]
        cursor.execute("""
        INSERT INTO measurements (structure_id, wavelength, phase_shift, transmission) 
        VALUES (?, ?, ?, ?)""", (structure_id, wavelength, phase_shift, transmission))

# 提交更改并关闭数据库
# 必须关闭数据库
conn.commit()
conn.close()

print("数据已成功导入数据库！")
