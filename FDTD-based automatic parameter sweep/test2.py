import numpy as np
import time
import importlib.util
import os

module_name = "lumapi"
file_path = "D:\\Program Files\\Lumerical\\v241\\api\\python\\lumapi.py"

spec = importlib.util.spec_from_file_location(module_name, file_path)
lumapi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lumapi) 

def xf_port(name,x,y,z,y_span,z_span,f):
    fdtd.addport()
    fdtd.set("name", name)
    fdtd.set("injection axis", 'x-axis')
    fdtd.set('x', x)
    fdtd.set('y', y)
    fdtd.set('y span', y_span)
    fdtd.set('z', z)
    fdtd.set('z span', z_span)
    fdtd.set('direction',f)

#长度单位默认米m，因此加上e-6变成微米，时间单位默认秒s，因此需要e-15
fdtd = lumapi.FDTD()
fdtd.save(str(221) + '.fsp')
fdtd.addfdtd(x=0,y=0,z=0,x_span=9e-6,y_span=10e-6,z_span=1e-6)
fdtd.select("FDTD")
fdtd.set('simulation time',8e-12)
fdtd.set('dt stability factor',0.99)
#"SiO2 (Glass) - Palik"
#"Si (Silicon) - Palik"

#基底材料
basis=fdtd.addrect(x=0,y=0,z=-2e-6,x_span=22e-6,y_span=16e-6,z_span=4e-6,material="SiO2 (Glass) - Palik")#material='SiO2(Glass)-Paliik'

#bus\drop波导
rec1=fdtd.addrect(x=0,y=3.6e-6,z=0,z_span=0.18e-6,y_span=0.4e-6,x_span=25e-6,material="Si (Silicon) - Palik")
rec3=fdtd.addrect(x=0,y=3.1e-6,z=0,z_span=0.18e-6,y_span=0.4e-6,x_span=1e-13,material="Si (Silicon) - Palik")
rec2=fdtd.addrect(x=0,y=-3.6e-6,z=0,z_span=0.18e-6,y_span=0.4e-6,x_span=25e-6,material="Si (Silicon) - Palik")
rec4=fdtd.addrect(x=0,y=-3.1e-6,z=0,z_span=0.18e-6,y_span=0.4e-6,x_span=1e-13,material="Si (Silicon) - Palik")

#硅环
ring1=fdtd.addring(x=0,y=0,z=0,z_span=0.18e-6,inner_radius=2.9e-6,outer_radius=3.3e-6,theta_start=0,theta_stop=360,material="Si (Silicon) - Palik")
ring2=fdtd.addring(x=0,y=0,z=0,z_span=0.18e-6,inner_radius=2.9e-6,outer_radius=3.3e-6,theta_start=90,theta_stop=270,material="Si (Silicon) - Palik")

#调整微环谐振器四个端口，并设置输入端口
xf_port("input_port",-4.2e-6,3.6e-6,0,3e-6,0.18e-6,'forward')
xf_port("2",-4.2e-6,-3.6e-6,0,3e-6,0.18e-6,'forward')
xf_port("3",4.2e-6,3.6e-6,0,3e-6,0.18e-6,'backward')
xf_port("4",4.2e-6,-3.6e-6,0,3e-6,0.18e-6,'backward')
fdtd.select("FDTD::ports"); # select the port group
fdtd.set("source port","input_port")


fdtd.setglobalsource('wavelength start',1500e-9)
fdtd.setglobalsource('wavelength stop',1600e-9)

fdtd.addprofile(name='1',x=0,y=0,z=0,x_span=11e-6,y_span=12e-6)



fdtd.run()