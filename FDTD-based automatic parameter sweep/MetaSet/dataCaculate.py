import numpy as np

def classicDataAcquisition(fdtd):
    Ex=fdtd.getdata("point", "Ex")
    Ex_angle=np.angle(Ex)
    T=fdtd.transmission("plane")
    T=np.float64(T)
    Ex_angle=Ex_angle[0,0,0,0]
    data=[Ex_angle, T]
    return data