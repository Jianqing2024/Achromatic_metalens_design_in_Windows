function Test(betaList)
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

z = linspace(start-0.5e-3,stop+0.5e-3,200)';
%% 计算光强
% 生成光场
Eout = Light_field_Emission_field(Ft,betaList,r,l,single,lambda,U);
Ein = Light_field_Incident_field(r,l,single,lambda,U);
Phase = Light_field_Phase_field(Ft,betaList,r,l,single,lambda,U);

save Phase.mat Phase
% 远场计算
E = RSaxis_GPU(Eout, lambda, X, Y, z);

%% 归一化/计算适应度
Enormal = normalizeArrayTo01(E);
Estandard = flat_top_gaussian(z, 1, start, stop, 0.1e-3);

figure(4)
plot(z,Enormal,z,Estandard)
%%
figure(5)
n=10;
zo=linspace(start,stop,n);
for i=1:n
    [eff(i), fwhm(i)]=...
        Focus_on_efficiency_lowSampling_GPU...
            (Eout,X,Y,Ein,lambda,zo(i),100,7e-6,0.1e-6);
    disp(zo(i))
end

figure(5)
subplot(2,1,1)
plot(zo,eff)
title('Efficiency')
subplot(2,1,2)
plot(zo,fwhm)
title('FWHM')
end