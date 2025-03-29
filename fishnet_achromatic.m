clear;clc

db = sqlite('structures.db', 'readonly');

numBaseValue=table2array(fetch(db, 'SELECT COUNT(DISTINCT baseValue) FROM structures;'));

data=cell(numBaseValue,1);
for i=1:numBaseValue
    sql=sprintf("SELECT * FROM structures WHERE baseValue = %d;",i);
    data{i}=fetch(db, sql);
end
close(db);

Fitness=zeros(numBaseValue,1);
lambda=[0.532e-6,0.800e-6];
for s=1:numBaseValue
    da=data{s};
    [rol,~]=size(da);
    
    R=0.25e-3;
    single=da.P(1);
    U=int16(R/single);
    x=linspace(0.5*single,(R-0.5*single),U);
    f=8.5e-3;
    
    phi=cell(2,1);
    for i=1:2
        phi{i}=wrapToPi(Hyperbolic_phase(x,lambda(i),f));
    end
    
    temData=cell(rol,1);
    for i=1:rol
        temData{i}=[da.angleIn532(i);da.angleIn800(i)];
    end
    
    difference=zeros(rol,1);
    Interpolation=zeros(U,1);
    structer=zeros(U,1);
    for i=1:U
        targetPhi=[phi{1}(i);phi{2}(i)];
        for j=1:rol
            difference(j)=sum(abs(targetPhi-temData{j}));
        end
        idx=find(difference==min(difference,[],"all"));
        Interpolation(i)=difference(idx);
        structer(i)=da.id(idx);
    end

    Fitness(s)=sum(Interpolation);
end

function phi=Hyperbolic_phase(r,lambda,f)
phi=-2*pi/lambda*(sqrt(r.^2+f^2)-f);
end

% function Fit=fittt(shift)
% r=0.25e-3;
% single=0.2e-6;
% lambda=linspace(0.532e-6,0.8e-6,2);
% U=int16(r/single);
% f=8.5e-3+shift(3);
% x=linspace(0.5*single,(r-0.5*single),U);
% 
% shift_phi=shift(1:2);
% 
% Targetphi=zeros(numel(lambda),numel(x));
% for i=1:numel(lambda)
%     Targetphi(i,:)=wrapToPi(Hyperbolic_phase(x,lambda(i),f)+shift_phi(i));
% end
% 
% %% 扫参
% data=load('p.mat');
% p=data.p;
% 
% %% 对比
% it=zeros(int16(U),1);
% interpolation=zeros(56,1);
% for i=1:int16(U)
%     for j=1:148
%         interpolation(j)=sum(abs(Targetphi(:,i)-p{j}))/2;
%     end
%     it(i)=min(interpolation);
% end
% 
% Fit = sum(it)/double(U);
% 
% end
% 
% function [Phase_spectrum,str]=fittt2(shift)
% r=0.25e-3;
% single=0.2e-6;
% lambda=linspace(0.532e-6,0.8e-6,2);
% U=int16(r/single);
% f=8.5e-3+shift(3);
% x=linspace(0.5*single,(r-0.5*single),U);
% 
% shift_phi=shift(1:2);
% 
% Targetphi=zeros(numel(lambda),numel(x));
% for i=1:numel(lambda)
%     Targetphi(i,:)=wrapToPi(Hyperbolic_phase(x,lambda(i),f)+shift_phi(i));
% end
% 
% %% 扫参
% data=load('p.mat');
% p=data.p;
% 
% %% 对比
% Phase_spectrum=zeros(2,U);
% interpolation=zeros(56,1);
% str=zeros(U,1);
% for i=1:U
%     for j=1:148
%         StrPhi=p{j};
%         interpolation(j)=sum(abs(Targetphi(:,i)-StrPhi))/10;
%     end
%     idx=find(interpolation==min(interpolation,[],"all"));
%     idx=idx(1);
%     str(i)=idx;
%     Phase_spectrum(:,i)=p{idx};
% end
% 
% end
% 
% function Targetphi=fittt3(shift)
% r=0.25e-3;
% single=0.2e-6;
% lambda=linspace(0.532e-6,0.8e-6,2);
% U=int16(r/single);
% f=8.5e-3+shift(3);
% x=linspace(0.5*single,(r-0.5*single),U);
% 
% shift_phi=shift(1:2);
% 
% Targetphi=zeros(numel(lambda),numel(x));
% for i=1:numel(lambda)
%     Targetphi(i,:)=wrapToPi(Hyperbolic_phase(x,lambda(i),f)+shift_phi(i));
% end
% 
% end