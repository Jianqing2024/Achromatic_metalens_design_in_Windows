import numpy as np
import MetaSet as ms
import importlib.util
import time

module_name = "lumapi"
file_path = "D:\\Program Files\\Lumerical\\v241\\api\\python\\lumapi.py"
spec = importlib.util.spec_from_file_location(module_name, file_path)
lumapi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lumapi) 

loopnum=5
matrix = np.zeros((loopnum, 2))

fdtd = lumapi.FDTD()

fdtd.save("fdtd_simulation.fsp")

radius=np.linspace(0.04e-6, 0.18e-6, loopnum)

start_time = time.time()

for i in range(loopnum):
    
    ms.setMetaFdtd(fdtd, 0.4e-6, 0.4e-6, 1e-6, -0.1e-6)
    ms.addMetaBase(fdtd, "SiO2 (Glass) - Palik", 0.4e-6, 0.4e-6, 0.4e-6)
    ms.addMetaSource(fdtd, 0.4e-6, 0.4e-6, -0.05e-6, 0.532e-6)
    ms.classicMonitorGroup(fdtd, 0.4e-6, 0.4e-6, 1e-6)
    ms.addMetaCircle(fdtd, "Si (Silicon) - Palik", radius[i], 0.6e-6)
    fdtd.run()
    data=ms.classicDataAcquisition(fdtd)
    matrix[i, :] = data
    fdtd.switchtolayout()
    fdtd.deleteall()

end_time = time.time()

elapsed_time = end_time - start_time
print(f"Simulation time: {elapsed_time} seconds")

#fdtd.save("fdtd_simulation.fsp")
print(matrix)