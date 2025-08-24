function parameter=parameter_preset
%% 阵列参数
S = load('ParameterData.mat');
r = S.r;
single = S.single;

parameter.r=r+0.5*single;
parameter.single=single;
parameter.lambda=linspace(0.8e-6, 0.5e-6, 5);
parameter.l=2.44e-3;

parameter.Fnum=400;
parameter.loop=7;

parameter.start=1.85e-3;
parameter.stop=2.65e-3;

end