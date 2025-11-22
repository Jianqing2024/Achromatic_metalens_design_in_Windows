clear;clc

para.r = 240e-6;

para.single = 0.8e-6;
para.lambda = 1.31e-6;
para.l = 2.44e-3;
para.U = int16(para.r/para.single*2);

para.Fnum = 400;

para.start = 1.85e-3;
para.stop = 2.65e-3;

para.Ft = Random_Matrix_Generation(para.U,para.Fnum);

save para.mat para
run step_2.m