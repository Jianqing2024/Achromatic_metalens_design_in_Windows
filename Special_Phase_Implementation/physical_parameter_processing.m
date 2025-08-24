function resultCells = physical_parameter_processing(radiusMat, xMat, yMat, num)
    % 将三个矩阵转化为列向量
    radiusVec = radiusMat(:);
    xVec = xMat(:);
    yVec = yMat(:);
    
    % 合并为一个n*3的新矩阵
    combinedMatrix = [radiusVec, xVec, yVec];
    
    % 删除半径为0的圆形
    combinedMatrix(combinedMatrix(:,1) == 0, :) = [];
    
    % 将矩阵按每5000个圆形分为一个cell数组
    resultCells = {};
    numCircles = size(combinedMatrix, 1);
    for i = 1:num:numCircles
        resultCells{end+1} = combinedMatrix(i:min(i+4999, numCircles), :);
    end
end