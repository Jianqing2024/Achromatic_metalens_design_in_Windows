clear;clc
load End.mat

r = 1.8e-3;
single = 0.4e-6;
U =  int64(2*r/single);

xc = linspace(-60e-6, 60e-6, 100);
zc = linspace(19e-3, 23e-3, 200);

[Ein_532, ~] = Light_field_Incident_field(r, single, 0.532e-6, U, 25e-3, 4.4e-6, 1);
[Ein_780, ~] = Light_field_Incident_field(r, single, 0.780e-6, U, 25e-3, 4.4e-6, 1);

E532 = Ein_532.*exp(1j*phase532);
E780 = Ein_780.*exp(1j*phase780);

x = linspace(-(r-0.5*single), (r-0.5*single), U);
y = linspace(-(r-0.5*single), (r-0.5*single), U);
[X, Y] = meshgrid(x,y);

% E532_xz = zeros(numel(xc), numel(zc));
% E780_xz = zeros(numel(xc), numel(zc));
% 
% for i = 1:numel(zc)
%     z = zc(i);
%     E532_xz(:, i) = RSradial_GPU(E532, 0.532e-6, X, Y, xc, z, 1);
%     E780_xz(:, i) = RSradial_GPU(E780, 0.780e-6, X, Y, xc, z, 1);
%     disp(i)
% end
% 
% save figPart1.mat E780_xz E532_xz
% 
% figure(1)
% subplot(2,1,1)
% imagesc(E532_xz)
% subplot(2,1,2)
% imagesc(E780_xz)
% 
% zz = linspace(20e-3, 22e-3, 3);
% 
% xc = linspace(-40e-6, 40e-6, 100);
% yc = linspace(-40e-6, 40e-6, 100);
% [Xc, Yc] = meshgrid(xc, yc);
% for i = 1:3
%     E532_xy{i} = RSarray_GPU(E532, 0.532e-6, X, Y, Xc, Yc, zz(i), 1);
%     E780_xy{i} = RSarray_GPU(E780, 0.780e-6, X, Y, Xc, Yc, zz(i), 1);
%     disp(i)
% end
% 
% save figPart2.mat E780_xy E532_xy

%%
zz = linspace(19e-3, 23e-3, 400);

E532_z = RSaxis_GPU(E532, 0.532e-6, X, Y, zz, 1);
E780_z = RSaxis_GPU(E780, 0.780e-6, X, Y, zz, 1);

save figPart3.mat E532_z E780_z zz