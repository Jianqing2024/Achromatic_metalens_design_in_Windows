clear;clc
load Light_field.mat
load para.mat

z = linspace(0.75e-3,3.75e-3,800);

zz = linspace(1.25e-3,3.25e-3,50);

% save Phase.mat Phase
%%
% E = RSaxis_GPU(Eout, lambda, X, Y, z);
% 
% save Eaxis.mat E z

%%
E_contrast = RSaxis_GPU(LF.control, para.lambda, LF.X, LF.Y, z);
% 
% save Eaxis_contrast.mat E_contrast z

%%
% for i=1:n
%     [eff(i), fwhm(i)]=...
%         Focus_on_efficiency_lowSampling_GPU...
%             (Eout,X,Y,Ein,lambda,zo(i),200,15e-6,0.5e-6);
%     disp(zo(i))
% end
% 
% fwhm = FWHM_Calculation_GPU(Eout,lambda,X,Y,32e-6,500,zz);
% save FWHM.mat fwhm zz
%%
% xCheck = linspace(-25e-6, 25e-6, 500);
% yCheck = linspace(-25e-6, 25e-6, 500);
% [XC, YC] = meshgrid(xCheck, yCheck);
% 
% num = 3;
% 
% z = [2e-3,2.25e-3,2.5e-3];
% 
% Earray = cell(5,1);
% 
% for i = 1:num
%     Earray{i} = RSarray_GPU(Eout, lambda, X, Y, XC, YC, z(i));
% end
% 
% save Exy.mat Earray XC YC z
%%
radial = 37.5e-6;

zz = linspace(1.5e-3, 3e-3, 750);
xCheck = linspace(-radial, radial, 160);
yCheck = linspace(-radial, radial, 160);
[XC, YC] = meshgrid(xCheck, yCheck);
% 
Exz = zeros(numel(yCheck), numel(zz));
for i = 1:numel(zz)
    Exz(:, i) = RSradial_GPU(LF.Eout, para.lambda, LF.X, LF.Y, yCheck, zz(i));
end
imagesc(Exz)
save Exz.mat Exz XC YC zz
%
Exz_constrast = zeros(numel(yCheck), numel(zz));
for i = 1:numel(zz)
    Exz_constrast(:, i) = RSradial_GPU(LF.control, para.lambda, LF.X, LF.Y, yCheck, zz(i));
end
imagesc(Exz_constrast)
save Exz_constrast.mat Exz_constrast XC YC zz
%%
