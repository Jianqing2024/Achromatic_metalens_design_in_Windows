clear;clc
r=20e-6;
single=0.4e-6;
lambda0=800e-6;
N=int64(2*r/single);
x=linspace(-r,r,2*N);
y=linspace(-r,r,2*N);
[X,Y]=meshgrid(x,y);

function phi=PHI(r,w)
phi=phi0(r)+Dispersion(r)(w-w0);
end
