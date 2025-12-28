function [Eout, phi] = NBphase(r,single,lambda,l, Fnum,start,stop,singleDownsampling,loop,popnum,Ft,Ft_low)
%% 焦点分布迭代计算
U = int64(r*2/single);
UDownsampling=int16(r/singleDownsampling*2);

x = linspace(-(r-0.5*singleDownsampling),(r-0.5*singleDownsampling),UDownsampling);
y = linspace(-(r-0.5*singleDownsampling),(r-0.5*singleDownsampling),UDownsampling);
[X,Y]=meshgrid(x,y);

R=zeros(loop,Fnum);
I=zeros(loop,Fnum);
L=zeros(loop,Fnum);

L(1,:)=linspace(start,stop,Fnum);
Eout=Light_field_Emission_field(Ft_low,L(1,:),r,l,singleDownsampling,lambda,UDownsampling);

I(1,:)=RSaxis_GPU(Eout, lambda, X, Y, L(1,:), 1);

for i=2:loop
    R(i,:)=I(i-1,:)./((1/Fnum)*sum(I(i-1,:)));
    L(i,1)=start;
    for j=2:Fnum
        L(i,j)=(L(i-1,j)-L(i-1,j-1)).*R(i,j)+L(i,j-1);
    end
    L(i,Fnum)=stop;
    Eout=Light_field_Emission_field(Ft_low,L(i,:),r,l,singleDownsampling,lambda,UDownsampling);
    I(i,:)=RSaxis_GPU(Eout, lambda, X, Y, L(i,:), 1);
    printProgress('焦点位置优化', i, loop)
end

InitL = L(loop,:);

%% 密集优化
para.r = r;
para.single = singleDownsampling;
para.lambda = lambda;
para.l = l;
para.U = UDownsampling;
para.Fnum = Fnum;
para.start = start;
para.stop = stop;

initPop = ...
    [InitL; ...
    Generate_Initial_Population(InitL, 0.05e-3, popnum-1, ...
    start, stop)];

fitFunc = @(x) Fitness(Ft_low,para,x);

options = optimoptions('ga', ...
    'Display', 'iter', ...
    'PopulationSize', popnum, ...
    'MaxGenerations', 500, ...
    'InitialPopulationMatrix', initPop, ... 
    'CrossoverFraction', 0.8, ...
    'OutputFcn', @gaStopAtFitness);

lb = (start-0.1e-3) * ones(1, Fnum);
ub = (stop+0.1e-3) * ones(1, Fnum);

[bestList, ~] = ga(fitFunc, double(Fnum), [], [], [], [], lb, ub, [], options);

Eout = Light_field_Emission_field(Ft, bestList, r, l, single, lambda, U);
phi = Light_field_Phase_field(Ft, bestList, r, l, single, lambda, U);
phi = wrapToPi(phi);

%% 验证
x = linspace(-(r-0.5*single),(r-0.5*single),U);
y = linspace(-(r-0.5*single),(r-0.5*single),U);
[X,Y]=meshgrid(x,y);

z = linspace(start-20e-6, stop+20e-6, 100);

E = RSaxis_GPU(Eout, lambda, X, Y, z, 1);

f1 = figure(1);
plot(z, E)
txt1 = sprintf("Wav = %d", lambda);
title(txt1)

txt2 = sprintf("Wav%3.0d.mat", lambda*1e9);
save(txt2, "phi", "Eout", "bestList")

txt3 = sprintf("Wav%3.0d.fig", lambda*1e9);
savefig(f1, txt3)

close all

function [state, options, optchanged] = gaStopAtFitness(options, state, flag)
    optchanged = false;
    targetFitness = 3;

    % 判断当前最优值是否低于目标
    if strcmp(flag, 'iter')
        currentBest = state.Best(end);
        if currentBest < targetFitness
            state.StopFlag = 'Fitness below threshold';
        end
    end
end
end