import importlib.util

module_name = "lumapi"
file_path = "D:\\Program Files\\Lumerical\\v241\\api\\python\\lumapi.py"

spec = importlib.util.spec_from_file_location(module_name, file_path)
lumapi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lumapi) 

# 启动 FDTD 进程
fdtd = lumapi.FDTD()
fdtd.save(str(222) + '.fsp') # 保存文件
# 添加 FDTD 仿真区域
fdtd.addfdtd()

# 设置仿真区域大小（根据实际需要调整）
fdtd.set("x span", 5e-6)  # x 方向范围 5 µm
fdtd.set("y span", 5e-6)  # y 方向范围 5 µm
fdtd.set("z span", 2e-6)  # z 方向范围 2 µm

# 设置边界条件
fdtd.set("x min bc", "periodic")  # X 方向最小边界：周期性
fdtd.set("x max bc", "periodic")  # X 方向最大边界：周期性
fdtd.set("y min bc", "periodic")  # Y 方向最小边界：周期性
fdtd.set("y max bc", "periodic")  # Y 方向最大边界：周期性
fdtd.set("z min bc", "PML")       # Z 方向最小边界：PML
fdtd.set("z max bc", "PML")       # Z 方向最大边界：PML

# 保存和运行仿真（可选）
fdtd.save("fdtd_simulation.fsp")
fdtd.run()