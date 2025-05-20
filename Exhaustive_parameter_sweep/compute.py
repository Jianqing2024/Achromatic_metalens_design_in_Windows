import sqlite3
from tqdm import tqdm
from MetaSet import advancedStructure as ad
from .dataManager import *

def Comput(ids):
    DB_PATH = 'D:/WORK/Achromatic_metalens_design_in_Windows/data/Main.db'
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    meta = ad.MetaEngine(parallel=True)
    meta.materialSet()

    for key, values in tqdm(ids.items(), desc="Base structures", unit="group"):
        strClass, baseValue = key[0], key[1]

        cursor.execute("""
        SELECT parameterA, parameterB FROM BaseParameter
        WHERE baseValue = ?
        """, (baseValue,))
        row = cursor.fetchone()
        p, h = row[0], row[1]

        meta.baseBuild(p)

        for id in tqdm(values, desc=f"→ base={baseValue}", unit="sim", leave=False):
            cursor.execute("SELECT * FROM Parameter WHERE ID = ?", (id,))
            row = cursor.fetchone()
            parameter = [row[3], row[4], row[5]]

            meta.structureBuild(strClass, parameter, h)
            meta.dataAcquisition()
            dataInput(meta, id, conn, cursor)
            meta.semi_Reset()

        meta.Reset()
    
    conn.close()

def STRUCT(meta, group, conn, cursor):
    dic = {}
    for index, item in enumerate(group):
        meta.Reset()
        name=f'test{index}.fsp'
        dic[name]=item["id"]
        strClass=item["class"]
        p=item["p"]
        h=item["h"]
        paramA=item["paramA"]
        paramB=item["paramB"]
        paramC=item["paramC"]
        
        parameter=parameter = [paramA, paramB, paramC]
        
        meta.baseBuild(p)
        meta.structureBuild(strClass, parameter, h)
        meta.fdtd.save(name)
        meta.fdtd.addjob(name)
         
    meta.fdtd.runjobs("FDTD")
    meta.fdtd.clearjobs()
            
    for name, id in dic.items():
        Ex, Trans = meta.StandardDataAcquisition(name)
        dataInput_Parallel(Ex, Trans, id, conn, cursor)


def ParallelComput(numParallel):
    DB_PATH = 'D:/WORK/Achromatic_metalens_design_in_Windows/data/Main.db'
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    meta = ad.MetaEngine(parallel=True)
    meta.materialSet()

    cursor.execute("SELECT ID, class, baseValue, parameterA, parameterB, parameterC FROM Parameter")
    all_rows = cursor.fetchall()

    group = []

    for row in tqdm(all_rows, desc="Task", unit="structures"):
        id = row[0]
        strClass = row[1]
        base_value = row[2]
        paramA = row[3]
        paramB = row[4]
        paramC = row[5]

        # 查询 BaseParameter 中的 baseValue 参数
        cursor.execute("SELECT parameterA, parameterB FROM BaseParameter WHERE baseValue = ?", (base_value,))
        base_row = cursor.fetchone()
        if base_row:
            base_paramA = base_row[0]
            base_paramB = base_row[1]
        else:
            base_paramA = base_paramB = None

        # 添加到当前组
        group.append({
            "id": id,
            "class": strClass,
            "paramA": paramA,
            "paramB": paramB,
            "paramC": paramC,
            "p": base_paramA,
            "h": base_paramB
        })

        if len(group) == numParallel:
            STRUCT(meta, group, conn, cursor)
            group=[]
                
    if group:
        STRUCT(meta, group, conn, cursor)

    conn.close()