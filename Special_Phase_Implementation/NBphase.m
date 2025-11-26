function [Eout, phi] = NBphase(r,single,lambda,l,U,Fnum,start,stop,Ft)
popnum = 50;
para.r = r;
para.single = single;
para.lambda = lambda;
para.l = l;
para.U = U;
para.Fnum = Fnum;
para.start = start;
para.stop = stop;

fitFunc = @(x) Fitness(Ft,para,x);

InitL = linspace(start, stop, Fnum);
initPop = ...
    [InitL; ...
    Generate_Initial_Population(InitL, 0.05e-3, popnum-1, ...
    start, stop)];

options = optimoptions('ga', ...
    'Display', 'iter', ...
    'PopulationSize', popnum, ...
    'MaxGenerations', 100, ...
    'InitialPopulationMatrix', initPop, ... 
    'CrossoverFraction', 0.8, ...
    'OutputFcn', @gaStopAtFitness);

lb = (start-0.1e-3) * ones(1, Fnum);
ub = (stop+0.1e-3) * ones(1, Fnum);

[bestList, ~] = ga(fitFunc, double(Fnum), [], [], [], [], lb, ub, [], options);

Eout = Light_field_Emission_field(Ft, bestList, r, l, single, lambda, U);
phi = Light_field_Phase_field(Ft, bestList, r, l, single, lambda, U);
phi = wrapToPi(phi);

x = linspace(-(r-0.5*single),(r-0.5*single),U);
y = linspace(-(r-0.5*single),(r-0.5*single),U);
[X,Y]=meshgrid(x,y);

z = linspace(10e-6, 100e-6, 100);

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