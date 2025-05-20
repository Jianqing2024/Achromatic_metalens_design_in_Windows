from .databaseProcessing import creatDatabase

def main_for_FOD():
    # 链接到主数据库, 根据类别和主值检索已有结构, 生成任务目录和任务数据库
    
    
    # 新建任务数据库, 提取主数据库中有用的部分进入任务数据库
    creatDatabase()
    
    # 根据任务目录进行计算，使用PSO算法进行计算

    
    # 从任务数据库回填主数据库
    

    # 从主数据库重新进行最优化计算和远场投射
