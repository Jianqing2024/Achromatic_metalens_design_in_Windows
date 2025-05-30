from .dataManager import *
from .compute import *

def Initial_structure_directory():
    use_class_1=True
    use_class_2=True
    use_class_3=True
    use_class_4=True
    single_P=True
    single_H=True
    
    DIC = {}

    # 主参数设置
    DIC['P'] = np.array([0.4e-6]) if single_P else np.linspace(0.3e-6, 0.5e-6, 4)
    DIC['H'] = np.array([0.7e-6])  if single_H else np.linspace(0.5e-6, 0.8e-6, 4)

    # 类别1
    if use_class_1:
        DIC['ParameterAForClass1'] = np.linspace(0.04e-6, 0.18e-6, 40)

    # 类别2
    if use_class_2:
        DIC['ParameterAForClass2'] = np.linspace(0.1e-6, 0.4e-6, 40)

    # 类别3
    if use_class_3:
        DIC['ParameterAForClass3'] = np.linspace(0.1e-6, 0.4e-6, 40)
        DIC['ParameterBForClass3'] = np.linspace(0.1e-6, 0.4e-6, 40)

    # 类别4
    if use_class_4:
        DIC['ParameterAForClass4'] = np.linspace(0.05e-6, 0.35e-6, 20)
        DIC['ParameterBForClass4'] = np.linspace(0.05e-6, 0.35e-6, 20)
        DIC['ParameterCForClass4'] = np.linspace(0.04e-6, 0.18e-6, 40)

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

def main_for_EPS_Parallel(Parallelnum, SpectralRange):
    ## 扫描库，重新计算任务目录
    ids=resumeTaskDirectory()
    #  计算重续任务量
    resumeCount()
    ## 根据任务目录计算
    ParallelComput(Parallelnum, SpectralRange)