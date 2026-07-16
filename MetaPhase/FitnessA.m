function FIT = FitnessA(Ft, r, single, lambda, l, Fnum, start, stop, U, x)
A = x(1);
V = x(2);
D = x(3);

ft = Focal_Sequence_Generation(start, Fnum, V, D);
Eout = Light_Field_SA_A(Ft, ft, r, l, single, lambda, U, A);

x = linspace(-(r-0.5*single),(r-0.5*single),U);
y = linspace(-(r-0.5*single),(r-0.5*single),U);

[X,Y]=meshgrid(x,y);

z=linspace(start-0.5e-3,stop+0.5e-3,100);

Enormal=normalizeArrayTo01(RSaxis_GPU(Eout, lambda, X, Y, z, 1.333));

Estandard = flat_top_gaussian(z, 1, start, stop, 0.05e-3);
FIT = sum(abs(Enormal-Estandard));

% figure(1)
% plot(z,Enormal,z,Estandard)
% drawnow
end