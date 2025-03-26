clear;clc;
data=load('SweepPhi.mat');
SweepPhi = data.SweepPhi;

p=cell(1,60);
% 单个结构相位/色散谱
for i=1:5
    Phi=SweepPhi{i};
    for j=1:12
        p{(i-1)*12+j}=Phi(:,j)';
    end
end

data = struct('structure_info', {}, 'measurements', {});

lambda=linspace(0.4e-6,0.6e-6,10);
lambda=num2cell(lambda,1);

for i=1:60
    data(i).structure_info = sprintf('%f',i);
    data(i).measurements = struct('wavelength', lambda, ...
        'phase_shift',num2cell(p{1, i}, 1),'transmission',num2cell(zeros(1,10)));
end

jsonData = jsonencode(data, 'PrettyPrint', true);

fileID = fopen('data.json', 'w');
fprintf(fileID, '%s', jsonData);
fclose(fileID);

disp('JSON 文件已生成: data.json');