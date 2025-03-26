% clear;clc;
% 预分配结构体数组
data = struct('structure_info', {}, 'measurements', {});

% 生成第一个纳米结构的数据
data(1).structure_info = 'Si_100x100x50';
data(1).measurements = struct( ...
    'wavelength', {500, 600}, ...
    'phase_shift', {45.0, 50.0}, ...
    'transmission', {0.85, 0.80} ...
);

% 生成第二个纳米结构的数据
data(2).structure_info = 'Si_200x200x100';
data(2).measurements = struct( ...
    'wavelength', {500, 600}, ...
    'phase_shift', {40.0, 42.0}, ...
    'transmission', {0.88, 0.86} ...
);

% 转换为 JSON
jsonData = jsonencode(data, 'PrettyPrint', true);

% 写入 JSON 文件
fileID = fopen('data.json', 'w');
fprintf(fileID, '%s', jsonData);
fclose(fileID);

disp('JSON 文件已生成: data.json');
