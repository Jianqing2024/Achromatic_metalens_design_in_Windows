clear;clc
% 基本参数相同的结构称为一组结构。每次循环从数据库中提取出一组结构，进行最优化处理
% 最优化处理包括三层：
% 最内层要选出在每个位置上最适合的结构，中间层要选出在这种位置排布下相位差最小的修正方案，最外层要决定使用哪一种基本参数
%% 参数确定
R=0.25e-3;
f=8.5e-3;
lambda=[0.532e-6;0.800e-6];

nvars=3;
lb=[-pi,-pi,-0.1e-3]; % 下界
ub=[pi,pi,0.1e-3];    % 上界
options=optimoptions('ga', 'PopulationSize', 40, 'MaxGenerations', 20000, 'FunctionTolerance', 1e-8);

parameter=[R;f;lambda];
save parameter.mat parameter
%% 优化

db = sqlite('structures.db', 'readonly');
numBaseValue=table2array(fetch(db, 'SELECT COUNT(DISTINCT baseValue) FROM structures;'));
% 
% opt=zeros(numBaseValue,1);
% fit=cell(numBaseValue,1);
% for i=1:numBaseValue
%     sql=sprintf("SELECT * FROM structures WHERE baseValue = %d;",i);
%     data=fetch(db, sql);
%     save("data.mat",data)
%     % 写完后改成那个函数
%     [opt(i), fit{i}] = ga(@OptimalSolutionCalculation, nvars, [], [], [], [], lb, ub, [], options);
% end
% 
% [bestFit,idx]=min(fit);
%%
idx=3;

sql=sprintf("SELECT * FROM structures WHERE baseValue = %d;",idx);
data=fetch(db, sql);
close(db);