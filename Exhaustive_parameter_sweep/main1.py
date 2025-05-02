import numpy as np
from collections import defaultdict
from MetaSet import advancedStructure as adv
import MetaSet as ms
import importlib.util
import sqlite3
import multiprocessing
from time import time
import importlib.util
import os

# 全局加载 lumapi 模块
spec = importlib.util.spec_from_file_location("lumapi", "D:\\Program Files\\Lumerical\\v241\\api\\python\\lumapi.py")
lumapi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lumapi)

def get_db_path():
    # 获取 main.py 的路径
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(base_dir, '..'))  # 回到 project/
    db_path = os.path.join(project_root, 'data', 'structures.db')
    return db_path

def split_matrix(matrix, num):
    n, m = matrix.shape
    avg_rows = n // num
    remainder = n % num

    # 前 remainder 份多一行，后面全是 avg_rows 行（最后一份最小）
    part_sizes = [avg_rows + 1 if i < remainder else avg_rows for i in range(num)]

    parts = []
    start = 0
    for size in part_sizes:
        parts.append(matrix[start:start + size])
        start += size

    return parts
def simulation(parameter,part,queue):
    fdtd=lumapi.FDTD(hide=True)

    fdtd.save(f"s{int(part)}.fsp")
        
    data = np.empty((0, 9))

    parameterPet=defaultdict(list)
    for row in parameter:
        param1, param2 = row[0], row[1]
        parameterPet[(param1, param2)].append(row)
        
    num = sum(len(v) for v in parameterPet.values())
        
    #pbar = tqdm(total=num, desc=f"进程 {int(part)} ", position=part)
        
    wav=[0.532e-6,0.800e-6]
    sourceName='s'
    groupName ='g'
    material1="SiO2 (Glass) - Palik"
    material2="TiO2 (Titanium Dioxide) - Devore"
    c=0
        
    for key, value in parameterPet.items():
        p,h=key[0],key[1]
        ms.setMetaFdtd(fdtd, p, p, 1e-6, -0.5e-6)
        ms.classicMonitorGroup(fdtd, p, p, 1e-6)
        ms.addMetaBase(fdtd, material1, p, p, 0.5e-6)
        for parameter in value:
            tic=time()
            l=parameter[2] # 十字结构长度
            w=parameter[3] # 十字结构宽度
            r=parameter[4] # 中心圆半径
                
            adv.fishnetset(fdtd, material2, h, l, w, r, name=groupName)
                
            main=np.array([[p,h,l,w,r]])
                
            ms.addMetaSource(fdtd, p, p, -0.25e-6, wav[0],name=sourceName)
            fdtd.run()
            data532 = ms.classicDataAcquisition(fdtd)
            fdtd.switchtolayout()
            
            adv.swichWaveLength(fdtd, wav[1], sourceName)
            fdtd.run()
            data800 = ms.classicDataAcquisition(fdtd)
            fdtd.switchtolayout()
            
            fdtd.select(sourceName)
            fdtd.delete()
                        
            Analysis=np.concatenate((main, data532, data800),axis=1)
            data = np.concatenate((data, Analysis),axis=0)
            fdtd.select(groupName)
            fdtd.delete()
            #pbar.update(1)
            c+=1
            toc=time()
            print(f"Process {part}: {c}/{num}, time={toc-tic}")
        fdtd.deleteall()
                
    print(f"[{part}] simulation done, sending to queue...")
    queue.put(data)
    print(f"[{part}] put completed.")
    fdtd.close()
def main(parallelsNum,parameter):
    processes = []
    queue = multiprocessing.Queue()

    for i in range(parallelsNum):
        iterations = parameter[i]
        p = multiprocessing.Process(target=simulation, args=(iterations, i, queue))
        processes.append(p)

    for p in processes:
        p.start()

    results = []
    for _ in range(parallelsNum):
        results.append(queue.get())
        
    print("数据收集结束")
    for p in processes:
        p.join()
            
    print("Join结束")
    return results

def mainFunction1():
    tic=time()
        
    print("扫参正在启动")
    
    DB_PATH = get_db_path()

    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    #"SiO2 (Glass) - Palik"

    # 计算参数
    parallelsNum=2
        
    #P=np.linspace(0.2e-6,0.5e-6,2)
    P=np.array([0.4e-6])
    #H=np.linspace(0.6e-6,0.8e-6,2)
    H=np.array([0.6e-6])
    #L=np.linspace(0.04e-6,0.5e-6,16)
    L=np.linspace(0.25e-6,0.4e-6,10)
    #W=np.linspace(0.04e-6,0.4e-6,16)
    W=np.array([0.11e-6])
    #R=np.linspace(0.04e-6,0.18e-6,16)
    R=np.array([0.12e-6])

    allParameterPet = np.full((0, 5), np.nan)
    for p in P:
        for h in H:
            for l in L:
                if l <= p:
                    for w in W:
                        if w < l:
                            for r in R:
                                if w <= 2 * r :
                                    allParameterPet = np.vstack([allParameterPet, np.array([p, h, l, w, r])])               
    parameter=split_matrix(allParameterPet,parallelsNum)
    results = main(parallelsNum, parameter)
    middle_result=np.concatenate(results, axis=0)
    print("完全退出并行")
    final_result=defaultdict(list)
        
    for row in middle_result:
        param1, param2 = row[0], row[1]
        final_result[(param1, param2)].append(row)
            
    counter=0
    for key, value in final_result.items():
        counter+=1
        for pa in value:
            p,h,l,w,r,a532,t532,a800,t800=pa[0],pa[1],pa[2],pa[3],pa[4],pa[5],pa[6],pa[7],pa[8]
                
            cursor.execute("""
            INSERT INTO structures (baseValue, P, H, L, W, R, angleIn532, transIn532, angleIn800, transIn800)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (int(counter), p, h, l, w, r, a532, t532, a800, t800))
                
    conn.commit()
    conn.close()
    toc=time()
    print(f'{toc-tic}s')
        
if __name__ == "__main__":
    mainFunction1()