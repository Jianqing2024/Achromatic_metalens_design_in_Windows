from Exhaustive_parameter_sweep import main

## 是否开启并行
## 是否初始化
parallel=True
initial=False

if initial:
    DIC=main.Initial_structure_directory()
    main.main_for_EPS_Initialization(DIC)

if parallel:
    main.main_for_EPS_Parallel(4)
else:
    main.main_for_EPS_NotParallel()