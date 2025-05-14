from .taskTargetGeneration import *

def main_for_EPS_Initialization():
    ## 初始化库，制定任务目录，区分类别和主参数
    #  清理库
    dataBaseClean()
    #  定义主参数，填充主值表
    P=np.linspace(0.4e-6,0.5e-6,3)
    H=np.linspace(0.5e-6,0.7e-6,3)
    defineMainvalue(P,H)
    #  定义参数，填充参数表
    L=np.linspace(0.1e-6,0.4e-6,5)
    W=np.linspace(0.1e-6,0.4e-6,5)
    R=np.linspace(0.05e-6,0.15e-6,5)
    for i in range(4):
        structerClass=i+1
        if structerClass==1:
            parameterFilling(structerClass, R)
        elif structerClass==2:
            parameterFilling(structerClass, L)
        elif structerClass==3:
            parameterFilling(structerClass, [L, W])
        elif structerClass==4:
            parameterFilling(structerClass, [L, W, R])
    #  计算任务总数
    databaseCount()
    ## 扫参，填充主数据库
    #  区分类和主参数
    ids=resumeTaskDirectory()
    #  根据任务目录计算
    
    
    
    
def main_for_EPS_Resume():
    ## 扫描库，重新计算任务目录
    ids=resumeTaskDirectory()
    print(ids)
