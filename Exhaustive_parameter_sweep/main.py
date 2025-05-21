from .dataManager import *
from .compute import *

def main_for_EPS_Initialization(DIC):
    ## 初始化库，制定任务目录，区分类别和主参数
    #  清理库
    dataBaseClean()
    #  解码主参数，填充主值表
    P=DIC['P']
    H=DIC['H']
    defineMainvalue(P,H)
    
    #  解码参数，填充参数表
    for i in range(4):
        structerClass=i+1
        if structerClass==1:
            parameterFilling(structerClass, DIC['ParameterAForClass1'])
        elif structerClass==2:
            parameterFilling(structerClass, DIC['ParameterAForClass2'])
        elif structerClass==3:
            parameterFilling(structerClass, [DIC['ParameterAForClass3'], DIC['ParameterBForClass3']])
        elif structerClass==4:
            parameterFilling(structerClass, [DIC['ParameterAForClass4'], DIC['ParameterBForClass4'], DIC['ParameterCForClass4']])
    #  计算任务总数
    databaseCount()
 
def Initial_structure_directory():
    DIC={   'P':np.linspace(0.4e-6,0.5e-6,6),
            'H':np.linspace(0.5e-6,0.8e-6,6),
            'ParameterAForClass1':np.linspace(0.04e-6,0.18e-6,40),
            'ParameterAForClass2':np.linspace(0.1e-6,0.4e-6,40),
            'ParameterAForClass3':np.linspace(0.1e-6,0.4e-6,20),
            'ParameterBForClass3':np.linspace(0.1e-6,0.4e-6,20),
            'ParameterAForClass4':np.linspace(0.1e-6,0.4e-6,10),
            'ParameterBForClass4':np.linspace(0.1e-6,0.4e-6,10),
            'ParameterCForClass4':np.linspace(0.04e-6,0.18e-6,10)}
    return DIC
   
def main_for_EPS_NotParallel():
    ## 扫描库，重新计算任务目录
    ids=resumeTaskDirectory()
    #  计算重续任务量
    resumeCount()
    ## 根据任务目录计算
    Comput(ids)

def main_for_EPS_Parallel(Parallelnum):
    ## 扫描库，重新计算任务目录
    ids=resumeTaskDirectory()
    #  计算重续任务量
    resumeCount()
    ## 根据任务目录计算
    ParallelComput(Parallelnum)