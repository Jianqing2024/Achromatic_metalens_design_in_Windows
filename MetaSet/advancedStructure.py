from .structSet import *
from .dataCaculate import *
import importlib.util
import time
import numpy as np

spec = importlib.util.spec_from_file_location("lumapi", "D:\\Program Files\\Lumerical\\v241\\api\\python\\lumapi.py")
lumapi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lumapi)

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
    
class Fishnet(lumapi.FDTD):
    def Computation(self, disc):
        
        self.save(f"s{int(part)}.fsp")
        data = np.empty((0, 9))

        parameterPet=defaultdict(list)
        for row in parameter:
            param1, param2 = row[0], row[1]
            parameterPet[(param1, param2)].append(row)
            
        num = sum(len(v) for v in parameterPet.values())
            
        wav=[0.532e-6,0.800e-6]
        sourceName='s'
        groupName ='g'
        material1="SiO2 (Glass) - Palik"
        material2="TiO2 (Titanium Dioxide) - Devore"
        c=0
            
        for key, value in parameterPet.items():
            p,h=key[0],key[1]
            setMetaFdtd(self, p, p, 1e-6, -1e-6)
            classicMonitorGroup(self, p, p, 1e-6)
            addMetaBase(self, material1, p, p, 1e-6)
            for parameter in value:
                tic=time()
                l=parameter[2] # 十字结构长度
                w=parameter[3] # 十字结构宽度
                r=parameter[4] # 中心圆半径
                    
                fishnetset(self, material2, h, l, w, r, name=groupName)
                    
                main=np.array([[p,h,l,w,r]])
                    
                addMetaSource(self, p, p, -0.5e-6, wav[0],name=sourceName)
                self.run()
                data532 = classicDataAcquisition(self)
                self.switchtolayout()
                
                swichWaveLength(self, wav[1], sourceName)
                self.run()
                data800 = classicDataAcquisition(self)
                self.switchtolayout()
                
                self.select(sourceName)
                self.delete()
                            
                Analysis=np.concatenate((main, data532, data800),axis=1)
                data = np.concatenate((data, Analysis),axis=0)
                self.select(groupName)
                self.delete()

                c+=1
                toc=time()
                print(f"Process {part}: {c}/{num}, time={toc-tic}")
            self.deleteall()
                    
        self.close()