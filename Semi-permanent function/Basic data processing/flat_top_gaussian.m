function y = flat_top_gaussian(x, height, flat_start, flat_end, sigma)
    % flat_top_gaussian - 基于高斯函数生成平顶函数
    % 
    % 输入参数：
    %   x - 自变量数组
    %   height - 平顶高度
    %   flat_start - 平顶起始位置
    %   flat_end - 平顶终止位置
    %   sigma - 高斯边缘的标准差
    %
    % 输出：
    %   y - 平顶函数的函数值

    % 高斯左边缘
    left_gauss = height * exp(-((x - flat_start).^2) / (2 * sigma^2));
    left_gauss(x >= flat_start) = 0;

    % 高斯右边缘
    right_gauss = height * exp(-((x - flat_end).^2) / (2 * sigma^2));
    right_gauss(x <= flat_end) = 0;

    % 平顶部分
    flat_region = height * ones(size(x));
    flat_region(x < flat_start | x > flat_end) = 0;

    % 合并
    y = left_gauss + right_gauss + flat_region;
end