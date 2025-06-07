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
    str = f"""
    addfdtd;
    set("x", 0);
    set("y", 0);

    set("x span", {size_x});
    set("y span", {size_y});
    set("z max", {zmax});
    set("z min", {zmin});

    set("x min bc", "periodic");
    set("x max bc", "periodic");
    set("y min bc", "periodic");
    set("y max bc", "periodic");
    set("z min bc", "PML");
    set("z max bc", "PML");
    """
    fdtd.eval(str)

def addMetaBase(fdtd, material, size_x, size_y, size_z, *,name="base"):
    """生成一个标准的基底结构, 其为一个立方体结构，
        特点在于 x max=0。尺寸和材料可调且无需乘以2。
        输入材料时请确定材料库中已经包含此种材料名。

    Args:
        fdtd (fdtd): 必须在选中的fdtd 窗口中进行设置
        material (str): 材料名为字符串, 必须与 FDTD 材料库完全一致
        size_x (float): x 方向尺寸
        size_y (float): y 方向尺寸
        size_z (float): z 方向尺寸
        name (str): 结构名称，默认为 "base"
    """
    str = f"""
    addrect;
    set("name","{name}");
    set("x", 0);
    set("y", 0);
    set("x span", {size_x*2});
    set("y span", {size_y*2});
  
    set("z max", 0);
    set("z min", {0-size_z});
    
    set("material", "{material}");
    """
    fdtd.eval(str)
    
def addMetaSource(fdtd, size_x, size_y, z, wavelength, *, name="source"):
    """建立平面波光源,以z轴为对称轴

    Args:
        fdtd (fdtd): 必须在选中的fdtd窗口中进行设置
        size_x (double): 字面
        size_y (double): 字面
        z (double): 字面
        wavelength (double): 字面
    """
    
    if len(wavelength)==1:
        str = f"""        
        addplane;
        set("x", 0);
        set("y", 0);
        set("z", {z});
    
        set("x span", {size_x});
        set("y span", {size_y});
        set("wavelength start", {wavelength});
        set("wavelength stop", {wavelength});
        set("name","{name}");
        """
        
    else:
        str = f"""        
        addplane;
        set("x", 0);
        set("y", 0);
        set("z", {z});
    
        set("x span", {size_x});
        set("y span", {size_y});
        set("wavelength start", {wavelength[0]});
        set("wavelength stop", {wavelength[1]});
        set("name","{name}");
        """
    
    fdtd.eval(str)
    
def classicMonitorGroup(fdtd, size_x, size_y, z):
    """建立一个经典监视器组，包括两个频域能量监视器，
        一个是平行于xy面的面监视器,称为plane;一个是与plane高度相同的点监视器,称为point
        考虑到多波长情况,为了适应532-800的消色差,加入全局监视器设置,将频率上的监视步长确定为5

    Args:
        fdtd (fdtd): fdtd窗口
        size_x (double): 字面
        size_y (double): 字面
        z (double)): 字面
    """
    str = f"""
        addpower;
        set("name", "point");
        set("monitor type", "point");
        set("x", 0);
        set("y", 0);
        set("z", {z});
        
        addpower;
        set("name", "plane");
        set("x", 0);
        set("y", 0);
        set("z", {z});
        set("x span", {size_x});
        set("y span", {size_y});
        
        setglobalmonitor("frequency points",5);
        """
    fdtd.eval(str)

def addMetaCircle(fdtd, material, radius, high, *,name="cylinder"):
    """建立一个圆柱结构,结构的底面在z=0处,位置在正中

    Args:
        fdtd (fdtd): 必须在选中的fdtd窗口中进行设置
        material (str): 材料名为字符串,必须与FDTD材料库完全一致
        radius (double): 字面
        high (double): 字面
        name (str): 默认为cylinder
    """
    str = f"""
        addcircle;
    
        set("name", "{name}");
        set("x", 0);
        set("y", 0);
        
        set("radius", {radius});
    
        set("z max", {high});
        set("z min", 0);
        
        set("material", "{material}");
    """
    fdtd.eval(str)

def addMetaRect(fdtd, material, size_x, size_y, size_z, *, name="rect"):
    """建立一个标准矩形柱,位置在正中

    Args:
        fdtd (fdtd): fdtd窗口
        material (str): 材料名
        size_x (double): 字面
        size_y (double): 字面
        size_z (double): 字面
        name (str): 默认为rect
    """
    str = f"""    
    addrect;
    set("name","{name}");

    set("x", 0);
    set("y", 0);
    set("x span", {size_x});
    set("y span", {size_y});
  
    set("z min", 0);
    set("z max", {size_z});
    
    set("material", "{material}");
    """
    fdtd.eval(str)