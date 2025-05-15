import sqlite3
from MetaSet import advancedStructure as ad
from .dataManager import *

def Comput(ids):
    DB_PATH = 'D:/WORK/Achromatic_metalens_design_in_Windows/data/Main.db'
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    #  初始化，建立计算对象，设置材料
    meta=ad.MetaEngine()
    meta.materialSet() # 暂且如此
    
    for key, values in ids.items():
        strClass,baseValue=key[0],key[1]
        cursor.execute("""
        SELECT parameterA, parameterB FROM BaseParameter
        WHERE baseValue = ?
        """, (baseValue,))
        row = cursor.fetchone()
        
        p, h = row[0], row[1]
        #   结构初始化
        meta.baseBuild(p)
        for id in values:
            #   分析输入，读取参数
            query = f"SELECT * FROM Parameter WHERE ID = ?"
            cursor.execute(query, (id,))
            row = cursor.fetchone()
            parameter=[row[3],row[4],row[5]]
            
            #   传入参数，建立结构
            meta.structureBuild(strClass, parameter, h)
            #   进行运算，提取数据
            meta.dataAcquisition()
            #   存入数据
            dataInput(meta, id, conn, cursor)
            #   半重置结构
            meta.semi_Reset()
        #   完全重置结构并Layout
        meta.Reset()