clear;clc;close all
colorA = slanCM('Greens');
colorB = slanCM('Reds');
colorC = slanCM('set2');

r = 25e-6;
single = 0.4e-6;
U =  int64(2*r/single);
x = linspace(-(r-0.5*single),(r-0.5*single),U);
y = linspace(-(r-0.5*single),(r-0.5*single),U);
[X, Y] = meshgrid(x, y);
R = sqrt(X.^2+Y.^2);

% load fig0part2.mat
% for i = 1:4
%     phase_f_780{i}(R>r) = NaN;
% 
%     figure(i)
%     ax1 = axes;
%     im = imagesc(ax1, x, y, phase_f_780{i});
%     im.AlphaData = ~isnan(phase_f_780{i});
%     axis image
%     ax1.XTick = [];
%     ax1.YTick = [];
%     ax1.Colormap = colorB;
%     hold on
%     theta = linspace(0, 2*pi, 500);
% 
%     xc = r * cos(theta);
%     yc = r * sin(theta);
% 
%     plot(xc, yc, 'k', 'LineWidth', 1.5);
%     hold off
%     axis off
% 
%     phase_f_532{i}(R>r) = NaN;
% 
%     figure(i+4)
%     ax2 = axes;
%     im = imagesc(ax2, x, y, phase_f_532{i});
%     im.AlphaData = ~isnan(phase_f_532{i});
%     axis image
%     ax2.XTick = [];
%     ax2.YTick = [];
%     ax2.Colormap = colorA;
%     hold on
%     theta = linspace(0, 2*pi, 500);
% 
%     xc = r * cos(theta);
%     yc = r * sin(theta);
% 
%     plot(xc, yc, 'k', 'LineWidth', 1.5);
%     hold off
%     axis off
% end

% LOC = Random_Matrix_Generation(U, 16);
% figure(1)
% ax = axes;
% imagesc(ax, LOC)
% axis image
% ax.Colormap = gray;
% ax.XTick = [];
% ax.YTick = [];
% ax.LineWidth = 2;

% load fig0part1.mat
% 
% figure(1)
% ax = axes;
% imagesc(phase_in_532)
% axis image
% ax.Colormap = colorA;
% ax.XTick = [];
% ax.YTick = [];
% ax.LineWidth = 2;

load Wav780.mat

figure(1)
ax = axes;
imagesc(wrapToPi(phi))
axis image
ax.Colormap = colorB;
ax.XTick = [];
ax.YTick = [];
ax.LineWidth = 2;
