clear;clc

r = 0.8e-3;
single = 0.4e-6;
Fnum = 400;
start = 23e-3;
stop = 25e-3;
U = int64(r*2/single);
lambda = 0.532e-6;
l = 20e-3;

Ft = Random_Matrix_Generation(U,Fnum);

[Eout, phi] = NBphase(r,single,lambda,l,U,Fnum,start,stop,Ft);