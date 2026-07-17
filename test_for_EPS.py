from MetaSweep import main
from MetaBase import dataBaseCreat as data
import numpy as np
## 是否开启并行
## 是否初始化
## 是否使用模板文件
parallel=True
initial=True
template=True

#  修改材料和波段后请在计算部分手动检验，此处仅作提示
material = 'TiO2_real'
#  第一个值是最大波长，第二个值是最小波长
SpectralRange = [0.800e-6, 0.532e-6]

if initial:
    data.DatabaseCreat(SpectralRange, material)
    DIC=main.Initial_structure_directory(
        P          = np.linspace(0.4e-6, 5e-6, 3),
        H          = np.linspace(0.4e-6, 0.7e-6, 3),
        class1_A   = np.linspace(0.04e-6, 0.21e-6, 20),
        class2_A   = np.linspace(0.1e-6, 0.4e-6, 20),
        class3_A   = np.linspace(0.1e-6, 0.4e-6, 20),
        class3_B   = np.linspace(0.1e-6, 0.4e-6, 20),
        class4_A   = np.linspace(0.05e-6, 0.35e-6, 10),
        class4_B   = np.linspace(0.05e-6, 0.35e-6, 10),
        class4_C   = np.linspace(0.04e-6, 0.18e-6, 10),
    )

if parallel:
    main.main_for_EPS_Parallel(8)
else:
    main.main_for_EPS_NotParallel(template, SpectralRange)