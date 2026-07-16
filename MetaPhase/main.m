function phi  = main()
%% 参数设置
para=parameter_preset();

U = para.U;
Fnum = para.Fnum;

Ft = Random_Matrix_Generation(U,Fnum);
fitnessFcn = @(x) FitnessA(Ft, x);

options = optimoptions('ga', ...
    'Display', 'iter', ...
    'PopulationSize', 50, ...
    'MaxGenerations', 1000, ... 
    'CrossoverFraction', 0.8);

% 3. 定义参数上下界
lb = [0e-3, 10e-9, 0e-6];
ub = [20e-3,  80e-9, 40e-6];

% 4. 执行遗传算法
[bestList, ~] = ga(fitnessFcn, 3, [], [], [], [], lb, ub, [], options);
%%

A = bestList(1);
V = bestList(2);
D = bestList(3);

para=parameter_preset();

r=para.r;
single=para.single;
lambda=para.lambda;

Fnum=para.Fnum;

l=para.l;

start=para.start;
stop=para.stop;

U=para.U;

popSize = 50;

fitnessFcn = @(x) FitnessB(Ft, x);

Init_ft = Focal_Sequence_Generation(start, Fnum, V, D)';
Init_At = A*ones(1,Fnum);

Init_ft_pop = [Generate_Initial_Population(Init_ft, 500e-9, popSize-1, start-0.1e-3, stop+0.1e-3);Init_ft];
Init_At_pop = [Generate_Initial_Population(Init_At, 1e-3, popSize-1, 0.000, 0.02);Init_At];
Init_pop = [Init_ft_pop,Init_At_pop];

options = optimoptions('ga', ...
    'Display', 'iter', ...
    'InitialPopulationMatrix', Init_pop, ...
    'PopulationSize', popSize, ...
    'MaxGenerations', 1000, ... 
    'CrossoverFraction', 0.8, ...
    'OutputFcn', @gaStopAtFitness);

% 3. 定义参数上下界
lb = [(start-0.1e-3)*ones(1,Fnum),0.1e-3*ones(1,Fnum)];
ub = [(stop+0.1e-3)*ones(1,Fnum),20e-3*ones(1,Fnum)];

% 4. 执行遗传算法
[bestList, ~] = ga(fitnessFcn, Fnum*2, [], [], [], [], lb, ub, [], options);

ft=bestList(1:Fnum);
At=bestList(Fnum+1:end);

[~, phi] = Light_Field_SA_B(Ft, ft, r, l, single, lambda, U, At);

save phase.mat phi

function [state, options, optchanged] = gaStopAtFitness(options, state, flag)
    optchanged = false;
    targetFitness = 5;

    % 判断当前最优值是否低于目标
    if strcmp(flag, 'iter')
        currentBest = state.Best(end);
        if currentBest < targetFitness
            state.StopFlag = 'Fitness below threshold';
        end
    end
end
end