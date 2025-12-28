import h5py
import numpy as np
import gdstk

# 读取 MATLAB v7.3 文件
file_path = "radius.mat"
with h5py.File(file_path, 'r') as f:
    # 假设保存的变量名就是 physical_parameter
    physical_parameter_refs = f['physical_parameter']

    # 先遍历，取出每个 cell 的数据
    physical_parameter = []
    for ref in physical_parameter_refs: # type: ignore
        data_ref = ref[0]  # cell 内容引用
        data = np.array(f[data_ref]).T  # MATLAB 行列转置
        physical_parameter.append(data)

print(f"共有 {len(physical_parameter)} 个半径组")
lib = gdstk.Library(unit=1e-6, precision=1e-9)
top = lib.new_cell("TOP")

i = 0
# 遍历每个半径组
for group in physical_parameter:
    i+=1
    print(i)

    if group.size == 0:
        continue  # 跳过空组
    radius = group[0,0]  # 同一组半径
    cell_name = f"CIRCLE_{radius:.6f}"
    circle_cell = lib.new_cell(cell_name)
    # 添加模板圆
    circle = gdstk.ellipse((0, 0), radius, tolerance=1e-3)
    circle_cell.add(circle)

    # 遍历组内所有圆的位置
    for row in group:
        _, x, y = row
        ref = gdstk.Reference(circle_cell, origin=(x, y))
        top.add(ref)

# 写 GDS 文件
lib.write_gds("physical_parameter_circles.gds")
print("GDS 文件已生成")