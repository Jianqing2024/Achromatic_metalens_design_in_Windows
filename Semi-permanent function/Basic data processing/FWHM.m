function fwhm = FWHM(x, y)

    if length(x) ~= length(y)
        error('x 和 y 必须是相同长度的一维向量');
    end

    % 找到 y 的最大值及其对应的半高
    maxY = max(y);
    halfMax = maxY / 2;

    % 找到 y 超过半高的点的索引
    indicesAboveHalfMax = find(y >= halfMax);

    % 如果无法找到两个点，使用近似值
    if isempty(indicesAboveHalfMax)
        % 如果完全没有超过半高的点，返回全域宽度
        fwhm = x(end) - x(1);
        return;
    elseif length(indicesAboveHalfMax) == 1
        % 如果只有一个超过半高的点，插值近似计算FWHM
        fwhm = 2 * (x(end) - x(indicesAboveHalfMax(1))); % 近似假设对称
        return;
    end

    % 对左边界进行线性插值以找到精确的交点
    if indicesAboveHalfMax(1) > 1
        % 确保索引在有效范围内再插值
        x1 = interp1(y(indicesAboveHalfMax(1)-1:indicesAboveHalfMax(1)), ...
                     x(indicesAboveHalfMax(1)-1:indicesAboveHalfMax(1)), ...
                     halfMax);
    else
        % 如果索引越界，直接使用当前点
        x1 = x(indicesAboveHalfMax(1));
    end

    % 对右边界进行线性插值以找到精确的交点
    if indicesAboveHalfMax(end) < length(y)
        % 确保索引在有效范围内再插值
        x2 = interp1(y(indicesAboveHalfMax(end):indicesAboveHalfMax(end)+1), ...
                     x(indicesAboveHalfMax(end):indicesAboveHalfMax(end)+1), ...
                     halfMax);
    else
        % 如果索引越界，直接使用当前点
        x2 = x(indicesAboveHalfMax(end));
    end

    % 如果插值失败或者边界位置异常，则返回近似宽度
    if isnan(x1) || isnan(x2)
        fwhm = x(end) - x(1);
    else
        % 计算FWHM为x2和x1之间的距离
        fwhm = x2 - x1;
    end
end