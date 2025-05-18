from Exhaustive_parameter_sweep import main
import numpy as np

if __name__ == "__main__":
    ## 是否需要初始化
    swich=2
    
    if swich==1:
        #  初始参数设置
        DIC=main.Initial_structure_directory()
        main.main_for_EPS_Initialization(DIC)
    else:
        main.main_for_EPS_Resume()