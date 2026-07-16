function parameter=parameter_preset
%% 阵列参数
parameter.r=240e-6;
parameter.single=0.8e-6;
parameter.lambda=1.200e-6;

parameter.l = 2.5e-3;

parameter.Fnum=100;

parameter.start=1.1e-3;
parameter.stop=2.1e-3;

parameter.U = int16(parameter.r/parameter.single*2);
end