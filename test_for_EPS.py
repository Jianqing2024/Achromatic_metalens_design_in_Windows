from Exhaustive_parameter_sweep import main

## 初始化，需调整
DIC=main.Initial_structure_directory()
main.main_for_EPS_Initialization(DIC)

## 是否开启并行
parallel=True

if parallel:
    main.main_for_EPS_Parallel(4)
else:
    main.main_for_EPS_NotParallel()