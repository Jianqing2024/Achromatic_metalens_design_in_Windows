function Full_WaveSimulation()
load dataPhase.mat X Y phase0 phase1 phase2 phase3 phase4
[~, f] = Read_Parameter();

lambda = linspace(0.8e-6, 0.5e-6, 5);
z = linspace(1e-6, f+10e-6, 100);

ZZ{1} = RSaxis(exp(1i*phase0),lambda(1), X, Y, z);
ZZ{2} = RSaxis(exp(1i*phase1),lambda(2), X, Y, z);
ZZ{3} = RSaxis(exp(1i*phase2),lambda(3), X, Y, z);
ZZ{4} = RSaxis(exp(1i*phase3),lambda(4), X, Y, z);
ZZ{5} = RSaxis(exp(1i*phase4),lambda(5), X, Y, z);

fig1 = figure(1);
tiledlayout("vertical")

nexttile
plot(z, ZZ{1})

nexttile
plot(z, ZZ{2})

nexttile
plot(z, ZZ{3})

nexttile
plot(z, ZZ{4})

nexttile
plot(z, ZZ{5})

savefig(fig1,"figFarField.fig","-v7.3")

function [r, f] = Read_Parameter()
    % 获取当前工作目录
    base_dir = pwd;
    % 拼接完整文件路径
    filename = fullfile(base_dir, 'data', 'parameter.txt');
    
    % 打开文件
    fid = fopen(filename, 'r');
    if fid == -1
        error('无法打开文件: %s', filename);
    end
    
    % 读取前两行
    line1 = fgetl(fid);
    line2 = fgetl(fid);
    fclose(fid);
    
    % 提取等号右边的数值
    r = str2double(strtrim(extractAfter(line1, '=')));
    f = str2double(strtrim(extractAfter(line2, '=')));
end
end