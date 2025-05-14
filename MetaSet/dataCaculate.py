import numpy as np

def classicDataAcquisition(fdtd):
    """用于单波长的标准计算函数,Ex_angle为相位,T为透射率

    Args:
        fdtd (fdtd): fdtd窗口

    Returns:
        list: list第一个数值为相位差,第二个数值为透射率.符合numpy的double格式
    """
    Ex=fdtd.getdata("point", "Ex")
    Ex_angle=np.angle(Ex)
    T=fdtd.transmission("plane")
    T=np.float64(T)
    Ex_angle=Ex_angle[0,0,0,0]
    data=np.array([[Ex_angle, T]])
    return data

def classicDataAcquisition_multyWav(fdtd):
    T=fdtd.transmission("plane")
    T = T.ravel()
    Ex=fdtd.getresult("point", "Ex")
    Ex = Ex.ravel()
    return Ex, T 