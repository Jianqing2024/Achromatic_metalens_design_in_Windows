from .structSet import *
from .dataCaculate import *
import importlib.util
import numpy as np
import os

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
    
def cross(fdtd, material, h, l, w, *, name="newGroup"):
    fdtd.addstructuregroup()
    fdtd.set("name", name)
    
    addMetaRect(fdtd, material, l, w, h, name="recX")
    fdtd.select("recX")
    fdtd.addtogroup(name)
    addMetaRect(fdtd, material, w, l, h, name="recY")
    fdtd.select("recY")
    fdtd.addtogroup(name)
    
def swichWaveLength(fdtd, wav, name):
    fdtd.select(name)
    fdtd.set("wavelength start", wav)
    fdtd.set("wavelength stop", wav)
    
class MetaEngine:
    def __init__(self, hide=True, name='test', parallel=False, template=False, SpectralRange=[0.532e-6, 0.800e-6]):
        lumapi_path = "D:\\Program Files\\Lumerical\\v241\\api\\python\\lumapi.py"

        spec = importlib.util.spec_from_file_location("lumapi", lumapi_path)
        if spec is None or spec.loader is None:
            raise ImportError("无法加载 lumapi 模块或 loader 为空")
        
        lumapi = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(lumapi)
        
        if template:
            base_dir = os.getcwd()
            template_path = os.path.join(base_dir, "data", "STANDARD.fsp")
            computation_path = os.path.join(base_dir, f"{name}.fsp")           
            if not os.path.isfile(template_path):
                raise FileNotFoundError(f"模板文件未找到: {template_path}")
            
            fdtd = lumapi.FDTD(template_path ,hide=True)
            fdtd.save(computation_path)
            fdtd.close()
        
            self.fdtd = lumapi.FDTD(computation_path, hide=hide)
            self.name = name
        else:
            self.fdtd = lumapi.FDTD(hide=hide)
            if not parallel:
                filename = f"{name}.fsp"
                self.fdtd.save(filename)
            
        self.template = template
        self.waveMin = SpectralRange[0]
        self.waveMax = SpectralRange[1]
        print(f"Spectral range : {self.waveMin} - {self.waveMax}")
        self.highEst=0.8e-6
        
    def materialSet(self):
        if self.template:
            # self.baseMaterial = "GaN"
            self.baseMaterial = "TiO2_2023"
            self.strMaterial = "SiO2 (Glass) - Palik"
            identification = self.fdtd.materialexists(self.baseMaterial)
            if not identification:
                raise RuntimeError("Material not properly assigned")
            else:
                print("Please note that you are using materials from the TEMPLLATE file.")
        else:
            self.baseMaterial = "TiO2_2023"
            self.strMaterial = "SiO2 (Glass) - Palik"
            print("Please note that you are using materials from the ORIGINAL material library.")

        print(f"BaseMaterial : {self.baseMaterial}\nStrMaterial : {self.strMaterial}")
        
    def baseBuild(self, p):
        setMetaFdtd(self.fdtd, p, p, self.highEst, -0.5e-6)
        classicMonitorGroup(self.fdtd, p, p, self.highEst)
        addMetaBase(self.fdtd, self.baseMaterial, p, p, 1e-6)
        addMetaSource(self.fdtd, p, p, -0.25e-6, [self.waveMin, self.waveMax])
        
    def structureBuild(self, strClass, parameter, h):
        if h > self.highEst:
            raise ValueError("Structure height exceeds the maximum height of the built-in FDTD region")
        if strClass == 1:
            r = parameter[0]
            addMetaCircle(self.fdtd, self.strMaterial, r, h, name='STR')
        elif strClass == 2:
            l = parameter[0]
            addMetaRect(self.fdtd, self.strMaterial, l, l, h, name='STR')
        elif strClass == 3:
            l, w = parameter[0], parameter[1]
            cross(self.fdtd, self.strMaterial, h, l, w, name='STR')
        elif strClass == 4:
            l, w, r = parameter[0], parameter[1], parameter[2]
            fishnetset(self.fdtd, self.strMaterial, h, l, w, r, name='STR')
            
    def dataAcquisition(self):
        self.Ex = []
        self.Trans = []

        self.fdtd.run()
        Ex, Trans = classicDataAcquisition_multyWav(self.fdtd)

        phase_array = np.angle(np.array(Ex))
        unwrapped = np.unwrap(phase_array)
        unwrapped -= 2 * np.pi * np.floor(unwrapped[0] / (2 * np.pi))

        self.Ex = unwrapped.tolist()
        self.Trans = Trans.tolist()
        
    def semi_Reset(self):
        self.fdtd.switchtolayout()
        self.fdtd.select('STR')
        self.fdtd.delete()
        
    def Reset(self):
        self.fdtd.switchtolayout()
        self.fdtd.deleteall()
        
    def structureBuild_ForDataEvaluation(self, strClass, parameter, h, id):
        if h > self.highEst:
            raise ValueError("Structure height exceeds the maximum height of the built-in FDTD region")
        if strClass == 1:
            r = parameter[0]
            addMetaCircle(self.fdtd, self.strMaterial, r, h, name=str(id))
        elif strClass == 2:
            l = parameter[0]
            addMetaRect(self.fdtd, self.strMaterial, l, l, h, name=str(id))
        elif strClass == 3:
            l, w = parameter[0], parameter[1]
            cross(self.fdtd, self.strMaterial, h, l, w, name=str(id))
        elif strClass == 4:
            l, w, r = parameter[0], parameter[1], parameter[2]
            fishnetset(self.fdtd, self.strMaterial, h, l, w, r, name=str(id))