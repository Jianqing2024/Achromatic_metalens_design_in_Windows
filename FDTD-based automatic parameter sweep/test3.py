import MetaSet
import importlib.util

module_name = "lumapi"
file_path = "D:\\Program Files\\Lumerical\\v241\\api\\python\\lumapi.py"
spec = importlib.util.spec_from_file_location(module_name, file_path)
lumapi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lumapi) 

fdtd=lumapi.FDTD(filename="TTT.fsp",hide=False)
#fdtd = lumapi.FDTD()

MetaSet.setMetaFdtd(fdtd, 0.4e-6, 0.4e-6, 1e-6, -0.1e-6)
MetaSet.addMetaBase(fdtd, "SiO2 (Glass) - Palik", 0.4e-6, 0.4e-6, 0.4e-6)
MetaSet.addMetaCircle(fdtd, "Si (Silicon) - Palik", 0.18e-6, 0.6e-6)

MetaSet.addMetaSource(fdtd, 0.4e-6, 0.4e-6, -0.05e-6, 0.532e-6)

fdtd.save("fdtd_simulation.fsp")
fdtd.run()