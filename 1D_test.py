import numpy as np
from MetaSet import advancedStructure as ad

# 参数定义
r = 80e-6
single = 0.4e-6
lambda0 = 0.8e-6
f = 60e-6

N = int(2 * r / single)
x = np.linspace(-r, r, N)

ftx = -(2 * np.pi) / lambda0 * (np.sqrt(x**2 + f**2) - f)
ftx = np.mod(ftx, 2 * np.pi)  # wrapTo2Pi

angle = np.loadtxt("d:/WORK/Achromatic_metalens_design_in_Windows/test/angle.txt")
angle = np.mod(angle, 2 * np.pi)  # wrapTo2Pi

diff = np.abs(ftx[:, None] - angle[None, :])
p = np.argmin(diff, axis=1)

radius = np.linspace(0.04e-6, 0.18e-6, len(angle))
R = radius[p]
print(R)

meta = ad.MetaEngine(template=True, parallel=False, SpectralRange=[0.800e-6,0.800e-6])

meta.fdtd.addfdtd()
meta.fdtd.set("x",0)
meta.fdtd.set("y",0)
meta.fdtd.set("x span", 2*r+1e-6)
meta.fdtd.set("y span", single)
meta.fdtd.set("z max", 70e-6)
meta.fdtd.set("z min", -0.5e-6)

meta.fdtd.addrect()
meta.fdtd.set("name","base")
meta.fdtd.set("x", 0)
meta.fdtd.set("y", 0)
meta.fdtd.set("material", "SiO2 (Glass) - Palik")
meta.fdtd.set("x span", 2*r+1e-6)
meta.fdtd.set("y span", single)
meta.fdtd.set("z min", -0.5e-6)
meta.fdtd.set("z max", 0)

meta.fdtd.addplane()
meta.fdtd.set("x span", 2*r+1e-6)
meta.fdtd.set("y span", single)
meta.fdtd.set("wavelength start", lambda0)
meta.fdtd.set("wavelength stop", lambda0)

def rec(x, r, meta, i):
    meta.fdtd.addcircle()
    meta.fdtd.set("x", x)
    meta.fdtd.set("y", 0)
    meta.fdtd.set("radius", r)
    meta.fdtd.set("z max", 0.7e-6)
    meta.fdtd.set("z min", 0)
    meta.fdtd.set("material", "TiO2_2023")
    meta.fdtd.set("name", f"c{i}")

for i in range(len(R)):
    rec(x[i], R[i], meta, i)
    if (i + 1) % 100 == 0:
        print(f"已完成 {i + 1} / {len(R)} 项")
    
meta.fdtd.save("test111.fsp")