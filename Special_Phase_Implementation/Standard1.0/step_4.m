clear

lo = load("para.mat");
para = lo.para;
lo = load('Light_field.mat');
LF = lo.LF;
clear lo

z = linspace(para.start-0.5e-3,para.stop+0.5e-3, 200);
E = RSaxis_GPU(LF.Eout, para.lambda,LF.X, LF.Y, z);
Enormal = normalizeArrayTo01(E);
Estandard = flat_top_gaussian(z, 1, para.start, para.stop, 0.1e-3);

%%
figure(5)
n=10;
zo=linspace(para.start-0.1e-3,para.stop+0.1e-3,n);
for i=1:n
    [eff(i), fwhm(i)]=...
        Focus_on_efficiency_lowSampling_GPU...
            (LF.Eout,LF.X,LF.Y,LF.Ein,para.lambda,zo(i),100,8e-6,0.08e-6);
    disp(zo(i))
end
figure(4)
subplot(3,1,1)
plot(z,Enormal,z,Estandard)
subplot(3,1,2)
plot(zo,eff)
title('Efficiency')
subplot(3,1,3)
plot(zo,fwhm)
title('FWHM')