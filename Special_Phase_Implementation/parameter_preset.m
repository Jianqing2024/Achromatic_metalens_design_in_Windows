function parameter=parameter_preset
%% 阵列参数
para = load('data.mat');
r = para.r;
single = para.single;

parameter.r=r;
parameter.single=single;
parameter.lambda=[0.8e-6, 0.532e-6];

parameter.Fnum=100;

parameter.start=1.8e-3;
parameter.stop=2.8e-3;

parameter.U = int16(parameter.r/parameter.single*2);
end