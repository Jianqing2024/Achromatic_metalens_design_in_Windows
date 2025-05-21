clear;clc
r=0.5e-3;
single=0.4e-6;
lambda0=0.8e-6;
f=24e-3;
N=int64(2*r/single);
x=linspace(-r,r,2*N);
y=linspace(-r,r,2*N);
[X,Y]=meshgrid(x,y);

R2=X.^2+Y.^2;

phi=-2*pi/lambda0*(sqrt(R2+f^2)-f);

checkX=linspace(-20e-6,20e-6,50);
checkZ=linspace(f-0.5e-3,f+0.5e-3,50);

xx=RSradial(1*exp(1i*phi),lambda0,X,Y,checkX,f);
zz=RSaxis(1*exp(1i*phi),lambda0,X,Y,checkZ);

[x2,y2,Uout]=Singlestep_Fdiffraction(1*exp(1i*phi), lambda0, single, f);
%%
figure(1)
subplot(2,2,1)
imagesc(x,y,phi)
axis equal
subplot(2,2,2)
imagesc(x2(1,:),y2(:,1),abs(Uout).^2)
axis equal
subplot(2,2,3)
plot(checkX,xx)
subplot(2,2,4)
plot(checkZ,zz)