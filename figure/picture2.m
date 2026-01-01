clear;clc;close all
load figPart3.mat
E780_z = normalizeArrayTo01(E780_z);
E532_z = normalizeArrayTo01(E532_z);

E_target = flat_top_gaussian(zz, 1, 20e-3, 22e-3, 0.2e-3);

f1 = figure(1);
f1.Units = "centimeters";
f1.Position = [30,2,18,12];
f1.Color = 'w';

ax = axes;
ax.Units = "centimeters";
ax.Position = [1,1,8,4.5];

plot(zz, E532_z, 'LineWidth', 1, 'Color', '#16a085')
hold on
plot(zz, E780_z, 'LineWidth', 1, 'Color', '#c0392b')

plot(zz, E_target, 'LineStyle', '--', 'Color', 'black')
hold off

ax.YLim = [0, 1.15];
ax.XTickMode = 'manual';
ax.YTickMode = 'manual';
ax.XTick = 19e-3:1e-3:23e-3;
ax.YTick = 0:0.5:1;
ax.XTickLabel = {};
ax.YTickLabel = {};

xline(20e-3)
xline(22e-3)