# Inverse_Design_For_Metalens
**Inverse_Design_For_Metalens**
开发中

计划包括三部分：A 基于LumericalFDTD的超透镜单元自动仿真、B 基于Matlab的相位函数优化和远场仿真、C 基于SQLite的数据库建设
希望扩展到：基于深度学习的逆向设计

2025/03/27
A 写了自动仿真程序，思路取自论文*Octave bandwidth photonic fishnet-achromaticmetalens*，但由于目标参数不同，因此需要重新计算数据。现在的问题是数据量实在太大了，可能还得优化

B 把matlab的遗传算法优化相位函数部分上传了

明天开始一定做数据库！

2025/03/27
1.上传了第五周写的数据库模块和一些示例数据

2.基本处理好了自动仿真模块的接口和一些函数，现在已经能进行最基础的仿真啦