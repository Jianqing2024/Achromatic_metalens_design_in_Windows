import MetaSet as ms
import importlib.util
import multiprocessing
import time

spec = importlib.util.spec_from_file_location("lumapi", "D:\\Program Files\\Lumerical\\v241\\api\\python\\lumapi.py")
lumapi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lumapi)

def testfunction(param):
    
    if param==0.532e-6:
        fdtd1=lumapi.FDTD()
        fdtd=fdtd1
    elif param==0.800e-6:
        fdtd2=lumapi.FDTD()
        fdtd=fdtd2
    
    ms.setMetaFdtd(fdtd,1e-6,1e-6,0.5e-6,-0.5e-6)
    ms.addMetaSource(fdtd,1e-6,1e-6,-0.5e-6,param)
    ms.classicMonitorGroup(fdtd,1e-6,1e-6,0.5e-6)
    ms.addMetaBase(fdtd,"SiO2 (Glass) - Palik",0.1e-6,0.1e-6,0.1e-6)
    fdtd.save(f"s{int(param*1e9)}.fsp")
    fdtd.run()
    data=ms.classicDataAcquisition(fdtd)
    return data


start_time_a = time.time()
if __name__ == "__main__":
    params = [0.532e-6, 0.800e-6]  # 两个不同的参数
    with multiprocessing.Pool(processes=2) as pool:
        results = pool.map(testfunction, params)
    
    print(results)

stop_time_a = time.time()
execution_time = stop_time_a - start_time_a
print(f"运算时间a: {execution_time} 秒")