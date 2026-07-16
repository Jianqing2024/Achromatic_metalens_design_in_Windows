from solid import *
from solid.utils import *
import os

def generate_array(nx, ny, pitch, radius, height):
    model = []
    for i in range(nx):
        for j in range(ny):
            x, y = i * pitch, j * pitch
            cyl = translate([x, y, 0])(cylinder(r=radius, h=height))
            model.append(cyl)
    return union()(*model)

model = generate_array(5, 5, 15, 3, 10)

# 渲染为字符串
scad_code = scad_render(model)

# 写入 .scad 文件
with open("cylinder_array.scad", "w", encoding="utf-8") as f:
    f.write("$fn=80;\n" + scad_code)

# 用 OpenSCAD 生成 STL（使用绝对路径）
openscad_path = r"D:\Openscad\OpenSCAD-2021.01-x86-64\openscad-2021.01\openscad.exe"
os.system(f'"{openscad_path}" -o cylinder_array.stl cylinder_array.scad')
