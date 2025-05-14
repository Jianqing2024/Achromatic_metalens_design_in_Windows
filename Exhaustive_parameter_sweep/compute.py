import sqlite3
from MetaSet import advancedStructure as ad

def Comput(ids):
    DB_PATH = 'D:/WORK/Achromatic_metalens_design_in_Windows/data/Main.db'
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    #  初始化，建立计算对象
    meta=ad.MetaEngine()
    
    for key, values in ids.items():
        strClass,baseValue=key[0],key[1]
        cursor.execute("""
        SELECT parameterA, parameterB FROM BaseParameter
        WHERE baseValue = ?
        """, (baseValue,))
        row = cursor.fetchone()
        
        p, h = row[0], row[1]
        
        for va in values:
            #   分析输入，计算参数
            query = f"SELECT * FROM Parameter WHERE ID = ?"
            cursor.execute(query, (2,))
            row = cursor.fetchone()
            parameter=[row[3],row[4],row[5]]
            
            #   传入参数，建立结构
        
            #   进行运算，提取数据
        
            #   半重置结构
            
        #   完全重置结构