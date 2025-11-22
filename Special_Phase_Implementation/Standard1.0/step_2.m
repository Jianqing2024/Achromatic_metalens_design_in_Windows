clear;

lo = load('para.mat');
para = lo.para;
clear lo

num = para.Fnum;
popnum = 50;

InitL = linspace(para.start, para.stop, num);
nitPop = ...
    [InitL; ...
    Generate_Initial_Population(InitL, 0.05e-3, popnum-1, ...
    para.start, para.stop)];

options = optimoptions('ga', ...
    'Display', 'iter', ...
    'PopulationSize', 50, ...
    'MaxGenerations', 1500, ...        % 设置最大迭代次数为1500
    'CrossoverFraction', 0.8, ...
    'OutputFcn', @gaStopAtFitness);    % 加入自定义终止函数

% 3. 定义参数上下界
lb = (para.start-0.1e-3) * ones(1, num);
ub = (para.stop+0.1e-3) * ones(1, num);

% 4. 执行遗传算法
[betaList, fval] = ga(@Fitness, num, [], [], [], [], lb, ub, [], options);

disp('目标函数的最小值:');
disp(fval);

para.ft = betaList;

save para.mat para

run step_3.m

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