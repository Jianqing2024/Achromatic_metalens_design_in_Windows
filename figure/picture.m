clear;clc;close all
load figPart1.mat
load figPart2.mat
load FWHM.mat

E532_xz = (E532_xz - min(E532_xz(:))) / (max(E532_xz(:)) - min(E532_xz(:)));
E780_xz = (E780_xz - min(E780_xz(:))) / (max(E780_xz(:)) - min(E780_xz(:)));

for i = 1:3
    E780_xy{i} = (E780_xy{i} - min(E780_xy{i}(:))) / (max(E780_xy{i}(:)) - min(E780_xy{i}(:)));
    E532_xy{i} = (E532_xy{i} - min(E532_xy{i}(:))) / (max(E532_xy{i}(:)) - min(E532_xy{i}(:)));
end

x = linspace(-40, 40, 100);

colorA = slanCM('Greens');
colorB = slanCM('Reds');
TickLength1 = [0.01, 0.1];
TickLength2 = [0.05, 0.1];

f1 = figure(1);
f1.Units = "centimeters";
f1.Position = [30,2,18,18];
f1.Color = 'w';

n1  =  tiledlayout(4, 4);

%%
ax1  = nexttile(1, [3, 1]);
imagesc([-60, 60], [19000, 23000], E532_xz')
yline(20000, 'k--')
yline(21000, 'k--')
yline(22000, 'k--')
ax1.XTickMode = 'manual';
ax1.YTickMode = 'manual';
ax1.XTick = -40:40:40;
ax1.YTick = 20000:1000:22000;
ax1.TickLength = TickLength1;
ax1.XTickLabel = {'-40', '0', '40'};
ax1.YTickLabel = {'22', '21', '20'};
ax1.Colormap = colorA;
ax1.FontName = 'Times New Roman';
ax1.FontSize = 8;
ax1.YAxisLocation = 'left';
ax1.XLabel.String = 'x (μm)';
ax1.XLabel.FontName = 'Times New Roman';
ax1.YLabel.String = 'z (mm)';
ax1.YLabel.FontName = 'Times New Roman';
[t1, s1] = title(ax1, 'Wavelength (nm)', '532');
t1.FontName = 'Times New Roman';
t1.FontWeight = 'bold';
t1.FontSize = 10;
s1.FontName = 'Times New Roman';
s1.FontSize = 9;
s1.FontWeight = 'bold';

ax2 = nexttile(2, [1, 1]);
imagesc([-40, 40], [-40, 40], E532_xy{1})
axis image
ax2.XTickMode = 'manual';
ax2.YTickMode = 'manual';
ax2.XTick = -40:40:40;
ax2.YTick = -40:40:40;
ax2.TickLength = TickLength2;
ax2.XTickLabel = {'-40', '0', '40'};
ax2.YTickLabel = {};
ax2.Colormap = colorA;
ax2.XLabel.String = 'x (μm)';
ax2.XLabel.FontName = 'Times New Roman';
ax2.XLabel.FontSize = 9;
fwhm = Fwhm532(1)*1e6;
t = sprintf('FWHM=%.2f μm', fwhm);
t2 = title(ax2, t);
t2.FontName = 'Times New Roman';
hold on
plot(x, -65*normalizeArrayTo01(E532_xy{1}(51, :))+40, 'k--', 'LineWidth', 0.8)
yline(ax2, 0)
hold off

ax3 = nexttile(3, [1, 1]);
imagesc([-40, 40], [-40, 40], E780_xy{1})
axis image
ax3.XTickMode = 'manual';
ax3.YTickMode = 'manual';
ax3.XTick = -40:40:40;
ax3.YTick = -40:40:40;
ax3.TickLength = TickLength2;
ax3.XTickLabel = {'-40', '0', '40'};
ax3.YTickLabel = {};
ax3.Colormap = colorB;
ax3.XLabel.String = 'x (μm)';
ax3.XLabel.FontName = 'Times New Roman';
ax3.XLabel.FontSize = 9;
fwhm = Fwhm780(1)*1e6;
t = sprintf('FWHM=%.2f μm', fwhm);
t3 = title(ax3, t);
t3.FontName = 'Times New Roman';
hold on
plot(x, -65*normalizeArrayTo01(E780_xy{1}(51, :))+40, 'k--', 'LineWidth', 0.8)
yline(ax3, 0)
hold off

ax4  = nexttile(4, [3, 1]);
imagesc([-60, 60], [19000, 23000], E780_xz')
yline(20000, 'k--')
yline(21000, 'k--')
yline(22000, 'k--')
ax4.XTickMode = 'manual';
ax4.YTickMode = 'manual';
ax4.XTick = -40:40:40;
ax4.YTick = 20000:1000:22000;
ax4.TickLength = TickLength1;
ax4.XTickLabel = {'-40', '0', '40'};
ax4.YTickLabel = {'22', '21', '20'};
ax4.Colormap = colorB;
ax4.FontName = 'Times New Roman';
ax4.FontSize = 8;
ax4.YAxisLocation = 'right';
ax4.XLabel.String = 'x (μm)';
ax4.XLabel.FontName = 'Times New Roman';
ax4.YLabel.String = 'z (mm)';
ax4.YLabel.FontName = 'Times New Roman';
[t4, s4] = title(ax4, 'Wavelength (nm)', '780');
t4.FontName = 'Times New Roman';
t4.FontWeight = 'bold';
t4.FontSize = 10;
s4.FontName = 'Times New Roman';
s4.FontSize = 9;
s4.FontWeight = 'bold';

ax5 = nexttile(6, [1, 1]);
imagesc([-40, 40], [-40, 40], E532_xy{2})
axis image
ax5.XTickMode = 'manual';
ax5.YTickMode = 'manual';
ax5.XTick = -40:40:40;
ax5.YTick = -40:40:40;
ax5.TickLength = TickLength2;
ax5.XTickLabel = {'-40', '0', '40'};
ax5.YTickLabel = {};
ax5.Colormap = colorA;
ax5.XLabel.String = 'x (μm)';
ax5.XLabel.FontName = 'Times New Roman';
ax5.XLabel.FontSize = 9;
fwhm = Fwhm532(2)*1e6;
t = sprintf('FWHM=%.2f μm', fwhm);
t5 = title(ax5, t);
t5.FontName = 'Times New Roman';
hold on
plot(x, -65*normalizeArrayTo01(E532_xy{2}(51, :))+40, 'k--', 'LineWidth', 0.8)
yline(ax5, 0)
hold off

ax6 = nexttile(7, [1, 1]);
imagesc([-40, 40], [-40, 40], E780_xy{2})
axis image
ax6.XTickMode = 'manual';
ax6.YTickMode = 'manual';
ax6.XTick = -40:40:40;
ax6.YTick = -40:40:40;
ax6.TickLength = TickLength2;
ax6.XTickLabel = {'-40', '0', '40'};
ax6.YTickLabel = {};
ax6.Colormap = colorB;
ax6.XLabel.String = 'x (μm)';
ax6.XLabel.FontName = 'Times New Roman';
ax6.XLabel.FontSize = 9;
fwhm = Fwhm780(2)*1e6;
t = sprintf('FWHM=%.2f μm', fwhm);
t6 = title(ax6, t);
t6.FontName = 'Times New Roman';
hold on
plot(x, -65*normalizeArrayTo01(E780_xy{2}(51, :))+40, 'k--', 'LineWidth', 0.8)
yline(ax6, 0)
hold off

ax7 = nexttile(10, [1, 1]);
imagesc([-40, 40], [-40, 40], E532_xy{3})
axis image
ax7.XTickMode = 'manual';
ax7.YTickMode = 'manual';
ax7.XTick = -40:40:40;
ax7.YTick = -40:40:40;
ax7.TickLength = TickLength2;
ax7.XTickLabel = {'-40', '0', '40'};
ax7.YTickLabel = {};
ax7.Colormap = colorA;
ax7.XLabel.String = 'x (μm)';
ax7.XLabel.FontName = 'Times New Roman';
ax7.XLabel.FontSize = 9;
fwhm = Fwhm532(3)*1e6;
t = sprintf('FWHM=%.2f μm', fwhm);
t7 = title(ax7, t);
t7.FontName = 'Times New Roman';
hold on
plot(x, -65*normalizeArrayTo01(E532_xy{3}(51, :))+40, 'k--', 'LineWidth', 0.8)
yline(ax7, 0)
hold off

ax8 = nexttile(11, [1, 1]);
imagesc([-40, 40], [-40, 40], E780_xy{3})
axis image
ax8.XTickMode = 'manual';
ax8.YTickMode = 'manual';
ax8.XTick = -40:40:40;
ax8.YTick = -40:40:40;
ax8.TickLength = TickLength2;
ax8.XTickLabel = {'-40', '0', '40'};
ax8.YTickLabel = {};
ax8.Colormap = colorB;
ax8.XLabel.String = 'x (μm)';
ax8.XLabel.FontName = 'Times New Roman';
ax8.XLabel.FontSize = 9;
fwhm = Fwhm780(3)*1e6;
t = sprintf('FWHM=%.2f μm', fwhm);
t8 = title(ax8, t);
t8.FontName = 'Times New Roman';
hold on
plot(x, -65*normalizeArrayTo01(E780_xy{3}(51, :))+40, 'k--', 'LineWidth', 0.8)
yline(ax8, 0)
hold off

%%
load figPart3.mat
E780_z = normalizeArrayTo01(E780_z);
E532_z = normalizeArrayTo01(E532_z);

E_target = flat_top_gaussian(zz, 1, 20e-3, 22e-3, 0.2e-3);

ax9 = nexttile(13, [1, 2]);
plot(ax9, zz, E532_z, 'LineWidth', 1, 'Color', '#16a085')

hold on
plot(ax9, zz, E780_z, 'LineWidth', 1, 'Color', '#c0392b')

plot(ax9, zz, E_target, 'LineStyle', '--', 'Color', 'black')
hold off

ax9.YLim = [0, 1.15];
ax9.XTickMode = 'manual';
ax9.YTickMode = 'manual';
ax9.XTick = 20e-3:1e-3:22e-3;
ax9.YTick = 0:0.25:1;
ax9.XTickLabel = {'20', '21', '22'};
ax9.YTickLabel = {'0', '0.25', '0.5', '0.75', '1'};

xline(20e-3)
xline(22e-3)
ax9.YLabel.String = 'Normalized intensity';
ax9.YLabel.FontName = 'Times New Roman';
ax9.YLabel.FontSize = 10;
ax9.XLabel.String = 'z (mm)';
ax9.XLabel.FontName = 'Times New Roman';
ax9.XLabel.FontSize = 10;
ax9.XGrid = 'on';
ax9.YGrid = 'on';

le = legend(ax9, '532nm', '780nm', 'target');
le.Location = 'westoutside';
le.FontName = 'Times New Roman';
le.ItemTokenSize = 16;

%%
cb1 = colorbar(ax1, 'Location', 'westoutside');
cb1.Ticks = [0, 0.5, 1];
cb1.FontName = 'Times New Roman';
cb1.FontSize = 8;
cb1.Label.String = 'Normalized field intensity';
cb1.Label.FontName = 'Times New Roman';
cb1.Label.FontSize = 9;

cb2 = colorbar(ax4, 'Location', 'eastoutside');
cb2.Ticks = [0, 0.5, 1];
cb2.FontName = 'Times New Roman';
cb2.FontSize = 8;
cb2.Label.String = 'Normalized field intensity';
cb2.Label.FontName = 'Times New Roman';
cb2.Label.FontSize = 9;

%%
ar1 = annotation('arrow');
ar1.Units = "centimeters";
ar1.Position = [5.85, 14, 0.5, 0.75];
ar1.HeadStyle = "vback3";

ar2 = annotation('arrow');
ar2.Units = "centimeters";
ar2.Position = [12.75, 14, -0.5, 0.75];
ar2.HeadStyle = "vback3";

ar3 = annotation('arrow');
ar3.Units = "centimeters";
ar3.Position = [5.85, 11.35, 0.6, 0];
ar3.HeadStyle = "vback3";

ar4 = annotation('arrow');
ar4.Units = "centimeters";
ar4.Position = [12.75, 11.35, -0.6, 0];
ar4.HeadStyle = "vback3";

ar3 = annotation('arrow');
ar3.Units = "centimeters";
ar3.Position = [5.85, 8.65, 0.5, -0.75];
ar3.HeadStyle = "vback3";

ar4 = annotation('arrow');
ar4.Units = "centimeters";
ar4.Position = [12.75, 8.65, -0.5, -0.75];
ar4.HeadStyle = "vback3";