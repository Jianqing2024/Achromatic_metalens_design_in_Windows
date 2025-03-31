import MetaSet as ms
import importlib.util
import multiprocessing
import time
spec = importlib.util.spec_from_file_location("lumapi", "D:\\Program Files\\Lumerical\\v241\\api\\python\\lumapi.py")
lumapi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lumapi)
start_time_b=time.time()

fdtd1=lumapi.FDTD()
ms.setMetaFdtd(fdtd1,1e-6,1e-6,0.5e-6,-0.5e-6)
ms.addMetaSource(fdtd1,1e-6,1e-6,-0.5e-6,0.532e-6)
ms.classicMonitorGroup(fdtd1,1e-6,1e-6,0.5e-6)
ms.addMetaBase(fdtd1,"SiO2 (Glass) - Palik",0.1e-6,0.1e-6,0.1e-6)
fdtd1.save("s532b.fsp")
fdtd1.run()
data1=ms.classicDataAcquisition(fdtd1)
print(data1)

fdtd2=lumapi.FDTD()
ms.setMetaFdtd(fdtd2,1e-6,1e-6,0.5e-6,-0.5e-6)
ms.addMetaSource(fdtd2,1e-6,1e-6,-0.5e-6,0.800e-6)
ms.classicMonitorGroup(fdtd2,1e-6,1e-6,0.5e-6)
ms.addMetaBase(fdtd2,"SiO2 (Glass) - Palik",0.1e-6,0.1e-6,0.1e-6)
fdtd2.save("s800b.fsp")
fdtd2.run()
data2=ms.classicDataAcquisition(fdtd2)
print(data2)
stop_time_b=time.time()
execution_time = stop_time_b - start_time_b
print(f"运算时间b: {execution_time} 秒")