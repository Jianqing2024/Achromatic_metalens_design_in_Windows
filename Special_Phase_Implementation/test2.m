clear;clc

r = 12e-6;
single = 0.4e-6;
lambda = 0.780e-6;
f = 60e-6;
U = int64(r*2/single);

x = linspace(-(r-0.5*single),(r-0.5*single),U);
y = linspace(-(r-0.5*single),(r-0.5*single),U);
[X,Y]=meshgrid(x,y);
x0=0;
y0=0;
R2 = (X-x0).^2+(Y-y0).^2;

phi=(2*pi/lambda)*(f-sqrt(R2+f.^2));

phi1 = wrapToPi(phi);

lambda = 0.532e-6;

phi=(2*pi/lambda)*(f-sqrt(R2+f.^2));
phi2 = wrapToPi(phi);

save single.mat phi1 phi2