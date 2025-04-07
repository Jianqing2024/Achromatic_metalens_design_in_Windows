from .structSet import addMetaCircle
from .structSet import addMetaRect

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
    fdtd.set("wavelength", wav)