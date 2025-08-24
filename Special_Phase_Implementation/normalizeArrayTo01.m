function normalizedArray = normalizeArrayTo01(inputArray)
    % 确保输入数组为一维
if ~isvector(inputArray)
        error('输入数组必须是一维矩阵');
end
    
    % 归一化计算到 [0,1]
    minVal = min(inputArray);
    maxVal = max(inputArray);
    normalizedArray = (inputArray - minVal) / (maxVal - minVal);
end