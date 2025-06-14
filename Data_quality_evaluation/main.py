from .Database_Manager import *
from .Simulation_evaluation import *
from .Numerical_evaluation import *

def Preliminary_numerical_evaluation(N):
    
    PhaseCoverage = Numerical_Evaluation(N)
    bestIdx = np.argmax(PhaseCoverage)
    print(bestIdx)
    return bestIdx
        
def Simulation_Evaluation(baseValue):
    ## 根据主值和设置值初始化参数对象
    COM = Command(baseValue)
    #  使用optuna优化，并导出id
    BestParameter, BestValue = Optimizer(COM)
    print(f"BestValue : {BestValue}")
    matched_ids = OneD_Index(BestParameter, COM)
    print(matched_ids)
    ## 建模并计算
    OneD_ModelAndRun(matched_ids, COM)