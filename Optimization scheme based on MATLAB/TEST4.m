clear;clc
%% 目标计算
r=12e-6;
single=0.4e-6;
lambda=linspace(0.4e-6,0.6e-6,10);
U=int16(r/single*2);
f=24e-6;
x=linspace(-(r-0.5*single),(r-0.5*single),U);
y=linspace(-(r-0.5*single),(r-0.5*single),U);
[X,Y]=meshgrid(x,y);
radiusSquared=(X).^2+(Y).^2;
radius=sqrt(radiusSquared);


phi=zeros(numel(lambda),numel(x));
for i=1:numel(lambda)
    Lambda=lambda(i);
    phi(i,:)=Hyperbolic_phase(x,Lambda,f)+Shift_phase(lambda,11.8959,Lambda);
end

%% 扫参
theta=linspace(0,330,12);
lambda=linspace(0.4e-6,0.6e-6,10);
[Theta,Lambda]=meshgrid(lambda,theta);

SweepPhi=cell(5,1);
for i=1:5
    str=sprintf("group%i.txt",i);
    SweepPhi{i}=(readmatrix(str))';
end
p=cell(60,1);
% 单个结构相位/色散谱
for i=1:5
    Phi=SweepPhi{i};
    for j=1:12
        p{(i-1)*12+j}=Phi(:,j);
    end
end

%% 对比

phi=phi(:,31:end);
P=zeros(10,30);

for i=1:30
    phi_target=phi(:,i);
    for j=1:60
        StrPhi=p{j};
        interpolation(j)=sum(abs(phi_target-StrPhi))/10;
    end
    idx=find(interpolation==min(interpolation,[],"all"));
    idx=idx(1);
    P(:,i)=p{idx};
    in(i)=min(interpolation,[],"all");
end



%% function
function phi=Hyperbolic_phase(r,lambda,f)
phi=-2*pi/lambda*(sqrt(r.^2+f^2)-f);
end

function phi=Shift_phase(lambda,delta,LAMBDA)
ln=min(lambda);
lx=max(lambda);
a=delta*(ln*lx/(lx-ln));
b=-delta*(ln/(lx-ln));
phi=a/LAMBDA+b;
end