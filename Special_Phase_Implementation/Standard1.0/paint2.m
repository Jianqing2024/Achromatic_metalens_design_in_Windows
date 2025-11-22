clear;clc
load Light_field.mat
load para.mat
X = LF.X;
Y = LF.Y;

start = parameter.start;
stop = parameter.stop;
r = parameter.r;
l = parameter.l;
single = parameter.single;
lambda = parameter.lambda;
U = int16(r/single*2);

E = RSaxis_GPU(LF.Eout, lambda, X, Y, linspace(0.5e-3,3.5e-3,300));
plot(linspace(0.5e-3,3.5e-3,300), E)

bbb = FWHM_Calculation_GPU(LF.Eout, lambda, X, Y, 20e-6, 200, 1.75e-3);