function FIT=Fitness(betaList)
%% 参数设定
% 导入原始设置
para = load('para.mat');

Ft = para.Ft;
para = para.parameter;

r=para.r;
single=para.single;
lambda=para.lambda;
l=para.l;

start=para.start;
stop=para.stop;

U=int16(r/single*2);
x = linspace(-(r-0.5*single), (r-0.5*single), U);
y = linspace(-(r-0.5*single), (r-0.5*single), U);
[X, Y] = meshgrid(x,y);

z = linspace(start-0.5e-3,stop+0.5e-3,100);
%% 计算光强
% 生成光场
Eout = Light_field_Emission_field(Ft,betaList,r,l,single,lambda,U);
% 远场计算
E = RSaxis_GPU(Eout, lambda, X, Y, z);

%% 归一化/计算适应度
Enormal = normalizeArrayTo01(E);
Estandard = flat_top_gaussian(z, 1, start, stop, 0.1e-3);
FIT = sum(abs(Enormal-Estandard));
% figure(1)
% plot(z,Enormal,z,Estandard)
% drawnow
end