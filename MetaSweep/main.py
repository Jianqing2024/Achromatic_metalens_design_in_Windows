from .dataManager import *
from .compute import *

def Initial_structure_directory(P, H,
                                class1_A=None, 
                                class2_A=None,
                                class3_A=None, class3_B=None,
                                class4_A=None, class4_B=None, class4_C=None):
    DIC = {'P': P, 'H': H}

    if class1_A is not None:
        DIC['ParameterAForClass1'] = class1_A
    if class2_A is not None:
        DIC['ParameterAForClass2'] = class2_A
    if class3_A is not None and class3_B is not None:
        DIC['ParameterAForClass3'] = class3_A
        DIC['ParameterBForClass3'] = class3_B
    if class4_A is not None and class4_B is not None and class4_C is not None:
        DIC['ParameterAForClass4'] = class4_A
        DIC['ParameterBForClass4'] = class4_B
        DIC['ParameterCForClass4'] = class4_C

    return DIC

def main_for_EPS_Initialization(DIC):
    ## 初始化库，制定任务目录，区分类别和主参数
    #  清理库
    dataBaseClean()
    #  解码主参数，填充主值表
    P=DIC['P']
    H=DIC['H']
    defineMainvalue(P,H)
    
    #  解码参数，填充参数表
    for structerClass in range(1,5):
        if structerClass==1 and 'ParameterAForClass1' in DIC:
            parameterFilling(structerClass, DIC['ParameterAForClass1'])
        elif structerClass==2 and 'ParameterAForClass2' in DIC:
            parameterFilling(structerClass, DIC['ParameterAForClass2'])
        elif structerClass==3 and 'ParameterAForClass3' in DIC:
            parameterFilling(structerClass, [DIC['ParameterAForClass3'], DIC['ParameterBForClass3']])
        elif structerClass==4 and 'ParameterAForClass4' in DIC:
            parameterFilling(structerClass, [DIC['ParameterAForClass4'], DIC['ParameterBForClass4'], DIC['ParameterCForClass4']])
    #  计算任务总数
    databaseCount()
   
def main_for_EPS_NotParallel(template, SpectralRange):
    ## 扫描库，重新计算任务目录
    ids=resumeTaskDirectory()
    #  计算重续任务量
    resumeCount()
    ## 根据任务目录计算
    Comput(ids, template, SpectralRange)

def main_for_EPS_Parallel(Parallelnum):
    ## 扫描库，重新计算任务目录
    ids=resumeTaskDirectory()
    #  计算重续任务量
    resumeCount()
    ## 根据任务目录计算
    ParallelComput(Parallelnum)