from .structSet import *
from .dataCaculate import *
import importlib.util
import numpy as np
import os

def fishnetset(fdtd, material, h, l, w, r, *, name="newGroup"):
    str = f"""
    addstructuregroup;
    set("name", "{name}");

    addrect;
    set("name", "recX");
    set("x", 0);
    set("y", 0);
    set("x span", {l});
    set("y span", {w});
    set("z min", 0);
    set("z max", {h});
    set("material", "{material}");
    select("recX");
    addtogroup("{name}");

    addrect;
    set("name", "recY");
    set("x", 0);
    set("y", 0);
    set("x span", {w});
    set("y span", {l});
    set("z min", 0);
    set("z max", {h});
    set("material", "{material}");
    select("recY");
    addtogroup("{name}");

    addcircle;
    set("name", "cie");
    set("x", 0);
    set("y", 0);
    set("radius", {r});
    set("z min", 0);
    set("z max", {h});
    set("material", "{material}");
    select("cie");
    addtogroup("{name}");
    """
    fdtd.eval(str)
    
def cross(fdtd, material, h, l, w, *, name="newGroup"):
    str = f"""
    addstructuregroup;
    set("name", "{name}");

    addrect;
    set("name", "recX");
    set("x", 0);
    set("y", 0);
    set("x span", {l});
    set("y span", {w});
    set("z min", 0);
    set("z max", {h});
    set("material", "{material}");
    select("recX");
    addtogroup("{name}");

    addrect;
    set("name", "recY");
    set("x", 0);
    set("y", 0);
    set("x span", {w});
    set("y span", {l});
    set("z min", 0);
    set("z max", {h});
    set("material", "{material}");
    select("recY");
    addtogroup("{name}");
    """
    fdtd.eval(str)
    
class MetaEngine:
    def __init__(self, hide=True, name='test', parallel=False, template=False, SpectralRange=[0.800e-6, 0.532e-6]):
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
        self.waveMax = SpectralRange[0]
        self.waveMin = SpectralRange[1]
        print(f"Spectral range : waveMax = {self.waveMax} | waveMin = {self.waveMin}")
        self.highEst=1e-6
        
    def materialSet(self):
        if self.template:
            # self.baseMaterial = "GaN"
            self.baseMaterial = "SiO2 (Glass) - Palik"
            self.strMaterial = "TiO2_2023"
            identification = self.fdtd.materialexists(self.baseMaterial)
            if not identification:
                raise RuntimeError("Material not properly assigned")
            else:
                print("Please note that you are using materials from the TEMPLLATE file.")
        else:
            self.baseMaterial = "SiO2 (Glass) - Palik"
            self.strMaterial = "TiO2_2023"
            print("Please note that you are using materials from the ORIGINAL material library.")

        print(f"BaseMaterial : {self.baseMaterial}\nStrMaterial : {self.strMaterial}")
        
    def baseBuild(self, p):
        # 一次性构建所有组件的脚本
        script = f"""
        # FDTD区域设置
        addfdtd;
        set("x", 0);
        set("y", 0);
        set("x span", {p});
        set("y span", {p});
        set("z max", {self.highEst});
        set("z min", {-0.5e-6});
        set("x min bc", "periodic");
        set("x max bc", "periodic");
        set("y min bc", "periodic");
        set("y max bc", "periodic");
        set("z min bc", "PML");
        set("z max bc", "PML");

        # 添加监视器
        addpower;
        set("name", "point");
        set("monitor type", "point");
        set("x", 0);
        set("y", 0);
        set("z", {self.highEst});
        
        addpower;
        set("name", "plane");
        set("x", 0);
        set("y", 0);
        set("z", {self.highEst});
        set("x span", {p});
        set("y span", {p});
        
        setglobalmonitor("frequency points", 5);

        # 添加基底
        addrect;
        set("name", "base");
        set("x", 0);
        set("y", 0);
        set("x span", {p * 2});
        set("y span", {p * 2});
        set("z max", 0);
        set("z min", {-1e-6});
        set("material", "{self.baseMaterial}");

        # 添加光源
        addplane;
        set("x", 0);
        set("y", 0);
        set("z", {-0.25e-6});
        set("x span", {p});
        set("y span", {p});
        set("wavelength start", {self.waveMin});
        set("wavelength stop", {self.waveMax});
        set("name", "source");
        """

        self.fdtd.eval(script)

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