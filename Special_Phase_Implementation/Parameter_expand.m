clear;clc
load para.mat

r=parameter.r;
single=parameter.single;
lambda=parameter.lambda;
l=parameter.l;

start=parameter.start;
stop=parameter.stop;

U=int16(r/single*2);
x = linspace(-(r-0.5*single), (r-0.5*single), U);
y = linspace(-(r-0.5*single), (r-0.5*single), U);
[X, Y] = meshgrid(x,y);

z = linspace(start-0.5e-3,stop+0.5e-3,200)';
%% 计算光强
% 生成光场
Eout = Light_field_Emission_field(Ft,betaList,r,l,single,lambda,U);
Ein = Light_field_Incident_field(r,l,single,lambda,U);
Phase = Light_field_Phase_field(Ft,betaList,r,l,single,lambda,U);

% Mini方柱
phi = readmatrix('gkj_MiniCube.txt');
phi = wrapTo2Pi(phi);

h = linspace(2,4,100);

height = zeros(U,U);
for i=1:U
    for j=1:U
        phase = Phase(i,j);

        if phase == 0
            height(i,j) = nan;
        else
            for k=1:numel(phi)
                diff(k) = abs(phase-phi(k));
            end
            [~, index] = min(diff);
            height(i,j) = h(index);
        end
    end
end

LF.X = X;
LF.Y = Y;
LF.Eout = Eout;
LF.Ein = Ein;
LF.Phase = Phase;
LF.height = height;
save('Light_field.mat','LF','-v7.3')