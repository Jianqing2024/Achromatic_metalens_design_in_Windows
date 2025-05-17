from Exhaustive_parameter_sweep import main
import numpy as np

if __name__ == "__main__":
    ## 是否需要初始化
    swich=2
    
    if swich==1:
        #  初始参数设置
        DIC={'P':np.linspace(0.4e-6,0.5e-6,4),
             'H':np.linspace(0.5e-6,0.7e-6,4),
             'ParameterAForClass1':np.linspace(0.04e-6,0.18e-6,10),
             'ParameterAForClass2':np.linspace(0.1e-6,0.4e-6,10),
             'ParameterAForClass3':np.linspace(0.1e-6,0.4e-6,8),
             'ParameterBForClass3':np.linspace(0.1e-6,0.4e-6,8),
             'ParameterAForClass4':np.linspace(0.1e-6,0.4e-6,8),
             'ParameterBForClass4':np.linspace(0.1e-6,0.4e-6,8),
             'ParameterCForClass4':np.linspace(0.04e-6,0.18e-6,8)}
        main.main_for_EPS_Initialization(DIC)
    else:
        main.main_for_EPS_Resume()