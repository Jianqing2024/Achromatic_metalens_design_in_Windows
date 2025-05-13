from .taskTargetGeneration import *

def main_for_EPS():
    ## 扫描库，制定任务目录，区分类别和主参数
    #  清理库
    dataBaseClean()
    #  定义主参数，填充主值表
    P=np.linspace(0.2e-6,0.5e-6,5)
    H=np.linspace(0.4e-6,0.8e-6,5)
    defineMainvalue(P,H)
    #  定义参数，填充参数表
    L=np.linspace(0.25e-6,0.4e-6,5)
    W=np.linspace(0.25e-6,0.4e-6,5)
    R=np.linspace(0.25e-6,0.4e-6,5)
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
    
    # 穷举扫参，填充主数据库