function Far_FieldSimulation()
load MonitorData.mat data
data = squeeze(data);

data = permute(data, [2,1,3]);

for i=1:5
    data(:, :, i) = flipud(data(:, :, i));
end

fig1 = figure(1);
tiledlayout

nexttile
imagesc(abs(data(:, :, 1)).^2)

nexttile
imagesc(abs(data(:, :, 2)).^2)

nexttile
imagesc(abs(data(:, :, 3)).^2)

nexttile
imagesc(abs(data(:, :, 4)).^2)

nexttile
imagesc(abs(data(:, :, 5)).^2)

savefig(fig1,"fullWave.fig","-v7.3")
end