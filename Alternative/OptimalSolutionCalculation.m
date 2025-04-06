function Fit=OptimalSolutionCalculation(shift)
% 在确定相位修正函数的修正值和焦距修正值后，计算
persistent data;
persistent parameter;

if isempty(data)
    d=load("data.mat");
    data=d.data;
end
if isempty(parameter)
    p=load('parameter.mat');
    parameter=p.parameter;
end

R=parameter(1);
f=parameter(2);
lambda=[parameter(3),parameter(4)];
single=data.P(1);

x=generate_vector(0.5*single, step_size, R);
U=numel(x);

f=f+shift(3);

phi=cell(2,1);
for i=1:2
    phi{i}=wrapToPi(Hyperbolic_phase(x,lambda(i),f))+shift(i);
end

temData=cell(rol,1);
for i=1:rol
    temData{i}=[da.angleIn532(i);da.angleIn800(i)];
end

difference=zeros(rol,1);
Interpolation=zeros(U,1);
for i=1:U
    targetPhi=[phi{1}(i);phi{2}(i)];
    for j=1:rol
        difference(j)=sum(abs(targetPhi-temData{j}));
    end
    idx=difference==min(difference,[],"all");
    Interpolation(i)=difference(idx);
end

Fit=sum(Interpolation);

function vec = generate_vector(start_pos, step_size, R)
    n = floor((R - start_pos) / step_size) + 1;
    vec = start_pos : step_size : start_pos + (n - 1) * step_size;
end

function phi=Hyperbolic_phase(r,lambda,f)
phi=-2*pi/lambda*(sqrt(r.^2+f^2)-f);
end
end