from .Database_Manager import *
from .Simulation_evaluation import *

def Numerical_evaluation():
    ## 数值评估
    #  建立/重置任务数据库
    TaskDatabase_Creat()
    
    #  简单处理数据，计算色散、评估线性情况
    
    #  评估数值选择最佳主值
    #  录入到任务数据库
    
def Simulation_Evaluation(baseValue):
    ## 根据主值和设置值初始化参数对象
    COM = Command(baseValue)
    #  使用optuna优化
    BestParameter, BestValue = Optimizer(COM)
    print(BestParameter, BestValue)
    ## 建模并计算，输出为图片