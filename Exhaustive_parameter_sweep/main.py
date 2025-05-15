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
    ## 扫参，填充主数据库
    #  区分类和主参数
    ids=resumeTaskDirectory()
    #  根据任务目录计算
    Comput(ids)
    
def main_for_EPS_Resume():
    ## 扫描库，重新计算任务目录
    ids=resumeTaskDirectory()
    #  计算重续任务量
    resumeCount()
    ## 根据任务目录计算
    Comput(ids)
