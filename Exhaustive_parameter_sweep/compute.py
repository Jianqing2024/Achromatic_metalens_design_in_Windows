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
    
def ParallelComput(ids, numParallel, total):
    counterToTotal=0
    #if numParallel > 4:
    #    raise RuntimeError("ERROR: 在开启大于四重并行前请确认设置; 如已经设置请注释此判断")
    
    DB_PATH = 'D:/WORK/Achromatic_metalens_design_in_Windows/data/Main.db'
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    meta = ad.MetaEngine(parallel=False)
    meta.materialSet()

    for key, values in ids.items():
        strClass, baseValue = key[0], key[1]

        cursor.execute("""
        SELECT parameterA, parameterB FROM BaseParameter
        WHERE baseValue = ?
        """, (baseValue,))
        row = cursor.fetchone()
        p, h = row[0], row[1]

        meta.baseBuild(p)
        chunks = (lambda v, n: [v[i:i + n] for i in range(0, len(v), n)])(values, numParallel)
        
        for groups in chunks:
            counter=0
            dict = {}
            for id in groups:
                name=f'test{counter}.fsp'
                dict[name]=id
                cursor.execute("SELECT * FROM Parameter WHERE ID = ?", (id,))
                row = cursor.fetchone()
                parameter = [row[3], row[4], row[5]]
                meta.structureBuild(strClass, parameter, h)
                meta.fdtd.save(name)
                meta.semi_Reset()
                meta.fdtd.addjob(name)
                counter+=1
            meta.fdtd.runjobs()
            
            for name, id in dict.items():
                Ex, Trans = meta.StandardDataAcquisition(name)
                dataInput_Parallel(Ex, Trans, id, conn, cursor)
                counterToTotal+=1
                print(f'Task progress: {counterToTotal} / {total}')
                
        meta.Reset()
        
    conn.close()