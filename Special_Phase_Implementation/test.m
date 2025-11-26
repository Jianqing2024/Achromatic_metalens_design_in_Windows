clear;clc

r = 12e-6;
single = 0.4e-6;

lambda = [0.780e-6, 0.532e-6];

data = load("End.mat");
Ex_plane = data.Ex_plane;
Ex_y = data.Ex_y;

U = size(Ex_plane,1);

E780_plane = Ex_plane(:,:,1);
E532_plane = Ex_plane(:,:,5);

x = linspace(-(r + 0.5*single), (r + 0.5*single), U);
y = linspace(-(r + 0.5*single), (r + 0.5*single), U);
[X, Y] = meshgrid(x, y);

z = linspace(2e-6,70e-6,769);
E780_plane_line = normalizeArrayTo01(RSaxis_GPU(E780_plane,0.780e-6,X,Y,z,1));
E532_plane_line = normalizeArrayTo01(RSaxis_GPU(E532_plane,0.532e-6,X,Y,z,1));

E780_y = abs(Ex_y(:,:,1)).^2;
E532_y = abs(Ex_y(:,:,5)).^2;

E780_y_line = normalizeArrayTo01((E780_y(349,:)+E780_y(350,:))/2);
E532_y_line = normalizeArrayTo01((E532_y(349,:)+E532_y(350,:))/2);

f = figure(1);
tiledlayout(2,3)

nexttile(1)
imagesc(E780_y)
nexttile(2)
plot(z, E780_y_line)
nexttile(3)
plot(z, E780_plane_line)

nexttile(4)
imagesc(E532_y)
nexttile(5)
plot(z, E532_y_line)
nexttile(6)
plot(z, E532_plane_line)