import sqlite3
from tqdm import tqdm
from MetaSet import advancedStructure as ad
from .dataManager import *

def Comput(ids):
    DB_PATH = 'D:/WORK/Achromatic_metalens_design_in_Windows/data/Main.db'
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    meta = ad.MetaEngine()
    meta.materialSet()
    counter = 0

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
            #tic = time()
            counter += 1

            cursor.execute("SELECT * FROM Parameter WHERE ID = ?", (id,))
            row = cursor.fetchone()
            parameter = [row[3], row[4], row[5]]

            meta.structureBuild(strClass, parameter, h)
            meta.dataAcquisition()
            dataInput(meta, id, conn, cursor)
            meta.semi_Reset()

        meta.Reset()
    
    conn.close()