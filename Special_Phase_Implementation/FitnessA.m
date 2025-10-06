function FIT = FitnessA(Ft, para, x)
A = x(1);
V = x(2);
D = x(3);

r=para.r;
single=para.single;
lambda=para.lambda;

Fnum=para.Fnum;

start=para.start;
stop=para.stop;

U=para.U;

ft = Focal_Sequence_Generation(start, Fnum, V, D);
Eout = Light_Field_SA_A(Ft, ft, r, single, lambda, U, A);

x = linspace(-(r-0.5*single),(r-0.5*single),U);
y = linspace(-(r-0.5*single),(r-0.5*single),U);

[X,Y]=meshgrid(x,y);

l = stop-start;

z=linspace(start-0.25*l,stop+0.25*l,50);

Enormal=normalizeArrayTo01(RSaxis_GPU(Eout, lambda, X, Y, z, 1));

Estandard = flat_top_gaussian(z, 1, start, stop, 0.05e-3);
FIT = sum(abs(Enormal-Estandard));

% figure(1)
% plot(z,Enormal,z,Estandard)
% drawnow
end