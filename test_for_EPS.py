from Exhaustive_parameter_sweep import main
from data import dataBaseCreat as data
## 是否开启并行
## 是否初始化
## 是否使用模板文件
parallel=True
initial=True
template=True

#  修改材料和波段后请在计算部分手动检验，此处仅作提示
material = 'TiO2_real'
#  第一个值是最大波长，第二个值是最小波长
SpectralRange = [0.780e-6,0.532e-6]

if initial:
    data.DatabaseCreat(SpectralRange, material)
    DIC=main.Initial_structure_directory()
    main.main_for_EPS_Initialization(DIC)

if parallel:
    main.main_for_EPS_Parallel(8)
else:
    main.main_for_EPS_NotParallel(template, SpectralRange)