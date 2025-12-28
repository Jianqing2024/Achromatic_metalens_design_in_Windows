clear;clc
load Phase_Big.mat

r = 1e-3;
single = 0.4e-6;
U = int64(r*2/single);
x = linspace(-(r + 0.5*single), (r + 0.5*single), U);
y = linspace(-(r + 0.5*single), (r + 0.5*single), U);
[X, Y] = meshgrid(x, y);

lambda = [0.780e-6, 0.532e-6];

z = linspace(9e-3, 13e-3, 250);
zz = linspace(10e-3, 12e-3, 5);

E780 = exp(1i*phase780);
E532 = exp(1i*phase532);

figure(1)
tiledlayout(2,1)

Eaxis780 = RSaxis_GPU(E780,lambda(1),X,Y,z,1);
nexttile
plot(z,Eaxis780)
drawnow

Eaxis532 = RSaxis_GPU(E532,lambda(2),X,Y,z,1);
nexttile
plot(z,Eaxis532)
drawnow

for i = 1:numel(zz)
    [Efficiency780(i),fwhm780(i)] = ...
    Focus_on_efficiency_lowSampling_GPU(E780,X,Y,ones(U,U),lambda(1),zz(i),100,15e-6,1e-6,1,1);
    [Efficiency532(i),fwhm532(i)] = ...
    Focus_on_efficiency_lowSampling_GPU(E532,X,Y,ones(U,U),lambda(2),zz(i),100,15e-6,1e-6,1,1);

    disp(i)
end