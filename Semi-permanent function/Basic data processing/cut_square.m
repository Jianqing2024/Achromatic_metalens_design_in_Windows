function result = cut_square(matrix, M)
    % 获取原矩阵的尺寸
    [N, ~] = size(matrix);
    
    % 计算中心点的位置
    center = floor(N / 2) + 1;
    
    % 计算提取区域的起始位置和结束位置
    start_idx = center - floor(M / 2);
    end_idx = start_idx + M - 1;
    
    % 提取小矩阵
    result = matrix(start_idx:end_idx, start_idx:end_idx);
end
