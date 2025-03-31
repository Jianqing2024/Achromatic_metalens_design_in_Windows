import MetaSet as ms
import importlib.util
import multiprocessing
import time
spec = importlib.util.spec_from_file_location("lumapi", "D:\\Program Files\\Lumerical\\v241\\api\\python\\lumapi.py")
lumapi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lumapi)

time_a=time.time()
fdtd1=lumapi.FDTD(hide=True)
ms.setMetaFdtd(fdtd1,1e-6,1e-6,0.5e-6,-0.5e-6)
ms.addMetaSource(fdtd1,1e-6,1e-6,-0.5e-6,0.532e-6)
ms.classicMonitorGroup(fdtd1,1e-6,1e-6,0.5e-6)
ms.addMetaBase(fdtd1,"SiO2 (Glass) - Palik",0.1e-6,0.1e-6,0.1e-6)
fdtd1.save("s532b.fsp")
fdtd1.run()
data1=ms.classicDataAcquisition(fdtd1)
print(data1)
time_b=time.time()
fdtd2=lumapi.FDTD(hide=False)
ms.setMetaFdtd(fdtd2,1e-6,1e-6,0.5e-6,-0.5e-6)
ms.addMetaSource(fdtd2,1e-6,1e-6,-0.5e-6,0.532e-6)
ms.classicMonitorGroup(fdtd2,1e-6,1e-6,0.5e-6)
ms.addMetaBase(fdtd2,"SiO2 (Glass) - Palik",0.1e-6,0.1e-6,0.1e-6)
fdtd2.save("s800b.fsp")
fdtd2.run()
data2=ms.classicDataAcquisition(fdtd2)
print(data2)
time_c=time.time()

execution_time=time_c-time_b-time_b+time_a
print(f"第二个比第一个慢: {execution_time} 秒")