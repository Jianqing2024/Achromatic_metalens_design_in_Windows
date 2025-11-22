clear
lo = load('para.mat');
para = lo.para;
clear lo

r=para.r;
single=para.single;
lambda=para.lambda;
l=para.l;

start=para.start;
stop=para.stop;

Ft = para.Ft;
ft = para.ft;

U=int16(r/single*2);
x = linspace(-(r-0.5*single), (r-0.5*single), U);
y = linspace(-(r-0.5*single), (r-0.5*single), U);
[X, Y] = meshgrid(x,y);

% 生成光场
Eout = Light_field_Emission_field(Ft,ft,r,l,single,lambda,U);
Ein = Light_field_Incident_field(r,l,single,lambda,U);
Phase = Light_field_Phase_field(Ft,ft,r,l,single,lambda,U);
EControl = Light_field_Control(r,single,lambda,U,(start+stop)/2,10e-6);

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
LF.control = EControl;
save('Light_field.mat','LF','-v7.3')

run step_4.m