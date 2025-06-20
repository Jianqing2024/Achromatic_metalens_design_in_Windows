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
    BestParameter, BestValue = Optimizer1D(COM)
    print(f"BestValue : {BestValue}")
    matched_ids = OneD_Index(BestParameter, COM)
    print(matched_ids)
    ## 建模并计算
    OneD_ModelAndRun(matched_ids, COM)

def Simulation_Evaluation_over(baseValue):
    ## 根据主值和设置值初始化参数对象
    COM = Command(baseValue)
    #  使用optuna优化，并导出id
    COM.Over = True
    BestParameter, BestValue = Optimizer1D(COM)
    print(f"BestValue : {BestValue}")
    matched_ids = OneD_Index(BestParameter, COM)
    ID_array, X, Y = Map_1D_Results_To_2D(COM, matched_ids)
    print(ID_array)
    save_MAT(ID_array, X, Y)
    
    
    
def GET():
    get_data()