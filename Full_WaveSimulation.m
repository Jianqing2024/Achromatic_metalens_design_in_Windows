function Full_WaveSimulation()
load dataPhase.mat X Y phase0 phase1 phase2 phase3 phase4
[~, f] = Read_Parameter();

lambda = linspace(0.8e-6, 0.5e-6, 5);
z = linspace(1e-6, f+1e-3, 300);

ZZ{1} = RSaxis_GPU(exp(1i*phase0),lambda(1), X, Y, z);
[~, i(1)] = max(ZZ{1});
ZZ{2} = RSaxis_GPU(exp(1i*phase1),lambda(2), X, Y, z);
[~, i(2)] = max(ZZ{2});
ZZ{3} = RSaxis_GPU(exp(1i*phase2),lambda(3), X, Y, z);
[~, i(3)] = max(ZZ{3});
ZZ{4} = RSaxis_GPU(exp(1i*phase3),lambda(4), X, Y, z);
[~, i(4)] = max(ZZ{4});
ZZ{5} = RSaxis_GPU(exp(1i*phase4),lambda(5), X, Y, z);
[~, i(5)] = max(ZZ{5});

Effi = zeros(5,1);
fwhm = zeros(5,1);

[sX,sY]=size(phase0);

for j=1:5

    if j == 1
        phase = phase0;
    elseif j == 2
        phase = phase1;
    elseif j == 3
        phase = phase2;
    elseif j == 4
        phase = phase3;
    elseif j == 5
        phase = phase4;
    end

[Effi(j),fwhm(j)]=...
    Focus_on_efficiency_lowSampling_GPU(exp(1i*phase),X,Y,ones(sX,sY),lambda(j),z(i(j)),200,7.5e-6,0.25e-6);
end

fig1 = figure(1);
subplot(5,1,1)
plot(z, normalizeArrayTo01(ZZ{1}))
txt = sprintf("lambda = %.4f/um, f = %.4f/um, Eff = %f, fwhm = %.2f/um", lambda(1)*1e6, z(i(1))*1e6, Effi(1), fwhm(1)*1e6);
title(txt)

subplot(5,1,2)
plot(z, normalizeArrayTo01(ZZ{2}))
txt = sprintf("lambda = %.4f/um, f = %.4f/um, Eff = %f, fwhm = %.2f/um", lambda(2)*1e6, z(i(2))*1e6, Effi(2), fwhm(2)*1e6);
title(txt)

subplot(5,1,3)
plot(z, normalizeArrayTo01(ZZ{3}))
txt = sprintf("lambda = %.4f/um, f = %.4f/um, Eff = %f, fwhm = %.2f/um", lambda(3)*1e6, z(i(3))*1e6, Effi(3), fwhm(3)*1e6);
title(txt)

subplot(5,1,4)
plot(z, normalizeArrayTo01(ZZ{4}))
txt = sprintf("lambda = %.4f/um, f = %.4f/um, Eff = %f, fwhm = %.2f/um", lambda(4)*1e6, z(i(4))*1e6, Effi(4), fwhm(4)*1e6);
title(txt)

subplot(5,1,5)
plot(z, normalizeArrayTo01(ZZ{5}))
txt = sprintf("lambda = %.4f/um, f = %.4f/um, Eff = %f, fwhm = %.2f/um", lambda(5)*1e6, z(i(5))*1e6, Effi(5), fwhm(5)*1e6);
title(txt)

savefig(fig1,"figFarField.fig")

save result.mat Effi fwhm

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