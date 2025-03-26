import importlib.util

module_name = "lumopi"
file_path = "D:\\Program Files\\Lumerical\\v241\\api\\python\\lumapi.py"

spec = importlib.util.spec_from_file_location(module_name, file_path)
lumopi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lumopi) 

print("bbb")