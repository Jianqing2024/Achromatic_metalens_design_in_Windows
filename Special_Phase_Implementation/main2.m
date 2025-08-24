clear;

load para.mat

num = parameter.Fnum;
popnum = 50;
nitPop = ...
    [InitL; ...
    Generate_Initial_Population(InitL, 0.05e-3, popnum-1, ...
    parameter.start, parameter.stop)];

options = optimoptions('ga', ...
    'Display', 'iter', ...
    'PopulationSize', 50, ...
    'MaxGenerations', 1500, ...        % 设置最大迭代次数为1500
    'CrossoverFraction', 0.8, ...
    'OutputFcn', @gaStopAtFitness);    % 加入自定义终止函数

% 3. 定义参数上下界
lb = (parameter.start-0.1e-3) * ones(1, num);
ub = (parameter.stop+0.1e-3) * ones(1, num);

% 4. 执行遗传算法
[betaList, fval] = ga(@Fitness, num, [], [], [], [], lb, ub, [], options);

% 5. 显示结果
disp('优化后的解:');
disp(betaList);      % 优化结果
disp('目标函数的最小值:');
disp(fval);   % 对应的目标函数最小值

save para.mat parameter Ft betaList

Test(betaList)

run Parameter_expand.m


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