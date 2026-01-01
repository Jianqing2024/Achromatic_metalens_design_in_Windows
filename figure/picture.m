clear;clc;close all
load figPart1.mat
load figPart2.mat
load bamako.mat
load lajolla.mat

E532_xz = (E532_xz - min(E532_xz(:))) / (max(E532_xz(:)) - min(E532_xz(:)));
E780_xz = (E780_xz - min(E780_xz(:))) / (max(E780_xz(:)) - min(E780_xz(:)));

colorA = slanCM('Greens');
colorB = slanCM('Reds');
TickLength1 = [0.01, 0.1];
TickLength2 = [0.05, 0.1];

f1 = figure(1);
f1.Units = "centimeters";
f1.Position = [30,2,18,14];
f1.Color = 'w';

t1  =  tiledlayout(3 ,4);
ax1  = nexttile(1, [3, 1]);
imagesc([-60, 60], [19000, 23000], E532_xz')
yline(20000, 'k--')
yline(21000, 'k--')
yline(22000, 'k--')
ax1.XTickMode = 'manual';
ax1.YTickMode = 'manual';
ax1.XTick = -40:40:40;
ax1.YTick = [];
ax1.TickLength = TickLength1;
ax1.XTickLabel = {};
ax1.YTickLabel = {};
ax1.Colormap = colorA;

ax2 = nexttile(2, [1, 1]);
imagesc([-40, 40], [-40, 40], E532_xy{1})
axis image
ax2.XTickMode = 'manual';
ax2.YTickMode = 'manual';
ax2.XTick = -40:40:40;
ax2.YTick = -40:40:40;
ax2.TickLength = TickLength2;
ax2.XTickLabel = {};
ax2.YTickLabel = {};
ax2.Colormap = colorA;

ax3 = nexttile(3, [1, 1]);
imagesc([-40, 40], [-40, 40], E780_xy{1})
axis image
ax3.XTickMode = 'manual';
ax3.YTickMode = 'manual';
ax3.XTick = -40:40:40;
ax3.YTick = -40:40:40;
ax3.TickLength = TickLength2;
ax3.XTickLabel = {};
ax3.YTickLabel = {};
ax3.Colormap = colorB;

ax4  = nexttile(4, [3, 1]);
imagesc([-60, 60], [19000, 23000], E780_xz')
yline(20000, 'k--')
yline(21000, 'k--')
yline(22000, 'k--')
ax4.XTickMode = 'manual';
ax4.YTickMode = 'manual';
ax4.XTick = -40:40:40;
ax4.YTick = -40:40:40;
ax4.TickLength = TickLength1;
ax4.XTickLabel = {};
ax4.YTickLabel = {};
ax4.Colormap = colorB;

ax5 = nexttile(6, [1, 1]);
imagesc([-40, 40], [-40, 40], E532_xy{2})
axis image
ax5.XTickMode = 'manual';
ax5.YTickMode = 'manual';
ax5.XTick = -40:40:40;
ax5.YTick = -40:40:40;
ax5.TickLength = TickLength2;
ax5.XTickLabel = {};
ax5.YTickLabel = {};
ax5.Colormap = colorA;

ax6 = nexttile(7, [1, 1]);
imagesc([-40, 40], [-40, 40], E780_xy{2})
axis image
ax6.XTickMode = 'manual';
ax6.YTickMode = 'manual';
ax6.XTick = -40:40:40;
ax6.YTick = -40:40:40;
ax6.TickLength = TickLength2;
ax6.XTickLabel = {};
ax6.YTickLabel = {};
ax6.Colormap = colorB;

ax7 = nexttile(10, [1, 1]);
imagesc([-40, 40], [-40, 40], E532_xy{3})
axis image
ax7.XTickMode = 'manual';
ax7.YTickMode = 'manual';
ax7.XTick = -40:40:40;
ax7.YTick = -40:40:40;
ax7.TickLength = TickLength2;
ax7.XTickLabel = {};
ax7.YTickLabel = {};
ax7.Colormap = colorA;

ax8 = nexttile(11, [1, 1]);
imagesc([-40, 40], [-40, 40], E780_xy{3})
axis image
ax8.XTickMode = 'manual';
ax8.YTickMode = 'manual';
ax8.XTick = -40:40:40;
ax8.YTick = -40:40:40;
ax8.TickLength = TickLength2;
ax8.XTickLabel = {};
ax8.YTickLabel = {};
ax8.Colormap = colorB;

% 左侧 colorbar（532 nm）
cb1 = colorbar(ax1, 'Location', 'westoutside');
cb1.Ticks = [0, 0.5, 1];
cb1.TickLabels = {};

% 右侧 colorbar（780 nm）
cb2 = colorbar(ax4, 'Location', 'eastoutside');
cb2.Ticks = [0, 0.5, 1];
cb2.TickLabels = {};

ax9 = axes;
plot(ax9, normalizeArrayTo01(E532_xy{1}(51, :)), 'k--')
pos = ax2.Position;
ax9.Position = pos;
ax9.Visible = 'off';
ax9.YLim = [0, 1.15];
yline(ax2, 0)

ax10 = axes;
plot(ax10, normalizeArrayTo01(E780_xy{1}(51, :)), 'k--')
pos = ax3.Position;
ax10.Position = pos;
ax10.Visible = 'off';
ax10.YLim = [0, 1.15];
yline(ax3, 0)

ax11 = axes;
plot(ax11, normalizeArrayTo01(E532_xy{2}(51, :)), 'k--')
pos = ax5.Position;
ax11.Position = pos;
ax11.Visible = 'off';
ax11.YLim = [0, 1.15];
yline(ax5, 0)

ax12 = axes;
plot(ax12, normalizeArrayTo01(E780_xy{2}(51, :)), 'k--')
pos = ax6.Position;
ax12.Position = pos;
ax12.Visible = 'off';
ax12.YLim = [0, 1.15];
yline(ax6, 0)

ax13 = axes;
plot(ax13, normalizeArrayTo01(E780_xy{2}(51, :)), 'k--')
pos = ax7.Position;
ax13.Position = pos;
ax13.Visible = 'off';
ax13.YLim = [0, 1.15];
yline(ax7, 0)

ax14 = axes;
plot(ax14, normalizeArrayTo01(E780_xy{2}(51, :)), 'k--')
pos = ax8.Position;
ax14.Position = pos;
ax14.Visible = 'off';
ax14.YLim = [0, 1.15];
yline(ax8, 0)