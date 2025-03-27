def setMetaFdtd(fdtd, size_x, size_y, zmax, zmin):
    """生成一个四周为周期性边界条件、上下两端为PML边界条件的FDTD区域.
        由于在x-y面上时常不对称,因此用zmax和zmin定义z方向的数值

    Args:
        fdtd (fdyd): 必须在选中的fdtd窗口中进行设置
        size_x (double): 字面
        size_y (double): 字面
        zmax (double): 字面
        zmin (double): 字面
    """
    fdtd.addfdtd()

    fdtd.set("x span", size_x)
    fdtd.set("y span", size_y)
    fdtd.set("z max", zmax)
    fdtd.set("z min", zmin)

    # 设置边界条件
    fdtd.set("x min bc", "periodic")
    fdtd.set("x max bc", "periodic")
    fdtd.set("y min bc", "periodic")
    fdtd.set("y max bc", "periodic")
    fdtd.set("z min bc", "PML")
    fdtd.set("z max bc", "PML")

def addMetaBase(fdtd, material, size_x, size_y, size_z):
    """生成一个标准的基底结构,其为一个立方体结构，
        特点在于x max=0.尺寸和材料可调且无需乘以2
        输入材料时请确定材料库中已经包含此种材料名

    Args:
        fdtd (fdtd): 必须在选中的fdtd窗口中进行设置
        material (str): 材料名为字符串,必须与FDTD材料库完全一致
        size_x (double): 字面
        size_y (double): 字面
        size_z (double): 字面
    """
    fdtd.addrect()

    fdtd.set("x", 0)
    fdtd.set("y", 0)
    fdtd.set("x span", size_x*2)
    fdtd.set("y span", size_y*2)
  
    fdtd.set("z max", 0)
    fdtd.set("z min", 0-size_z)
    
    fdtd.set("material", material)
    
def addMetaCircle(fdtd, material, radius, high):
    """建立一个圆柱结构,结构的底面在z=0处,位置在正中

    Args:
        fdtd (fdtd): 必须在选中的fdtd窗口中进行设置
        material (str): 材料名为字符串,必须与FDTD材料库完全一致
        radius (double): 字面
        high (double): 字面
    """
    fdtd.addcircle()
    
    fdtd.set("x", 0)
    fdtd.set("y", 0)
    
    fdtd.set("radius", radius)
  
    fdtd.set("z max", high)
    fdtd.set("z min", 0)
    
    fdtd.set("material", material)
    
def addMetaSource(fdtd, size_x, size_y, z, wavelength):
    """建立平面波光源,以z轴为对称轴

    Args:
        fdtd (fdtd): 必须在选中的fdtd窗口中进行设置
        size_x (_type_): 字面
        size_y (_type_): 字面
        z (_type_): 字面
        wavelength (_type_): 字面
    """
    fdtd.addplane()
    fdtd.set("x", 0)
    fdtd.set("y", 0)
    fdtd.set("z", z)
    
    fdtd.set("x span", size_x)
    fdtd.set("y span", size_y)
    
    fdtd.set("wavelength start", wavelength)
    fdtd.set("wavelength stop", wavelength)
    
def classicMonitorGroup(fdtd, size_x, size_y, z):
    fdtd.addpower(name="point")
    fdtd.set("monitor type", "point")
    fdtd.set("x", 0)
    fdtd.set("y", 0)
    fdtd.set("z", z)
    
    fdtd.addpower(name="plane")
    fdtd.set("x", 0)
    fdtd.set("y", 0)
    fdtd.set("z", z)
    fdtd.set("x span", size_x)
    fdtd.set("y span", size_y)
    