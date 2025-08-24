% 版本说明：9.0
%
% 重新把不同部分的程序拆出来

clear;clc;

%% 参数设置
parameter=parameter_preset;

r=parameter.r;
single=parameter.single;
lambda=parameter.lambda;
l=parameter.l;

Fnum=parameter.Fnum;
loop=parameter.loop;

start=parameter.start;
stop=parameter.stop;

U=int16(r/single*2);
%% 焦点分布迭代计算
Ft = Random_Matrix(Fnum, U);

R=zeros(loop,Fnum);
I=zeros(loop,Fnum);
L=zeros(loop,Fnum);

L(1,:)=linspace(start,stop,Fnum);
Eout=Light_field_Emission_field(Ft,L(1,:),r,l,single,wav,U);

I(1,:)=Intensity_calculation(Eout,wav,r,single,L(1,:));

for i=2:loop
    R(i,:)=I(i-1,:)./((1/Fnum)*sum(I(i-1,:)));
    L(i,1)=start;
    for j=2:Fnum
        L(i,j)=(L(i-1,j)-L(i-1,j-1)).*R(i,j)+L(i,j-1);
    end
    L(i,Fnum)=stop;
    Eout=Light_field_Emission_field(Ft,L(i,:),r,l,single,wav,U);
    I(i,:)=Intensity_calculation(Eout,wav,r,single,L(i,:));

    figure(1)
    plot(L(i,:),I(i,:))
    drawnow

    printProgress('焦点位置优化', i, loop)
end

%% 光场重生成
x = linspace(-(r-0.5*single),(r-0.5*single),U);
y = linspace(-(r-0.5*single),(r-0.5*single),U);

[X,Y]=meshgrid(x,y);

target_phi=Light_field_Phase_field(Ft,L(loop,:),r,l,single,lambda,U);
Ein=Light_field_Incident_field(r,l,single,lambda,U);
Eout=Light_field_Emission_field(Ft,L(loop,:),r,l,single,lambda,U);

zo=linspace(1.25e-3,3.25e-3,1000);
I=Intensity_calculation(Eout,lambda,r,single,zo);
figure(2)
plot(zo,I)
%%
disp('现在进行细调')
InitL=L(loop,:);
save para.mat parameter Ft InitL

run main2.m