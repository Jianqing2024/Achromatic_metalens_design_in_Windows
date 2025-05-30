clear;clc
r=1e-3;
single=0.4e-6;
lambda0=0.8e-6;
f=5e-3;
N=int64(2*r/single);
x=linspace(-r,r,N);

for i=1:N
    ftx(i)=-(2*pi)/lambda0*(sqrt((x(i))^2+f^2)-f);
end
ftx=wrapTo2Pi(ftx);

angle=readmatrix("angle.txt");
angle=wrapTo2Pi(angle);

for i=1:N
    target=ftx(i);
    for j=1:numel(angle)
        diff(j)=abs(target-angle(j));
    end

    [~, minIDX]=min(diff);
    p(i)=minIDX;
end

radius=linspace(0.04e-6,0.18e-6);

R=radius(p);