function pop = Generate_Initial_Population(x0, u, popSize, lb, ub)
% 手动生成初始种群
% x0:    已知较优个体（1×num变量）
% u:     扰动幅度（标量或与 x0 同长度）
% popSize: 总种群数量（整数）
% lb/ub: 变量上下限

    numVars = length(x0);
    pop = zeros(popSize, numVars);
    
    for i = 1:popSize
        % 添加随机扰动
        delta = u .* (2*rand(1, numVars) - 1);  % [-u, +u] 区间
        pop(i, :) = sort(x0 + delta);
    end

    % 确保在上下界之间
    pop = min(max(pop, lb), ub);
    
end
