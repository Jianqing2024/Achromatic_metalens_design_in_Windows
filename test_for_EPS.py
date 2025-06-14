from Exhaustive_parameter_sweep import main
from data import dataBaseCreat as data
## 是否开启并行
## 是否初始化
parallel=True
initial=True
template=True

#  修改材料和波段后请在计算部分手动检验，此处仅作提示
material = 'TiO2_2023'
#  此处确定定义，第一个值是最大波长，第二个值是最小波长
SpectralRange = [0.8e-6,0.5e-6]

if initial:
    data.DatabaseCreat(SpectralRange, material)
    DIC=main.Initial_structure_directory()
    main.main_for_EPS_Initialization(DIC)

if parallel:
    main.main_for_EPS_Parallel(4)
else:
    main.main_for_EPS_NotParallel(template, SpectralRange)