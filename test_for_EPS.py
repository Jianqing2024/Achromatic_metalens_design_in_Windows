from Exhaustive_parameter_sweep import main
from data import dataBaseCreat as data
## 是否开启并行
## 是否初始化
parallel=True
initial=False
template=True
SpectralRange=[0.5e-6,0.6e-6]

if initial:
    data.DatabaseCreat(SpectralRange)
    DIC=main.Initial_structure_directory()
    main.main_for_EPS_Initialization(DIC)

if parallel:
    main.main_for_EPS_Parallel(4, SpectralRange)
else:
    main.main_for_EPS_NotParallel(template, SpectralRange)