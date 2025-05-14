from .structSet import *
from .dataCaculate import *
from collections import defaultdict
import importlib.util
import numpy as np

def fishnetset(fdtd, material, h, l, w, r, *, name="newGroup"):
    fdtd.addstructuregroup()
    fdtd.set("name", name)
    
    addMetaRect(fdtd, material, l, w, h, name="recX")
    fdtd.select("recX")
    fdtd.addtogroup(name)
    addMetaRect(fdtd, material, w, l, h, name="recY")
    fdtd.select("recY")
    fdtd.addtogroup(name)
    addMetaCircle(fdtd, material, r, h, name="cie")
    fdtd.select("cie")
    fdtd.addtogroup(name)
    
def swichWaveLength(fdtd, wav, name):
    fdtd.select(name)
    fdtd.set("wavelength start", wav)
    fdtd.set("wavelength stop", wav)
    
class MetaEngine:
    def __init__(self, hide=True, name='aaa'):
        lumapi_path = "D:\\Program Files\\Lumerical\\v241\\api\\python\\lumapi.py"

        spec = importlib.util.spec_from_file_location("lumapi", lumapi_path)
        lumapi = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(lumapi)
        
        self.fdtd = lumapi.FDTD(hide=hide)
        filename = f"{name}.fsp"
        self.fdtd.save(filename)


