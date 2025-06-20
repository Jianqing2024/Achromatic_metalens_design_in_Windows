clear;clc
load MonitorData.mat
data = squeeze(dataa);
clear dataa

x = linspace(-50.6, 50.6, size(data,2));
y = linspace(1, 160, size(data,1));

data = permute(data, [2,1,3]);

for i=1:5
    data(:, :, i) = flipud(data(:, :, i));
end

fig1 = figure(1);
tiledlayout

nexttile
imagesc(x, y, abs(data(:, :, 1)).^2)

nexttile
imagesc(x, y, abs(data(:, :, 2)).^2)

nexttile
imagesc(x, y, abs(data(:, :, 3)).^2)

nexttile
imagesc(x, y, abs(data(:, :, 4)).^2)

nexttile
imagesc(x, y, abs(data(:, :, 5)).^2)