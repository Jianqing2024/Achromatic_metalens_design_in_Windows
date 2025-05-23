## Design_For_Metalens

**_Windows部分_**

**循此苦旅直抵群星**

目前用于设计消色差超透镜

此部分主要包括三个功能: 调用Lumapi，复检meep的计算结果；调用optuna计算出最佳参数组和该参数组下的最佳相位修正值；调用matlab进行远场仿真

其中，远场仿真使用的代码使用衍射积分法，基于瑞利-索末菲衍射积分公式，使用前需先手动将其加入到Matlab路径中

# 注意事项

LumAPI接口路径需要手动修改

在使用并行运算功能前务必将LumericalFDTD软件GUI页面中的Resource部分设置好

必须在GUI页面中设置好模板文件的材料