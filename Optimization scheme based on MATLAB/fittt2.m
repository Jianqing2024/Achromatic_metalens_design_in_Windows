function [Phase_spectrum,str]=fittt2(shift)
r=0.25e-3;
single=0.2e-6;
lambda=linspace(0.532e-6,0.8e-6,2);
U=int16(r/single);
f=8.5e-3+shift(3);
x=linspace(0.5*single,(r-0.5*single),U);

shift_phi=shift(1:2);

Targetphi=zeros(numel(lambda),numel(x));
for i=1:numel(lambda)
    Targetphi(i,:)=wrapToPi(Hyperbolic_phase(x,lambda(i),f)+shift_phi(i));
end

%% 扫参
data=load('p.mat');
p=data.p;

%% 对比
Phase_spectrum=zeros(2,U);
interpolation=zeros(56,1);
str=zeros(U,1);
for i=1:U
    for j=1:148
        StrPhi=p{j};
        interpolation(j)=sum(abs(Targetphi(:,i)-StrPhi))/10;
    end
    idx=find(interpolation==min(interpolation,[],"all"));
    idx=idx(1);
    str(i)=idx;
    Phase_spectrum(:,i)=p{idx};
end

end